import disnake
import configparser


class Config:
    def __init__(self, directory):
        self.directory = directory
        self.config = configparser.ConfigParser()
        self.load()

    def load(self):
        # TODO Expose as public attributes
        self.config.read(f"{self.directory}/config.ini")
        self.token = str(self.config.get("server", "token"))
        self.botname = str(self.config.get("server", "name", fallback="Discord Bot"))
        self.botcolour = disnake.Colour(int(self.config.get("server", "colour", fallback="0xffff00"), 16))
        system_channel = self.config.get("server", "system_channel", fallback=None)
        self.system_channel = int(system_channel) if system_channel else None
        self.logo = str(self.config.get("server", "logo", fallback=None))
        self.language = str(self.config.get("server", "language", fallback="en-gb"))

    def update(self, section, option, value):
        self.config[section][option] = value
        with open(f"{self.directory}/config.ini", "w") as configfile:
            self.config.write(configfile)
        self.load()

    def get(self, section, option, fallback=None):
        return self.config.get(section, option, fallback=fallback)
