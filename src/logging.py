import logging.config


def setup_logging(verbose: int) -> None:
    if verbose >= 3:
        level = "DEBUG"
    elif verbose == 2:
        level = "INFO"
    else:
        level = "WARN"

    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
            },
        },
        "handlers": {
            "default": {
                "level": f"{level}",
                "formatter": "standard",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",  # Default is stderr
            },
        },
        "loggers": {
            "": {  # root logger
                "handlers": ["default"],
                "level": f"{level}",
                "propagate": False,
            },
            "src": {
                "handlers": ["default"],
                "level": f"{level}",
                "propagate": False,
            },
            "__main__": {  # if __name__ == '__main__'
                "handlers": ["default"],
                "level": f"{level}",
                "propagate": False,
            },
        },
    }
    logging.config.dictConfig(LOGGING_CONFIG)
