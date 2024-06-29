from io import BytesIO
from pathlib import Path
from time import time

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
        image_format = "webp"

        # Сохранение картинки с измененным размеров в буфер
        # с необходимым расширением файла
        buffer = BytesIO()
        resized_img.save(buffer, format=image_format)

        # Запись буфера в File object джанги
        file_object = File(
            buffer, f"{img_filename_without_format}.{image_format}"
        )

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


def slug_check_and_gen(object):
    """
    Функция проверки поля name у предоставляемого объекта, создания на его
    основе слага и записи в поле slug предоставляемого объекта.

    Перед генерацией слага проверяются след.случаи:
    1) Если слага ранее не было (т.е в бд slug=None).

    2) Если слаг уже был и нужно сгенерировать его еще раз - для случаев,
    когда у объекта изменяется name и нужно обновить слаг.

    3) Если имя, предоставляемое в метод ген-ции слагов slugify(), состоит из
    символов и метод возвращает пустую строку - генерируется слаг след.вида
    default_slug_timestamp(время на момент создания слага).
    """
    if object.slug is None:
        object.slug = slugify(object.name)
        if object.slug == "":
            object.slug = slugify(f"default_slug_{time()}")
    elif object.slug == "":
        object.slug = slugify(f"default_slug_{time()}")
    elif object.slug:
        object.slug = slugify(object.name)
        if object.slug == "":
            object.slug = slugify(f"default_slug_{time()}")
