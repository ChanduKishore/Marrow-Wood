from fruit import Fruit


inventory_items = {'Fruits':Fruit}
import json
import os
from time import time

# save_file_name = 'save.txt'
# def load_save_file(save_file):
#     with open(save_file,'r') as f:
#         data = json.loads(f.read())
#
#     return data
#
# if os.path.exists(save_file_name):
#     save_data = load_save_file(save_file_name)
#     start_time = time()
#     day = save_data['day']
#     initial_hours = save_data['hours']
#     person_stats = save_data['person']
#     person_inventory = person_stats['inventory']
#
# for x in person_inventory:
#     print({**x[1], 'new':'o'})