from io import BytesIO
from pathlib import Path

from django.core.files import File
from django.utils.text import slugify as django_slugify
from PIL import Image


def image_resize(image):
    try:
        with Image.open(image) as img:
            img.load()

        pic_size = (367, 507)

        resized_img = img.resize(pic_size)

        img_filename_without_format = Path(image.file.name).name.split(".")[0]

        # Save the resized image into the buffer, noting the correct file type
        buffer = BytesIO()
        resized_img.save(buffer, format="webp")

        # Wrap the buffer in File object
        file_object = File(buffer, f"{img_filename_without_format}.webp")

        return file_object
    except ValueError:
        return None


def slugify(string):
    """Встроенная django-функция slugify, модифицированная
    для обработки кириллицы"""
    alphabet = {
        "а": "a",
        "б": "b",
        "в": "v",
        "г": "g",
        "д": "d",
        "е": "e",
        "ё": "yo",
        "ж": "zh",
        "з": "z",
        "и": "i",
        "й": "j",
        "к": "k",
        "л": "l",
        "м": "m",
        "н": "n",
        "о": "o",
        "п": "p",
        "р": "r",
        "с": "s",
        "т": "t",
        "у": "u",
        "ф": "f",
        "х": "kh",
        "ц": "ts",
        "ч": "ch",
        "ш": "sh",
        "щ": "shch",
        "ы": "i",
        "э": "e",
        "ю": "yu",
        "я": "ya",
    }

    return django_slugify("".join(alphabet.get(w, w) for w in string.lower()))
