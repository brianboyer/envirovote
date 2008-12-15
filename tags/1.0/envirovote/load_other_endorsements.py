#!/usr/bin/env python
from django.core.management import setup_environ
import settings
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
    #Gerald Connolly	hou	VA	11	Clean Water Action	http://www.cleanwateraction.org/2008endorsements	2008
    reader = csv.DictReader(f, (
        'name',
        'race_type',
        'state',
        'district',
        'org_name',
        'url',
        'year',
        )
    )

    #load load load!
    for e in reader:
        org_name = e['org_name']
        year = e['year']
        endorsement_url = e['url']
        #get/create organization
        try:
            org = Organization.objects.get(name=org_name)
        except:
            org = Organization.objects.create(name=org_name)
        names = e['name'].strip().split(' ')
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

d = "data/endorsements/"
for n in os.listdir(d):
    if n.endswith('csv') & (n.find('forget') < 0):
        f = open("%s%s" % (d,n))
        load_endorsements(f)
        f.close()

#load_endorsements(open('data/endorsements/Vote Smart/Sierra Club 2008 endorsements.csv'))
