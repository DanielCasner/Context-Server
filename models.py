from django.db import models
import cPickle as pickle

class DataChannel(models.Model):
    "Information about a single data source"
    chanID = models.IntegerField(primary_key=True, unique=True, verbose_name="Channel ID",
        help_text="Unique integer primary key for the channel, you can specify but it must be unique.")
    name = models.CharField(max_length=255, verbose_name="Name of the data channel",
                            help_text="Human readable name of the data channel")
    derived = models.BooleanField(help_text="Channel data is derived from other channels",
                                  default=False)
    source = models.CharField(max_length=255, verbose_name="Source code URL", blank=True,
                              help_text="Where to get source code for this channel's data generator")
    rest = models.TextField(verbose_name="JSON data.", default=pickle.dumps({}, 0),
                            help_text="Additional fields without fixed schema")

    def getRest(self):
        return pickle.loads(self.rest)

    def setRest(self, d):
        self.rest = pickle.dumps(d, 2)

    def asJSON(self):
        d = self.getRest()
        d.update({'chanID': self.chanID, "name": self.name, "derived": self.derived, "source": self.source})
        return repr(d)


class DataEntry(models.Model):
    """Table for storing context data, either raw or derrived.
This table is designed for flexibility so the schema is not complete, most of the channel data is stored as JSON."""
    time = models.DateTimeField(auto_now_add=True, editable=False,
                                verbose_name="Timestamp for this data entry")
    interval = models.TimeDeltaField(default=0, editable=False,
                                     verbose_name="Time interval width for this data entry.")
    location = models.GeoField(blank=True, null=True, editable=False,
                               verbose_name="Geo-location for this data entry.")
    channel = models.ForeignKey('DataChannel', editable=False, verbose_name="Data channel")
    
    rest = models.TextField(verbose_name="JSON data", default=pickle.dumps({}, 0), editable=False,
                            help_text="Non-fixed-schema data")

    def getRest(self):
        return pickle.loads(self.rest)

    def setRest(self, d):
        self.rest = pickle.dumps(d, 2)

    def asJSON(self):
        d = self.getRest()
        d.update({"time": self.time, "channel": self.channel})
        return
