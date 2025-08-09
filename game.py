import pygame
from day_and_night_cycle import DayNightCycle
from consumable import Consumable, Bush
from utils import  DialogBox,RenderUtils, Inventory
from character import CharacterStats
from game_machinism import HungerMechanism
from setup import Dimensions

class Logs():
    def __init__(self, time_obj,log_contents='' ):
        self.log_contents = log_contents
        self.time_obj = time_obj

    def get_latest_log(self):
        return self.log_contents

    def update_log(self, content):
        previous_logs = [log for i,log in enumerate(self.log_contents.split('\n')[::-1]) if log and i%2]
        previous_log = previous_logs[:1] if previous_logs else ''
        if not content in previous_log:
            log_time = f'Day: {self.time_obj.day}/ {self.time_obj.render_time()}'
            self.log_contents += f'{log_time}\n{content}\n'
        # print('log_content',self.log_contents)
        return self.log_contents


class GameWindow(Dimensions,RenderUtils,DialogBox,Inventory):
    def __init__(self,time_obj, followers, log, surrounding_items):
        Dimensions.__init__(self)
        RenderUtils.__init__(self)
        self.title = 'Marrow Wood'
        self.icon = pygame.image.load('images/forest-icon.jpg')
        self.time_control = 500
        self.start_time = pygame.time.get_ticks()
        self.clock = pygame.time.Clock()
        self.current_selection = followers[0]
        self.surrounding_items = surrounding_items


        # game objects
        self.time_obj = time_obj
        self.followers = followers
        self.log = log

        #navigation tabs
        self.navigation_height = self.height/15
        self.left_navigation = [
            {'name':'Followers','status':True,
             'screen':self.followers_screen,
             'screen_dims':(self.half_screen_width, self.height - (self.one_tenth_screen_height + self.navigation_height), 0, self.one_tenth_screen_height + self.navigation_height, 'grey')},
            {'name':'Knowledge','status':False, 'screen':self.sample, 'screen_dims':''},
            {'name':'Craftings','status':False, 'screen':self.sample, 'screen_dims':''}]

        self.right_navigation = [{
            'name':'Game Logs','status':True,
             'screen':self.game_logs_screen,
             'screen_dims':(self.half_screen_width,self.height-self.navigation_height,self.half_screen_width,self.navigation_height)},
            {'name':'Inventory','status':False, 'screen':self.inventory_screen,
             'screen_dims':(self.half_screen_width,self.height-self.navigation_height,self.half_screen_width,self.navigation_height,'black')},
            {'name':'Surroundings','status':False, 'screen':self.surroundings_screen,
             'screen_dims':(self.half_screen_width,self.height-self.navigation_height,self.half_screen_width,self.navigation_height,self.surrounding_items,'black')}]

        self.set_nav_buttons(self.half_screen_width,self.navigation_height,0,self.height/10,self.left_navigation)
        self.set_nav_buttons(self.half_screen_width,self.navigation_height,self.half_screen_width,0,self.right_navigation)

        self.dialog_box = DialogBox(self.half_screen_width, self.height - self.navigation_height, self.half_screen_width, self.navigation_height, self.log.log_contents, self.screen, self.render_text, '#64FCF8')
        self.inventory = Inventory(self.half_screen_width,self.height-self.navigation_height,self.half_screen_width,self.navigation_height,self.render_text,self.render_surface,self.screen)

    def sample(self):
        self.render_surface(self.width, self.height, 0, self.navigation_height + self.one_tenth_screen_height, 'green')


    def load_save(self):
        pass

    def time_screen(self):
        self.render_surface(self.half_screen_width, self.height/10,0,0,'#F2F2F2')
        self.render_text(f'Day: {self.time_obj.day}', (10, 0))
        self.render_text(self.time_obj.render_time(), (10, 24))
        self.time_obj.update_time(self.get_delta_time_s())


    def set_nav_buttons(self, width,height,x,y,buttons_dict):
        # number of buttons in navigation pane
        n_buttons = len(buttons_dict)
        button_width = width / n_buttons
        button_height = height
        for i,button in enumerate(buttons_dict):
            pos_x = x + (i * button_width)
            pos_y = y
            button['button_obj']= self.create_button(button_width, button_height,pos_x,pos_y,button['name'])

    def update_button_status(self,button_objs,active_button):
        for button in button_objs:
            if button['name'] != active_button['name']:
                button['status'] = False
            else:
                button['status'] = True

    def navigation_tab(self,buttons_dict):

        for i,current_button_dict in enumerate(buttons_dict):
            button = current_button_dict['button_obj']
            screen = current_button_dict['screen']
            screen_dims = current_button_dict['screen_dims']
            if button.process(self.screen):
                self.update_button_status(buttons_dict,current_button_dict)

            if current_button_dict['status']:
                screen(*screen_dims)
                button.set_button_color('pressed','black')
            else:
                button.set_button_color('normal')


    def render_status_bar(self,width,height,x,y,label,progress_amount,color):
        bar_x = x + 50
        border_offset = 2
        progress_amount = progress_amount if progress_amount > 0 else 0
        self.render_text(label,(x,y), color='white')
        self.render_surface(width, height, bar_x, y, 'white')
        self.render_surface(progress_amount, (height - 2*border_offset),bar_x+border_offset,y+border_offset,color)


    def follower_selection(self, object, follower_obj):
        mousePos = pygame.mouse.get_pos()
        if object.collidepoint(mousePos):
            # self.set_button_color('hover')
            if pygame.mouse.get_pressed()[0] :
                self.current_selection = follower_obj



    def follower_stats(self, follower, width, height, x, y):
        stats = follower.get_stats()
        progress_bars = [('health','green'), ('food', 'red' ),('water', 'light blue')]
        status_bar_height = height/8
        status_bar_width = width/2
        padding = 10
        
        self.render_surface(width,height,x,y,'#163E64')
        self.render_text(follower.name,(x+padding,y+padding), color='white')
        follower_surface = pygame.Rect(x, y, width, height)
        for i, bar_tuple in enumerate(progress_bars):
            label, color = bar_tuple
            pos_x = x + padding
            pos_y = y + 4*padding + i*(status_bar_height + padding/2)
            label_name = label[0].upper() + label[1:]
            progress = stats[label]/stats[f'max_{label}'] * status_bar_width *.98
            self.render_status_bar(status_bar_width, status_bar_height, pos_x , pos_y , label_name, progress, color)
            self.follower_selection(follower_surface, follower)


    def followers_screen(self, width, height, x, y, color):
        self.render_surface(width, height, x, y, color)
        for i,follower in enumerate(self.followers):
            padding = 2
            tile_height = 2*self.one_tenth_screen_height
            pos_y = y + (i * (tile_height + padding))
            self.follower_stats(follower,width, tile_height, x, pos_y)


    def game_logs_screen(self,width, height, x, y, color ='#0B3041'):
        self.render_surface(width, height, x, y, color)

        self.dialog_box.update_text(self.log.get_latest_log())
        self.dialog_box.render()
        # self.render_text('This section will render Game Logs',(x,y), color='#64FCF8')



    def inventory_screen(self,width, height, x, y, color ='#0B3041'):
        # self.render_surface(width, height, x, y, color)
        self.inventory.render(self.current_selection)
        # self.render_text(self.current_selection.name,(x+10,y+250), color='#64FCF8')


    def surroundings_screen(self,width, height, x, y, items,color ='#0B3041'):
        self.render_surface(width, height, x, y, color)
        for item in items:
            item.render_graphics(width,x,y)

        # self.render_text('This section will render surroundings screen',(x,y), color='#64FCF8')


    def get_delta_time_s(self):
        return (pygame.time.get_ticks() - self.start_time) // self.time_control


    def render_game_screen(self):
        pygame.display.set_caption(self.title)
        pygame.display.set_icon(self.icon)



        # Render time screen
        self.time_screen()

        #render left navigation pane
        self.navigation_tab(self.left_navigation)
        self.navigation_tab(self.right_navigation)
        #render followers_screen


        pygame.display.update()
        self.clock.tick(60)




time_object = DayNightCycle(0)



#set up character objects
person1_stats = {'name':'First Follower', 'health':10, 'food':60, 'water':50, 'max_health':100, 'max_food':100, 'max_water':100, 'last_ate':0, 'last_drink': 0, 'inventory':[] }
person2_stats = {'name':'Second Follower', 'health':80, 'food':60, 'water':50, 'max_health':100, 'max_food':100, 'max_water':100, 'last_ate':0, 'last_drink': 0, 'inventory':[] }
person1 = CharacterStats(**person1_stats)
person2 = CharacterStats(**person2_stats)
bush = Bush('Near By Bush')
surrounding_items = [bush]
# person.add_to_inventory(apple)
# person.add_to_inventory(orange)

follower_objects = [person1, person2]
log = Logs(time_object)

hunger_mechanism =[]
for person in follower_objects:
    hunger_mechanism.append(HungerMechanism(person, time_object, log, surrounding_items))


game = GameWindow( time_object, follower_objects, log, surrounding_items)



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    for person in hunger_mechanism:
        person.simulate()

    game.render_game_screen()