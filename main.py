import datetime

from Subprocess.screen_manager import ScreenManager
from Subprocess.json_handler import JsonDataBase
from Subprocess.console_massage_handler import Console
from Subprocess.logger import Logger


def main():
    Console.info("Starting.")
    Logger.create_log()
    Console.info("Reading Json File.")
    data = JsonDataBase()

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
                    data.get_screens()[screen_name]["ending_time"] = \
                        data.get_screens()[screen_name]["starting_time"] + datetime.timedelta(minutes=cool_down)
                    data.get_screens()[screen_name]["how_many_times_are_down_the_screen"] += 1

                    Console.info(screen_name + " Server down or screen not found at " + str(datetime.datetime.now()))
                    Logger.log(screen_name + " Server down or screen not found at " + str(datetime.datetime.now()))

                if data.get_screens()[screen_name]["ending_time"] <= datetime.datetime.now():
                    # run bash script.
                    if screen_name in ScreenManager.screen_list():
                        # double check.
                        data.get_screens()[screen_name]["starting_time"] = None
                        data.get_screens()[screen_name]["ending_time"] = None
                        continue

                    ScreenManager.run_bash_script(bash_file)

                    Console.info("Bash script run at " + str(datetime.datetime.now()))
                    Logger.log("Bash script run at " + str(datetime.datetime.now()))

                    data.get_screens()[screen_name]["starting_time"] = None
                    data.get_screens()[screen_name]["ending_time"] = None


if __name__ == '__main__':
    main()
