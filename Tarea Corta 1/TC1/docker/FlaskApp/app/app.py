# Flask App for PostgreSQL
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/drivers", methods=['GET'])
def get_drivers():
    """
        SELECT   driverId,
                 driverRef,
                 assignedNumber,
                 code,
                 forename,
                 surname,
                 dob,
                 nationality,
                 url
                 
        FROM     DRIVER
        
        ORDER BY driverId;                 
    """
    return "<p>Drivers</p>"

@app.route("/constructors", methods=['GET'])
def get_constructors():
    """
        SELECT   constructorId,
                 constructorRef,
                 name,
                 nationality,
                 url
                 
        FROM     CONSTRUCTOR
        
        ORDER BY constructorId;                    
    """
    return "<p>Constructors</p>"

@app.route("/circuit/<int:id>/laps", methods=['GET'])
def get_laps(id):
    """
        SELECT   L.lapId,
                 L.driverId,
                 CONCAT(D.forename, ' ', D.surname) AS driverName,
                 D.code AS driverCode,
                 R.raceId,
                 R.name AS raceName,
                 R.year,
                 R.date,
                 L.lap,
                 L.position,
                 L.timeObtained,
                 L.milliseconds
        
        FROM     LAP L LEFT JOIN RACE R
                            on L.raceId = R.raceId
                        LEFT JOIN CIRCUIT C
                            on R.circuitId = C.circuitId
                        LEFT JOIN DRIVER D
                            on L.driverId = D.driverId
        
        WHERE    C.circuitId = id       
    """
    return "<p>Laps for circuit with id: " + str(id) + "</p>"

@app.route("/drivers/<int:id>/laps", methods=['GET'])
def get_laps_driver(id):
    """
        SELECT   L.lapId,
                 L.driverId,
                 CONCAT(D.forename, ' ', D.surname) AS driverName,
                 D.code AS driverCode,
                 R.raceId,
                 R.name AS raceName,
                 R.year,
                 R.date,
                 L.lap,
                 L.position,
                 L.timeObtained,
                 L.milliseconds
        
        FROM     LAP L LEFT JOIN RACE R
                          on L.raceId = R.raceId
                        LEFT JOIN DRIVER D
                            on L.driverId = D.driverId
        
        WHERE    L.driverId = id
    """
    return "<p>Laps for driver with id: " + str(id) + "</p>"

@app.route("/driver/<int:id>/total_races", methods=['GET'])
def get_total_races_driver(id):
    """
        SELECT   D.driverId,
                 D.forename,
                 D.surname,
                 D.code,
                 COUNT(DISTINCT R.raceId) AS totalRaces
        
        FROM     DRIVER D LEFT JOIN LAP L
                            on D.driverId = L.driverId
                          LEFT JOIN RACE R
                            on L.raceId = R.raceId
        
        WHERE    D.driverId = id
        
        GROUP BY D.driverId, D.forename, D.surname, D.code
    """

@app.route("/driver/<int:id>/pitstops", methods=['GET'])
def get_pitstops_driver(id):
    """
        SELECT   P.pitstopId,
                 P.driverId,
                 CONCAT(D.forename, ' ', D.surname) AS driverName,
                 D.code AS driverCode,
                 R.raceId,
                 R.name AS raceName,
                 R.year,
                 R.date,
                 P.lap,
                 P.stop,
                 P.time,
                 P.duration,
                 P.milliseconds
        
        FROM     PITSTOP P LEFT JOIN DRIVER D
                                on P.driverId = D.driverId
                           LEFT JOIN RACE R
                                on P.raceId = R.raceId
        
        WHERE    P.driverId = id
    """
    return "<p>Pitstops for driver with id: " + str(id) + "</p>"

if __name__ == "__main__":
    # Run on localhost:5000
    app.run(host='localhost', port=5000)
