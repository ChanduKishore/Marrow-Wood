import pygame

class CharacterHealth():
    def __init__(self, health, food, water, max_health, max_food,max_water, last_ate = 0, last_drink = 0):
        self.health = health
        self.food = {'quantity':food, 'last_consumed':last_ate}
        self.water = {'quantity':water, 'last_consumed':last_drink}
        self.stamina = 100
        self.max_health = max_health
        self.max_stamina = 100
        self.max_food = max_food
        self.max_water = max_water
        self.status = 'Normal'

    def get_stats(self):
        return {'health':self.health, 'food':self.food['quantity'], 'water':self.water['quantity'], 'max_health':self.max_health, 'max_food':self.max_food, 'max_water':self.max_water, 'last_ate':self.food['last_consumed'], 'last_drink': self.water['last_consumed'] }

    def stats(self):
        character_stats = f'''Health:{self.health} Food:{self.food['quantity']} Water:{self.water['quantity']} Status:{self.status}'''
        return character_stats

    def hunger(self, quantity=1):
        self.food['quantity'] -= quantity
        if self.food['quantity'] < 0:
            self.health -= quantity
            self.food['quantity'] = 0

        self.update_status()


    def thirst(self, quantity=1):
        self.water['quantity'] -= quantity
        if self.water['quantity'] < 0:
            self.health -= quantity
            self.water['quantity'] = 0

        self.update_status()


    def eat(self, quantity):
        if self.food['quantity'] < self.max_food:
            self.food['quantity'] += quantity
        else:
            self.status = self.throwup()

        if self.food['quantity'] >= self.max_food:
            self.food['quantity'] = self.max_food



    def drink(self, quantity):
        if self.food['quantity'] <= self.max_water:
            self.water['quantity'] += quantity

        else:
            self.throwup()
        if self.water['quantity'] >= self.max_water:
            self.water['quantity'] = self.max_water



    def throwup(self):
        return 'ThrowUp'

    def recover(self, health_gain):
        self.health += health_gain

    def update_status(self, new_status=None):
        if self.health <= 0:
            self.status = 'Dead'

        elif self.food['quantity'] < self.max_food/2:
            self.status = 'Hungry'

        elif self.water['quantity'] < self.max_water/2:
            self.status = 'Thirsty'
        else:
            self.status = 'Normal'

        if new_status:
            self.status = new_status
            return self.status

        return self.status

    def get_last_consumption(self, item):
        return item['last_consumed']


class CharacterInventory():
    def __init__(self,name):
        self.name = name
        self.inventory = []
        self.food_serving = 0
        self.available_inventory = 2


    def unlock_inventory(self):
        self.available_inventory += 1

    def add_item(self, item):
        self.inventory.append(item)

    def add_to_inventory(self, item):
        self.inventory.append(item)

    def update_inventory(self):
        expired_items = []
        for i,item in enumerate(self.inventory):
            if not item.available_quantity:
                expired_items.append(i)
        for index in expired_items:
            self.inventory.pop(index)


    def add_to_plate(self, hrs):
        for item in self.inventory:
            # check if character got any edible food
            # and food_serving will store the food same as max_food
            if item.edible:
                if self.food['quantity'] + self.food_serving < self.max_food:
                    self.food_serving += item.consume()
                self.food['last_consumed'] = hrs


        self.update_inventory()

    def get_inventory_stats(self):
        self.update_inventory()
        inventory = [ (item.name,item.get_details()) for item in self.inventory]
        stats = {'name':self.name, 'inventory':inventory}
        return stats

    def inventory_stats(self):
        self.update_inventory()
        inventory_items = [f'{item.available_quantity}*{item.name}' for item in self.inventory]
        inventory_items = ','.join(inventory_items)
        return f' Inventory:[{inventory_items}]'

    def got_food(self):
        for item in self.inventory:
            if item.edible:
                return True

        return False



class HungerMechanism(CharacterHealth, CharacterInventory):
    def __init__(self, name, health, food, water, max_health, max_food,max_water, last_ate, last_drink, time_object, log, surrounding_items):
        CharacterHealth.__init__(self,health, food, water, max_health, max_food,max_water, last_ate, last_drink)
        CharacterInventory.__init__(self,name)
        self.time_object = time_object
        self.surrounding_items = surrounding_items

        self.hours = time_object.hours
        self.time = time_object.time
        self.am_or_pm = time_object.am_or_pm

        self.hunger_time = 10
        self.thirst_time = 5
        self.food_timing = time_object.time
        self.water_timing = time_object.time
        self.last_ate = 1
        self.log = log.log_contents
        self.update_log = log.update_log

    def check_hungry(self):
        return  self.food['quantity'] < self.max_food/2

    def check_last_ate(self):
        return self.time_object.get_hours() - self.food['last_consumed'] > self.last_ate

    def update_food_time(self, ):
        self.food_timing = self.time_object.get_time() - 1

    def update_water_time(self, ):
        self.water_timing = self.time_object.get_time() - 1

    def simulate_hunger(self):
        if self.time_object.get_time() - self.food_timing >= self.hunger_time and self.check_last_ate() :
            self.hunger(1)
            self.update_food_time()



    def simulate_thirst(self):
        if self.time_object.get_time() - self.water_timing >= self.thirst_time:
            self.thirst(2)
            self.update_water_time()
            self.update_status('Thirsty')


    def simulate_eating(self):
        increment = 0.5

        if self.food['quantity'] < self.max_food  and self.got_food():
            self.add_to_plate(self.time_object.get_hours())
            self.update_log(f'{self.name}: Consumed Food')
        if self.food_serving != 0 and self.food['quantity'] <= self.max_food:
            self.eat(increment)
            self.food_serving -= increment

    def regain_health(self):
        increment = 0.1
        if self.health < self.max_health and self.food['quantity'] != 0 :
            self.recover(increment)
            self.food['quantity'] -= increment

    def simulate(self):
        #simulating hunger
        #character will lost 1 food  every 15 of game time
        #implement when sleeping hunger suppresses to half
        self.simulate_hunger()
        #simulate thirst
        # self.simulate_thirst()
        #simulate eating & drinking
        self.simulate_eating()

        #simulate regain health
        self.regain_health()

        #simulate gathering food




class SurvivalInstinct(HungerMechanism):
    def __init__(self,name,health, food, water, max_health, max_food,max_water, last_ate, last_drink,time_object, log, surrounding_items):
        HungerMechanism.__init__(self,name,health, food, water, max_health, max_food,max_water, last_ate, last_drink,time_object, log, surrounding_items)
        self.memory = []

    def get_berries(self):
        for item in self.surrounding_items:
            if item.consumable_name.lower() == 'berries':
                self.add_to_inventory(item.transfer_items())
                self.update_log(f'{self.name}: Gathered Berries from near by Bushes')

    def simulate(self):
        super().simulate()

        if self.check_hungry():
            self.update_log(f'{self.name}: Hungry')
            if not self.inventory:
                self.get_berries()


class CharacterModel( SurvivalInstinct):
    def __init__(self, name, health, food, water, max_health, max_food,max_water, last_ate , last_drink,time_object, log, surrounding_items ):
        SurvivalInstinct.__init__(self,name,health, food, water, max_health, max_food,max_water, last_ate, last_drink,time_object, log, surrounding_items)



    def get_status(self):
        return f'{self.name}: {self.status}'















