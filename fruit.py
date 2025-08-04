class Fruit():
    def __init__(self, name, energy, quantity):
        self.name = name
        self.energy = energy
        self.quantity = quantity
        self.catagory = 'Fruit'
        self.edible = True

    def consume(self):
        self.quantity -= 1
        return self.energy

    def get_details(self):
        return {'name':self.name, 'energy':self.energy, 'quantity':self.quantity}

apple = Fruit('apple', 20, 50)
orange = Fruit('orange', 20, 50)

