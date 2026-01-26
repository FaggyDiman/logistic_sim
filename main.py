from os import environ
from tracemalloc import start

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import json

import pygame

import builder
import draws
from simState import weeks

towns = []
Screen, Clock = None, None
selected_town = None
cycles = 0

with open('constants.json', 'r') as f:
    CNST = json.load(f)


def askStartValues() -> bool:
    '''
    Prompts the user to choose whether to use default settings or input custom values for the simulation.
    
    :return: True if default settings are chosen, False otherwise
    :rtype: bool
    '''
    response = input("Do you want to start with default settings? (y/n): ").lower()

    if response == 'y':
        return True
    else:
        try:
            CNST['WIDTH'] = int(input("Enter the width of the surface (default 1250): ") or CNST['WIDTH'])
            CNST['HEIGHT'] = int(input("Enter the height of the surface (default 800): ") or CNST['HEIGHT'])
            CNST['TOWN_NUM'] = int(input("Enter the number of towns (default 32): ") or CNST['TOWN_NUM'])
            CNST['START_POPULATION'] = int(input("Enter the starting population for each town (default 1000): ") or CNST['START_POPULATION'])
            START_WAREHOUSE_FOOD = int(input("Enter the starting food in warehouse for each town (default 1000): ") or CNST['START_WAREHOUSE'][0])
            START_WAREHOUSE_GOODS = int(input("Enter the starting goods in warehouse for each town (default 0): ") or CNST['START_WAREHOUSE'][1])
            CNST['START_WAREHOUSE'] = [START_WAREHOUSE_FOOD, START_WAREHOUSE_GOODS]
            CNST['POP_CF'] = float(input("Enter the population starting deviation coefficient (default 0.15): ") or CNST['POP_CF'])
            print("Done! Starting simulation...")
        except ValueError:
            print("Invalid input. Using default settings.")
        return False

def StartNewSimulation() -> None:
    '''
    Initializes a new simulation (light-reset)
    
    :return: None
    '''
    global towns, Screen, Clock, selected_town, cycles, weeks

    towns = builder.initializeMap(CNST['TOWN_NUM'], CNST['START_POPULATION'], CNST['START_WAREHOUSE'], CNST['POP_CF'], CNST['WIDTH'], CNST['HEIGHT'], generation_type=4)
    if towns is None:
        print("Error: Could not generate a fully-connected map after multiple attempts.")
        exit(1)
    Screen, Clock = draws.createWindow(CNST['WIDTH'], CNST['HEIGHT'])
    cycles = 0
    weeks = 0
    selected_town = None

askStartValues()
StartNewSimulation()

running = True
### Start of main loop ###  
while running:
    
    Screen.fill((255, 255, 255))  
    draws.drawRoads(Screen, towns)
    draws.drawTowns(Screen, towns)
    draws.drawTurns(Screen, weeks)
    draws.drawSelectionBox(Screen, selected_town)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN: ## handle selection box
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for town in towns:
                if ((mouse_x - town.x) ** 2 + (mouse_y - town.y) ** 2) <= 16 ** 2:
                    selected_town = town
            
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_r: ##if key R pressed, restart simulation
                StartNewSimulation()
        elif event.type == pygame.VIDEORESIZE:
            Screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            

    pygame.display.flip()
    Clock.tick(60)
    cycles += 1

    if cycles%50 == 0:
        weeks += 1
### End of main loop ###