-- Create the CIRCUIT table
CREATE TABLE CIRCUIT (
    circuitId INTEGER PRIMARY KEY,
    circuitRef VARCHAR(32),
    name VARCHAR(128),
    location VARCHAR(255),
    country VARCHAR(255),
    latitude Decimal(8,6),
    longitude Decimal(9,6),
    altitude INTEGER
);

-- Create the CONSTRUCTOR table
CREATE TABLE CONSTRUCTOR (
    constructorId SERIAL PRIMARY KEY,
    constructorRef VARCHAR(32),
    name VARCHAR(64),
    nationality VARCHAR(64),
    url VARCHAR(128)
);

-- Create the DRIVER table
CREATE TABLE DRIVER (
    driverId SERIAL PRIMARY KEY,
    driverRef VARCHAR(64),
    assignedNumber INT,
    code VARCHAR(3),
    forename VARCHAR(64),
    surname VARCHAR(64),
    dob DATE,
    nationality VARCHAR(64),
    url VARCHAR(128)
);

-- Create the RACE table
CREATE TABLE RACE (
    raceId SERIAL PRIMARY KEY,
    year VARCHAR(4),
    round INT,
    circuitId INT REFERENCES CIRCUIT(circuitId),
    name VARCHAR(64),
    calendarDate DATE,
    timeObtained TIME,
    url VARCHAR(128),
    fp1_date DATE,
    fp1_time TIME,
    fp2_date DATE,
    fp2_time TIME,
    fp3_date DATE,
    fp3_time TIME,
    quali_date DATE,
    quali_time TIME,
    sprint_date DATE,
    sprint_time TIME
);


-- Create the RESULT table
CREATE TABLE RESULT (
    resultId SERIAL PRIMARY KEY,
    raceId INT REFERENCES RACE(raceId),
    driverId INT REFERENCES DRIVER(driverId),
    constructorId INT REFERENCES CONSTRUCTOR(constructorId),
    numberObtained INT,
    grid INT,
    position INT,
    positionText VARCHAR(2),
    positionOrder INT,
    points INT,
    laps INT,
    timeObtained VARCHAR(16),
    milliseconds VARCHAR(16),
    fastestLap VARCHAR(16),
    rank VARCHAR(2),
    fastestLapTime VARCHAR(16),
    fastestLapSpeed VARCHAR(16),
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
    points INT,
    status VARCHAR(32)
);

-- Create the CONSTRUCTOR_STANDING table
CREATE TABLE CONSTRUCTOR_STANDING (
    constructorStandingId SERIAL PRIMARY KEY,
    raceId INT REFERENCES RACE(raceId),
    constructorId INT REFERENCES CONSTRUCTOR(constructorId),
    points INT,
    position INT,
    positionText VARCHAR(4),
    wins INT
);

-- Create the DRIVER_STANDING table
CREATE TABLE DRIVER_STANDING (
    driverStandingsId SERIAL PRIMARY KEY,
    raceId INT REFERENCES RACE(raceId),
    driverId INT REFERENCES DRIVER(driverId),
    points INT,
    position INT,
    positionText VARCHAR(4),
    wins INT
);

-- Create the LAP_TIME table
CREATE TABLE LAP_TIME (
    raceId INT REFERENCES RACE(raceId),
    driverId INT REFERENCES DRIVER(driverId),
    lap INT,
    position INT,
    timeObtained TIME,
    milliseconds VARCHAR(16),
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
    milliseconds VARCHAR(16),
    PRIMARY KEY (raceId, driverId, stop)
);

-- Create the QUALIFYING table
CREATE TABLE QUALIFYING (
    qualifyId SERIAL PRIMARY KEY,
    raceId INT REFERENCES RACE(raceId),
    driverId INT REFERENCES DRIVER(driverId),
    constructorId INT REFERENCES CONSTRUCTOR(constructorId),
    assignedNumber INT,
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
    resultId SERIAL PRIMARY KEY,
    raceId INT REFERENCES RACE(raceId),
    driverId INT REFERENCES DRIVER(driverId),
    constructorId INT REFERENCES CONSTRUCTOR(constructorId),
    numberObtained INT,
    grid INT,
    position INT,
    positionText VARCHAR(4),
    positionOrder INT,
    points DECIMAL(5,2),
    laps INT,
    timeObtained VARCHAR(16),
    milliseconds VARCHAR(16),
    fastestLap VARCHAR(16),
    fastestLapTime VARCHAR(16),
    statusId INT REFERENCES STATUS(statusId)
);

-- Load data into CIRCUIT table
COPY CIRCUIT(
    circuitId,
    circuitRef,
    name,
    location,
    country,
    latitude,
    longitude,
    altitude
) FROM './data/circuits.csv'
DELIMITER ','
CSV HEADER;

-- Load data into CONSTRUCTOR table
COPY CONSTRUCTOR(
    constructorId,
    constructorRef,
    name,
    nationality,
    url
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
    nationality,
    url
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
    calendarDate,
    timeObtained,
    url,
    fp1_date,
    fp1_time,
    fp2_date,
    fp2_time,
    fp3_date,
    fp3_time,
    quali_date,
    quali_time,
    sprint_date,
    sprint_time
) FROM './data/races.csv'
DELIMITER ','
CSV HEADER;

-- Load data into RESULT table
COPY RESULT(
    resultId,
    raceId,
    driverId,
    constructorId,
    numberObtained,
    grid,
    position,
    positionText,
    positionOrder,
    points,
    laps,
    timeObtained,
    milliseconds,
    fastestLap,
    rank,
    fastestLapTime,
    fastestLapSpeed,
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
    constructorStandingId,
    raceId,
    constructorId,
    points,
    position,
    positionText,
    wins
) FROM './data/constructor_standings.csv'
DELIMITER ','
CSV HEADER;

-- Load data into DRIVER_STANDING table
COPY DRIVER_STANDING(
    driverStandingsId,
    raceId,
    driverId,
    points,
    position,
    positionText,
    wins
) FROM './data/driver_standings.csv'
DELIMITER ','
CSV HEADER;

-- Load data into LAP_TIME table
COPY LAP_TIME(
    raceId,
    driverId,
    lap,
    position,
    timeObtained,
    milliseconds
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
    duration,
    milliseconds
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
    resultId,
    raceId,
    driverId,
    constructorId,
    numberObtained,
    grid,
    position,
    positionText,
    positionOrder,
    points,
    laps,
    timeObtained,
    milliseconds,
    fastestLap,
    fastestLapTime,
    statusId
) FROM './data/sprint_results.csv'
DELIMITER ','
CSV HEADER;