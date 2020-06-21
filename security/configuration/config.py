from json import load, dumps
from flask import Flask


class Config:
    def __init__(self, config_path: str, reload=False):
        """
        Configuration handler
        :param config_path: Path to the configuration file which is going to be used for storing and loading changes
        :param reload: Sync file and handler during execution (Hot Reload)
        """
        self._config_path = config_path

        with open(config_path, 'r') as file:
            self._config = dict(load(file))

        self.reload = reload

    def __setitem__(self, key, value):
        self._config.update({key: value})

        if self.reload:
            with open(self._config_path, 'w') as file:
                file.write(dumps(self._config, indent=4))

    def __getitem__(self, key):
        if self.reload:
            with open(self._config_path, 'r') as file:
                self._config = dict(load(file))

        return self._config[key]

    def apply_to_app(self, app: Flask):
        """ Applies all config keys matching flask.* to the Flask app """
        for item in filter(lambda x: x[0].startswith('flask.'), self._config.items()):
            app.config[item[0]] = item[1]
