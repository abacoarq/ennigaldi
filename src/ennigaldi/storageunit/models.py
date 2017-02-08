from django.db import models

class Unit(models.Model):
    # Locations can be recursive for maximum flexibility,
    # e.g. building > wing > room > furniture > shelf
    # or in any other way required by the organization.
    # Root-level locations will have this set to NULL:
    parent = models.ForeignKey('self', models.CASCADE, null=True)
    # A code that identifies the location, if any.
    acronym = models.CharField(max_length=15)
    # Keep the name short, follow conventions
    name = models.CharField(max_length=32, blank=True)
    # Spectrum 4.0 Location note
    # VRA Core 4   location > notes
    # Notes on the location or its name (e.g. "so-called", "condemned", etc.)
    note = models.TextField(blank=True)

    def __str__(self):
        if self.parent:
            parent_string = self.parent.__str__() + ' › '
        else:
            parent_string = ''
        return parent_string + self.acronym + ' ' + self.name

    class Meta:
        unique_together = ('parent', 'acronym')
