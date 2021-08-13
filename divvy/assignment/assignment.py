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
from .attempt import Attempt


class Assignment:
    @staticmethod
    def __all_for_same_assigment(attempts):
        if not attempts:
            return True

        return all([attempts[0].for_same_assignment(a) for a in attempts])

    @classmethod
    def from_bblearn_assignment_download_zip(cls, zip_path, name=None, file_factory=BBLearnSubmittedFile):
        zip_path = Path(zip_path)
        if not name:
            name = zip_path.stem

        adz = BBLearnAssignmentDownloadZip(zip_path)

        files = []
        for filename in adz.file_infolist():
            try:
                files.append(
                    file_factory.from_bblearn_filename(filename, adz)
                )
            except InvalidBBLearnSubmittedFilenameError:
                pass

        attempts = [
            Attempt(list(attempt_group))
            for _, attempt_group
            in groupby(
                sorted(
                    sorted(files, key=lambda f: f.timestamp),
                    key=lambda f: f.author
                ),
                key=lambda f: f.timestamp)
        ]

        return cls(name=name, attempts=attempts)

    @classmethod
    def from_divvy_assignment_dir(cls, dir_path, file_factory=BBLearnSubmittedFile):
        dir_path = Path(dir_path)
        name = dir_path.name
        location = AssignmentDirectory(dir_path)

        attempts = []
        attempt_dirs = sorted(dir_path.iterdir(), key=lambda p: p.name)
        for attempt_dir in attempt_dirs:
            (author, timestamp) = attempt_dir.name.split('_')
            files = []
            for submitted_file in attempt_dir.iterdir():
                files.append(file_factory(name=submitted_file.name,
                                          author=author,
                                          timestamp=timestamp,
                                          for_assignment=name,
                                          location=location))
                attempts.append(Attempt(files))

        return cls(name=name, attempts=attempts)

    def __init__(self, name, attempts):
        self.__user_attempts = {}
        self.__name = name

        if not attempts:
            raise EmptyAssignmentError("Assignments must have attempts")

        attempts = sorted(
            sorted(attempts, key=lambda attempt: attempt.submitted_on),
            key=lambda attempt: attempt.submitted_by
        )

        attempts_by_user = sorted([
            list(g) for k, g
            in groupby(
                attempts,
                key=lambda attempt: attempt.submitted_by
            )
        ], key=lambda g: g[0].submitted_by)

        for attempts in attempts_by_user:
            self.__user_attempts[attempts[0].submitted_by] = attempts

    @property
    def name(self):
        return self.__name

    @property
    def submitters(self):
        return list(self.__user_attempts.keys())

    @property
    def attempts(self):
        return list(chain.from_iterable(self.__user_attempts.values()))

    @property
    def latest_attempts(self, ):
        return [attempts[-1] for attempts in self.__user_attempts.values()]

    def attempts_for(self, username):
        return self.__user_attempts.get(username)

    def latest_for(self, username):
        attempts_for_user = self.attempts_for(username)
        if not attempts_for_user:
            return None

        return attempts_for_user[-1]

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
