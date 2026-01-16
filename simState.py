from builder import Town as Town

def CalculatePaths(towns: list) -> None:
    for town in towns:
        town.calculatePaths(towns)