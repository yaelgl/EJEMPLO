# Este archivo contiene el modelo de la simulación de la ciudad.
# Un auto recorre la ciudad desde un estacionamiento hasta otro, evitando obstáculos y respetando los semáforos.
# Autores: 
#       A01749581 Mariana Balderrábano Aguilar	
#       A01749898 Jennyfer Nahomi Jasso Hernández	
#       A01750338 Min Che Kim				
#       A01750911 Yael Michel García López		
# Fecha de creación: 14/11/2024
# Última modificación: 22/11/2024

import mesa
from agents3 import Car, TrafficLight, Parking, Obstacle
from directions3 import getDirections

class CityModel(mesa.Model):
    """
    Clase que representa el modelo de la simulación del recorrido de un auto para llegar 
    de un estacionamiento a otro
    """

    def __init__(self, numCars, gridWidth, gridHeight, startParkings, endParkings):
        """
        Inicializa el modelo de la simulación.
        
        Params:
            numCars (int): Número de autos en la simulación.
            gridWidth (int): Ancho de la cuadrícula.
            gridHeight (int): Altura de la cuadrícula.
            startParkings (list): Lista con los números estacionamientos de inicio de los autos.
            endParkings (list): Lista con los números estacionamientos de destino de los autos.
        """
        super().__init__()
        self.numCars = numCars
        self.grid = mesa.space.MultiGrid(gridWidth, gridHeight, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True
        self.carsInDest = 0
        # Crear un diccionario de direcciones
        self.directions = getDirections()

        # Posiciones de los semáforos
        trafficLightsPos = [
            # Rojo
            (8, 23), (8, 22),
            (8, 18), (8, 17),
            (17, 9), (17, 8),
            (2, 5), (2, 4),
            (5, 1), (5, 0),
            # Verde
            (6, 21), (7, 21),
            (6, 16), (7, 16),
            (18, 7), (19, 7),
            (0, 6), (1, 6),
            (6, 2), (7, 2)
        ]

        # Posiciones de los estacionamientos
        parkingsPos = [
            (2, 14),
            (3, 21),
            (3, 6),
            (4, 12),
            (4, 3),
            (5, 17),
            (8, 15),
            (9, 2),
            (10, 19),
            (10, 12),
            (10, 7),
            (17, 21),
            (17, 6),
            (17, 4),
            (20, 18),
            (20, 15),
            (20, 4)
        ]

        # Direcciones de salida de los estacionamientos
        self.parkingsDirections = {
            (2, 14): ["left"],    # Estacionamiento 1
            (3, 21): ["up"],      # Estacionamiento 2
            (3, 6): ["down"],     # Estacionamiento 3
            (4, 12): ["down"],    # Estacionamiento 4
            (4, 3): ["up"],       # Estacionamiento 5
            (5, 17): ["right"],   # Estacionamiento 6
            (8, 15): ["left"],    # Estacionamiento 7
            (9, 2): ["down"],     # Estacionamiento 8
            (10, 19): ["down"],   # Estacionamiento 9
            (10, 12): ["down"],   # Estacionamiento 10
            (10, 7): ["up"],      # Estacionamiento 11
            (17, 21): ["up"],     # Estacionamiento 12
            (17, 6): ["right"],   # Estacionamiento 13
            (17, 4): ["right"],   # Estacionamiento 14
            (20, 18): ["down"],   # Estacionamiento 15
            (20, 15): ["up"],     # Estacionamiento 16
            (20, 4): ["left"]     # Estacionamiento 17
        }

        # Direcciones de entrada a los estacionamientos
        self.parkingEntry = {
            (1, 14): ["right"],    # Estacionamiento 1
            (3, 22): ["down"],      # Estacionamiento 2
            (3, 5): ["up"],     # Estacionamiento 3
            (4, 11): ["up"],    # Estacionamiento 4
            (4, 4): ["down"],       # Estacionamiento 5
            (6, 17): ["left"],   # Estacionamiento 6
            (7, 15): ["right"],    # Estacionamiento 7
            (9, 1): ["up"],     # Estacionamiento 8
            (10, 18): ["up"],  # Estacionamiento 9
            (10, 11): ["up"],   # Estacionamiento 10
            (10, 8): ["down"],      # Estacionamiento 11
            (17, 22): ["down"],     # Estacionamiento 12
            (18, 6): ["left"],   # Estacionamiento 13
            (18, 4): ["left"],   # Estacionamiento 14
            (20, 17): ["up"],   # Estacionamiento 15
            (20, 16): ["down"],     # Estacionamiento 16
            (19, 4): ["right"]     # Estacionamiento 17
        }

        # Crear y colocar semáforos en la cuadrícula
        for i, pos in enumerate(trafficLightsPos):
            initialState = "red" if i < 10 else "green"
            trafficLight = TrafficLight(i, self, pos, initialState)
            self.schedule.add(trafficLight)
            self.grid.place_agent(trafficLight, pos)

        totalParkings = len(parkingsPos)
        baseCapacity = numCars // totalParkings
        extraCapacity = numCars % totalParkings
        
        # Crear y colocar estacionamientos en la cuadrícula
        for i, pos in enumerate(parkingsPos):
            capacity = baseCapacity + (1 if i < extraCapacity else 0)
            parking = Parking(i, self, pos, capacity)
            self.schedule.add(parking)
            self.grid.place_agent(parking, pos)

        # Definir las posiciones de los obstáculos (edificios y glorietas)
        cuadros = [
            {"x": 2, "y": 12, "width": 4, "height": 10},
            {"x": 8, "y": 19, "width": 4, "height": 3},
            {"x": 8, "y": 12, "width": 4, "height": 5},
            {"x": 16, "y": 18, "width": 6, "height": 4},
            {"x": 16, "y": 12, "width": 6, "height": 4},
            {"x": 2, "y": 6, "width": 4, "height": 2},
            {"x": 2, "y": 2, "width": 4, "height": 2},
            {"x": 8, "y": 6, "width": 4, "height": 2},
            {"x": 8, "y": 2, "width": 4, "height": 2},
            {"x": 16, "y": 2, "width": 2, "height": 6},
            {"x": 20, "y": 2, "width": 2, "height": 6},
            {"x": 13, "y": 9, "width": 2, "height": 2},
        ]

        # Convertir las posiciones de los obstáculos en una lista de tuplas
        self.obstaclePos = [(x, y) for cuadro in cuadros for x in range(cuadro["x"], cuadro["x"] + cuadro["width"]) for y in range(cuadro["y"], cuadro["y"] + cuadro["height"])]

        # Crear y colocar obstáculos en la cuadrícula
        for i, pos in enumerate(self.obstaclePos):
            barrier = Obstacle(i, self, pos)
            self.schedule.add(barrier)
            self.grid.place_agent(barrier, pos)
        
        # Crear y colocar autos en la cuadrícula si numCars es mayor que 0
        if self.numCars > 0:
            for i in range(self.numCars):
                if i < len(startParkings) and i < len(endParkings):
                    start = startParkings[i] - 1
                    end = endParkings[i] - 1
                    if start < len(parkingsPos) and end < len(parkingsPos):
                        start = parkingsPos[start]
                        end = parkingsPos[end]
                        # carsAgent = Car(len(trafficLightsPos) + len(parkingsPos) + len(self.obstaclePos) + i, 
                        #                 self, parkingsPos[start-1], parkingsPos[end-1])
                        carsAgent = Car(len(trafficLightsPos) + len(parkingsPos) + len(self.obstaclePos) + i, 
                                        self, start, end)
                        self.schedule.add(carsAgent)
                        self.grid.place_agent(carsAgent, carsAgent.now)

                        startParking = [agent for agent in self.schedule.agents if isinstance(agent, Parking) and agent.pos == start][0]
                        if startParking.addCar():
                            print(f"El auto {carsAgent.unique_id} se estacionó en el estacionamiento {startParking.unique_id + 1}")
                        else:
                            print(f"El estacionamiento {startParking.unique_id + 1} está lleno")
        
    def nearestParking(self, currentPos):
        """
        Encuentra el estacionamiento disponible más cercano.

        Params:
            currentPos (tuple): La posición actual del auto.

        Returns:
            tuple: La posición del estacionamiento disponible más cercano
        """       
        minDist = float('inf')
        nearest = None

        for parking in [agent for agent in self.schedule.agents if isinstance(agent, Parking)]:
            if parking.currentCars < parking.capacity:
                distance = abs(parking.pos[0] - currentPos[0]) + abs(parking.pos[1] - currentPos[1])
                if distance < minDist:
                    minDist = distance
                    nearest = parking.pos
        #print(f"Nearest: {nearest}")
        return nearest
    
    def availability(self):
        """Disponibilidad de cada estacionamiento"""
        for parking in [agent for agent in self.schedule.agents if isinstance(agent, Parking)]:
            print(f"Estacionamiento {parking.unique_id + 1}: {parking.currentCars}/{parking.capacity}")
   
    def step(self):
        """
        Avanza la simulación un paso en el tiempo.
        """
        if self.carsInDest == self.numCars:
            self.running = False 
        else:
            for agent in self.schedule.agents:
                if isinstance(agent, TrafficLight):
                    agent.changeState()
                elif isinstance(agent, Car):
                    if agent.pos == agent.dest:
                        self.carsInDest += 1
            #self.availability()
        self.schedule.step()