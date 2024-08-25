-- Create the CIRCUIT table
CREATE TABLE CIRCUIT (
    circuitId SERIAL PRIMARY KEY,
    name VARCHAR(255),
    location VARCHAR(255),
    country VARCHAR(255)
);

-- Create the CONSTRUCTOR table
CREATE TABLE CONSTRUCTOR (
    constructorId SERIAL PRIMARY KEY,
    name VARCHAR(255),
    nationality VARCHAR(255)
);

-- Create the DRIVER table
CREATE TABLE DRIVER (
    driverId SERIAL PRIMARY KEY,
    driverRef VARCHAR(255),
    assignedNumber INT,
    code VARCHAR(3),
    forename VARCHAR(255),
    surname VARCHAR(255),
    dob DATE,
    nationality VARCHAR(255)
);

-- Create the RACE table
CREATE TABLE RACE (
    raceId SERIAL PRIMARY KEY,
    year INT,
    round INT,
    circuitId INT REFERENCES CIRCUIT(circuitId),
    name VARCHAR(255),
    date DATE,
    timeObtained TIME
);

-- Create the RESULT table
CREATE TABLE RESULT (
    resultId SERIAL PRIMARY KEY,
    raceId INT REFERENCES RACE(raceId),
    driverId INT REFERENCES DRIVER(driverId),
    constructorId INT REFERENCES CONSTRUCTOR(constructorId),
    grid INT,
    position INT,
    points DECIMAL(5,2),
    laps INT,
    statusId INT REFERENCES STATUS(statusId)
);

-- Create the STATUS table
CREATE TABLE STATUS (
    statusId SERIAL PRIMARY KEY,
    status VARCHAR(255)
);

-- Create the CONSTRUCTOR_RESULT table
CREATE TABLE CONSTRUCTOR_RESULT (
    constructorResultId SERIAL PRIMARY KEY,
    raceId INT REFERENCES RACE(raceId),
    constructorId INT REFERENCES CONSTRUCTOR(constructorId),
    points DECIMAL(5,2),
    status VARCHAR(255)
);

-- Create the CONSTRUCTOR_STANDING table
CREATE TABLE CONSTRUCTOR_STANDING (
    constructorStandingsId SERIAL PRIMARY KEY,
    raceId INT REFERENCES RACE(raceId),
    constructorId INT REFERENCES CONSTRUCTOR(constructorId),
    points DECIMAL(5,2),
    position INT
);

-- Create the DRIVER_STANDING table
CREATE TABLE DRIVER_STANDING (
    driverStandingsId SERIAL PRIMARY KEY,
    raceId INT REFERENCES RACE(raceId),
    driverId INT REFERENCES DRIVER(driverId),
    points DECIMAL(5,2),
    position INT
);

-- Create the LAP_TIME table
CREATE TABLE LAP_TIME (
    raceId INT REFERENCES RACE(raceId),
    driverId INT REFERENCES DRIVER(driverId),
    lap INT,
    position INT,
    timeObtained TIME,
    PRIMARY KEY (raceId, driverId, lap)
);

-- Create the PIT_STOP table
CREATE TABLE PIT_STOP (
    raceId INT REFERENCES RACE(raceId),
    driverId INT REFERENCES DRIVER(driverId),
    stop INT,
    lap INT,
    timeObtained TIME,
    duration VARCHAR(255),
    PRIMARY KEY (raceId, driverId, stop)
);

-- Create the QUALIFYING table
CREATE TABLE QUALIFYING (
    qualifyId SERIAL PRIMARY KEY,
    raceId INT REFERENCES RACE(raceId),
    driverId INT REFERENCES DRIVER(driverId),
    constructorId INT REFERENCES CONSTRUCTOR(constructorId),
    position INT,
    q1 TIME,
    q2 TIME,
    q3 TIME
);

-- Create the SEASON table
CREATE TABLE SEASON (
    year INT PRIMARY KEY,
    url VARCHAR(255)
);

