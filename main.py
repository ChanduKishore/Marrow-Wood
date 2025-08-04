from  day_and_night_cycle import *
import json
from time import time, sleep
from character import CharacterStats
import os
from inventory_items import inventory_items

log_file = 'log.txt'
if not os.path.exists(log_file):
    with open(log_file,'w') as f:
        f.write('Day: 0\n')

def clear_screen():
      os.system('cls' if os.name == 'nt' else 'clear')


save_file_name = 'save.txt'

def save_game_data(data):
    with open('save.txt','w') as f:
        f.write(json.dumps(data))

def load_save_file(save_file):
    with open(save_file,'r') as f:
        data = json.loads(f.read())

    return data

if os.path.exists(save_file_name):
    save_data = load_save_file(save_file_name)
    start_time = time()
    day = save_data['day']
    initial_hours = save_data['hours']
    person_stats = save_data['person']
    person_inventory = person_stats['inventory']

else:
    start_time = time()
    day = 0
    initial_hours = 0
    person_stats = {'health':100, 'food':100, 'water':100, 'max_health':100, 'max_food':100, 'max_water':100, 'last_ate':0, 'last_drink': 0, 'inventory':[] }
    person_inventory = [["Fruits", {"name": "apple", "energy": 20, "quantity": 100}],["Fruits", {"name": "orange", "energy": 20, "quantity": 50}]]

def fill_inventory(character,inventory, inv_items):
    for item in inventory:
        item_class = inv_items[item[0]]
        item_properties = item[1]
        person.add_item(item_class(**item_properties))


person = CharacterStats(**person_stats)
fill_inventory(person,person_inventory, inventory_items)


print(f'Day: {day}')
while True:
    log_info = ''

    hours = initial_hours + mark_game_hours(start_time, 4)
    minutes = f'{(mark_real_seconds(start_time)*15 % 60):02d}'
    hour = 12 if hours % 12 == 0 else hours % 12
    current_day =  mark_days(hours)
    if current_day != day:
        day = current_day
        log_info += f'\nDay: {day}'
        print(log_info)


    last_ate = person.get_last_consumption(person.food)
    last_drink = person.get_last_consumption(person.water)
    if hours - last_ate > 3:
        person.hunger(2)

    if hours - last_drink > 2:
        person.thirst(1)

    if f'{hour} {mark_am_or_pm(hours).upper()}' in ["6 AM" ,"10 PM" ]:
        person.eat(hours)
        person.drink(20,hours)

    if person.health < person.max_health:
        person.recover()

    if minutes == '00':
        game_data = {'day':day, 'hours': hours, 'person':person.get_stats()}
        save_game_data(game_data)

    log_time = f'{hour}:{minutes} {mark_am_or_pm(hours).upper()} {times_of_day(hours).upper()}'
    person_stats_info = f'{person.name}:{person.stats()}'
    log_info +=f'\n{log_time}\n{person_stats_info}'
    with open(log_file,'a') as f:
        f.write(log_info)

    print(log_time)
    print(person_stats_info)


    if person.status == 'Dead':
        break
    sleep(1)
    # clear_screen()