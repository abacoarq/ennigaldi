from django.db import models

###########################################################
# General location information for use in several models
# Move to a specific application for integration with
# PostGIS and other metadata when project grows.
# Also distinguish between places that must be
# geographically located and those that only need to be
# named, e.g. Description content > Place.
# In the end it depends on the use the museum wants to
# make of different Place information types.
# Spectrum 4.0 several fields with 'place' data
# VRA Core 4   location
# DCMI         spatial
class Place(models.Model):
    location_name_types = (
        ('corporate', 'Corporate'),
        ('geographic', 'Geographic'),
        ('personal', 'Personal'),
        ('other', 'Other'),
    )
    location_name = models.CharField(max_length=63)
    location_name_type = models.CharField(max_length=11, default='geographic', choices=location_name_types)
    # location > extent is used to disambiguate or specify
    # the character of a location, e.g. if one is referring
    # to the city of Rome, to the province with the
    # same name, or to the Roman Empire.
    location_extent = models.CharField(max_length=63, blank=True)
    # The following fields record modern location data.
    email = models.EmailField(blank=True)
    phone_primary = models.CharField(max_length=31, blank=True)
    phone_secondary = models.CharField(max_length=31, blank=True)
    website = models.CharField(max_length=255, blank=True)
    address_1 = models.CharField(max_length=35, blank=True)
    address_2 = models.CharField(max_length=35, blank=True)
    city = models.CharField(max_length=35, blank=True)
    state_province = models.CharField(max_length=35, blank=True)
    zip_code = models.CharField(max_length=35, blank=True)
    country = models.CharField(max_length=35, blank=True)

    def __str__(self):
        comp = self.location_extent if self.location_extent else self.city
        return self.location_name + ' (' + comp + ')'

class PlaceType(models.Model):
    location_types = (
        ('creation', 'Creation'),
        ('discovery', 'Discovery'),
        ('exhibition', 'Exhibition'),
        ('formerOwner', 'Location of former owner'),
        ('formerRepository', 'Former repository'),
        ('formerSite', 'Former site'),
        ('installation', 'Installed location'),
        ('intended', 'Unbuilt project intended for'),
        ('owner', 'Owner location'),
        ('performance', 'Performed at'),
        ('publication', 'Publication'),
        ('repository', 'Repository'),
        ('site', 'Current location on site'),
        ('other', 'Other'),
    )
    location = models.ForeignKey(Place, models.PROTECT)
    work = models.ForeignKey('genericmodel', models.PROTECT)
    location_type = models.CharField(max_length=31, choices=location_types, default='creation')

    class Meta:
        abstract=True
# /VRA Core 4  location
###########################################################
