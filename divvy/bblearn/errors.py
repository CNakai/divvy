from divvy.errors import DivvyError

class InvalidFilenameError(DivvyError):
    def __init__(self, filename, message=None):
        self.filename = filename
        if not message:
            self.message = f"Invalid BBLearn filename:\n\t{filename}"
        super().__init__(self.message)
