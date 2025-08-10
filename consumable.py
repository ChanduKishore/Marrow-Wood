from setup import Dimensions
from utils import RenderUtils

class Consumable():
    def __init__(self, name, energy, quantity):


        self.name = name
        self.energy = energy
        self.available_quantity = quantity
        self.edible = True

    def consume(self):
        self.available_quantity -= 1
        return self.energy

    def get_details(self):
        return {'name':self.name, 'energy':self.energy, 'quantity':self.available_quantity}


class Bush(Dimensions,RenderUtils, Consumable):
    def __init__(self, name, time_object):
        RenderUtils.__init__(self)
        Dimensions.__init__(self)
        self.name = name
        self.available_quantity = 200
        self.energy = 2
        self.max = 300
        self.transfer_quantity = 30
        self.time_object = time_object
        self.consumable_name = 'Berries'
        self.growth_period = 10*60
        self.next_availability = self.time_object.time + self.growth_period



    def grow_berries(self):
        if self.next_availability < self.time_object.time and  self.available_quantity < self.max :
            self.available_quantity = self.max

        if self.time_object.time > self.next_availability :
            self.next_availability = self.time_object.time + self.growth_period

    def transfer_items(self):
        if self.available_quantity:
            self.available_quantity -= self.transfer_quantity
            return Consumable(self.consumable_name, self.energy, self.transfer_quantity)
        else: None


    def render_graphics(self, width, x,y ):
        self.grow_berries()
        tile_height = 2 * self.one_tenth_screen_height
        self.render_surface(width, tile_height, x, y, '#03A5A5')
        self.render_surface(width/7, self.one_tenth_screen_height, x+10, y+30, 'green')
        self.render_text(self.name.upper(), (x+10,y+10,))
        self.render_text(f'{self.consumable_name}: {self.available_quantity}/{self.max}', (x+80,y+50,) )
        if  self.available_quantity < self.max :
            self.render_text(f'Avaialble in {int((self.next_availability - self.time_object.time) / 60)}:{((self.next_availability - self.time_object.time) % 60):02d}', (x + width / 2, y + 10))