#!/usr/bin/env python
from django.core.management import setup_environ
import settings
setup_environ(settings)

from races.models import Candidate, Race

curr_prez = Race.objects.get(race_type='pre',year=2008)
last_prez = Race.objects.create(race_type='pre',year=2004)
curr_prez.last_race = last_prez
curr_prez.save()

Candidate.objects.create(name='John Kerry',party='Democatic',last_elected='0',race=last_prez,)

