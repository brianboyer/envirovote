from django.db import models
from races.models import Candidate

# Create your models here.
class Organization(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(blank=True,null=True)
    #state = models.CharField(max_length=2)
    #diff between fringe groups vs mainstream groups?
    
    def __unicode__(self):
        return self.name
        
class Endorsement(models.Model):
    organization = models.ForeignKey(Organization)
    candidate = models.ForeignKey(Candidate)
    url = models.URLField(blank=True,null=True)
    # positive vs negitive endorsements? dirty dozen?
    
    def __unicode__(self):
        return "%s endorsed %s in %s" % (self.organization.name,self.candidate.name,self.candidate.race.year)    
