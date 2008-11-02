from django.db import models
from django.contrib.localflavor.us.us_states import STATE_CHOICES
from django.contrib.humanize.templatetags import humanize

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
    tally_updated = models.DateTimeField(blank=True, null=True)
    tally_notes = models.CharField(max_length=200, blank=True)
    winner = models.ForeignKey("Candidate", blank=True, null=True, related_name="won")
    projected = models.BooleanField()

    def __unicode__(self):
        return "%s %s" % (self.state, self.race_type)
        
    def _get_title(self):
        """shows the proper title of the race"""
        if self.race_type == 'pre':
            return "President of the United States"
        elif self.race_type == 'con':
            return "U.S. House of Representatives, representing the %s District of %s" % (humanize.ordinal(self.district),self.get_state_display())
        elif self.race_type == 'sen':
            return "U.S. Senate, representing %s" % (self.get_state_display())
        elif self.race_type == 'gub':
            return "Governor of %s" % (self.get_state_display())
        else:
            return "I don't know what race type this is"
    title = property(_get_title)
    
    def _get_greenist(self):
        """returns the greenist candidate in this race"""
        high = 0
        ret = None
        for c in self.candidate_set.all():
            if c.endorsement_count > high:
                ret = c
                
        return ret
    greenist = property(_get_greenist)
    
    def get_candidate_percentages(self):
        candidates = self.candidate_set.order_by('-votes')
        #there's totally a more pythonic way to do this.  oh well.
        total = 0
        for c in candidates:
            total += c.votes
        return [ (c, 100*float(c.votes)/total) for c in candidates]
    
    
class Candidate(models.Model):
    name = models.CharField(max_length=200)
    photo = models.URLField(blank=True)
    race = models.ForeignKey(Race)
    is_key = models.BooleanField()
    last_elected = models.IntegerField(blank=True, null=True)
    votes = models.IntegerField(blank=True, null=True)
    
    #links = models.TextField(blank=True) ??
    #political courage test results
    #badges (dirty dozen, etc.  set table?  array?  merge w/ links?)
    
    def __unicode__(self):
        return self.name
        
    def _get_endorsement_count(self):
        return self.endorsement_set.count()
    endorsement_count = property(_get_endorsement_count)
