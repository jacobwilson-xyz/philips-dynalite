import logging
import requests
import base64
import dotenv
import sys
import os


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def encode_credentials(username, password):
    """Encodes username and password for basic authentication."""
    logger.info("Encoding credentials")
    credentials = f"{username}:{password}".encode()
    return base64.b64encode(credentials).decode("utf-8")


class DynaliteConfig:
    """Holds Dynalite configuration details."""

    def __init__(self):
        logger.info("Loading configuration")
        self.username = os.environ.get('DYNALITE_USERNAME')
        self.password = os.environ.get('DYNALITE_PASSWORD')
        self.gateway_url = os.environ.get('DYNALITE_GATEWAY_URL')
        self.deault_fade_time = os.environ.get('DYNALITE_DEFAULT_FADE', 2000)
        self.auth = self.username is not None and self.password is not None

    def get_gateway_url(self):
        return self.gateway_url

    def get_authorization_header(self):
        if self.auth:
            return {"Authorization": f"Basic {encode_credentials(self.username, self.password)}"}
        else:
            return {}


def send_dynalite_command(config, endpoint, params):
    """Sends a command to the Dynalite system."""
    logger.info(f"Sending Dynalite command")
    url = f"http://{config.get_gateway_url()}/{endpoint}"
    headers = config.get_authorization_header()
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    logger.info(f"Command sent. url={url}, params={params}, headers={headers}")


def set_dynalite_preset(config: DynaliteConfig, area_id: int, preset_id: int, fade_time: int = None) -> None:
    """Sets a Dynalite preset.

    Args:
        config (DynaliteConfig): The Dynalite configuration object.
        area_id (int): The ID of the Dynalite area.
        preset_id (int): The ID of the Dynalite preset.
        fade_time (int, optional): The fade time in milliseconds. Defaults to 2000.
    """
    logger.info(f"Setting Dynalite preset: area_id={area_id}, preset_id={preset_id}, fade_time={fade_time}")
    params = {"a": area_id, "p": preset_id, "f": fade_time or config.deault_fade_time}
    send_dynalite_command(config, "SetDyNet.cgi", params)


def set_dynalite_channel(config: DynaliteConfig, area_id: int, channel_id: int, value: int, fade_time: int = None) -> None:
    """Sets a specific Dynalite channel to a specified value (0-100).

    Args:
        config (DynaliteConfig): The Dynalite configuration object.
        area_id (int): The ID of the Dynalite area.
        channel_id (int): The ID of the Dynalite channel.
        value (int): The new channel value (0-100)
        fade_time (int, optional): The fade time in milliseconds. Defaults to 2000.
    """
    logger.info(f"Setting Dynalite chanel: area_id={area_id}, channel_id={channel_id}, value={value}, fade_time={fade_time}")
    params = {"a": area_id, "c": channel_id, "l": value, "f": fade_time or config.deault_fade_time}
    send_dynalite_command(config, "SetDyNet.cgi", params)


def help():
    print(f"""
    Available commands:

    - set_preset <area_id> <preset_id> (fade_time): 
        Sets a Dynalite preset for the specified area.

    - set_channel <area_id> <channel_id> <value> (fade_time):
        Sets the value of a specific Dynalite channel in the given area.
        Value must be between 0 and 100.
    """)
    

if __name__ == "__main__":
    try:
        dotenv.load_dotenv()
        config = DynaliteConfig()
        function = sys.argv[1]
        if function == "set_preset":
            area_id = int(sys.argv[2])
            preset_id = int(sys.argv[3])
            fade_time = int(sys.argv[4]) if len(sys.argv) > 4 else int(config.deault_fade_time)
            set_dynalite_preset(config, area_id, preset_id, int(fade_time))
        elif function == "set_channel":
            area_id = int(sys.argv[2])
            channel_id = int(sys.argv[3])
            value = int(sys.argv[4])
            fade_time = int(sys.argv[5]) if len(sys.argv) > 5 else int(config.deault_fade_time)
            set_dynalite_channel(config, area_id, channel_id, int(value), int(fade_time))
        elif function == "help" or function is None:
            help()
        else:
            print(f"Invalid function: {function}")
    except (IndexError, ValueError) as e:
        logger.error(f"Error: Invalid arguments provided. {e}")
        print("Error: Invalid arguments provided.")
        help()
