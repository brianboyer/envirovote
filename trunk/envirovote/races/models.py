from django.db import models
from django.contrib.localflavor.us.us_states import STATE_CHOICES

RACE_TYPE_CHOICES = (
    ('pre', 'Presidental'),
    ('sen', 'Senatorial'),
    ('con', 'Congressional'),
    ('gub', 'Gubernatorial'),
)

class Race(models.Model):
    race_type = models.CharField(max_length=3, choices=RACE_TYPE_CHOICES)
    state = models.CharField(max_length=2, choices=STATE_CHOICES, blank=True, null=True)
    district = models.IntegerField(blank=True, null=True)
    is_key = models.BooleanField()
    headline = models.CharField(max_length=200, blank=True)
    deck = models.CharField(max_length=200, blank=True)
    body = models.TextField(blank=True)
    #results - array?, no, vote count on candidate
    #winner - no, on candidate
    #percent reported
    #get greenness from candidate

    def __unicode__(self):
        return "%s %s" % (self.state, self.race_type)
    
class Candidate(models.Model):
    name = models.CharField(max_length=200)
    photo = models.URLField(blank=True)
    race = models.ForeignKey(Race)
    is_key = models.BooleanField()
    incumbent = models.BooleanField()
    last_elected = models.IntegerField(blank=True, null=True)
    #votes = models.IntegerField(blank=True, null=True)
    #is_winner = models.BooleanField
    
    #links = models.TextField(blank=True) ??
    #political courage test results
    #badges (dirty dozen, etc.  set table?  array?  merge w/ links?)
    
    def __unicode__(self):
        return self.name