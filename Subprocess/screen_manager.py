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
            Console.info(f"Trying to execute the script in :{script_path}")
            script_dir = ScreenManager._get_directory(script_path)
            if script_dir is None:
                Console.error(f"{script_path} this script not exist.")
                Logger.log(f"{script_path} this script not exist.")
                return None

            os.chdir(script_dir)
            result = subprocess.run(['bash', os.path.abspath(os.path.expanduser(script_path))], check=False, text=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            if result.returncode == 0:
                Console.info("Run a bash script on " + script_path)
                Logger.log("Run a bash script on " + script_path)
                return True
            else:
                Console.error(f"Error occurred while running '{script_path}'. Exit code: {result}")
                Logger.log(f"Error occurred while running '{script_path}'. Exit code: {result}")

        except subprocess.CalledProcessError as e:
            Console.error(f"Unable to execute '{script_path}'. {e}")
            Logger.log(f"Unable to execute '{script_path}'. {e}")

    @staticmethod
    def _get_directory(file_path):
        if file_path.startswith('~'):
            file_path = os.path.expanduser(file_path)
        else:
            raise ValueError(file_path + " is not an expected path type.")
        if not os.path.exists(file_path):
            return None
        try:
            directory = os.path.dirname(file_path)
        except (OSError, ValueError):
            return None
        return directory
