from __future__ import annotations
import math
from numpy import average
import pygame
import pygame.gfxdraw
import random
import json


with open('constants.json', 'r') as f:
    CNST = json.load(f)

class Town:
    def __init__(self, name: str | int, population: int, warehouse: list, roads: list, road_count: int, x: int, y: int, isMain: bool, isAlive: bool) -> None:
        self.name = name
        self.population = population
        self.warehouse = warehouse
        self.roads = roads
        self.road_count = road_count
        self.x = x
        self.y = y
        self.isMain = isMain
        self.isAlive = isAlive

    def __repr__(self) -> str:
        return f"town{self.name}"
    
    def appendRoad(self, other_town: Town) -> None:
        if other_town in self.roads:
            return None
        self.roads.append(other_town)
        self.road_count += 1
        other_town.roads.append(self)
        other_town.road_count += 1

    def clearRoads(self) -> None:
        for other in self.roads:
            other.roads.remove(self)
            other.road_count -= 1
        self.roads = []
        self.road_count = 0

    def removeRoad(self, other_town: Town) -> None:
        if other_town in self.roads:
            self.roads.remove(other_town)
            self.road_count -= 1
            other_town.roads.remove(self)
            other_town.road_count -= 1

def initializeTowns(num_towns: int, start_population: int, start_warehouse: list, pop_cf: float, width: int, height: int) -> list:
    towns = []
    for town in range(num_towns):
        name = town
        population = int(start_population + start_population * random.uniform(pop_cf, -pop_cf))
        warehouse = start_warehouse.copy()
        roads = []
        attempts = 0
        isAlive = True
        road_count = 0
        while attempts < 100:
            x = random.randint(0, width)
            y = random.randint(0, height)
            valid = True
            for other in towns:
                if abs(x - other.x) < CNST['NB_ZONE_TOWN'] or abs(y - other.y) < CNST['NB_ZONE_TOWN']:
                    valid = False
                    break
            if x < CNST['NB_ZONE_BORDER'] or x > width - CNST['NB_ZONE_BORDER'] or y < CNST['NB_ZONE_BORDER'] or y > height - CNST['NB_ZONE_BORDER']:
                valid = False
            if valid:
                break
            attempts += 1
        if attempts >= 100:
            return None  # Failed to place towns without overlap
        isMain = (town == 0)
        towns.append(Town(name, population, warehouse, roads, road_count, x, y, isMain, isAlive))
    return towns
    
def drawTowns(Screen: pygame.Surface, towns: list) -> None | int:

    alive_towns = [town for town in towns if town.isAlive]
    
    if not alive_towns:
        return 0

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

def createWindow(width: int, height: int) -> pygame.Surface:
    pygame.init()
    Clock = pygame.time.Clock()
    Screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption("Torgash")
    pygame.display.set_icon(pygame.image.load("icon.png"))
    Screen.fill((255, 255, 255))  
    return Screen, Clock

def initializeRoads(towns: list, generation_type: int) -> None:
    '''
    Initializing roads between towns
    
    :param towns: List of towns (Town objects)
    :type towns: list
    :param generation_type: 1 — random, 2 — hubs, 3 — one line
    :type generation_type: int
    '''
    min_road_quantity = len(towns) + 2
    max_road_quantity = int(len(towns) * 1.3)

    def checkForConnectivity(towns: list) -> bool:
        visited = set()

        def dfs(town: Town):
            visited.add(town)
            for neighbor in town.roads:
                if neighbor not in visited:
                    dfs(neighbor)

        dfs(towns[0])
        return len(visited) == len(towns)
    
    def checkForIntersection(p1, p2, p3, p4):

        def cp(o, a, b):
            return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

        check1 = cp(p1, p2, p3) * cp(p1, p2, p4) < 0
        check2 = cp(p3, p4, p1) * cp(p3, p4, p2) < 0

        return check1 and check2
    
    def noAnyIntersections(towns: list) -> bool:
        ''' Check if any roads intersect '''
        edges = []
        seen = set()

        for t1 in towns:
            for t2 in t1.roads:
                edge_id = frozenset((t1, t2))
                if edge_id not in seen:
                    seen.add(edge_id)
                    edges.append((t1, t2))

        for i, (a1, a2) in enumerate(edges):
            p1 = (a1.x, a1.y)
            p2 = (a2.x, a2.y)

            for b1, b2 in edges[i + 1:]:

                if {a1, a2} & {b1, b2}:
                    continue

                p3 = (b1.x, b1.y)
                p4 = (b2.x, b2.y)

                if checkForIntersection(p1, p2, p3, p4):
                    return False

        return True

    def checkDistance(px, py, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        denom = dx * dx + dy * dy
        if denom == 0:
            distance = math.hypot(px - x1, py - y1)
        else:
            t = ((px - x1) * dx + (py - y1) * dy) / denom
            t = max(0.0, min(1.0, t))  
            nx = x1 + t * dx
            ny = y1 + t * dy
            distance = math.hypot(px - nx, py - ny)
        if distance <= CNST['NB_ZONE_ROAD']:
            return True
        else:
            return False

    def checkMaxLength(town1: Town, town2: Town) -> bool:
        distance = math.hypot(town1.x - town2.x, town1.y - town2.y)
        if distance <= CNST['MAX_ROAD_LENGTH']:
            return True
        else:
            return False

    match generation_type:
        case 1:  # Random 
            attempts = 0
            total_roads = 0
            road_quantity = random.randint(min_road_quantity, max_road_quantity)
            while attempts < 100000000:
                attempts += 1
                print('Attempting road generation, attempt number:', attempts)
                if total_roads >= road_quantity and checkForConnectivity(towns) and noAnyIntersections(towns):
                    break
                else:
                    for town in towns:
                        town.clearRoads()
                    total_roads = 0
                    for town in towns:
                        attemps_create_road = 0
                        if road_quantity - total_roads >= 8:
                            potential_roads = random.randint(1, 4)
                        else:
                            potential_roads = random.randint(1, 3)
                        while (len(town.roads) < potential_roads):
                            other_town = random.choice(towns)
                            if other_town != town and other_town not in town.roads:
                                town.appendRoad(other_town)
                                total_roads += 1    

                    delete_random = random.randint(3, min_road_quantity // 2)
                    for _ in range(delete_random):
                        town = random.choice(towns)
                        if town.roads:
                            town.removeRoad(random.choice(town.roads))

                    for town in towns:
                        for other in towns:
                            if other != town:
                                for under_check_town in towns:
                                    if under_check_town != town and under_check_town != other:
                                        if checkDistance(under_check_town.x, under_check_town.y, town.x, town.y, other.x, other.y):
                                            town.removeRoad(other)
                                            
        case 2:  # Hubs
            # To be implemented
            pass
        case 3:  # One line
            # To be implemented
            pass
    return None

def drawRoads(Screen: pygame.Surface, towns: list) -> None:
    drawn_edges = set()

    for town in towns:
        for connected_town in town.roads:
            edge_id = frozenset((town, connected_town))
            if edge_id not in drawn_edges:
                pygame.gfxdraw.line(Screen, town.x, town.y, connected_town.x, connected_town.y, (122, 122, 122))
                drawn_edges.add(edge_id)