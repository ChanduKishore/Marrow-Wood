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
    def __init__(self, name):
        RenderUtils.__init__(self)
        Dimensions.__init__(self)
        self.name = name
        self.available_quantity = 200
        self.energy = 20
        self.max = 250
        self.transfer_quantity = 5
        self.consumable_name = 'berries'


    def grow_berries(self):
        if self.available_quantity < self.max:
            self.available_quantity += self.max

    def transfer_items(self):
        if self.available_quantity:
            self.available_quantity -= self.transfer_quantity
            return Consumable(self.consumable_name, self.energy, self.transfer_quantity)
        else: None


    def render_graphics(self, width, x,y ):

        tile_height = 2 * self.one_tenth_screen_height
        self.render_surface(width, tile_height, x, y, '#03A5A5')
        self.render_surface(width/7, self.one_tenth_screen_height, x+10, y+30, 'green')
        self.render_text(self.name.upper(), (x+10,y+10,))
        self.render_text(f'Available: {self.available_quantity}', (x+80,y+50,) )
