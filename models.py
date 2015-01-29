from django.db import models

class DataChannel(models.Model):
    "Information about a single data source"
    name = models.CharField(max_length=255, verbose_name="Name of the data channel",
                            help_text="Human readable name of the data channel")
    derived = models.BooleanField(help_text="Channel data is derived from other channels",
                                  default=False)
    source = models.CharField(max_length=255, verbose_name="Source code URL", blank=True,
                              help_text="Where to get source code for this channel's data generator")
    rest = models.TextField(verbose_name="JSON data.", default="{}",
                            help_text="Additional fields without fixed schema")



class DataEntry(models.Model):
    """Table for storing context data, either raw or derrived.
This table is designed for flexibility so the schema is not complete, most of the channel data is stored as JSON."""
    time = models.DateTimeField(auto_now_add=True, editable=False,
                                verbose_name="Timestamp for this data entry")
    channel = models.ForeignKey('DataChannel', editable=False, verbose_name="Data channel")
    rest = models.TextField(verbose_name="JSON data", default="{}", editable=False,
                            help_text="Non-fixed-schema data")
