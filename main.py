import json
import datetime
import subprocess

from Subprocess.screen_manager import ScreenManager
from Subprocess.json_handler import JsonDataBase
from Subprocess.console_massage_handler import Console
from Subprocess.logger import Logger


def main():
    Console.info("Starting.")
    Logger.create_log()
    Console.info("Reading Json File.")
    data = JsonDataBase()

    # searching_cool_down_in_sec: int = 5
    # waiting_cool_down_in_sec: int = 10

    # started_time = datetime.datetime.now()
    # ended_time = started_time + datetime.timedelta(seconds=waiting_cool_down_in_sec)
    # is_screen_is_down = {"build": True, "survival": False}

    while True:
        # for every screen. and check start and end time.
        for screen_name, its_property in data.get_screens().items():
            cool_down = data.get_screens()[screen_name]["waiting_cool_down_in_min"]
            starting_in = data.get_screens()[screen_name]["starting_time"]
            bash_file = data.get_screens()[screen_name]["bash_script_path"]

            if screen_name not in ScreenManager.screen_list():
                # server is down or screen not found.

                if starting_in is None:
                    data.get_screens()[screen_name]["starting_time"] = datetime.datetime.now()
                    data.get_screens()[screen_name]["ending_time"] =\
                        data.get_screens()[screen_name]["starting_time"] + datetime.timedelta(minutes=cool_down)
                    data.get_screens()[screen_name]["how_many_times_are_down_the_screen"] += 1

                    Console.log("Server down or screen not found at " + str(datetime.datetime.now()))

                if data.get_screens()[screen_name]["ending_time"] <= datetime.datetime.now():
                    # run bash script.
                    ScreenManager.run_bash_script(bash_file)
                    Console.log("Bash script run at " + str(datetime.datetime.now()))

                    data.get_screens()[screen_name]["starting_time"] = None
                    data.get_screens()[screen_name]["ending_time"] = None


if __name__ == '__main__':
    main()
