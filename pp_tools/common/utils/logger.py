from datetime import datetime
import logging
import os
from pp_tools.common.constants import LOGS_PATH



def get_logger(logger_name: str = "pp_tools", level: str = "INFO", logger_filename = "pp_tools", flag_stdout: bool = False) -> logging.Logger:
    now = datetime.now()
    sufix = now.strftime("%Y_%m_%d")
    filename = os.path.basename(logger_filename)
    if filename.find(".py") > 0:
        filename_base = filename[:-3]
    _logger_filename = "{0}_{1}.log".format(filename_base, sufix)
    logger_full_filename = os.path.join(LOGS_PATH, _logger_filename)
    if flag_stdout:
        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    else:
        logging.basicConfig(
            filename=logger_full_filename,
            filemode='a+'
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    logger = logging.getLogger(logger_name)
    LEVEL = logging._nameToLevel.get('INFO')
    if level in logging._nameToLevel:
        LEVEL = logging._nameToLevel.get(level)
    logger.setLevel(LEVEL)
    return logger
