# noinspection PyUnresolvedReferences,PyPackageRequirements
import factory
import random
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from django.utils import timezone
from django.db.models import signals
from base.models import (
    LocationType,
    LocationSite,
    Profile,
    IUCNStatus,
    Taxon,
    Survey,
)


class LocationTypeF(factory.django.DjangoModelFactory):
    """
    Location type factory
    """

    class Meta:
        model = LocationType

    name = factory.Sequence(lambda n: 'Test location type %s' % n)
    description = u'Only for testing'
    allowed_geometry = 'POINT'


class LocationSiteF(factory.django.DjangoModelFactory):
    """
    Location site factory
    """

    class Meta:
        model = LocationSite

    location_type = factory.SubFactory(LocationTypeF)
    geometry_point = Point(
        random.uniform(-180.0, 180.0),
        random.uniform(-90.0, 90.0)
    )


class ProfileF(factory.django.DjangoModelFactory):
    """
    Profile site factory
    """

    class Meta:
        model = Profile

    user = factory.SubFactory(User)
    qualifications = factory.Sequence(lambda n: "qualifications%s" % n)
    other = factory.Sequence(lambda n: "other%s" % n)


class IUCNStatusF(factory.django.DjangoModelFactory):
    """
    Iucn status factory
    """
    class Meta:
        model = IUCNStatus

    category = factory.Sequence(lambda n: u'Test name %s' % n)
    sensitive = False


@factory.django.mute_signals(signals.pre_save)
class TaxonF(factory.django.DjangoModelFactory):
    """
    Taxon factory
    """
    class Meta:
        model = Taxon

    iucn_status = factory.SubFactory(IUCNStatusF)
    common_name = factory.Sequence(lambda n: u'Test common name %s' % n)
    scientific_name = factory.Sequence(
            lambda n: u'Test scientific name %s' % n)
    author = factory.Sequence(lambda n: u'Test author %s' % n)


class SurveyF(factory.django.DjangoModelFactory):
    """
    Survey factory
    """
    class Meta:
        model = Survey

    date = timezone.now()

    @factory.post_generation
    def sites(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for site in extracted:
                self.sites.add(site)
