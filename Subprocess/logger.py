import datetime
import os
from Subprocess.console_massage_handler import Console


class Logger:
    _prefix = "[ScreenManager] "
    _current_log = "log-" + str(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")) + ".txt"

    @staticmethod
    def create_log():
        try:
            print(Logger._current_log)
            os.makedirs("logs", exist_ok=True)
            with open("logs/" + Logger._current_log, 'w') as f:
                f.write('# ----------------------- Logs ----------------------- \n')
            Console.info("A new Log file created successfully.")
        except IOError:
            Console.warn("Could not create a Log.")

    @staticmethod
    def log(massage):
        # "[ScreenManager] at mm/dd  HH:MM:SS -> "
        time = datetime.datetime.now()
        log_prefix = f"{Logger._prefix} at {time.month}/{time.day} {time.hour}:{time.minute}:{time.second} -> "
        try:
            with open("logs/" + Logger._current_log, 'a') as data:
                data.write(log_prefix + massage + "\n")
            Console.info("'" + massage + "'" + " successfully Logged.")
        except IOError:
            Console.warn("Fail to logged the msg '" + massage + "'")
