from __future__ import annotations
import math
import heapq  
import json
from traffic import increment_traffic, get_all_traffic

try:
    with open('constants.json', 'r') as f:
        CNST = json.load(f)
except Exception:
    CNST = {}

ROAD_EXHAUSTION = CNST.get('ROAD_EXHAUSTION', 1.0)
TOLL_MAP = {
    'Laissez-Faire': 0.05,
    'Basic': 0.15,
    'Collector': 0.30
}

class Town:
    '''
    Represents a town in the simulation with properties like population, warehouse, roads, etc.
    '''
    archetypes = ['Collector', 'Laissez-Faire', 'Basic']

    def __init__(self, name: str | int, population: int, warehouse: list, roads: list, road_count: int, x: int, y: int, isMain: bool, isAlive: bool, agentType: str) -> None:
        self.name = name
        self.population = population
        # warehouse[0] = Food, warehouse[1] = Goods (Production)
        self.warehouse = warehouse 
        self.roads = roads
        self.road_count = road_count
        self.x = x
        self.y = y
        self.isMain = isMain
        self.isAlive = isAlive
        self.AgentType = agentType

    def __repr__(self) -> str:
        return f"Town<{self.name}>"

    def appendRoad(self, other_town: 'Town') -> None:
        if other_town in self.roads:
            return
        self.roads.append(other_town)
        self.road_count += 1
        other_town.roads.append(self)
        other_town.road_count += 1

    def removeRoad(self, other_town: 'Town') -> None:
        if other_town in self.roads:
            self.roads.remove(other_town)
            self.road_count -= 1
            other_town.roads.remove(self)
            other_town.road_count -= 1

    def find_best_route_to_main(self):
        '''
        Finds the most profitable route to the nearest Main town using Dijkstra's algorithm.
        We maximize: (StartingGoods - TravelCost - Tolls).
        Since Dijkstra finds minima, we minimize (TotalCost).

        :return: (main_town, path_of_towns, fees_list) or (None, None, None)
        '''
        if self.isMain:
            # If this town is the main hub, there's no route to find; keep return arity consistent
            return None, [], [], 0.0

        # Priority Queue: (current_cost, current_town_id, current_town, path_list)
        # We store the town's id as the second tuple element so Python won't try to compare Town objects when costs tie
        pq = [(0, id(self), self, [])] 
        
        visited_costs = {self: 0} # Minimum cost to reach each town
        best_main_route = None
        min_total_cost = float('inf')

        while pq:
            cost, _, current, path = heapq.heappop(pq)

            # If we found a Main town
            if current.isMain:
                if cost < min_total_cost:
                    min_total_cost = cost
                    best_main_route = (current, path + [current])
                # Don't stop here; there may be another main town or a cheaper path
                continue
            
            # If the current path is already more expensive than the best found, skip this branch
            if cost >= min_total_cost:
                continue

            # Check neighbors
            for neighbor in current.roads:
                # 1. Travel cost
                dist = math.hypot(neighbor.x - current.x, neighbor.y - current.y)
                travel_cost = dist * ROAD_EXHAUSTION
                
                # 2. Toll (if neighbor is not Main and not the start, it charges a toll for passing through it)
                # Note: Toll is usually charged on entry. Main town does not charge (we sell there).
                toll_cost = 0
                if not neighbor.isMain:
                    rate = TOLL_MAP.get(neighbor.AgentType, 0)
                    toll_cost = self.warehouse[1] * rate

                new_cost = cost + travel_cost + toll_cost

                if neighbor not in visited_costs or new_cost < visited_costs[neighbor]:
                    visited_costs[neighbor] = new_cost
                    # Add the neighbor to the path
                    heapq.heappush(pq, (new_cost, id(neighbor), neighbor, path + [current]))

        if best_main_route:
            main_town, final_path = best_main_route
            # Build list of payments for execute_trade
            # Path looks like [Start, A, B, Main]. We pay A and B.
            fees_to_pay = [] 
            
            # Skip Start (self), take all intermediate towns
            for town in final_path[1:-1]: 
                rate = TOLL_MAP.get(town.AgentType, 0)
                amount = int(self.warehouse[1] * rate)
                if amount > 0:
                    fees_to_pay.append((town, amount))

            # Compute total travel cost (road expenses only) along the final path
            travel_cost = 0.0
            for i in range(len(final_path) - 1):
                a = final_path[i]
                b = final_path[i + 1]
                travel_cost += math.hypot(b.x - a.x, b.y - a.y) * ROAD_EXHAUSTION

            return main_town, final_path, fees_to_pay, travel_cost
        
        return None, None, None, None

    def execute_trade(self):
        '''
        Full cycle: find route -> traverse path -> pay tolls on entry -> increase traffic on each segment -> apply travel costs -> sell remaining goods.
        '''
        if self.warehouse[1] <= 0:
            return 

        target_main, path, fees, travel_cost = self.find_best_route_to_main()

        if not target_main:
            return 

        # fee map for quick lookup by town
        fee_map = {town: amount for town, amount in fees}

        # Goods currently carried
        goods = self.warehouse[1]

        # Traverse path edge by edge. We increment traffic on each edge by the amount of goods
        # that pass that segment. Upon arrival to each intermediate town we pay its fee (if any).
        for i in range(len(path) - 1):
            a = path[i]
            b = path[i + 1]

            # increment traffic for edge a<->b by current carried goods
            increment_traffic(a, b, int(goods))

            # arrive at b — if b charges a toll, pay from carried goods
            if b in fee_map:
                amt = min(fee_map[b], goods)
                if amt > 0:
                    b.warehouse[1] += amt
                    goods -= amt
                    self.warehouse[1] -= amt
                    if goods <= 0:
                        # nothing left to continue the trip
                        self.warehouse[1] = 0
                        return

        # After traversing, deduct travel cost from remaining goods
        deduct = int(travel_cost)
        if goods <= deduct:
            self.warehouse[1] = 0
            return
        goods -= deduct
        self.warehouse[1] = goods

        # Final sale at the main market
        goods_to_sell = goods
        if goods_to_sell > 0:
            target_main.warehouse[1] += goods_to_sell
            self.warehouse[1] = 0 

            # Town receives payment in food (exchange)
            exchange_rate = CNST.get('PAYMENT_CF', 1.5)
            food_received = goods_to_sell * exchange_rate
            self.warehouse[0] += food_received
            

    def produceGoods(self):
        produced = int(self.population * CNST.get('PRODUCTION_CF', 1))
        self.warehouse[1] += produced

    def consumeFood(self):
        consumed = int(self.population * CNST.get('HUNGER_CF', 1))
        self.warehouse[0] -= consumed

    def deathfromHunger(self):
        if self.warehouse[0] < 0:
            hunger_deficit = abs(self.warehouse[0])
            lost_population = int(hunger_deficit / CNST.get('HUNGER_CF', 1))
            
            self.population -= lost_population
            self.warehouse[0] = 0 
            
            if self.population <= 0:
                self.population = 0
                self.isAlive = False
    
    def clearRoads(self) -> None:
        for other in list(self.roads): 
            other.roads.remove(self)
            other.road_count -= 1
        self.roads = []
        self.road_count = 0