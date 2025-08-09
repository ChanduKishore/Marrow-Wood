import pygame

class CharacterHealthStats():
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


    def eat(self, quantity, hrs):
        if self.food['quantity'] < self.max_food:
            self.food['quantity'] += quantity
        else:
            self.status = self.throwup()

        if self.food['quantity'] >= self.max_food:
            self.food['quantity'] = self.max_food

        self.food['last_consumed'] = hrs
        self.update_status('Consumed food')



    def drink(self, quantity, hrs):
        if self.food['quantity'] <= self.max_water:
            self.water['quantity'] += quantity

        else:
            self.throwup()
        if self.water['quantity'] >= self.max_water:
            self.water['quantity'] = self.max_water
        self.water['last_consumed'] = hrs
        self.update_status('Consumed water')



    def throwup(self):
        return 'ThrowUp'

    def recover(self, health_gain):
        self.health += health_gain

    def update_status(self, new_status=None):
        if self.health < 0:
            self.health <= 0
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




class CharacterStats(CharacterHealthStats):
    def __init__(self, name, health, food, water, max_health, max_food,max_water,inventory, last_ate = 0, last_drink = 0):
        CharacterHealthStats.__init__(self, health, food, water, max_health, max_food, max_water, last_ate = last_ate, last_drink = last_drink)
        self.name = name
        self.inventory = []
        self.food_serving = 0

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


    def eat(self, hrs):
        for item in self.inventory:
            # check if character got any edible food
            # and food_serving will store the food same as max_food
            if item.edible:
                if self.food['quantity'] + self.food_serving < self.max_food:
                    self.food_serving += item.consume()
                self.food['last_consumed'] = hrs


        self.update_inventory()

    def get_stats(self):
        self.update_inventory()
        inventory = [ (item.name,item.get_details()) for item in self.inventory]
        stats = {**super().get_stats(),'name':self.name, 'inventory':inventory}
        return stats

    def stats(self):
        self.update_inventory()
        inventory_items = [f'{item.available_quantity}*{item.name}' for item in self.inventory]
        inventory_items = ','.join(inventory_items)
        return f'{super().stats()} Inventory:[{inventory_items}]'

    def got_food(self):
        for item in self.inventory:
            if item.edible:
                return True

        return False

    def get_status(self):
        return f'{self.name}: {self.status}'



















