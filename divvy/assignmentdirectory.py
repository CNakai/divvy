from pathlib import Path
from .filelocation import FileLocation


class AssignmentDirectory(FileLocation):
    def __init__(self, path):
        path = Path(path)
        if not path.is_dir():
            raise Exception(
                f"{path} does not lead to a Divvy assignment directory"
            )
        super().__init__(path)

    def get_data(self, bblearn_submitted_file):
        file_path = (
            self.path /
            Path(bblearn_submitted_file.author +
                 "_" + bblearn_submitted_file.timestamp) /
            Path(bblearn_submitted_file.name)
        )
        with open(file_path, 'rb') as file:
            file_bytes = file.read()

        return file_bytes
