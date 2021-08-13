class FileLocation:
    def __init__(self, path):
        self.__path = path

    @property
    def path(self):
        return self.__path

    def get_data(self, file):
        raise NotImplementedError
