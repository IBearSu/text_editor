from fileinput import filename


class StatusBar:
    def __init__(self, name_of_file = "Untitled",status = "Initializing"):
        self.name_of_file = name_of_file
        self.status = status
