from sys import exit
import toml

from divvy import BBLearnSubmittedFile


class RubricFile(BBLearnSubmittedFile):
    @classmethod
    def from_bblearn_submitted_file(cls, bsf):
        try:
            filename, tail = bsf.name.split('__gradee_')
            gradee, extensions = tail.split('.', maxsplit=1)
        except ValueError:
            #TODO: raise InvalidRubricFilenameError
            print(f"Bad rubric filename: bsf.name")
            exit(1)

        return cls(
            grader=bsf.author,
            gradee=gradee,
            name=f"{filename}.{extensions}",
            timestamp=bsf.timestamp,
            for_assignment=bsf.for_assignment,
            location=bsf.location,
        )

    def __init__(self, grader, gradee, name, timestamp, for_assignment, location):
        self.__gradee = gradee
        super().__init__(name=name,
                         author=grader,
                         timestamp=timestamp,
                         for_assignment=for_assignment,
                         location=location)
        try:
            self.__content = toml.loads(self.get_data().decode())
        except toml.TomlDecodeError:
            self.__content = None

    def __str__(self):
        return self.bblearn_name

    def __additional_str_parts(self):
        return super().__additional_str_parts + [
            f"gradee='{self.gradee}'"
        ]

    @property
    def gradee(self):
        """The student whose work this rubric is assessing"""
        return self.__gradee

    @property
    def grader(self):
        """The student who filled in the rubric"""
        return self.author

    @property
    def is_valid(self):
        return self.__content is not None

    def get_total(self, reference=None):
        def score(rubric_part):
            if not isinstance(rubric_part, dict):
                return 0
            return (rubric_part.get('score', 0) +
                    sum([score(subpart) for subpart in rubric_part.values()]))

        return score(self.__content) if self.is_valid else None

    def same_gradee_as(self, other):
        return self.gradee == other.gradee
