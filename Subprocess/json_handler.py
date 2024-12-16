import json
from datetime import datetime

from Subprocess.console_massage_handler import Console


class JsonDataBase:
    # Structure.
    # screens = {
    #     "build": {
    #         "bash_script_path": "shehara/start.sh",
    #         "waiting_cool_down_in_min": 5,
    #         "is_screen_is_down": True,
    #         "how_many_times_are_down_the_screen": 0,
    #         "last_down_time": datetime.datetime.now(),
    #         "if_screen_not_found_while_checking_run_this_script": "copy error log files using a bash script."
    #     },
    #     "survival": {
    #         "bash_script_path": "shehara/start.sh",
    #         "waiting_cool_down_in_min": 5,
    #         "is_screen_is_down": True,
    #         "how_many_times_are_down_the_screen": 0,
    #         "starting_time":None,
    #         "ending_time":None,
    #         "last_down_time": datetime.datetime.now(),
    #         "if_screen_not_found_while_checking_run_this_script": "copy error log files using a bash script."
    #     }
    # }

    def __init__(self):
        self.screens = {}

        with open("data/handle.json") as data:
            self.json_data = json.load(data)
        self._generate_structure_of_data()

    def _generate_structure_of_data(self):
        for screens in self.json_data["screens"]:
            screen_name = screens["screen_name"]

            local_dict = {}
            bash_script_path = screens["bash_script_path"]
            checking_cool_down_in_minutes = screens["checking_cool_down_in_minutes"]
            if_screen_not_found_while_checking_run_this_script: str = screens["optional"][
                "if_screen_not_found_while_checking_run_this_script"]
            local_dict["bash_script_path"] = bash_script_path
            local_dict["waiting_cool_down_in_min"] = checking_cool_down_in_minutes
            local_dict["how_many_times_are_down_the_screen"] = 0
            local_dict["starting_time"] = None
            local_dict["ending_time"] = None

            if if_screen_not_found_while_checking_run_this_script == "copy error log files using a bash script.":
                local_dict["if_screen_not_found_while_checking_run_this_script"] = ""
            else:
                local_dict[
                    "if_screen_not_found_while_checking_run_this_script"] = if_screen_not_found_while_checking_run_this_script
            self.screens[screen_name] = local_dict
        Console.info("Data is successfully imported.")

    def get_screens(self) -> dict:
        return self.screens
