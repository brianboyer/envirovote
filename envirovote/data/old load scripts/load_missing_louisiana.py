#!/usr/bin/env python
from django.core.management import setup_environ
import settings
setup_environ(settings)

from races.models import Candidate, Race

prev_2 = Race.objects.get(state='LA',district=2,year=2006)
louisiana_2 = Race.objects.create(race_type='hou',state='LA',district=2,year=2008,last_race=prev_2)

prev_4 = Race.objects.get(state='LA',district=4,year=2006)
louisiana_4= Race.objects.create(race_type='hou',state='LA',district=4,year=2008,last_race=prev_4)

Candidate.objects.create(name='William Jefferson',party='Democatic',last_elected='1',race=louisiana_2,)
Candidate.objects.create(name='Helena Moreno',party='Democratic',last_elected='0',race=louisiana_2,)
Candidate.objects.create(name='Anh Cao',party='Republican',last_elected='0',race=louisiana_2,)
Candidate.objects.create(name='Malik Rahim',party='Green',last_elected='0',race=louisiana_2,)
Candidate.objects.create(name='Gregory Kahn',party='Libertarian',last_elected='0',race=louisiana_2,)

Candidate.objects.create(name='Willie Banks Jr.',party='Democratic',last_elected='0',race=louisiana_4,)
Candidate.objects.create(name='Gerard Bowen',party='Independant',last_elected='0',race=louisiana_4,)
Candidate.objects.create(name='Paul Carmouche',party='Democratic',last_elected='0',race=louisiana_4,)
Candidate.objects.create(name='John Fleming Jr.',party='Republican',last_elected='0',race=louisiana_4,)
Candidate.objects.create(name='Chris D. Gorman',party='Republican',last_elected='0',race=louisiana_4,)


