from django.contrib.auth import get_user_model
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from versatileimagefield.image_warmer import VersatileImageFieldWarmer

User = get_user_model()


@receiver(post_save, sender=User)
def warm_versatile_images(sender, instance, **kwargs):
    if sender == User:
        if instance.avatar:
            warmer = VersatileImageFieldWarmer(
                instance_or_queryset=instance, rendition_key_set="headshot", image_attr="avatar"
            )
            num_created, failed_to_create = warmer.warm()


@receiver(post_delete, sender=User)
def delete_files(sender, instance, **kwargs):
    if sender == User:
        # Deletes Image Renditions
        instance.avatar.delete_all_created_images()
        # Deletes Original Image
        instance.avatar.delete(save=False)
