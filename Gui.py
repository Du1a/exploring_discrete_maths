# Gui
# DQ

import pygame
import pygame.locals
import sys
from Graphs import Floyds_Graph, Kruskals_Graph

pygame.init()

class Screen:
    __WIN_WIDTH = 2520
    __WIN_HEIGHT = 1375
    __WIN = pygame.display.set_mode((__WIN_WIDTH, __WIN_HEIGHT))
    __MID_SURFACE = pygame.surface.Surface((__WIN_WIDTH, 15000))
    __COMMANDS = ['Select the algorithm you want an example question for:',
                  'Then select the number of nodes you want in the graph:',
                  'Click screen for new example',
                  "Perform Kruskal's Algorithm on the following graph:",
                  'Sort arcs into ascending order:', 'Connected:',
                  "Perform Floyd's Algorithm on the following distance matrix:",
                  'Construct initial route matrix:', 'Update matrices: pass',
                  'No changes', "Final matrices:"]
    __TITLE = 'Examples Generator'
    __COLOURS = {'black':pygame.Color(0, 0, 0), 'white':pygame.Color(255, 255, 255),
                 'blue':pygame.Color(0, 200, 255), 'red':pygame.Color(255, 0, 0),
                 'green':pygame.Color(0, 200, 0), 'yellow':pygame.Color(255, 255, 60)}
    __FONT = 'timesnewroman'
    __FONTS = {'title':pygame.font.SysFont(__FONT, 60), 'selection':pygame.font.SysFont(__FONT, 50),
               'commands':pygame.font.SysFont(__FONT, 40), 'numbers':pygame.font.SysFont(__FONT, 33)}
    __RELATIVE_NODE_POSITIONS = {'4':((0,0), (2,0), (0,2), (2,2)),
                                 '5':((2,0), (0,1), (4,1), (1,2), (3,2)),
                                 '6':((1,0), (2,0), (0,1), (3,1), (1,2), (2,2)),
                                 '7':((3,0), (2,1), (4,1), (0,2), (6,2), (2,3), (4,3)),
                                 '8':((3,0), (2,1), (4,1), (0,2), (6,2), (2,3), (4,3), (3,4))}
    __RADIUS = 40
    __CELL_SIZE = 80
    __Y_SPACES = {'initial_selection':80, 'secondary_selection':40, 'questions':30}
    __X_INDENT = 40

    def __init__(self):
        colours = {'black':Screen.__COLOURS['black'],
                   'yellow':Screen.__COLOURS['yellow'],
                   'green':Screen.__COLOURS['green']}
        self.__kruskals_button = Button("Kruskal's Algorithm", Screen.__FONTS['selection'], colours,
                                        Screen.__WIN_WIDTH//2-2*Screen.__Y_SPACES['secondary_selection'],
                                        Screen.__WIN_WIDTH//4)
        self.__floyds_button = Button("Floyd's Algorithm", Screen.__FONTS['selection'], colours,
                                      Screen.__WIN_WIDTH//2-2*Screen.__Y_SPACES['secondary_selection'],
                                      Screen.__WIN_WIDTH//4)
        self.__node_buttons = [Button(f'{i}', Screen.__FONTS['selection'], colours,
                                      Screen.__WIN_WIDTH//6-2*Screen.__Y_SPACES['secondary_selection'],
                                      Screen.__WIN_WIDTH//8)
                                      for i in range(Floyds_Graph.MIN_NO_NODES, Floyds_Graph.MAX_NO_NODES+1)]
        self.__node_buttons += [Button('Any', Screen.__FONTS['selection'], colours,
                                       Screen.__WIN_WIDTH//6-2*Screen.__Y_SPACES['secondary_selection'],
                                       Screen.__WIN_WIDTH//8)]

        self.__reset_button = Button('Reset', Screen.__FONTS['commands'], colours,
                                     Screen.__WIN_WIDTH//10, Screen.__WIN_WIDTH//16)
        self.__input = [None, None]
        self.__screen = None
        self.__is_changed = False
        self.__bottom = None
        self.__arc_list = None
        self.__is_final = False
        self.__scroll_by = 80
        self.__y_position = 0
        self.__y_pos_to_blit = 0
        self.__nodes = {}
        self.__graph = None
        self.__display()

    # decorator
    def __show_clickable(func):
        def inner(self):
            self.__show_text(Screen.__COMMANDS[2], Screen.__FONTS['numbers'],
                             Screen.__COLOURS['red'], Screen.__COLOURS['white'],
                             (Screen.__WIN_WIDTH-200, 80), 0)
            func(self)
        return inner        

    def __display(self):
        pygame.display.set_caption(Screen.__TITLE)
        fps = pygame.time.Clock()
        fps.tick(60)
        while True:
            self.__get_input()
            self.__set_screen()
            self.__reset_button.display(Screen.__WIN_WIDTH-self.__reset_button.width*1.2,
                                        self.__y_pos_to_blit+Screen.__Y_SPACES['questions']//2,
                                        Screen.__MID_SURFACE, Screen.__WIN)
            self.__bottom = self.__y_pos_to_blit
            if self.__screen == self.__floyds_button.name:
                self.__scroll_by = self.__bottom/20
            else:
                self.__scroll_by = self.__bottom/50
            
    def __get_input(self):
        if data:=self.__handle_events():
            if data == self.__reset_button.name:
                self.__input = [None, None]
                self.__screen = None
                self.__y_position = 0
            elif not self.__input[0]:
                self.__input[0] = data
            elif not self.__input[1]:
                self.__input[1] = data
        if (self.__input[0] not in (Button.buttons[0].name, Button.buttons[1].name, None)
            or self.__input[1] in (Button.buttons[0].name, Button.buttons[1].name)):
            Button.unclick()
            self.__input = [None, None]
        if self.__input[0] and self.__input[1]:
            self.__screen = self.__input[0]

    def __handle_events(self):
        y_change = 0
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in [4,5]:
                    if self.__screen != None and 0 >= self.__y_position >= -self.__bottom:
                        if event.button == 4 and self.__y_position <= -self.__scroll_by:
                            y_change = max(self.__scroll_by, self.__y_position)
                        elif event.button == 5 and self.__y_position >= -self.__bottom+self.__scroll_by:
                            y_change = max(-self.__scroll_by, -self.__bottom)
                else:
                    mouse_pos = pygame.mouse.get_pos()
                    self.__is_changed = True
                    for button in Button.buttons:
                        if button.name == self.__reset_button.name:
                            if button.check_is_clicked(mouse_pos, self.__y_position):
                                Button.unclick()
                                return button.name
                        elif button.check_is_clicked(mouse_pos) and self.__screen == None:
                            return button.name
        self.__scroll(y_change)
        pygame.display.flip()

    def __scroll(self, change):
        self.__y_position += change
        Screen.__WIN.blit(Screen.__MID_SURFACE, (0, self.__y_position))
    
    def __fill(self, colour):
        Screen.__MID_SURFACE.fill(colour)
        Screen.__WIN.blit(Screen.__MID_SURFACE, (0, self.__y_position))

    def __set_screen(self):
        self.__fill(Screen.__COLOURS['white'])
        self.__y_pos_to_blit = Screen.__Y_SPACES['initial_selection']//2
        if self.__screen == None:
            self.__display_home_screen()
        elif self.__screen == self.__kruskals_button.name:
            self.__display_kruskals()
        elif self.__screen == self.__floyds_button.name:
            self.__display_floyds()

    def __display_home_screen(self):
        self.__show_text(Screen.__COMMANDS[0], Screen.__FONTS['title'])
        self.__y_pos_to_blit += 0.5*Screen.__Y_SPACES['initial_selection']
        self.__kruskals_button.display(Screen.__X_INDENT, self.__y_pos_to_blit,
                                       Screen.__MID_SURFACE, Screen.__WIN)
        self.__y_pos_to_blit = self.__floyds_button.display(Screen.__WIN_WIDTH//2+Screen.__X_INDENT,
                                                            self.__y_pos_to_blit, self.__MID_SURFACE,
                                                            self.__WIN)
        self.__y_pos_to_blit += 0.5*Screen.__Y_SPACES['initial_selection']
        self.__show_text(Screen.__COMMANDS[1], Screen.__FONTS['selection'])
        self.__y_pos_to_blit += Screen.__Y_SPACES['initial_selection']//2
        self.__y_pos_to_blit = [self.__node_buttons[i].display(Screen.__X_INDENT*6*(i+0.6)*2,
                                                               self.__y_pos_to_blit,
                                                               self.__MID_SURFACE, self.__WIN)
                                                               for i in range(len(self.__node_buttons))][0]
    
    @__show_clickable
    def __display_floyds(self):
        Button.unclick()
        if self.__is_changed:
            self.__graph = Floyds_Graph(self.__input[1])
            self.__y_position = 0
            Screen.__WIN.blit(Screen.__MID_SURFACE, (0, self.__y_position))
        self.__is_changed = False
        self.__show_text(Screen.__COMMANDS[6], Screen.__FONTS['commands'])
        self.__show_distance_matrix()
        self.__show_text(Screen.__COMMANDS[7], Screen.__FONTS['commands'])
        self.__show_matrices()
        for i in range(len(self.__graph)): 
            self.__show_text(Screen.__COMMANDS[8]+' '+str(i+1), Screen.__FONTS['commands'])
            self.__show_matrices(i)

        self.__show_text(Screen.__COMMANDS[10], Screen.__FONTS['commands'])
        self.__show_matrices(True)
    
    def __show_matrices(self, i=False):
        self.__show_distance_matrix(i)
        self.__show_route_matrix(i)
    
    def __show_distance_matrix(self, k=False):
        y_pos = self.__y_pos_to_blit
        for i in range(len(self.__graph)+2):
            pygame.draw.aaline(Screen.__MID_SURFACE, Screen.__COLOURS['black'],
                               (Screen.__X_INDENT, self.__y_pos_to_blit),
                               (Screen.__X_INDENT+Screen.__CELL_SIZE*(len(self.__graph)+1),
                                self.__y_pos_to_blit))
            pygame.draw.aaline(Screen.__MID_SURFACE, Screen.__COLOURS['black'],
                               ((i*self.__CELL_SIZE)+Screen.__X_INDENT, y_pos),
                               ((i*self.__CELL_SIZE)+Screen.__X_INDENT,
                                y_pos+(self.__CELL_SIZE*(len(self.__graph)+1))))
            self.__y_pos_to_blit += Screen.__CELL_SIZE
            if i != len(self.__graph)+1:
                for j in range(len(self.__graph)+1):
                    if k is i-1 or k is j-1:
                        back_colour = Screen.__COLOURS['blue']
                    else:
                        back_colour = Screen.__COLOURS['white']
                    x_char_pos = Screen.__X_INDENT+Screen.__CELL_SIZE*(j+0.5)
                    y_char_pos = self.__y_pos_to_blit-Screen.__CELL_SIZE*0.5
                    if j == i and j != 0:
                        self.__show_text('-', Screen.__FONTS['commands'],
                                         Screen.__COLOURS['black'], back_colour,
                                         (x_char_pos, y_char_pos), False)
                    elif j == 0 and i != 0:
                        self.__show_text(self.__graph.nodes[i-1].name,
                                         Screen.__FONTS['commands'],
                                         Screen.__COLOURS['black'], back_colour,
                                         (x_char_pos, y_char_pos), False)
                    elif i == 0 and j != 0:
                        self.__show_text(self.__graph.nodes[j-1].name,
                                         Screen.__FONTS['commands'],
                                         Screen.__COLOURS['black'], back_colour,
                                         (x_char_pos, y_char_pos), False)
                    elif j != 0:
                        text_colour = Screen.__COLOURS['black']
                        match k:
                            case bool():
                                if k:
                                    weight = self.__graph.get_path_weight(len(self.__graph)-1, i-1, j-1) 

                                elif (weight:=self.__graph.weight(i-1, j-1)) == Floyds_Graph.LACK_CONNECTION:
                                    weight = '∞'

                            
                            case int():
                                if (weight:=self.__graph.get_path_weight(k, i-1, j-1)) == Floyds_Graph.LACK_CONNECTION:
                                    weight = '∞'
                                if self.__graph.get_change(k, i-1, j-1):
                                    text_colour = Screen.__COLOURS['red']
                        self.__show_text(weight, Screen.__FONTS['commands'], text_colour,
                                         back_colour, (x_char_pos, y_char_pos), False)

    def __show_route_matrix(self, k):
        match k:
            case bool():
                is_bool = True
                is_updated = True
            case _:
                is_updated = False
                is_bool = False
        self.__y_pos_to_blit -= Screen.__CELL_SIZE*(len(self.__graph)+2)
        y_pos = self.__y_pos_to_blit
        for i in range(len(self.__graph)+1):
            pygame.draw.aaline(Screen.__MID_SURFACE, Screen.__COLOURS['black'],
                               (Screen.__WIN_WIDTH-Screen.__X_INDENT,
                                self.__y_pos_to_blit),
                                (Screen.__WIN_WIDTH-(Screen.__X_INDENT+Screen.__CELL_SIZE*(len(self.__graph)+1)), self.__y_pos_to_blit))
            pygame.draw.aaline(Screen.__MID_SURFACE, Screen.__COLOURS['black'],
                               (Screen.__WIN_WIDTH-((i*self.__CELL_SIZE)+Screen.__X_INDENT), y_pos),
                               (Screen.__WIN_WIDTH-((i*self.__CELL_SIZE)+Screen.__X_INDENT),
                                y_pos+(self.__CELL_SIZE*(len(self.__graph)+1))))
            self.__y_pos_to_blit += Screen.__CELL_SIZE  
            for j in range(len(self.__graph)+1):
                y_char_pos = self.__y_pos_to_blit-Screen.__CELL_SIZE*0.5
                x_char_pos = Screen.__WIN_WIDTH-(Screen.__X_INDENT+Screen.__CELL_SIZE*(len(self.__graph)-j+0.5))
                if j == 0 and i != 0:
                    self.__show_text(self.__graph.nodes[i-1].name, Screen.__FONTS['commands'],
                                     Screen.__COLOURS['black'], Screen.__COLOURS['white'],
                                     (x_char_pos, y_char_pos), False)
                elif (i == 0 or k is False) and j != 0:
                    self.__show_text(self.__graph.nodes[j-1].name, Screen.__FONTS['commands'],
                                     Screen.__COLOURS['black'], Screen.__COLOURS['white'],
                                     (x_char_pos, y_char_pos), False)
                elif j != 0:
                    if self.__graph.get_change(k, i-1, j-1) and not is_bool:
                        text_colour = Screen.__COLOURS['red']
                        is_updated = True
                    else:
                        text_colour = Screen.__COLOURS['black']
                    backgroud_colour = Screen.__COLOURS['white']
                    if not is_bool:
                        if j == k+1:
                            backgroud_colour = Screen.__COLOURS['blue']
                        self.__show_text(self.__graph.get_path(k, i-1, j-1),
                                         Screen.__FONTS['commands'], text_colour,
                                         backgroud_colour, (x_char_pos, y_char_pos),
                                         False)
                    else:
                        self.__show_text(self.__graph.get_path(len(self.__graph)-1, i-1, j-1),
                                         Screen.__FONTS['commands'], text_colour,
                                         backgroud_colour, (x_char_pos, y_char_pos), False)
        pygame.draw.aaline(Screen.__MID_SURFACE, Screen.__COLOURS['black'],
                           (Screen.__WIN_WIDTH-Screen.__X_INDENT, self.__y_pos_to_blit),
                           (Screen.__WIN_WIDTH-(Screen.__X_INDENT+Screen.__CELL_SIZE*(len(self.__graph)+1)),
                            self.__y_pos_to_blit))
        pygame.draw.aaline(Screen.__MID_SURFACE, Screen.__COLOURS['black'],
                           (Screen.__WIN_WIDTH-(((i+1)*self.__CELL_SIZE)+Screen.__X_INDENT), y_pos),
                           (Screen.__WIN_WIDTH-(((i+1)*self.__CELL_SIZE)+Screen.__X_INDENT),
                            y_pos+(self.__CELL_SIZE*(len(self.__graph)+1))))
        self.__y_pos_to_blit += Screen.__CELL_SIZE
        if not is_updated:
            self.__show_text(Screen.__COMMANDS[9], Screen.__FONTS['commands'])
            self.__y_pos_to_blit += Screen.__Y_SPACES['questions']

    def __show_text(self, text, font, text_colour=None, background_colour=None,
                    centre=None, change_in_y_pos=True):
        if isinstance(text, int):
            text = str(text)
        if not text_colour:
            text_colour = Screen.__COLOURS[list(Screen.__COLOURS.keys())[0]]
            if not background_colour:
                background_colour = Screen.__COLOURS[list(Screen.__COLOURS.keys())[1]]
                if not centre:
                    centre = (Screen.__WIN_WIDTH//2, self.__y_pos_to_blit)
        text = font.render(text, True, text_colour, background_colour)
        text_rect = text.get_rect()
        text_rect.center = centre
        Screen.__MID_SURFACE.blit(text, text_rect)
        Screen.__WIN.blit(Screen.__MID_SURFACE, (0, 0))
        if change_in_y_pos:
            match change_in_y_pos:
                case bool():
                    self.__y_pos_to_blit = text_rect.y + text_rect.height
                case int():
                    self.__y_pos_to_blit += change_in_y_pos
    
    @__show_clickable
    def __display_kruskals(self):
        Button.unclick()
        if self.__is_changed:
            self.__graph = Kruskals_Graph(self.__input[1])
            self.__arc_list = list(self.__graph.selected_arcs.items())
            self.__y_position = 0
            Screen.__WIN.blit(Screen.__MID_SURFACE, (0, self.__y_position))
        self.__show_text(Screen.__COMMANDS[3], Screen.__FONTS['commands'])
        self.__show_graph()
        self.__y_pos_to_blit += Screen.__Y_SPACES['initial_selection']//2
        self.__show_text(Screen.__COMMANDS[4], Screen.__FONTS['commands'])
        self.__y_pos_to_blit += Screen.__Y_SPACES['questions']
        self.__display_sorted_arcs()
        self.__y_pos_to_blit += Screen.__Y_SPACES['questions']
        no_connected_arcs = 0
        i = 0
        connected_values = list(self.__graph.selected_arcs.values())
        unconnected_values = list(self.__graph.arcs.values())
        while no_connected_arcs < len(self.__graph) -1:
            if connected_values[i]:
                self.__show_text(f'Connect {connected_values[i][0].name} to {connected_values[i][1].name}',
                                 Screen.__FONTS['commands'])
                no_connected_arcs += 1
            else:
                self.__show_text(f'Do not connect {unconnected_values[i][0].name} to {unconnected_values[i][1].name} - forms cycle',
                                 Screen.__FONTS['commands'])
            self.__show_graph(i)
            self.__y_pos_to_blit += Screen.__Y_SPACES['questions']
            i+=1

        self.__show_text(Screen.__COMMANDS[5], Screen.__FONTS['commands'])
        self.__is_final = True
        self.__show_graph(i-1)
        self.__is_final = False
    
    def __show_graph(self, k=False):
        self.__y_pos_to_blit += 2*Screen.__RADIUS
        if k is not False:
            node_centres = [[(Screen.__RELATIVE_NODE_POSITIONS[str(len(self.__graph))][i][j]+1)*Screen.__Y_SPACES['questions']*8+Screen.__Y_SPACES['questions']*7-400
                             if j==0 else (Screen.__RELATIVE_NODE_POSITIONS[str(len(self.__graph))][i][j]+j)*Screen.__Y_SPACES['questions']*7-Screen.__Y_SPACES['questions']*7+self.__y_pos_to_blit
                             for j in range(2)] for i in range(len(self.__graph))] 
        else:  
            node_centres = [[(Screen.__RELATIVE_NODE_POSITIONS[str(len(self.__graph))][i][j]+1)*Screen.__Y_SPACES['questions']*8+Screen.__Y_SPACES['questions']*7-400
                             if j==0 else (Screen.__RELATIVE_NODE_POSITIONS[str(len(self.__graph))][i][j])*Screen.__Y_SPACES['questions']*7+self.__y_pos_to_blit+Screen.__RADIUS
                             for j in range(2)] for i in range(len(self.__graph))]
        self.__nodes = {self.__graph.nodes[i]:node_centres[i]
                        for i in range(len(node_centres))}
        self.__is_changed = False
        self.__connect_graph(k)
        for node in self.__nodes:
            pygame.draw.circle(Screen.__MID_SURFACE, Screen.__COLOURS['black'],
                               self.__nodes[node], Screen.__RADIUS, 1)
            self.__show_text(node.name, Screen.__FONTS['commands'],
                             Screen.__COLOURS['black'], Screen.__COLOURS['white'],
                             self.__nodes[node]) 

        Screen.__WIN.blit(Screen.__MID_SURFACE, (0, self.__y_position))
        self.__y_pos_to_blit += Screen.__RADIUS

    def __connect_graph(self, k):
        if k is False:
            arcs = self.__graph.arcs
        else:
            arcs = {self.__arc_list[i][0]:self.__arc_list[i][1] for i in range(k)}
        for arc in arcs:
            if arcs[arc]:
                start, end = self.__nodes[arcs[arc][0]], self.__nodes[arcs[arc][1]]
                pygame.draw.aaline(Screen.__MID_SURFACE, Screen.__COLOURS['black'],
                                   start, end, 1)
                self.__show_text(str(arc[0]), Screen.__FONTS['numbers'],
                                 Screen.__COLOURS['black'], Screen.__COLOURS['white'],
                                 ((start[0]+end[0])//2+(start[0]-end[0])//5,
                                  (start[1]+end[1])//2+(start[1]-end[1])//5), False)
        
        if k is not False:
            if self.__arc_list[k][1]:
                arcs = self.__arc_list
                start, end = self.__nodes[arcs[k][1][0]], self.__nodes[arcs[k][1][1]]
                if not self.__is_final:
                    colour = Screen.__COLOURS['red']
                else:
                    colour = Screen.__COLOURS['black']
            else:
                arcs = list(self.__graph.arcs.items())
                start, end = self.__nodes[arcs[k][1][0]], self.__nodes[arcs[k][1][1]]
                colour = Screen.__COLOURS['blue']
            pygame.draw.aaline(Screen.__MID_SURFACE, colour, start, end, 1)
            self.__show_text(str(arcs[k][0][0]), Screen.__FONTS['numbers'], colour,
                             Screen.__COLOURS['white'],
                             ((start[0]+end[0])//2+(start[0]-end[0])//5,
                              (start[1]+end[1])//2+(start[1]-end[1])//5), False)
        Screen.__WIN.blit(Screen.__MID_SURFACE, (0, self.__y_position))

    def __display_sorted_arcs(self):
        for arc in self.__graph.arcs:
            self.__y_pos_to_blit += Screen.__Y_SPACES['questions']
            self.__show_text(f'{self.__graph.arcs[arc][0].name+self.__graph.arcs[arc][1].name}:{arc[0]}',
                             Screen.__FONTS['commands'])

class Button:
    buttons = []

    def __init__(self, name, font, colours, width, height):
        self.__name = name
        self.__font = font
        self.__colours = colours
        self.__width = width
        self.__height = height
        self.__is_clicked = False
        self.__rect = None
        Button.buttons.append(self)
    
    @classmethod
    def unclick(cls):
        for button in Button.buttons:
            button.is_clicked = False

    @property
    def width(self):
        return self.__width
    
    @property
    def name(self):
        return self.__name

    @property
    def _is_clicked(self):
        return self.__is_clicked

    @_is_clicked.setter
    def is_clicked(self, value):
        self.__is_clicked = value
    
    def display(self, x_pos, y_pos, *surfaces):
        self.__rect = pygame.draw.rect(surfaces[0], self.__get_rect_colour(),
                                       (x_pos, y_pos, self.__width, self.__height))
        try:
            self.__show_text(self.__name, self.__font, self.__rect.center,
                             self.__colours['black'], *surfaces)
        except:
            self.__show_text(self.__name, self.__font, self.__rect.center,
                             self.__colours[list(self.__colours.keys())[0]], *surfaces)
        return self.__rect.y+self.__height
    
    def check_is_clicked(self, mouse_pos, y_change=False):
        if y_change:
            mouse_pos = list(mouse_pos)
            mouse_pos[1] -= y_change
            if (self.__rect.x-self.__width <= mouse_pos[0] <= self.__rect.x+self.__width
                and self.__rect.y-self.__height <= mouse_pos[1] <= self.__rect.y+self.__height):
                self.__is_clicked = True
                return True
        if self.__rect.collidepoint(mouse_pos):
            self.__is_clicked = True
            return True

    def __get_rect_colour(self):
        if self.__is_clicked:
            return self.__colours[list(self.__colours.keys())[1]]
        return self.__colours[list(self.__colours.keys())[2]]
    
    def __show_text(self, text, font, centre, text_colour, *surfaces):
        background_colour = self.__get_rect_colour()
        text = font.render(text, True, text_colour, background_colour)
        text_rect = text.get_rect()
        text_rect.center = centre
        self.__name_rect = text_rect
        surfaces[0].blit(text, self.__name_rect)
        self.__blit_layers(*surfaces)
        return text_rect.y + text_rect.height
    
    def __blit_layers(self, *surfaces):
        for i in range(len(surfaces)-1):
            surfaces[i+1].blit(surfaces[i], (0,0))
    
if __name__ == '__main__':
    gui = Screen()
