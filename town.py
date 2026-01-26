from __future__ import annotations

class Town:
    '''
    Represents a town in the simulation with properties like population, warehouse, roads, etc.
    '''

    archetypes = ['Collector', 'Laissez-Faire', 'Basic']

    def __init__(self, name: str | int, population: int, warehouse: list, roads: list, road_count: int, x: int, y: int, isMain: bool, isAlive: bool, agentType: str) -> None:
        '''
        Initializes a Town object.
        
        :param name: Name or identifier of the town
        :param population: Population of the town
        :param warehouse: List of warehouse items
        :param roads: List of connected towns
        :param road_count: Number of roads
        :param x: X coordinate
        :param y: Y coordinate
        :param isMain: Whether this is the main town
        :param isAlive: Whether the town is alive
        :param agentType: Type of agent for the town
        '''
        self.name = name
        self.population = population
        self.warehouse = warehouse
        self.roads = roads
        self.road_count = road_count
        self.x = x
        self.y = y
        self.isMain = isMain
        self.isAlive = isAlive
        self.AgentType = agentType

    def __repr__(self) -> str:
        '''
        Returns a string representation of the town.
        
        :return: String representation
        '''
        return f"town{self.name}"

    def appendRoad(self, other_town: 'Town') -> None:
        '''
        Adds a road connection to another town if not already connected.
        
        :param other_town: The town to connect to
        :return: None
        '''
        if other_town in self.roads:
            return None
        self.roads.append(other_town)
        self.road_count += 1
        other_town.roads.append(self)
        other_town.road_count += 1

    def clearRoads(self) -> None:
        '''
        Removes all road connections from this town.
        
        :return: None
        '''
        for other in self.roads:
            other.roads.remove(self)
            other.road_count -= 1
        self.roads = []
        self.road_count = 0

    def removeRoad(self, other_town: 'Town') -> None:
        '''
        Removes the road connection to the specified town.
        
        :param other_town: The town to disconnect from
        :return: None
        '''
        if other_town in self.roads:
            self.roads.remove(other_town)
            self.road_count -= 1
            other_town.roads.remove(self)
            other_town.road_count -= 1
    
    def findRoute(self, towns: list):
        '''
        Find a route to the nearest Main town.
        
        :param towns: List of towns
        '''
        pass
        

    def calculateSaldo(self, towns: list):
        '''
        Placeholder for calculating saldo (not implemented).
        
        :param towns: List of towns
        '''
        pass

    def calculateFee(self):
        pass



def CalculatePaths(towns: list) -> None:
    '''
    Calculates paths for each town in the list of towns.
    
    :param towns: List of Town objects
    :type towns: list
    :return: None
    '''
    for town in towns:
        town.calculatePaths(towns)
