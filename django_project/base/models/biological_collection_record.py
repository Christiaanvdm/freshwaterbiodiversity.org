# coding=utf-8
"""Biological collection record model definition.

"""

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.dispatch import receiver

from base.models.location_site import LocationSite
from base.utils.gbif import update_fish_collection_record
from base.models.taxon import Taxon


class BiologicalCollectionRecord(models.Model):
    """Biological collection model."""
    CATEGORY_CHOICES = (
        ('alien', 'Alien'),
        ('indigenous', 'Indigenous'),
        ('translocated', 'Translocated')
    )
    site = models.ForeignKey(
        LocationSite,
        models.CASCADE,
        related_name='fish_collection_records',
    )
    original_species_name = models.CharField(
        max_length=100,
        blank=True,
        default='',
    )
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        blank=True,
    )
    present = models.BooleanField(
        default=True,
    )
    collection_date = models.DateField(
        default=timezone.now
    )
    collector = models.CharField(
        max_length=100,
        blank=True,
        default='',
    )
    owner = models.ForeignKey(
        User,
        models.SET_NULL,
        blank=True,
        null=True,
    )
    notes = models.TextField(
        blank=True,
        default='',
    )
    taxon_gbif_id = models.ForeignKey(
        Taxon,
        models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Taxon GBIF ',
    )

    # noinspection PyClassicStyleClass
    class Meta:
        """Meta class for project."""
        app_label = 'base'
        abstract = True

    def on_post_save(self):
        update_fish_collection_record(self)


@receiver(models.signals.post_save)
def collection_post_save_handler(sender, instance, **kwargs):
    """
    Fetch taxon from original species name.
    """
    if not issubclass(sender, BiologicalCollectionRecord):
        return

    models.signals.post_save.disconnect(
            collection_post_save_handler,
    )
    instance.on_post_save()
    models.signals.post_save.connect(
            collection_post_save_handler,
    )
