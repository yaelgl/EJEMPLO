# Este programa contiene las clases de los agentes que se utilizan en la simulación de la ciudad.   
# Autores: 
#       A01749581 Mariana Balderrábano Aguilar	
#       A01749898 Jennyfer Nahomi Jasso Hernández	
#       A01750338 Min Che Kim				
#       A01750911 Yael Michel García López		
# Fecha de creación: 14/11/2024
# Última modificación: 22/11/2024

import mesa, heapq

class Parking(mesa.Agent):
    """Clase que representa un estacionamiento"""
    def __init__(self, uniqueId, model, pos, capacity) -> None:
        """
        Agente que representa un estacionamiento
        
        Params:
            uniqueId (int): Identificador único del agente.
            model (CityModel): El modelo al que pertenece el agente.
            pos (tuple): La posición del estacionamiento en la cuadrícula.
            capacity (int): La capacidad del estacionamiento.
        """
        super().__init__(uniqueId, model)
        self.pos = pos
        self.capacity = capacity
        self.currentCars = 0
    
    def addCar(self):
        """Añade un coche al estacionamienro si hay espacio disponible"""
        if self.currentCars < self.capacity:
            self.currentCars += 1
            return True
        return False
    
    def removeCar(self):
        """Disminuye el cupo (capacidad) cuando el carro sale del estacionamiento"""
        if self.currentCars > 0:
            self.currentCars -= 1

class TrafficLight(mesa.Agent):
    """Clase que representa un semáforo"""
    def __init__(self, uniqueId, model, pos, initialState) -> None:
        """
        Agente que representa un semáforo
        
        Params:
            uniqueId (int): Identificador único del agente.
            model (CityModel): El modelo al que pertenece el agente.
            pos (tuple): La posición del semáforo en la cuadrícula.
            initialState (str): El estado inicial del semáforo.
        """
        super().__init__(uniqueId, model)
        self.pos = pos
        self.state = initialState
        self.step_count = -1

    def changeState(self):
        """Cambia el estado del semáforo"""        
        self.step_count += 1
        
        if self.state == "green" and self.step_count >= 5:
            self.state = "yellow"
            self.step_count = 0
        elif self.state == "yellow" and self.step_count >= 2:
            self.state = "red"
            self.step_count = 0
        elif self.state == "red" and self.step_count >= 5:
            self.state = "green"
            self.step_count = 0

class Car(mesa.Agent):
    """
    Clase que representa un automóvil.
    """

    def __init__(self, unique_id, model, parkingNow, parkingDest) -> None:
        """
        Agente que representa un auto
        
        Params:
            unique_id (int): Identificador único del agente.
            model (CityModel): El modelo al que pertenece el agente.
            parkingNow (tuple): La posición inicial del auto (estacionamiento de origen).  
            parkingDest (tuple): La posición de destino del auto (estacionamiento de destino).
        """
        super().__init__(unique_id, model)
        self.now = parkingNow
        self.dest = parkingDest
        self.pos = self.now
        self.path = self.calculatePath(self.now, self.dest, model.directions)
        self.left = False

    def move(self):
        """
        Mueve el automóvil a la siguiente posición, dependiendo de las condiciones de su entorno.
        """
        if self.path is None or len(self.path) == 0:
            return
        
        nextPos = self.path[1]

        if nextPos == self.dest:
            destParking = [agent for agent in self.model.grid.get_cell_list_contents([self.dest]) if isinstance(agent, Parking)][0]
            if destParking.currentCars < destParking.capacity:
                destParking.addCar()
                self.model.grid.remove_agent(self)
                self.path = None
                print(f"El coche {self.unique_id} se ha estacionado en el estacionamiento {destParking.unique_id + 1}")
            else:
                print(f"El coche {self.unique_id} no encontró espacio en {self.dest}. Buscando otro estacionamiento.")
                newDest = self.model.nearestParking(self.pos)
                if newDest:
                    self.dest = newDest
                    self.path = self.calculatePath(self.pos, self.dest, self.model.directions)
                    print(f"El coche {self.unique_id} nuevo path: {self.path}")
                else:
                    print(f"El coche {self.unique_id} no encontró estacionamiento.")
            return
        else:
            if self.path is None:
                return
            else:
                nextPos = self.path[1]
                
                # Verifica si hay un semáforo en la siguiente posición
                for agent in self.model.grid.get_cell_list_contents([nextPos]):
                    if isinstance(agent, TrafficLight):
                        if agent.state == "red":
                            return

                # Mover el auto si no hay otro auto en la siguiente posición
                if not any(isinstance(agent, Car) for agent in self.model.grid.get_cell_list_contents([nextPos])):
                    self.leaveParking()
                    self.model.grid.move_agent(self, nextPos)
                    self.pos = nextPos
                    self.path = self.path[1:]
                else:
                    self.waiting = True
    

    def calculatePath(self, initial, dest, directions):
        """
        Calcula el camino que debe de seguir el auto para llegar a su destino, respetando las direcciones de cada celda.

        Params:
            initial (tuple): La posición inicial del auto.
            dest (tuple): La posición de destino del auto.
            directions (dict): Diccionario de direcciones posibles desde cada celda.

        Returns:
            list: Lista de posiciones que componen el camino desde initial hasta dest.
        """
        queue = []
        heapq.heappush(queue, (0, initial))
        costs = {initial: 0}
        paths = {initial: []}

        while queue:
            currentCost, currentPos = heapq.heappop(queue)
            if currentPos == dest:
                return paths[currentPos] + [dest]

            # Obtener las direcciones posibles desde la posición actual
            possible_directions = directions.get(currentPos, [])
            if currentPos in self.model.parkingsDirections:
                for direction in self.model.parkingsDirections[currentPos]:
                    if direction not in possible_directions:
                        possible_directions.append(direction)

            if currentPos in self.model.parkingEntry:
                for direction in self.model.parkingEntry[currentPos]:
                    if direction not in possible_directions:
                        possible_directions.append(direction)

            for direc in possible_directions:
                if direc == "up":
                    newPos = (currentPos[0], currentPos[1] + 1)
                elif direc == "down":
                    newPos = (currentPos[0], currentPos[1] - 1)
                elif direc == "left":
                    newPos = (currentPos[0] - 1, currentPos[1])
                elif direc == "right":
                    newPos = (currentPos[0] + 1, currentPos[1])

                newCost = currentCost + 1

                if newPos not in costs or newCost < costs[newPos]:
                    costs[newPos] = newCost
                    paths[newPos] = paths[currentPos] + [currentPos]
                    heapq.heappush(queue, (newCost, newPos))
        
        return None 

    def step(self):
        """Avanza un paso en la simulación"""
        self.move()
    
    def getPath(self):
        """Regresa la ruta calculada del coche"""
        return self.path
    
    def leaveParking(self):
        """Cuando el carro sale del estacionamiento"""
        if not self.left:
            startParking = [agent for agent in self.model.grid.get_cell_list_contents([self.now]) if isinstance(agent, Parking)][0]
            startParking.removeCar()
            self.left = True


class Obstacle(mesa.Agent):
    """
    Clase que representa obstáculos en el mapa (edificios y glorietas)
    """
    def __init__(self, unique_id, model, pos) -> None:
        """
        Inicializa un nuevo obstáculo.

        Params:
            unique_id (int): Identificador único del agente.
            model (CityModel): El modelo al que pertenece el agente.
            pos (tuple): La posición del obstáculo en la cuadrícula.
        """
        super().__init__(unique_id, model)
        self.pos = pos