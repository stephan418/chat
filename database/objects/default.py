class DBObject:
    """
    Superclass of all Database objects
    """
    def get_item(self, name: str):
        return self.__dict__.get(name)

    def has_item(self, name: str):
        return name in self.__dict__

    def set_item(self, name: str, value):
        self.__dict__.update({name: value})
