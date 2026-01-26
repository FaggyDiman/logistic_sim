

def CalculatePaths(towns: list) -> None:
    '''
    Calculates paths for each town in the list of towns.
    
    :param towns: List of Town objects
    :type towns: list
    :return: None
    '''
    for town in towns:
        town.calculatePaths(towns)
