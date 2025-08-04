import pygame

class CharacterHungerMachanism():
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
        if self.food['quantity'] <= self.max_food:
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

    def recover(self):
        if self.food['quantity'] > 0 and self.water['quantity'] > 20:
            self.health += 10
            self.food['quantity'] -= 5
            self.water['quantity'] -= 5
            self.status = 'Recovering'

        if self.health >= self.max_health:
            self.health = self.max_health

        if self.health < 0:
            self.health = 0

        if self.food['quantity'] <= 0:
            self.food['quantity'] = 0
        if self.water['quantity'] <= 0:
            self.water['quantity'] = 0


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


class CharacterPygameStats():
    def __init__(self, name):
        self.name = name
        self.surf = pygame.Surface((0, 0))
        self.font = pygame.font.SysFont('Arial', 14)
        self.title = self.font.render(self.name.upper(), True, 'black', )

    def status_bar(self, label, stats, w,h,x,y,color, surface):

        bar_stats = stats[label] / stats[f'max_{label}']
        bar_stats = 0 if bar_stats < 0 else bar_stats
        stat_label = self.font.render(label.upper(), True, 'black', )
        stat_bar = pygame.Surface((w*0.5+4, h*0.15+4))
        stat_bar_filler = pygame.Surface((w*0.5*bar_stats, h*0.15))
        stat_bar.fill('#ffffff')
        stat_bar_filler.fill(color)
        surface.blit(stat_label, (x+10, y))
        surface.blit(stat_bar, (w*.2, y))
        surface.blit(stat_bar_filler, (w*.2 +2, y+2))

    def pygame_display_stats(self, w,h,x,y, color, surface):
        stats = self.get_stats()
        self.surf =  pygame.Surface((w,h))
        self.surf.fill(color)

        surface.blit(self.surf,(x,y))
        surface.blit(self.title,(x+10,y+5))

        self.status_bar('health',stats,w,h,x,y+25,'dark green', surface)
        self.status_bar('food', stats, w, h, x, y + 45,'red', surface)
        self.status_bar('water', stats, w, h, x, y + 65,'light blue', surface)


class CharacterStats(CharacterHungerMachanism):
    def __init__(self, name, health, food, water, max_health, max_food,max_water,inventory, last_ate = 0, last_drink = 0):
        CharacterHungerMachanism.__init__(self, health, food, water, max_health, max_food,max_water, last_ate = last_ate, last_drink = last_drink)
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
            if not item.quantity:
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
        inventory = [ (item.catagory,item.get_details()) for item in self.inventory]
        stats = {**super().get_stats(),'name':self.name, 'inventory':inventory}
        return stats

    def stats(self):
        self.update_inventory()
        inventory_items = [f'{item.quantity}*{item.name}' for item in self.inventory]
        inventory_items = ','.join(inventory_items)
        return f'{super().stats()} Inventory:[{inventory_items}]'

    def got_food(self):
        for item in self.inventory:
            if item.edible:
                return True

        return False

    def get_status(self):
        return f'{self.name}: {self.status}'








person_stats = {'health':100, 'food':60, 'water':100, 'max_health':100, 'max_food':100, 'max_water':100, 'last_ate':20, 'last_drink': 0 }

# person2 = CharacterStats(**person_stats)
#
#
# from fruits import Fruits
#
# apple = Fruits('apple',20, 50)
# orange = Fruits('orange',20,50)
#
# print(person2.stats())
#
# person2.add_item(apple)
#
# person2.eat(60)
#
# print(person2.stats())










