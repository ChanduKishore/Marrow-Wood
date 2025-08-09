import pygame


class Button():
    def __init__(self, x, y, width, height, font, buttonText='Button'):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.alreadyPressed = False
        self.font = font
        self.buttonText = buttonText

        self.fillColors = {
            'normal': '#D9D9D9',
            'pressed': '#ffffff',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.set_button_color('normal')
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.buttonSurf = self.font.render(self.buttonText, True, (128, 128, 128))

    def set_button_color(self, state, font_color=(128, 128, 128)):
        self.buttonSurface.fill(self.fillColors[state])
        self.buttonSurf = self.font.render(self.buttonText, True, font_color)

    def process(self, surface):
        action = False
        mousePos = pygame.mouse.get_pos()

        if self.buttonRect.collidepoint(mousePos):
            # self.set_button_color('hover')
            if pygame.mouse.get_pressed()[0] and self.alreadyPressed == False:
                self.alreadyPressed = True
                # self.set_button_color('pressed')
                action = True

            if not pygame.mouse.get_pressed()[0]:
                self.alreadyPressed = False

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        surface.blit(self.buttonSurface, self.buttonRect)
        return action


class RenderUtils(Button):

    def __init__(self):
        pygame.init()
        self.font_size= 16
        self.font_family = 'calibri'

    def create_font(self, font_size=16, font_family=None, bold=False, italic=False, color='black'):
        if font_family:
            font = pygame.font.SysFont(font_family, font_size, bold, italic)
        else:
            font = pygame.font.SysFont(self.font_family, font_size, bold, italic)

        return font
    def render_text(self, text, pos,color='black', font_size=16, font_family=None, bold=False, italic=False):

        font = self.create_font(font_size,font_family,bold,italic,color)

        text = font.render(text, True, color)
        self.screen.blit(text, pos)

        return font.get_height()

    def create_button(self, width, height, x, y, name, font_size=16, font_family=None, bold=False, italic=False, color='black'):
        font = self.create_font(font_size,font_family,bold,italic,color)
        return Button(x, y, width, height, font, name)

    def update_button_status(self, button_objs, active_button):
        for button in button_objs:
            if button['name'] != active_button['name']:
                button['status'] = False
            else:
                button['status'] = True

    def render_surface(self,width, height,x,y,color):
        surface = pygame.Surface((width, height))
        surface.fill(color)
        self.screen.blit(surface, (x, y))




class DialogBox():
    def __init__(self, w, h,x,y, text,surface, render_text, font_color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.surface = surface
        self.text = text
        self.index = 0
        self.y_delta = 0
        self.render_text = render_text
        self.font_color = font_color
        self.padding = 5

    def update_text(self, new_text):
        self.text = new_text

    def calc_y_delta(self, font_height):
        self.y_delta = int(self.h/font_height)
    def render(self):
        ### Text
        y = self.y + self.padding
        lines = self.text.split('\n')
        extra_line_space = 4
        padding = 10
        for i,line in enumerate(lines[-self.y_delta:]):

            font_height = self.render_text(line, (self.x + padding , y), color = self.font_color, font_size = 13 )
            self.calc_y_delta(font_height + extra_line_space*1.5)
            if not 'Day' == line[:3]:
                y+= extra_line_space
            y += font_height + extra_line_space



class Inventory():
    def __init__(self,w,h,x,y,render_text, render_surface, screen ,slots = 7, rows = 4):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.screen = screen
        self.slots = slots
        self.rows = rows
        self.slot_size = self.w/self.slots
        self.render_text = render_text
        self.render_surface = render_surface


    def render_slots(self,pos_y,offset, padding):
        slot_index = 0
        for row in range(self.rows):
            y = pos_y + row * self.slot_size + padding
            x = self.x + offset
            for i in range(0, self.slots):
                self.render_surface(self.slot_size - offset , self.slot_size - offset, x, y, 'dark grey')
                x += self.slot_size
                slot_index += 1

    def inventory_item_slot(self, item,x,y):
        if item:
            self.render_text(item.name[0].upper(), (x+15,y+10), 'black', font_size = 24 )
            self.render_text(f'x{item.available_quantity}', (x + self.slot_size / 2, y + self.slot_size / 1.5), 'black', )

    def render(self, char_obj):
        items = char_obj.inventory
        offset = 2
        padding = 5
        slot_pos_y = self.y + 10*offset
        self.render_surface(self.w, self.h, self.x, self.y, 'white')
        self.render_text(char_obj.name,(self.x + offset*padding , self.y + padding),'black',font_size = 18)
        self.render_slots(slot_pos_y,offset, padding)

        if len(items):
            slot_index = 0
            for row in range(self.rows):
                y = slot_pos_y + row * self.slot_size + offset # adjustment needed
                x = self.x + offset
                for i in range( 0, self.slots):
                    item = items[slot_index] if len(items) > slot_index  else None
                    self.inventory_item_slot(item,x,y)
                    x += self.slot_size
                    slot_index += 1


