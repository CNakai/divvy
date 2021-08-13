class DivvyError(Exception):
    pass


# TODO: Replace with assertions?
class EmptyAssignmentError(DivvyError):
    pass


# TODO: Replace with assertions?
class EmptyAttemptError(DivvyError):
    pass


class InvalidBBLearnSubmittedFilenameError(DivvyError):
    def __init__(self, filename, message=None):
        self.filename = filename
        if not message:
            self.message = f"Invalid BBLearn filename:\n\t{filename}"
        super().__init__(self.message)


# TODO: Add origins
class MultipleOriginError(DivvyError):
    pass


# TODO: Remind of destination
class UnsuitableDestinationError(DivvyError):
    pass
