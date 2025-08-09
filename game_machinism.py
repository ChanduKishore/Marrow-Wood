class HungerMechanism():
    def __init__(self, character, time_object, log, surrounding_items):
        self.character = character
        self.time_object = time_object
        self.last_ate = character.food['last_consumed']
        self.last_drink = character.water['last_consumed']
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
        return  self.character.food['quantity'] < self.character.max_food/2

    def check_last_ate(self):
        return self.time_object.get_hours() - self.character.food['last_consumed'] > self.last_ate

    def update_food_time(self, ):
        self.food_timing = self.time_object.get_time() - 1

    def update_water_time(self, ):
        self.water_timing = self.time_object.get_time() - 1

    def simulate_hunger(self):
        if self.time_object.get_time() - self.food_timing >= self.hunger_time and self.check_last_ate() :
            self.character.hunger(1)
            self.update_food_time()

        if self.check_hungry():
            self.update_log(f'{self.character.name}: Hungry')
            if not self.character.inventory:
                self.get_berries()

    def simulate_thirst(self):
        if self.time_object.get_time() - self.water_timing >= self.thirst_time:
            self.character.thirst(2)
            self.update_water_time()
            self.character.update_status('Thirsty')


    def simulate_eating(self):
        increment = 0.5

        if self.character.food['quantity'] < self.character.max_food/2  and self.character.got_food():
            self.character.eat(self.time_object.get_hours())
            self.update_log(f'{self.character.name}: Consumed Food')
        if self.character.food_serving != 0 and self.character.food['quantity'] <= self.character.max_food:
            self.character.food['quantity'] += increment
            self.character.food_serving -= increment

    def get_berries(self):
        for item in self.surrounding_items:
            if item.consumable_name == 'berries':
                self.character.add_to_inventory(item.transfer_items())
                self.update_log(f'{self.character.name}: Gathered Berries from near by Bushes')

    def regain_health(self):
        increment = 0.1
        if self.character.health < self.character.max_health and self.character.food['quantity'] != 0 :
            self.character.recover(increment)
            self.character.food['quantity'] -= increment







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















