class File:
    def __init__(self, name, author, timestamp, location):
        self.__name = name
        self.__author = author
        self.__timestamp = timestamp
        self.__location = location

    def __str__(self):
        return f"{self.name} by {self.author}"

    def __repr__(self):
        str_parts = [
            f"name='{self.name}'",
            f"author='{self.author}'",
            f"timestamp='{self.timestamp}'",
            *self.__additional_str_parts(),
            f"location='{repr(self.__location)}'"
        ]
        return f"File({', '.join(str_parts)})"

    def __additional_str_parts(self):
        return []

    @property
    def name(self):
        """The filename minus BBLearn's add-ons"""
        return self.__name

    @property
    def author(self):
        """The username of the student who submitted the file"""
        return self.__author

    @property
    def timestamp(self):
        """The timestamp for the submission attempt the file is from"""
        return self.__timestamp

    @property
    def location(self):
        return self.__location

    def get_data(self):
        return self.__location.get_data(self)

    def same_author_as(self, other):
        return self.author == other.author

    def same_timestamp_as(self, other):
        return self.timestamp == other.timestamp

    def save(self, to):
        with open(to, 'wb') as out_file:
            out_file.write(self.get_data())
