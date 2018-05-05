from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _


class Location(models.Model):
    city = models.CharField(_('City'), max_length=32)
    geolocation = models.PointField(_('Location'))

    class Meta:
        ordering = ('city',)

    def __str__(self):
        return self.city


class Measurement(models.Model):
    # location = models.OneToOneField('locations.Location',
    # on_delete=models.CASCADE)
    # Change field type to store more than one measure for location
    location = models.ForeignKey('locations.Location',
                                 on_delete=models.CASCADE)
    proxy = models.CharField(_('proxy'), max_length=16)
    avg_resp_proxy = models.CharField(_('avg_resp_proxy'), max_length=32)
    avg_avail_proxy = models.CharField(_('Average available proxy'),
                                       max_length=32)
    avg_resp_direct = models.CharField(_('avg_resp_direct'), max_length=32)
    avg_avail_direct = models.CharField(_('Average available direct'),
                                        max_length=32)
    date = models.DateField(auto_now=True)

    class Meta:
        ordering = ('date',)

    def __str__(self):
        return '{} - {}'.format(self.date, self.location.city)
