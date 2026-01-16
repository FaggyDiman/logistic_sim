import pygame
import pygame.gfxdraw
from typing import List


def drawTowns(Screen: pygame.Surface, towns: list) -> None | int:

    alive_towns = [town for town in towns if town.isAlive]
    dead_towns = [town for town in towns if not town.isAlive]

    populations = [town.population for town in alive_towns]
    min_p = min(populations)
    max_p = max(populations)
    pop_range = max_p - min_p

    minimum_green = 100
    maximum_green = 255
    
    for town in alive_towns:
        if pop_range == 0:
            ratio = 1.0
        else:
            ratio = (town.population - min_p) / pop_range
        
        current_green = int(minimum_green + (maximum_green - minimum_green) * ratio)
        color = (0, current_green, 0)
        
        pygame.draw.circle(Screen, (0,0,0), (town.x, town.y), 12, 5)
        pygame.draw.circle(Screen, color, (town.x, town.y), 12, 4)
        pygame.draw.circle(Screen, (0,0,0), (town.x, town.y), 12, 1)
        pygame.draw.circle(Screen, color, (town.x, town.y), 3)

    for town in dead_towns:

        pygame.draw.circle(Screen, (0,0,0), (town.x, town.y), 12, 1)

def drawRoads(Screen: pygame.Surface, towns: list) -> None:
    drawn_edges = set()

    for town in towns:
        for connected_town in town.roads:
            edge_id = frozenset((town, connected_town))
            if edge_id not in drawn_edges:
                pygame.gfxdraw.line(Screen, town.x, town.y, connected_town.x, connected_town.y, (122, 122, 122))
                drawn_edges.add(edge_id)
