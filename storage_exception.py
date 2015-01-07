class StorageException(Exception):
    def __init__(self, value, message):
        self.__value = value
        self.__message = message

    def __str__(self):
        return repr(self.__message)
