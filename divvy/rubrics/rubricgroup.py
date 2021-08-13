from divvy.errors import EmptyAttemptError, MultipleOriginError


class Attempt:
    @staticmethod
    def from_same_attempt(files1, file2):
        return (files1.for_same_assignment_as(file2) and
                files1.same_author_as(file2) and
                files1.same_timestamp_as(file2))

    @staticmethod
    def all_from_same_attempt(files):
        if not files:
            return True

        return all([Attempt.from_same_attempt(files[0], sf) for
                    sf in files])

    def __init__(self, files):
        if not files:
            raise EmptyAttemptError("Attempts must have s")

        if not Attempt.all_from_same_attempt(files):
            raise MultipleOriginError("s must be from the same attempt")

        self.__files = list(sorted(files, key=lambda f: f.name))

    def __str__(self):
        return "{} attempt for {} on {}".format(
            self.submitted_by, self.submitted_for, self.submitted_on
        )

    def __repr__(self):
        _reprs = ','.join([repr(f) for f in self.files])
        return f"Attempt('{_reprs}')"

    @property
    def submitted_by(self):
        return self.files[0].author

    @property
    def submitted_on(self):
        return self.files[0].timestamp

    @property
    def submitted_for(self):
        return self.files[0].for_assignment

    @property
    def files(self):
        return self.__files.copy()

    def by_same_author(self, other):
        return self.submitted_by == other.submitted_by

    def for_same_assignment(self, other):
        return self.submitted_for == other.submitted_for
