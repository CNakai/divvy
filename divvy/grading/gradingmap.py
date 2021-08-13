from json import dump, load
from random import shuffle, seed

from divvy.assignment import Assignment


class GradingMap:
    @classmethod
    def from_participants_location(cls, participants_location,
                                   gradees_per_grader, order_seed=None):
        if participants_location.is_dir():
            participants = Assignment.from_divvy_assignment_dir(
                participants_location
            ).submitters
        elif is_zipfile(participants_location):
            participants = Assignment.from_bblearn_assignment_download_zip(
                participants_location
            ).submitters
        else:
            participants = (
                participants_location.read_text().replace('\r', '').split('\n')
            )

        return cls.from_participant_list(participants, gradees_per_grader,
                                        order_seed)


    @classmethod
    def from_participant_list(cls, participants, gradees_per_grader,
                              order_seed=None):
        if gradees_per_grader >= len(participants):
            pass  # TODO: Raise appropriate exception
        seed(order_seed)
        participants = list(sorted(participants))
        shuffle(participants)

        # We simulate slices that wrap around from the end of the list to the
        # front and vice versa by copying the participant list three times and
        # then looping over the middle of that list.  Thus we get the
        # participants starting with the first, but the indices reflect the
        # position in the looped list.
        n = len(participants)
        looped_participants = participants * 3
        grader_map = {}
        for (i, participant) in list(enumerate(looped_participants))[n:-n]:
            # The next gradees_per_grader participants after the current
            # participant are those the current participant will grade
            gradees = looped_participants[i+1:(i + 1 + gradees_per_grader)]
            grader_map[participant] = gradees

        return cls(grader_map)

    @classmethod
    def load_from_file(cls, filename):
        with open(filename) as f:
            return cls(load(f))

    def __init__(self, grader_map):
        self.__grader_map = grader_map

        gradee_map = {}
        for grader, gradees in grader_map.items():
            for gradee in gradees:
                if gradee_map.get(gradee):
                    gradee_map[gradee].append(grader)
                else:
                    gradee_map[gradee] = [grader]

        self.__gradee_map = gradee_map

    @property
    def graders(self):
        return list(self.__grader_map.keys())

    @property
    def gradees(self):
        return list(self.__gradee_map.keys())

    def gradees_for(self, grader):
        return self.__grader_map.get(grader)

    def graders_for(self, gradee):
        return self.__gradee_map.get(gradee)

    def save(self, to):
        with open(to, 'w') as grading_assignment_file:
            dump(self.__grader_map, grading_assignment_file, indent=4)
