# all races must have a last_race, and all last_races must have a winner
# TODO what about two races w/o a greenest candidate?  it should work if they have a winner.
def calculate_meter_info(races):
    total_races = 0
    decided_races = 0
    green_races = 0
    previous_green_races = 0
    percent_green = 0
    percent_change = 0
    for race in races:
        total_races += 1
        if race.winner:
            decided_races += 1
            if race.winner == race.greenest:
                green_races += 1
            if race.last_race.winner == race.last_race.greenest:
                previous_green_races += 1
    if decided_races > 0:
        percent_green = 100 * float(green_races) / float(decided_races)
        percent_change = 100 * (float(green_races) - float(previous_green_races)) / float(decided_races)
    remaining_races = total_races - decided_races
    return {'decided_races': decided_races, 'remaining_races': remaining_races, 'green_races': green_races, 'percent_green': percent_green, 'percent_change': percent_change,}
    
        
        
