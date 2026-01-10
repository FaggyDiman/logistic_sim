from math import e
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import random
import builder
import json

with open('constants.json', 'r') as f:
    CNST = json.load(f)


def askStartValues() -> bool:
    response = input("Do you want to start with default settings? (y/n): ").lower()

    if response == 'y':
        return True
    else:
        try:
            CNST['WIDTH'] = int(input("Enter the width of the surface (default 1200): ") or CNST['WIDTH'])
            CNST['HEIGHT'] = int(input("Enter the height of the surface (default 800): ") or CNST['HEIGHT'])
            CNST['TOWN_NUM'] = int(input("Enter the number of towns (default 12): ") or CNST['TOWN_NUM'])
            CNST['START_POPULATION'] = int(input("Enter the starting population for each town (default 1000): ") or CNST['START_POPULATION'])
            START_WAREHOUSE_FOOD = int(input("Enter the starting food in warehouse for each town (default 1000): ") or CNST['START_WAREHOUSE'][0])
            START_WAREHOUSE_GOODS = int(input("Enter the starting goods in warehouse for each town (default 0): ") or CNST['START_WAREHOUSE'][1])
            CNST['START_WAREHOUSE'] = [START_WAREHOUSE_FOOD, START_WAREHOUSE_GOODS]
            CNST['POP_CF'] = float(input("Enter the population starting deviation coefficient (default 0.1): ") or CNST['POP_CF'])
            print("Done! Starting simulation...")
        except ValueError:
            print("Invalid input. Using default settings.")
        return False


askStartValues()
towns = builder.initializeTowns(CNST['TOWN_NUM'], CNST['START_POPULATION'], CNST['START_WAREHOUSE'], CNST['POP_CF'], CNST['WIDTH'], CNST['HEIGHT'])
if towns is None:
    print("Error: Could not place towns with the given parameters.")
    exit(1)
builder.initializeRoads(towns, generation_type=1)
Screen, Clock = builder.createWindow(CNST['WIDTH'], CNST['HEIGHT'])

cycles = 0
running = True
while running:
    
    Screen.fill((255, 255, 255))  
    builder.drawRoads(Screen, towns)
    builder.drawTowns(Screen, towns)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.VIDEORESIZE:
            Screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            

    pygame.display.flip()
    Clock.tick(60)
    cycles += 1
### End of main loop ###