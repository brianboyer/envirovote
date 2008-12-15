#!/usr/bin/env python
from django.core.management import setup_environ
import settings
import sys
setup_environ(settings)

from races.models import Candidate, Race
from endorsements.models import Endorsement, Organization 
import csv
import os
from django.db.models import Q

def load_endorsements(f):
    print '===',f.name,'==='
    reader = csv.reader(f)
    n = os.path.basename(f.name)
    org_name,year = n.split('.')[0].rstrip(' endorsements').rsplit(' ',1)
    endorsement_url = reader.next()[0]
    # "AL","U.S. House",7,"Artur Davis","Democratic"
    reader = csv.DictReader(f, (
        'state',
        'race_type',
        'district',
        'name',
        'party',
        )
    )

    #get/create organization
    try:
        org = Organization.objects.get(name=org_name)
    except:
        org = Organization.objects.create(name=org_name)

    #load load load!
    for e in reader:
        names = e['name'].split(' ')
        candidate = None
        try:
            if len(names) == 2:
                try:
                    candidate = Candidate.objects.get(Q(name__contains=names[0]) & Q(name__contains=names[1]) & Q(race__year__exact=year))
                except:
                    try:
                        candidate = Candidate.objects.get(Q(name__contains=names[0]) & Q(name__endswith=names[1]) & Q(race__year__exact=year))
                    except:
                        try:
                            candidate = Candidate.objects.get(Q(name__contains=names[1]) & Q(race__year__exact=year) & Q(race__state__exact=e['state']))
                        except Exception, inst:
                            print "fail 2 name:",e,inst
            elif len(names) == 3:
                try:
                    candidate = Candidate.objects.get(Q(name__contains=names[0]) & Q(name__contains=names[2]) & Q(race__year__exact=year))
                except:
                    try:
                        candidate = Candidate.objects.get(Q(name__contains=names[1]) & Q(name__contains=names[2]) & Q(race__year__exact=year))
                    except:
                        try:
                            candidate = Candidate.objects.get(Q(name__contains=names[2]) & Q(race__year__exact=year) & Q(race__state__exact=e['state']))
                        except Exception, inst:
                            print "fail 3 name:",e,inst
            if candidate:
                endorsement = Endorsement.objects.create(organization=org,candidate=candidate,url=endorsement_url)    
        except Exception, inst:
            print 'fuckin fail:',e,inst
                
    f.close()

d = "data/endorsements/Vote Smart/"
for n in os.listdir(d):
    if n.endswith('csv') & (n.find('endorsements') > 0) & (n.find('forget') < 0):
        f = open("%s%s" % (d,n))
        load_endorsements(f)
        f.close()

#load_endorsements(open('data/endorsements/Vote Smart/Sierra Club 2008 endorsements.csv'))
