from django.db import models
import pickle

class RestModelBase(models.Model):
    "A base model which includes the ability to have a schema free extension field called rest"
    rest = models.TextField(verbose_name="JSON data.", default=pickle.dumps({}, 0),
                            help_text="Additional fields without fixed schema")

    def getRest(self):
        return pickle.loads(self.rest)

    def setRest(self, d):
        self.rest = pickle.dumps(d, 1)

    def asJSON(self):
        d = self.getRest()
        d.update(self.__dict__)
        return repr(d)

    def updateFromJSON(self, newData, replaceRest=False):
        if replaceRest:
            d = {}
        else:
            d = self.getRest()
        for k, v in newData.items()
            if k in hasattr(self, k):
                setattr(self, k, v)
            else:
                d[k] = v
        self.setRest(d)

class DataChannel(RestModelBase):
    "Information about a single data source"
    chanID = models.IntegerField(primary_key=True, unique=True, verbose_name="Channel ID",
        help_text="Unique integer primary key for the channel, you can specify but it must be unique.")
    name = models.CharField(max_length=255, verbose_name="Name of the data channel",
                            help_text="Human readable name of the data channel")
    derived = models.BooleanField(help_text="Channel data is derived from other channels",
                                  default=False)
    source = models.CharField(max_length=255, verbose_name="Source code URL", blank=True,
                              help_text="Where to get source code for this channel's data generator")

class GeoZone(models.Model):
    """A geographic zone which has been calculated from specific GeoLocations"""
    lat = models.FloatField(verbose_name="Latitude",  help_text="Latitude of GeoZone average in degrees",
                            null=False, editable=True)
    lon = models.FloatField(verbose_name="Longitude", help_text="Longitude of GeoZone average in degrees",
                            null=False, editable=True)
    radius = models.FloatField(help_text="Radius of the zone in meters",
                               null = False, editable=True)

    def __repr__(self):
        return self.__dict__

class GeoLocation(models.Model):
    """Store information about the location of a data entry"""
    lat = models.FloatField(verbose_name="Latitude",  help_text="Latitude of data point in degrees",
                            editable=False, null=False)
    lon = models.FloatField(verbose_name="Longitude", help_text="Longitude of data point in degrees",
                            editable=False, null=False)
    zone = models.ForeignKey('GeoZone', blank=True, null=True, editable=True)

    def __repr__(self):
        return self.__dict__

class DataEntry(RestModelBase):
    """Table for storing context data, either raw or derrived.
This table is designed for flexibility so the schema is not complete, most of the channel data is stored as JSON."""
    time = models.DateTimeField(auto_now_add=True, editable=False,
                                verbose_name="Timestamp for this data entry")
    interval = models.TimeDeltaField(default=0, editable=False,
                                     verbose_name="Time interval width for this data entry.")
    geoloc = models.ForeignKey('GeoLocation', blank=True, null=True, editable=False,
                               verbose_name="Geo-location for this data entry.")
    channel = models.ForeignKey('DataChannel', editable=False, verbose_name="Data channel")
