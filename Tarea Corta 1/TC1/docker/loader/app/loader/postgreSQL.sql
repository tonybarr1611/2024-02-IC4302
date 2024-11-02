-- Create the STATUS table
CREATE TABLE IF NOT EXISTS STATUS (
    statusId SERIAL PRIMARY KEY,
    status VARCHAR(255)
);

-- Create the CIRCUIT table
CREATE TABLE IF NOT EXISTS CIRCUIT (
    circuitId INTEGER PRIMARY KEY,
    circuitRef VARCHAR(32),
    name VARCHAR(128),
    location VARCHAR(255),
    country VARCHAR(255),
    lat Decimal(8,6),
    lng Decimal(9,6),
    alt INTEGER,
    url VARCHAR(255)
);

-- Create the SEASON table
CREATE TABLE IF NOT EXISTS SEASON (
    year INT PRIMARY KEY,
    url VARCHAR(255)
);

-- Create the CONSTRUCTOR table
CREATE TABLE IF NOT EXISTS CONSTRUCTOR (
    constructorId SERIAL PRIMARY KEY,
    constructorRef VARCHAR(32),
    name VARCHAR(64),
    nationality VARCHAR(64),
    url VARCHAR(128)
);

-- Create the DRIVER table
CREATE TABLE IF NOT EXISTS DRIVER (
    driverId SERIAL PRIMARY KEY,
    driverRef VARCHAR(64),
    assignedNumber VARCHAR(16),
    code VARCHAR(16),
    forename VARCHAR(64),
    surname VARCHAR(64),
    dob DATE,
    nationality VARCHAR(64),
    url VARCHAR(128)
);

-- Create the RACE table
CREATE TABLE IF NOT EXISTS RACE (
    raceId SERIAL PRIMARY KEY,
    year VARCHAR(4),
    round INT,
    circuitId INT REFERENCES CIRCUIT(circuitId),
    name VARCHAR(64),
    calendarDate VARCHAR(64),
    timeObtained VARCHAR(64),
    url VARCHAR(128),
    fp1_date VARCHAR(64),
    fp1_time VARCHAR(64),
    fp2_date VARCHAR(64),
    fp2_time VARCHAR(64),
    fp3_date VARCHAR(64),
    fp3_time VARCHAR(64),
    quali_date VARCHAR(64),
    quali_time VARCHAR(64),
    sprint_date VARCHAR(64),
    sprint_time VARCHAR(64)
);

-- Create the RESULT table
CREATE TABLE IF NOT EXISTS RESULT (
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

-- Create the CONSTRUCTOR_RESULT table
CREATE TABLE IF NOT EXISTS CONSTRUCTOR_RESULT (
    constructorResultId SERIAL PRIMARY KEY,
    raceId INT REFERENCES RACE(raceId),
    constructorId INT REFERENCES CONSTRUCTOR(constructorId),
    points INT,
    status VARCHAR(32)
);

-- Create the CONSTRUCTOR_STANDING table
CREATE TABLE IF NOT EXISTS CONSTRUCTOR_STANDING (
    constructorStandingId SERIAL PRIMARY KEY,
    raceId INT REFERENCES RACE(raceId),
    constructorId INT REFERENCES CONSTRUCTOR(constructorId),
    points INT,
    position INT,
    positionText VARCHAR(4),
    wins INT
);

-- Create the DRIVER_STANDING table
CREATE TABLE IF NOT EXISTS DRIVER_STANDING (
    driverStandingsId SERIAL PRIMARY KEY,
    raceId INT REFERENCES RACE(raceId),
    driverId INT REFERENCES DRIVER(driverId),
    points INT,
    position INT,
    positionText VARCHAR(4),
    wins INT
);

-- Create the LAP_TIME table
CREATE TABLE IF NOT EXISTS LAP_TIME (
    raceId INT REFERENCES RACE(raceId),
    driverId INT REFERENCES DRIVER(driverId),
    lap INT,
    position INT,
    timeObtained TIME,
    milliseconds VARCHAR(16),
    PRIMARY KEY (raceId, driverId, lap)
);

-- Create the PIT_STOP table
CREATE TABLE IF NOT EXISTS PIT_STOP (
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
CREATE TABLE IF NOT EXISTS QUALIFYING (
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

-- Create the SPRINT_RESULT table
CREATE TABLE IF NOT EXISTS SPRINT_RESULT (
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