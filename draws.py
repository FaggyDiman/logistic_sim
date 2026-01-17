import pygame
import pygame.gfxdraw

def createWindow(width: int, height: int) -> pygame.Surface:
    pygame.init()
    Clock = pygame.time.Clock()
    Screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption("Torgash")
    pygame.display.set_icon(pygame.image.load("icon.png"))
    Screen.fill((255, 255, 255))  
    return Screen, Clock

def drawTowns(Screen: pygame.Surface, towns: list) -> None | int:

    alive_towns = [town for town in towns if (town.isAlive and not town.isMain)]
    dead_towns = [town for town in towns if (not town.isAlive and not town.isMain)]
    main_hub = [town for town in towns if town.isMain]

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

    for town in main_hub:
        rect = pygame.Rect(town.x-10, town.y-10, 20, 20)
        pygame.draw.rect(Screen, (255, 215, 0), rect)

def drawRoads(Screen: pygame.Surface, towns: list) -> None:
    drawn_edges = set()

    for town in towns:
        for connected_town in town.roads:
            edge_id = frozenset((town, connected_town))
            if edge_id not in drawn_edges:
                pygame.gfxdraw.line(Screen, town.x, town.y, connected_town.x, connected_town.y, (122, 122, 122))
                drawn_edges.add(edge_id)
