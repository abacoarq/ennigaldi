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
    pass

class PlaceType(models.Model):
    pass
# /VRA Core 4  location
###########################################################
