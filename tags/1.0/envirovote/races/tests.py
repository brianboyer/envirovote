import unittest
from races.models import Candidate, Race
from endorsements.models import Endorsement, Organization
from races.helpers import calculate_meter_info

class HelpersTestCase(unittest.TestCase):
    
    def setUp(self):
        
        org1 = Organization.objects.create(name='Sierra Club')
        org2 = Organization.objects.create(name='League of Conservation Voters')
        org3 = Organization.objects.create(name='The Strangelove Institute for Environmental Studies')
        
        mi_prev_race = Race.objects.create(race_type='sen',state='MI',year=1994,last_race=None)
        mi_prev_can1 = Candidate.objects.create(name='Mitt Romney',race=mi_prev_race)
        mi_prev_can2 = Candidate.objects.create(name='Joe Patt',race=mi_prev_race)
        mi_prev_race.winner = mi_prev_can2
        mi_prev_race.save()
        mi_prev_can1_end1 = Endorsement.objects.create(organization=org3,candidate=mi_prev_can1)
        mi_prev_can2_end1 = Endorsement.objects.create(organization=org1,candidate=mi_prev_can2)
        mi_prev_can2_end2 = Endorsement.objects.create(organization=org2,candidate=mi_prev_can2)
        
        mi_curr_race = Race.objects.create(race_type='sen',state='MI',year=2000,last_race=mi_prev_race)
        mi_curr_can1 = Candidate.objects.create(name='Mitt Romney',race=mi_curr_race)
        mi_curr_can2 = Candidate.objects.create(name='Kwame Kilpatrick',race=mi_curr_race)
        mi_curr_race.winner = mi_curr_can2
        mi_curr_race.save()
        
        ak_prev_race = Race.objects.create(race_type='sen',state='AK',year=1994,last_race=None)
        ak_curr_race = Race.objects.create(race_type='sen',state='AK',year=2000,last_race=ak_prev_race)
        
        il_prev_race = Race.objects.create(race_type='sen',state='IL',year=1994,last_race=None)
        il_prev_can1 = Candidate.objects.create(name='Dennis Hastert',race=il_prev_race)
        il_prev_can2 = Candidate.objects.create(name='Barack Obama',race=il_prev_race)
        il_prev_race.winner = il_prev_can1
        il_prev_race.save()
        il_prev_can2_end1 = Endorsement.objects.create(organization=org1,candidate=il_prev_can2)
        
        il_curr_race = Race.objects.create(race_type='sen',state='IL',year=2000,last_race=il_prev_race)
        il_curr_can1 = Candidate.objects.create(name='Dennis Hastert',race=il_curr_race)
        il_curr_can2 = Candidate.objects.create(name='Dick Durbin',race=il_curr_race)
        il_curr_race.winner = il_curr_can1
        il_curr_race.save()
        il_curr_can2_end1 = Endorsement.objects.create(organization=org1,candidate=il_curr_can2)
        
        ca_prev_race = Race.objects.create(race_type='sen',state='CA',year=1994,last_race=None)
        ca_prev_can1 = Candidate.objects.create(name='Arnold Schwartzenegger',race=ca_prev_race)
        ca_prev_can2 = Candidate.objects.create(name='Gary Coleman',race=ca_prev_race)
        ca_prev_race.winner = ca_prev_can2
        ca_prev_race.save()
        ca_prev_can2_end1 = Endorsement.objects.create(organization=org1,candidate=ca_prev_can2)
        
        ca_curr_race = Race.objects.create(race_type='sen',state='CA',year=2000,last_race=ca_prev_race)
        ca_curr_can1 = Candidate.objects.create(name='Arnold Schwartzenegger',race=ca_curr_race)
        ca_curr_can2 = Candidate.objects.create(name='Gary Coleman',race=ca_curr_race)
        ca_curr_race.winner = ca_curr_can2
        ca_curr_race.save()
        ca_curr_can2_end1 = Endorsement.objects.create(organization=org1,candidate=ca_curr_can2)
        
        ny_prev_race = Race.objects.create(race_type='sen',state='NY',year=1994,last_race=None)
        ny_prev_can1 = Candidate.objects.create(name='Rudy Guiliani',race=ny_prev_race)
        ny_prev_can2 = Candidate.objects.create(name='Hillary Clinton',race=ny_prev_race)
        ny_prev_race.winner = ny_prev_can1
        ny_prev_race.save()
        ny_prev_can2_end1 = Endorsement.objects.create(organization=org1,candidate=ny_prev_can2)
        
        ny_curr_race = Race.objects.create(race_type='sen',state='NY',year=2000,last_race=ny_prev_race)
        ny_curr_can1 = Candidate.objects.create(name='Rudy Guiliani',race=ny_curr_race)
        ny_curr_can2 = Candidate.objects.create(name='Hillary Clinton',race=ny_curr_race)
        ny_curr_race.winner = ny_curr_can2
        ny_curr_race.save()
        ny_curr_can2_end1 = Endorsement.objects.create(organization=org1,candidate=ny_curr_can2)
        
        ma_prev_race = Race.objects.create(race_type='sen',state='MA',year=1994,last_race=None)
        ma_prev_can1 = Candidate.objects.create(name='Joe Lieberman',race=ma_prev_race)
        ma_prev_can2 = Candidate.objects.create(name='Joe Biden',race=ma_prev_race)
        ma_prev_race.winner = ma_prev_can1
        ma_prev_race.save()
        ma_prev_can2_end1 = Endorsement.objects.create(organization=org1,candidate=ma_prev_can2)
        
        ma_curr_race = Race.objects.create(race_type='sen',state='MA',year=2000,last_race=ma_prev_race)
        ma_curr_can1 = Candidate.objects.create(name='Joe Lieberman',race=ma_curr_race)
        ma_curr_can2 = Candidate.objects.create(name='Joe Biden',race=ma_curr_race)
        ma_curr_race.winner = ma_curr_can2
        ma_curr_race.save()
        ma_curr_can2_end1 = Endorsement.objects.create(organization=org1,candidate=ma_curr_can2)
    
    def test_calculate_meter_info(self):
        
        # no races
        races = Race.objects.filter(year=1999)
        info = calculate_meter_info(races)
        self.assertEqual(info['decided_races'],0)
        self.assertEqual(info['remaining_races'],0)
        self.assertEqual(info['green_races'],0)
        self.assertEqual(info['percent_green'],0)
        self.assertEqual(info['percent_change'],0)
        
        # no races decided
        races = Race.objects.filter(year=2000,state='AK')
        info = calculate_meter_info(races)
        self.assertEqual(info['decided_races'],0)
        self.assertEqual(info['remaining_races'],1)
        self.assertEqual(info['green_races'],0)
        self.assertEqual(info['percent_green'],0)
        self.assertEqual(info['percent_change'],0)
        
        # one race decided
        races = Race.objects.filter(year=2000,state='MI')
        info = calculate_meter_info(races)
        self.assertEqual(info['decided_races'],1)
        self.assertEqual(info['remaining_races'],0)
        
        # previously green winner, current winner no endorsements
        # and, previous green winner is opposed in his greenness
        races = Race.objects.filter(year=2000,state='MI')
        info = calculate_meter_info(races)
        self.assertEqual(info['green_races'],0)
        self.assertEqual(info['percent_green'],0)
        self.assertEqual(info['percent_change'],-100)
        
        #previously green winner, current green winner
        races = Race.objects.filter(year=2000,state='CA')
        info = calculate_meter_info(races)
        self.assertEqual(info['green_races'],1)
        self.assertEqual(info['percent_green'],100)
        self.assertEqual(info['percent_change'],0)
    
        #previously not green winner, current not green winner
        races = Race.objects.filter(year=2000,state='IL')
        info = calculate_meter_info(races)
        self.assertEqual(info['green_races'],0)
        self.assertEqual(info['percent_green'],0)
        self.assertEqual(info['percent_change'],0)

        #previously not green winner, current green winner
        races = Race.objects.filter(year=2000,state='NY')
        info = calculate_meter_info(races)
        self.assertEqual(info['green_races'],1)
        self.assertEqual(info['percent_green'],100)
        self.assertEqual(info['percent_change'],100)
        
        #the whole shebang
        races = Race.objects.filter(year=2000)
        info = calculate_meter_info(races)
        self.assertEqual(info['decided_races'],5)
        self.assertEqual(info['remaining_races'],1)
        self.assertEqual(info['green_races'],3)
        self.assertEqual(info['percent_green'],100*3/5)
        self.assertEqual(info['percent_change'],100*1/5)
        
    def tearDown(self):
        pass
