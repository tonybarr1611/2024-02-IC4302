CREATE TABLE STATUS (
    statusId VARCHAR(128) PRIMARY KEY,
    status VARCHAR(255)
);

CREATE TABLE CIRCUIT (
    circuitId VARCHAR(128) PRIMARY KEY,
    circuitRef VARCHAR(255),
    name VARCHAR(255),
    location VARCHAR(255),
    country VARCHAR(255),
    lat FLOAT,
    lng FLOAT,
    alt VARCHAR(128),
    url VARCHAR(255)
);

CREATE TABLE SEASON (
    year VARCHAR(128) PRIMARY KEY,
    url VARCHAR(255)
);

CREATE TABLE CONSTRUCTOR (
    constructorId VARCHAR(128) PRIMARY KEY,
    constructorRef VARCHAR(255),
    name VARCHAR(255),
    nationality VARCHAR(255),
    url VARCHAR(255)
);

CREATE TABLE DRIVER (
    driverId INT, PRIMARY KEY,
    driverRef VARCHAR(255),
    assignedNumber VARCHAR(255),
    code VARCHAR(255),
    forename VARCHAR(255),
    surname VARCHAR(255),
    dob VARCHAR(255),
    nationality VARCHAR(255),
    url VARCHAR(255)
);

CREATE TABLE RACE (
    raceId INT PRIMARY KEY,
    year VARCHAR(128),
    round VARCHAR(128),
    circuitId VARCHAR(128),
    name VARCHAR(255),
    calendarDate VARCHAR(255),
    timeObtained VARCHAR(255),
    url VARCHAR(255),
    fp1_date VARCHAR(255),
    fp1_time VARCHAR(255),
    fp2_date VARCHAR(255),
    fp2_time VARCHAR(255),
    fp3_date VARCHAR(255),
    fp3_time VARCHAR(255),
    quali_date VARCHAR(255),
    quali_time VARCHAR(255),
    sprint_date VARCHAR(255),
    sprint_time VARCHAR(255),
    FOREIGN KEY (circuitId) REFERENCES CIRCUIT(circuitId)
);

CREATE TABLE CONSTRUCTOR_RESULT (
    constructorResultId VARCHAR(128) PRIMARY KEY,
    raceId INT,
    constructorId VARCHAR(128),
    points VARCHAR(128),
    status VARCHAR(255),
    FOREIGN KEY (raceId) REFERENCES RACE(raceId),
    FOREIGN KEY (constructorId) REFERENCES CONSTRUCTOR(constructorId)
);

CREATE TABLE CONSTRUCTOR_STANDING (
    constructorStandingsId VARCHAR(128) PRIMARY KEY,
    raceId INT,
    constructorId VARCHAR(128),
    points VARCHAR(128),
    position VARCHAR(128),
    positionText VARCHAR(128),
    wins VARCHAR(128),
    FOREIGN KEY (raceId) REFERENCES RACE(raceId),
    FOREIGN KEY (constructorId) REFERENCES CONSTRUCTOR(constructorId)
);

CREATE TABLE DRIVER_STANDING (
    driverStandingsId VARCHAR(128) PRIMARY KEY,
    raceId INT,
    driverId INT,
    points VARCHAR(128),
    position VARCHAR(128),
    positionText VARCHAR(128),
    wins VARCHAR(128),
    FOREIGN KEY (raceId) REFERENCES RACE(raceId),
    FOREIGN KEY (driverId) REFERENCES DRIVER(driverId)
);


CREATE TABLE LAP_TIME (
    raceId INT,
    driverId INT,
    lap INT,
    position INT,
    timeObtained VARCHAR(64),
    milliseconds VARCHAR(16),
    PRIMARY KEY (raceId, driverId, lap),
    FOREIGN KEY (raceId) REFERENCES RACE(raceId),
    FOREIGN KEY (driverId) REFERENCES DRIVER(driverId)
);

CREATE TABLE PIT_STOP (
    raceId INT,
    driverId INT,
    stop VARCHAR(128),
    lap VARCHAR(128),
    timeObtained VARCHAR(255),
    duration VARCHAR(56),
    milliseconds VARCHAR(128),
    PRIMARY KEY (raceId, driverId, stop),
    FOREIGN KEY (raceId) REFERENCES RACE(raceId),
    FOREIGN KEY (driverId) REFERENCES DRIVER(driverId)
);

CREATE TABLE QUALIFYING (
    qualifyId VARCHAR(128) PRIMARY KEY,
    raceId INT,
    driverId INT,
    constructorId VARCHAR(128),
    assignedNumber VARCHAR(128),
    position VARCHAR(128),
    q1 VARCHAR(255),
    q2 VARCHAR(255),
    q3 VARCHAR(255),
    FOREIGN KEY (raceId) REFERENCES RACE(raceId),
    FOREIGN KEY (driverId) REFERENCES DRIVER(driverId),
    FOREIGN KEY (constructorId) REFERENCES CONSTRUCTOR(constructorId)
);


CREATE TABLE RESULT (
    resultId VARCHAR(128) PRIMARY KEY,
    raceId INT,
    driverId INT,
    constructorId VARCHAR(128),
    assignedNumber VARCHAR(128),
    grid VARCHAR(128),
    position VARCHAR(128),
    positionText VARCHAR(128),
    positionOrder VARCHAR(128),
    points VARCHAR(128),
    laps VARCHAR(128),
    timeObtained VARCHAR(255),
    milliseconds VARCHAR(128),
    fastestLap VARCHAR(128),
    rank VARCHAR(128),
    fastestLapTime VARCHAR(255),
    fastestLapSpeed VARCHAR(56),
    statusId VARCHAR(128),
    FOREIGN KEY (raceId) REFERENCES RACE(raceId),
    FOREIGN KEY (driverId) REFERENCES DRIVER(driverId),
    FOREIGN KEY (constructorId) REFERENCES CONSTRUCTOR(constructorId)
);

CREATE TABLE SPRINT_RESULT (
    resultId VARCHAR(128) PRIMARY KEY,
    raceId INT,
    driverId INT,
    constructorId VARCHAR(128),
    assignedNumber VARCHAR(128),
    grid VARCHAR(128),
    position VARCHAR(128),
    positionText VARCHAR(128),
    positionOrder VARCHAR(128),
    points VARCHAR(128),
    laps VARCHAR(128),
    timeObtained VARCHAR(255),
    milliseconds VARCHAR(128),
    fastestLap VARCHAR(128),
    fastestLapTime VARCHAR(255),
    statusId VARCHAR(128),
    FOREIGN KEY (raceId) REFERENCES RACE(raceId),
    FOREIGN KEY (driverId) REFERENCES DRIVER(driverId),
    FOREIGN KEY (constructorId) REFERENCES CONSTRUCTOR(constructorId)
);