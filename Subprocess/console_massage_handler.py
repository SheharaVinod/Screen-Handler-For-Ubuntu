from Subprocess.logger import Logger

class Console:
    _prefix = "[ScreenManager] "

    @staticmethod
    def info(massage):
        print(Console._prefix, "INFO: ", massage)

    @staticmethod
    def warn(massage):
        print(Console._prefix, "WARN: ", massage)

    @staticmethod
    def error(massage):
        print(Console._prefix, "ERROR: ", massage)

    @staticmethod
    def log(massage):
        Logger.log(massage)