-- Create the SPRINT_RESULT table
CREATE TABLE SPRINT_RESULT (
    sprintResultId SERIAL PRIMARY KEY,
    raceId INT REFERENCES RACE(raceId),
    driverId INT REFERENCES DRIVER(driverId),
    constructorId INT REFERENCES CONSTRUCTOR(constructorId),
    position INT,
    points DECIMAL(5,2),
    laps INT,
    statusId INT REFERENCES STATUS(statusId)
);

-- Load data into CIRCUIT table
COPY CIRCUIT(
    circuitId, 
    name, 
    location, 
    country
) FROM './data/circuits.csv'
DELIMITER ','
CSV HEADER;

-- Load data into CONSTRUCTOR table
COPY CONSTRUCTOR(
    constructorId, 
    name, 
    nationality
) FROM './data/constructors.csv'
DELIMITER ','
CSV HEADER;

-- Load data into DRIVER table
COPY DRIVER(
    driverId, 
    driverRef, 
    assignedNumber, 
    code, 
    forename, 
    surname, 
    dob, 
    nationality
) FROM './data/drivers.csv'
DELIMITER ','
CSV HEADER;

-- Load data into RACE table
COPY RACE(
    raceId, 
    year, 
    round, 
    circuitId, 
    name, 
    date, 
    timeObtained
) FROM './data/races.csv'
DELIMITER ','
CSV HEADER;

-- Load data into RESULT table
COPY RESULT(
    resultId, 
    raceId, 
    driverId, 
    constructorId, 
    grid, 
    position, 
    points, 
    laps, 
    statusId
) FROM './data/results.csv'
DELIMITER ','
CSV HEADER;

-- Load data into STATUS table
COPY STATUS(
    statusId, 
    status
) FROM './data/status.csv'
DELIMITER ','
CSV HEADER;

-- Load data into CONSTRUCTOR_RESULT table
COPY CONSTRUCTOR_RESULT(
    constructorResultId, 
    raceId, 
    constructorId, 
    points, 
    status
) FROM './data/constructor_results.csv'
DELIMITER ','
CSV HEADER;

-- Load data into CONSTRUCTOR_STANDING table
COPY CONSTRUCTOR_STANDING(
    constructorStandingsId, 
    raceId, 
    constructorId, 
    points, 
    position
) FROM './data/constructor_standings.csv'
DELIMITER ','
CSV HEADER;

-- Load data into DRIVER_STANDING table
COPY DRIVER_STANDING(
    driverStandingsId, 
    raceId, 
    driverId, 
    points, 
    position
) FROM './data/driver_standings.csv'
DELIMITER ','
CSV HEADER;

-- Load data into LAP_TIME table
COPY LAP_TIME(
    raceId, 
    driverId, 
    lap, 
    position, 
    timeObtained
) FROM './data/lap_times.csv'
DELIMITER ','
CSV HEADER;

-- Load data into PIT_STOP table
COPY PIT_STOP(
    raceId, 
    driverId, 
    stop, 
    lap, 
    timeObtained, 
    duration
) FROM './data/pit_stops.csv'
DELIMITER ','
CSV HEADER;

-- Load data into QUALIFYING table
COPY QUALIFYING(
    qualifyId, 
    raceId, 
    driverId, 
    constructorId, 
    position, 
    q1, 
    q2, 
    q3
) FROM './data/qualifying.csv'
DELIMITER ','
CSV HEADER;

-- Load data into SEASON table
COPY SEASON(
    year, 
    url
) FROM './data/seasons.csv'
DELIMITER ','
CSV HEADER;

-- Load data into SPRINT_RESULT table
COPY SPRINT_RESULT(
    sprintResultId, 
    raceId, 
    driverId, 
    constructorId, 
    position, 
    points, 
    laps, 
    statusId
) FROM './data/sprint_results.csv'
DELIMITER ','
CSV HEADER;
