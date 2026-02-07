'''
Draws selection highlights and info box
'''

import pygame
from src.town import Town


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

def drawInfoBox(Screen: pygame.Surface, selected_town: Town) -> None:
    '''
    Draws an info box with details about the selected town.
    
    :param Screen: Surface to draw onto
    :type Screen: pygame.Surface
    :param selected_town: The currently selected town
    :type selected_town: Town
    :return: None
    '''
    if selected_town:
        font = pygame.font.SysFont(None, 18)
        info_lines = [
            f"Population: {selected_town.population}",
            f"Warehouse Food: {selected_town.warehouse[0]}",
            f"Agent Type: {selected_town.AgentType}"
        ]
        for i, line in enumerate(info_lines):
            text = font.render(line, True, (0, 0, 0))
            Screen.blit(text, (10, 20 + i * 30))

def drawRoute(Screen: pygame.Surface, route: list) -> None:
    '''
    Draws highlight route from a town to the main hub.
    Red line for the full path, yellow line for the trade route to the main city.
    :param Screen: Surface to draw onto
    :param route: List of towns representing the route
    '''
    if route and len(route) > 1:
        for i in range(len(route) - 1):
            pygame.draw.line(Screen, (255, 0, 0), (route[i].x, route[i].y), (route[i+1].x, route[i+1].y), 3)
        
        for i in range(len(route) - 1):
            pygame.draw.line(Screen, (255, 255, 0), (route[i].x, route[i].y), (route[i+1].x, route[i+1].y), 1)