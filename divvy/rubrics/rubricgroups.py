from itertools import chain, groupby
from os import mkdir
from pathlib import Path

from divvy import (
    AssignmentDirectory,
    BBLearnAssignmentDownloadZip,
    BBLearnSubmittedFile
)
from divvy.errors import (
    EmptyAssignmentError,
    InvalidBBLearnSubmittedFilenameError,
    UnsuitableDestinationError
)
from divvy.assignment import Assignment
from .rubricfile import RubricFile


class RubricGroups:
    @classmethod
    def from_divvy_assignment(cls, divvy_assignment, name=None):
        rubric_files = []
        for file in divvy_assignment.files:
            rubric_files.append(RubricFile.from_bblearn_submitted_file(file))

        rubric_groups = [
            RubricGroup(sorted(list(rubric_group), key=lambda rf: rf.grader))
            for _, rubric_group
            in groupby(sorted(rubric_files, key=lambda rf: rf.gradee),
                       key=lambda rf: rf.gradee)
        ]

        name = name or divvy_assignment.name
        return cls(name=name, rubric_groups=rubric_groups)

    def __init__(self, name, rubric_groups):
        self.__name = name

        rubric_groups = sorted(rubric_groups,
                               key=lambda rg: rg.rubrics[0].gradee)
        self.__rubric_groups_by_gradee = {}
        for rg in rubric_groups:
            self.__rubric_groups_by_gradee[rg.gradee] = rg

    @property
    def name(self):
        return self.__name

    def rubric_group_for_gradee(self, gradee):
        return self.__rubric_groups_by_gradee.get(gradee)

    def save_path(self, to):
        return to / Path(self.name)

    def save(self, to):
        to = Path(to) / Path(self.name)
        if to.exists():
            raise UnsuitableDestinationError(
                f"The given save path already exists:\n\t{to}"
            )
        mkdir(to)

        for attempt in self.attempts:
            attempt_path = to / Path(
                attempt.submitted_by + "_" + attempt.submitted_on
            )
            mkdir(attempt_path)
            for file in attempt.files:
                file_path = attempt_path / Path(file.name)
                file.save(file_path)
