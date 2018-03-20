# coding=utf-8
"""IUCN Status model definition.

"""

from django.db import models
from django.dispatch import receiver


class IUCNStatus(models.Model):
    """IUCN status model."""
    CATEGORY_CHOICES = (
        ('LC', 'Least Concern'),
        ('NT', 'Near Threatened'),
        ('VU', 'Vulnerable'),
        ('EN', 'Endangered'),
        ('CR', 'Critically Endangered'),
        ('EW', 'Extinct In The Wild'),
        ('EX', 'Extinct'),
    )

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        blank=True,
        default='',
    )
    sensitive = models.BooleanField(
        default=False
    )

    def __str__(self):
        return u'%s' % self.category

    # noinspection PyClassicStyleClass
    class Meta:
        """Meta class for project."""
        app_label = 'fish'
        verbose_name_plural = 'IUCN Status'
        verbose_name = 'IUCN Status'


@receiver(models.signals.pre_save, sender=IUCNStatus)
def iucn_status_post_save_handler(sender, instance, **kwargs):
    if instance.category:
        # if the category is Critically Endangered or Endangered or
        # Vulnerable then the iucn status is sensitive
        if instance.category == 'CR' or \
                instance.category == 'EN' or \
                instance.category == 'VU':
            instance.sensitive = True
        else:
            instance.sensitive = False
