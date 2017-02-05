from django.db import models

class Unit(models.Model):
    # Locations can be recursive for maximum flexibility,
    # e.g. building > wing > room > furniture > shelf
    # or in any other way required by the organization.
    # Root-level locations will have this set to NULL:
    unit_parent = models.ForeignKey('self', models.PROTECT, blank=True)
    # A code that identifies the location, if any.
    unit_id = models.CharField(max_length=7, blank=True)
    # Keep the name short, follow conventions
    unit_name = models.CharField(max_length=32)
    # Spectrum 4.0 Location note
    # VRA Core 4   location > notes
    # Notes on the location or its name (e.g. "so-called", "condemned", etc.)
    unit_note = models.TextField(blank=True)

    def __str__(self):
        if unit_parent:
            parent_string = ' in ' + unit_parent
        else:
            parent_string = ''
        return unit_id + ' ' + unit_name + parent_string
