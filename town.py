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
    
    def findRoute(self, towns: list) -> list['Town'] | None:
        '''
        Finds the best route to the main town considering both distance and taxes.
        Uses Dijkstra's algorithm to minimize total cost = distance_cost + tax_cost.
        Distance cost: 1 product per 5 pixels
        Tax cost: tax_rate * product volume (where tax_rate depends on town's AgentType)
        
        :param towns: List of all towns in the map
        :return: List of towns representing the path from self to main town, or None if no path exists
        '''
        import math
        import heapq
        
        # Find the main town
        main_town = None
        for town in towns:
            if town.isMain:
                main_town = town
                break
        
        if main_town is None or self == main_town:
            return [self] if self.isMain else None
        
        # Tax rates based on AgentType
        def get_tax_rate(town: 'Town') -> float:
            if town.AgentType == 'Collector':
                return 0.9
            elif town.AgentType == 'Laissez-Faire':
                return 0.1
            elif town.AgentType == 'Basic':
                return 0.4
            else:
                return 0.5
        
        # Calculate cost between two connected towns
        def calculate_cost(from_town: 'Town', to_town: 'Town') -> float:
            distance = math.hypot(to_town.x - from_town.x, to_town.y - from_town.y)
            distance_cost = distance / 5.0
            tax_cost = get_tax_rate(to_town)
            return distance_cost + tax_cost
        
        # Dijkstra's algorithm
        distances = {town: float('infinity') for town in towns}
        distances[self] = 0
        previous = {town: None for town in towns}
        pq = [(0, id(self), self)]
        visited = set()
        
        while pq:
            current_dist, _, current_town = heapq.heappop(pq)
            
            if current_town in visited:
                continue
            
            visited.add(current_town)
            
            if current_town == main_town:
                break
            
            if current_dist > distances[current_town]:
                continue
            
            for neighbor in current_town.roads:
                if neighbor in visited:
                    continue
                
                cost = calculate_cost(current_town, neighbor)
                new_distance = distances[current_town] + cost
                
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current_town
                    heapq.heappush(pq, (new_distance, id(neighbor), neighbor))
        
        # Reconstruct path
        if distances[main_town] == float('infinity'):
            return None
        
        path = []
        current = main_town
        while current is not None:
            path.append(current)
            current = previous[current]
        
        path.reverse()
        return path
        

    def calculateSaldo(self, towns: list):
        '''
        Placeholder for calculating saldo (not implemented).
        
        :param towns: List of towns
        '''
        pass