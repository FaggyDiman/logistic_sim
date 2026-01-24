'''
Draws module
'''
import pygame
import pygame.gfxdraw

from builder import Town


def createWindow(width: int, height: int) -> pygame.Surface:
    '''
    creates a pygame Surface to work with
    
    :param width: Width of the window
    :type width: int
    :param height: Height of the window
    :type height: int
    :return: pygame.Surface
    :rtype: Surface
    '''
    pygame.init()
    Clock = pygame.time.Clock()
    Screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption("Torgash")
    pygame.display.set_icon(pygame.image.load("icon.png"))
    Screen.fill((255, 255, 255))  
    return Screen, Clock

def drawTowns(Screen: pygame.Surface, towns: list) -> None:
    '''
    Draws every town from the list
    
    :param Screen: Surface to draw onto
    :type Screen: pygame.Surface
    :param towns: List of towns
    :type towns: list
    :return: None 
    '''

    alive_towns = [town for town in towns if (town.isAlive and not town.isMain)]
    dead_towns = [town for town in towns if (not town.isAlive and not town.isMain)]
    main_hub = [town for town in towns if town.isMain]

    populations = [town.population for town in alive_towns]
    min_p = min(populations)
    max_p = max(populations)
    pop_range = max_p - min_p

    minimum_green = 100
    maximum_green = 255
    minimum_red = 100
    maximum_red = 255
    minimum_blue = 100
    maximum_blue = 255
    
    for town in alive_towns:
        if pop_range == 0:
            ratio = 1.0
        else:
            ratio = (town.population - min_p) / pop_range
        
        if town.AgentType == 'Basic':
            current_intensity = int(minimum_green + (maximum_green - minimum_green) * ratio)
            color = (0, current_intensity, 0)
        elif town.AgentType == 'Collector':
            current_intensity = int(minimum_red + (maximum_red - minimum_red) * ratio)
            color = (current_intensity, 0, 0)
        elif town.AgentType == 'Laissez-Faire':
            current_intensity = int(minimum_blue + (maximum_blue - minimum_blue) * ratio)
            color = (0, 0, current_intensity)
        else:
            color = (0, int(minimum_green + (maximum_green - minimum_green) * ratio), 0)  # default to green
        
        pygame.draw.circle(Screen, (0,0,0), (town.x, town.y), 10, 5)
        pygame.draw.circle(Screen, color, (town.x, town.y), 10, 4)
        pygame.draw.circle(Screen, (0,0,0), (town.x, town.y), 10, 1)

        if town.AgentType == 'Collector':
            pygame.draw.circle(Screen, (255, 0, 0), (town.x, town.y), 2)

        if town.AgentType == 'Laissez-Faire':
            pygame.draw.circle(Screen, (0, 0, 255), (town.x, town.y), 2)

        if town.AgentType == 'Basic':
            pygame.draw.circle(Screen, (0, 255, 0), (town.x, town.y), 2)

    for town in dead_towns:

        pygame.draw.circle(Screen, (0,0,0), (town.x, town.y), 12, 1)

    for town in main_hub:
        rect = pygame.Rect(town.x-10, town.y-10, 20, 20)
        pygame.draw.rect(Screen, (255, 215, 0), rect)

def drawRoads(Screen: pygame.Surface, towns: list) -> None:
    '''
    Draws roads between connected towns.
    
    :param Screen: Surface to draw onto
    :type Screen: pygame.Surface
    :param towns: List of towns
    :type towns: list
    :return: None
    '''
    drawn_edges = set()

    for town in towns:
        for connected_town in town.roads:
            edge_id = frozenset((town, connected_town))
            if edge_id not in drawn_edges:
                pygame.gfxdraw.line(Screen, town.x, town.y, connected_town.x, connected_town.y, (122, 122, 122))
                drawn_edges.add(edge_id)

def drawTurns(Screen: pygame.Surface, cycles: int) -> None: #draw simulation turns counter
    '''
    Draws the simulation turns counter on the screen.
    
    :param Screen: Surface to draw onto
    :type Screen: pygame.Surface
    :param cycles: Number of simulation cycles/turns
    :type cycles: int
    :return: None
    '''
    font = pygame.font.SysFont(None, 16)
    turns_text = font.render(f'Turns: {cycles}', True, (0, 0, 0))
    Screen.blit(turns_text, (10, 10))

def drawSelectionBox(Screen: pygame.Surface, selected_town: Town) -> None:
    '''
    Draws a selection box around the selected town.
    
    :param Screen: Surface to draw onto
    :type Screen: pygame.Surface
    :param selected_town: The currently selected town
    :type selected_town: Town
    :return: None
    '''
    if selected_town:
        pygame.draw.circle(Screen, (0, 0, 0), (selected_town.x, selected_town.y), 16, 2)