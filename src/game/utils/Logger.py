from time import asctime, strftime, localtime

level = {
    "INFO": 0,
    "DEBUG": 1,
}


class Logger:
    def __init__(self, callingFrom, path, givenLevel, shouldArchive=False):
        self.name = f"{type(callingFrom).__name__}-{strftime('%Y%m%d', localtime())}"
        self.path = path
        self.shouldArchive = shouldArchive
        self.callingFrom = callingFrom.__class__
        self.level = level[givenLevel]
        with open(f"{self.path}/{self.name}.log"):
            pass

    def log(self, message: str, exception=None):
        self.storeMessage(message, "LOG", exception)

    def debug(self, message: str, exception=None):
        self.storeMessage(message, "DEBUG", exception)

    def warn(self, message: str, exception=None):
        self.storeMessage(message, "WARN", exception)

    def error(self, message: str, exception=None):
        self.storeMessage(message, "ERROR", exception)

    def storeMessage(self, message, name, exception):
        nice_message = f"[{asctime(localtime())}]: {name} {self.callingFrom}: {message}\n"
        if exception is not None:
            nice_message += f"{exception.__traceback__} \n"
        try:
            if self.level <= level[name]:
                print(nice_message, end="")
        except KeyError:
            pass

        try:
            with open(f"{self.path}/{self.name}.log", "a") as file:
                file.write(nice_message)
        except IOError as e:
            raise IOError(f"Failed to add {name} to log with message {message}\n {e}")

    def archive(self):
        if not self.shouldArchive:
            return
        try:
            with open(f"{self.path}/{self.name}.log", "r") as copyToArchive:
                with open(f"{self.path}/LOG-{self.name}.log") as archive:
                    archive.write(copyToArchive.read())
        except IOError:
            raise IOError("Failed to archive log")
