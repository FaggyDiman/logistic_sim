from builder import Town as Town

weeks = 0

def CalculatePaths(towns: list) -> None:
    for town in towns:
        town.calculatePaths(towns)
