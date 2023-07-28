from sys import path

from jproperties import Properties


class PropertiesUtils(Properties):
    def __init__(self, file):
        super().__init__()
        with open(file, "rb") as config_file:
            self.load(config_file)

    def getInt(self, key):
        return int(self.get(key).data)

    def getStr(self, key):
        return str(self.get(key).data)

    def getBoolean(self, key):
        return self.get(key).data == "true"

    def getFloat(self, key):
        return float(self.get(key).data)

    def getProperty(self, key):
        return self.get(key).data