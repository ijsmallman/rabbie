import logging


def init_root_logger(file_name: str,
                     file_log_level=logging.DEBUG,
                     console_log_level=logging.INFO) -> None:
    """
    Initialise logger and attach console and file handlers

    Parameters
    ----------
    file_name: str
        name for log file
    file_log_level: [logging.NOTSET, logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
        log level for file log handler (default: logging.DEBUG)
    console_log_level: [logging.NOTSET, logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
        log level for console log handler (default: logging.INFO)
    """
    logging.getLogger().setLevel(logging.DEBUG)
    fh = logging.FileHandler(file_name)
    fh.setLevel(file_log_level)
    ch = logging.StreamHandler()
    ch.setLevel(console_log_level)
    log_formatter = logging.Formatter('%(asctime)s %(name)s [%(levelname)s] %(message)s')
    fh.setFormatter(log_formatter)
    ch.setFormatter(log_formatter)
    logging.getLogger().addHandler(fh)
    logging.getLogger().addHandler(ch)
