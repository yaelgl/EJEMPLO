from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from agents3 import Car, TrafficLight, Parking, Obstacle
from model3 import CityModel

def agent_portrayal(agent):
    """
    Define cómo se visualizan los agentes en la cuadrícula.

    Params:
        agent (mesa.Agent): El agente a visualizar.

    Returns:
        dict: Un diccionario con las propiedades de visualización del agente.
    """
    if isinstance(agent, Car):
        portrayal = {"Shape": "circle",
                     "Color": "blue",
                     "Filled": "true",
                     "Layer": 3,
                     "r": 0.8}
    elif isinstance(agent, TrafficLight):
        color = "red" if agent.state == "red" else "green" if agent.state == "green" else "yellow"
        portrayal = {"Shape": "rect",
                     "Color": color,
                     "Filled": "true",
                     "Layer": 1,
                     "w": 1,
                     "h": 1}
    elif isinstance(agent, Parking):
        color = "gray" if agent.currentCars < agent.capacity else "orange"
        portrayal = {"Shape": "rect",
                     "Color": color,
                     "Filled": "true",
                     "Layer": 2,
                     "w": 1,
                     "h": 1}
    elif isinstance(agent, Obstacle):
        portrayal = {"Shape": "rect", 
                     "Color": "#5B9BD5", 
                     "Filled": "true", 
                     "Layer": 0, 
                     "w": 1, 
                     "h": 1}
    return portrayal

grid = CanvasGrid(agent_portrayal, 24, 24, 500, 500)

server = ModularServer(CityModel,
                       [grid],
                       "City Model",
                       {"numCars": 17, "gridWidth": 24, "gridHeight": 24, "startParkings": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17], "endParkings": [2, 3, 4, 5, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 2]})

server.port = 8080
server.launch()