from time import asctime, strftime, localtime
from os import mkdir
from main.utils.PropertiesUtils import PropertiesUtils

log_path = "./log"
level = {
    "INFO": 0,
    "ERROR": 1,
    "DEBUG": 2,
    "ALL": 4
}
default_level=PropertiesUtils("./defaults.properties").getStr("log_level")

class Logger:
    def __init__(self, calling_from, given_level=default_level, is_archive=False, path=log_path):
        self.name = f"{type(calling_from).__name__}-{strftime('%Y%m%d', localtime())}"
        self.path = path
        self.is_archive = is_archive
        self.calling_from = calling_from.__class__
        self.level = level[given_level]
        try:
            mkdir(log_path)
        except FileExistsError:
            self.debug("Directory ./log exists already... skipping creation")
        with open(f"{self.path}/{self.name}.log", "w"):
            self.debug(f"Created log file {self.name}.log")

    def log(self, message: str, exception=None):
        self.store_message(message, "LOG", exception)

    def debug(self, message: str, exception=None):
        self.store_message(message, "DEBUG", exception)

    def warn(self, message: str, exception=None):
        self.store_message(message, "WARN", exception)

    def error(self, message: str, exception=None):
        self.store_message(message, "ERROR", exception)

    def store_message(self, message, name, exception):
        nice_message = f"[{asctime(localtime())}]: {name} {self.calling_from}: {message}\n"
        if exception is not None:
            nice_message += f"{exception.__traceback__}\n"
        try:
            if self.level >= level[name]:
                print(nice_message, end="")
        except KeyError:
            self.warn(f"Unknown log level {name}")

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
