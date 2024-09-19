from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from .models import Product


@receiver(post_delete, sender=Product)
def post_delete_image(sender, instance, *args, **kwargs):
    """При удалении объекта товара будет удаляться связанное изображение"""
    instance.image.delete(save=False)


@receiver(pre_save, sender=Product)
def pre_save_delete_old_image(sender, instance, *args, **kwargs):
    """Перед сохранением объекта товара будет удаляться связанное изображение"""
    try:
        old_image = Product.objects.get(pk=instance.pk).image
    except Product.DoesNotExist:
        return False
    else:
        old_image.delete(save=False)
