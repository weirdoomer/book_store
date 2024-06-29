from os import remove
from pathlib import Path

from django.conf import settings
from django.core.files.storage import FileSystemStorage


class OverwriteImageStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            remove(Path(settings.MEDIA_ROOT, name))
        return name
