from io import BytesIO
from pathlib import Path

from django.core.files import File
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
