import os
import logging
import pathlib

LOGDIR = pathlib.Path.home() / ".logs"


def get_daiquiri_logger(name, level):
    if not LOGDIR.exists():
        LOGDIR.mkdir(parents=True)
    import daiquiri

    daiquiri.setup(
        outputs=(daiquiri.output.STDERR, daiquiri.output.File(directory=str(LOGDIR))),
        level=level,
    )

    logger = daiquiri.getLogger(name)
    return logger


def Logger(name=None, level=logging.INFO, without_daiquiri=None):
    daiquiri_env_key = "{}_NO_DAIQUIRI".format(name.upper())
    without_daiquiri = without_daiquiri or os.getenv(daiquiri_env_key) in {"true", "1"}
    if without_daiquiri:
        logger = logging.getLogger(name)
        logger.setLevel(level)
    else:
        logger = get_daiquiri_logger(name, level)

    if os.getenv("DEBUG"):
        logger.setLevel(logging.DEBUG)

    return logger
