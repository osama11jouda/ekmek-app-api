import os
import re
from typing import Union

from flask_uploads import UploadSet, IMAGES
from werkzeug.datastructures import FileStorage

IMAGE_SET = UploadSet('images', IMAGES)


def save_image(image: FileStorage, folder: str, name: str= None) -> str:
    return IMAGE_SET.save(image, folder, name)


def get_path(filename: str, folder: str) -> str:
    return IMAGE_SET.path(filename=filename, folder=folder)


def _retrieve_filename(file: Union[str, FileStorage], folder: str) -> str:
    if isinstance(file, FileStorage):
        return file.filename
    return file


def image_any_format(file: Union[str, FileStorage], folder: str) -> Union[None, str]:
    filename = _retrieve_filename(file)
    for _format in IMAGES:
        image = f"{filename}.{_format}"
        image_path = get_path(image, folder)
        if os.path.isfile(image_path):
            return image_path
    return None


def is_filename_safe(file: Union[str, FileStorage], folder: str) -> bool:
    filename = _retrieve_filename(file)
    allowed_format = '|'.join(IMAGES)
    regex = f"^[a-zA-Z0-9][a-zA-Z0-9_()-\.]*\.({allowed_format})$"
    return re.match(regex, filename) is not None


def get_basename(file: Union[str, FileStorage]) -> str:
    filename = _retrieve_filename(file)
    return os.path.split(filename)[1]


def get_extension(file: Union[str, FileStorage]) -> str:
    filename = _retrieve_filename(file)
    return os.path.splitext(filename)[1]
