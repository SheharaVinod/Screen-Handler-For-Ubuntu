import os
import subprocess

from Subprocess.console_massage_handler import Console
from Subprocess.logger import Logger


class ScreenManager:

    @staticmethod
    def screen_list() -> list:
        try:
            list_of_running_screen_names = []
            output = subprocess.check_output(['screen', '-ls'], stderr=subprocess.DEVNULL, text=True)
            output_lines = output.strip().split("\n")

            if len(output_lines) <= 1:
                # No screen sessions are currently running.
                return []

            for item in output_lines[1:-1]:
                split_from_tab = item.split("\t")[1]
                remove_dot = split_from_tab.split(".")[1]
                list_of_running_screen_names.append(remove_dot)

            if len(list_of_running_screen_names) == 0:
                # No screen sessions are currently running.
                return []

            return list_of_running_screen_names

        except subprocess.CalledProcessError:
            # No screen sessions are currently running.
            return []

        except FileNotFoundError:
            # Error: 'screen' command not found. Make sure it is installed and in your PATH.
            return []

    @staticmethod
    def is_screen_running(screen_name) -> bool:
        try:
            list_of_running_screens = ScreenManager.screen_list()
            Console.info("Checking for screen " + screen_name)
            if screen_name in list_of_running_screens:
                Console.info("Found the screen")
                return True
            return False
        except subprocess.CalledProcessError:
            Console.warn("There is no screen found on that name - " + screen_name)
            return False

    @staticmethod
    def terminate_screen(screen_name) -> bool:
        # deprecated.
        try:
            subprocess.run(['screen', '-S', screen_name, '-X', 'quit'], check=True)
            return True
        except subprocess.CalledProcessError as e:
            Console.warn(e)
            return False

    @staticmethod
    def run_bash_script(script_path):
        try:
            subprocess.run(['bash', script_path], check=True, env=os.environ.copy())
            Console.info("Run a bash script on " + script_path)
            Logger.log("Run a bash script on " + script_path)

        except subprocess.CalledProcessError as e:
            Console.error(f"Unable to execute '{script_path}'. {e}")

