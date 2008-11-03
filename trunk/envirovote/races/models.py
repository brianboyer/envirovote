from django.db import models
from django.contrib.humanize.templatetags import humanize
#from pvs.Util import doWebServiceCall
#from pvs.Common import PVSException

RACE_TYPE_CHOICES = (
    ('pre', 'President'),
    ('sen', 'Senate'),
    ('hou', 'House'),
    ('gov', 'Governor'),
)

STATE_CHOICES = (
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming'),
)

PARTY_TYPE_CHOICES = (
    ('AI', 	'American Independent'),
    ('C', 	'Constitution'),
    ('D', 	'Democrat'),
    ('G', 	'Green'),
    ('I', 	'Independent'),
    ('IP', 	'Independence'),
    ('L', 	'Libertarian'),
    ('Ref', 'Reform'),
    ('R', 	'Republican'),
    ('PF', 	'Peace and Freedom Party'),
    ('S', 	'Socialist'),
    ('SW', 	'Socialist Workers Party'),
)

class Race(models.Model):
    race_type = models.CharField(max_length=3, choices=RACE_TYPE_CHOICES)
    state = models.CharField(max_length=2, choices=STATE_CHOICES, blank=True, null=True)
    district = models.IntegerField(blank=True, null=True)
    year = models.IntegerField()
    last_race = models.ForeignKey("Race", blank=True, null=True)
    is_key = models.BooleanField()
    headline = models.CharField(max_length=200, blank=True, null=True)
    deck = models.CharField(max_length=200, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    tally_updated = models.DateTimeField(blank=True, null=True)
    tally_notes = models.CharField(max_length=200, blank=True, null=True)
    winner = models.ForeignKey("Candidate", blank=True, null=True, related_name="won")
    projected = models.BooleanField()

    def __unicode__(self):
        return "%s (%s)" % (self.title, self.year)
        
    def _get_title(self):
        """shows the proper title of the race"""
        if self.race_type == 'pre':
            return "President of the United States"
        elif self.race_type == 'hou' and self.district == 0:
            return "U.S. House of Representatives, At Large for %s" % (self.get_state_display())
        elif self.race_type == 'hou':
            return "U.S. House of Representatives, %s District of %s" % (humanize.ordinal(self.district),self.get_state_display())
        elif self.race_type == 'sen':
            return "U.S. Senate, %s" % (self.get_state_display())
        elif self.race_type == 'gov':
            return "Governor of %s" % (self.get_state_display())
        else:
            return "I don't know what race type this is"
    title = property(_get_title)
    
    def _get_greenest(self):
        """returns the greenest candidate in this race"""
        high = 0
        ret = None
        for c in self.candidate_set.all():
            count = c.endorsement_set.count()
            if count > high:
                high = count
                ret = c
        return ret
    greenest = property(_get_greenest)
    
    def get_candidate_percentages(self):
        candidates = self.candidate_set.order_by('-votes')
        #there's totally a more pythonic way to do this.  oh well.
        total = 0
        for c in candidates:
            total += c.votes
        return [ (c, 100*float(c.votes)/total) for c in candidates]
        
    def get_absolute_url(self):
        return '/race/%s/' % self.id


class Candidate(models.Model):
    name = models.CharField(max_length=200)
    party = models.CharField(max_length=120)
    photo = models.URLField(blank=True, null=True)
    race = models.ForeignKey(Race)
    is_key = models.BooleanField()
    last_elected = models.IntegerField(blank=True, null=True)
    votes = models.IntegerField(blank=True, null=True)
    vote_pc = models.CharField(max_length=15,blank=True, null=True)
    pvs_candidate_id = models.IntegerField(blank=True,null=True)
    extra_info = models.TextField(blank=True,null=True)
    
    #links = models.TextField(blank=True) ??
    #political courage test results
    #badges (dirty dozen, etc.  set table?  array?  merge w/ links?)
    
    def _get_vote_percentage(self):
        """get the percentage of the votes this guy got"""
        if vote_pc:
            return vote_pc
        tot = 0
        for c in self.race.candidate_set.all():
            tot += c.votes
        return (float(self.votes)/tot)*100
    vote_percentage = property(_get_vote_percentage)

    def _get_party_abbv(self):
        """full party name"""
        for k,v in PARTY_TYPE_CHOICES:
            if k == self.party:
                return v
    party_abbv = property(_get_party_abbv)
    
    def __unicode__(self):
        return "%s (%s)" % (self.name,self.party)
