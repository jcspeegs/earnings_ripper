import logging
from functools import wraps
from os.path import join, makedirs
import re


def verbose_get(func):
    @wraps(func)
    def wrapper(url, dry_run=False, *args, **kwargs):
        logging.info(f'Ripping {url}')
        if dry_run is True:
            return url
        else:
            return func(url, *args, **kwargs)
    return wrapper


def cleanse_filename(filename: str):
    replace = ' ()-_'
    pattern = f"[{''.join([re.escape(char) for char in replace])}]+"
    return re.sub(pattern, '_', filename).strip('_').lower()


def write_file(directory, filename: str, content: bytes, dry_run=False):
    ''' Write file and create directory if it does not exist'''
    logger = logging.getLogger(__name__)
    file = join(directory, filename)
    logger.info(f'writing {file}')
    if dry_run is not True:
        makedirs(directory, exist_ok=True)
        with open(file, 'wb') as fl:
            fl.write(content)
