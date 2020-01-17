"""restful api implement based on gunicorn """
import logging
from flask import Flask
from gunicorn.app.base import BaseApplication

from app import APP


class Application(BaseApplication):
    """ implement of application based on gunicorn """
    def __init__(self, app, config) -> None:
        self.app = app
        self.config = config
        BaseApplication.__init__(self)

    def load_config(self) -> None:
        for key, value in self.config.items():
            if key in self.cfg.settings and value is not None:
                self.cfg.set(key, value)

    def init(self, parser, opts, args):
        pass

    def load(self) -> Flask:
        return self.app

    @staticmethod
    def stop():
        """Shutting down AI restAPI service"""
        logging.info("Shutting down AI restAPI service")


GUNICORN_APP = Application(
    app=APP,
    config={
        "bind": "0.0.0.0:8888",
        "workers": 5,
        "timeout": 10000,
        "threads": 5,
    },
)


if __name__ == '__main__':
    GUNICORN_APP.run()
