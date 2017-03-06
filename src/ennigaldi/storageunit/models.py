from django.db import models

class Unit(models.Model):
    unit_types = (
            ('exhibit', 'Exhibit'),
            ('laboratory', 'Laboratory'),
            ('reserve', 'Reserve'),
            ('archive', 'Archive'),
            ('library', 'Library'),
            ('transport', 'Transport'),
            )
    # Locations can be recursive for maximum flexibility,
    # e.g. building > wing > room > furniture > shelf
    # or in any other way required by the organization.
    # Root-level locations will have this set to NULL:
    parent = models.ForeignKey('self', models.CASCADE, null=True, help_text="Storage units are arranged in hierarchies, such as:<br />Room > Furniture > Shelf")
    # A code that identifies the location, if any.
    acronym = models.CharField(max_length=15, help_text="A code or number that identifies the location, if any. Best practices:<br />- Rooms should be numbered<br />- Shelves should be designated with capital letters starting from the bottom")
    # Keep the name short, follow conventions
    name = models.CharField(max_length=31, blank=True, help_text="Sould be clear and short")
    unit_type = models.CharField(max_length=31, choices=unit_types, default='exhibit')
    # Spectrum 4.0 Location note
    # VRA Core 4   location > notes
    # Notes on the location or its name (e.g. "so-called", "condemned", etc.)
    note = models.TextField(blank=True, help_text="Any required observations on the identification or conditions of this unit")

    def __str__(self):
        if self.parent:
            parent_string = self.parent.__str__() + ' › '
        else:
            parent_string = ''
        return parent_string + self.acronym + ' ' + self.name

    def get_absolute_url(self):
        return reverse('unit-detail', kwargs={'pk': self.pk})

    class Meta:
        unique_together = ('parent', 'acronym')
