# Este archivo contiene el código para el servidor de la simulación de tráfico.
# Autores: 
#       A01749581 Mariana Balderrábano Aguilar	
#       A01749898 Jennyfer Nahomi Jasso Hernández	
#       A01750338 Min Che Kim				
#       A01750911 Yael Michel García López		
# Fecha de creación: 20/11/2024
# Última modificación: 22/11/2024

import mesa
from model3 import CityModel
from flask import Flask, jsonify
from agents3 import Car

port = 8000

app = Flask(__name__, static_url_path='')

# Crea una instancia del modelo CityModel
cityModel = CityModel(
    numCars = 2,
    gridWidth = 24,
    gridHeight = 24,
    startParkings = [1,2],
    endParkings = [2,3]
    )

# Define la ruta GET (raíz)
@app.route('/', methods=['GET'])
def index():
    return jsonify({"mesage": "Hello world from CityModel"})

# Define la ruta GET / POST para obtener las posiciones de los autos
@app.route('/positions', methods=['GET', 'POST'])
def positions():
    carPaths = []

    for car in cityModel.schedule.agents:
        if isinstance(car, Car):
            carPaths.append({
                # f"path_{car.unique_id}": [{"x": pos[0], "z": pos[1]} for pos in car.getPath()]
                # })
                f"path": [{"x": pos[0], "z": pos[1]} for pos in car.getPath()]
                })
    
    return jsonify({"carPaths": carPaths})

# Define la ruta GET /path/<carId> para obtener la ruta de un auto específico
@app.route('/path/<int:carId>', methods=['GET'])
def getCarPath(carId):
    for car in cityModel.schedule.agents:
        if isinstance(car, Car) and car.unique_id == carId:
            carPath = [{"x": pos[0], "z": pos[1]} for pos in car.getPath()]
            return jsonify({f"path_{car.unique_id}": carPath})
    return jsonify({"error": "Car not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)

