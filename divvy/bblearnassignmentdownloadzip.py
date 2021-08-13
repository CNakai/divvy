from zipfile import is_zipfile, ZipFile
from .filelocation import FileLocation


class BBLearnAssignmentDownloadZip(FileLocation):
    def __init__(self, path):
        if not is_zipfile(path):
            raise Exception(
                f"{path} does not lead to a BBlearn assignment download zip"
            )
        super().__init__(path)

    def file_infolist(self):
        with ZipFile(self.path) as zf:
            return zf.namelist()

    def get_data(self, bblearn_submitted_file):
        with ZipFile(self.path) as zf:
            file_bytes = zf.read(bblearn_submitted_file.bblearn_name)
        return file_bytes
