# Gatling Simulation Configuration

## 1. Dependencies and Libraries
The required classes from Gatling libraries are imported to create the simulation:
- `io.gatling.javaapi.core.*`
- `io.gatling.javaapi.http.*`

`CoreDsl` and `HttpDsl` are used to facilitate the creation of scenarios and HTTP requests.

## 2. HTTP Protocol

    HttpProtocolBuilder httpProtocol = http
        .baseUrl("https://videogamedb.uk/api")
        .acceptHeader("application/json");

## 3. Test Scenarios
Four different scenarios are defined, each with its own purpose and load pattern, all of this tests are based on gets from the databases:

### Test 1: Baseline Test

    ScenarioBuilder baselineTest = scenario("Baseline Test")
        .exec(http("Baseline test")
            .get("/videogame")
            .check(status().is(200)));

It checks that the server responds with a status code 200, indicating success.
This test is injected with 10 users simultaneously (atOnceUsers(10)).

### Test 2: High Concurrency Test


    ScenarioBuilder highConcurrencyTest = scenario("High Concurrency Test")
        .exec(http("High concurrency test")
            .get("/videogame")
            .check(status().is(200)));

Simulates a high load with 50 users over a period of 300 seconds (5 minutes).
The goal is to observe how the API handles multiple concurrent requests.

### Test 3: Long Duration Test

    ScenarioBuilder longDurationTest = scenario("Long Duration Test")
        .exec(http("Long duration test")
            .get("/videogame")
            .check(status().is(200)));

Simulates 10 users continuously per second for 900 seconds (15 minutes).
Evaluates how the API performs over a prolonged period under a moderate load.

### Test 4: Ramp-Up/Ramp-Down Test

    ScenarioBuilder rampUpRampDownTest = scenario("Ramp-Up/Ramp-Down Test")
        .exec(http("Ramp-Up/Ramp-Down test")
            .get("/videogame")
            .check(status().is(200)));

Simulates a scenario where the load gradually increases over 300 seconds (Ramp-Up) and then decreases over another 300 seconds (Ramp-Down).
This allows observing how the API handles gradual increases and decreases in load.

## 4. Set-Up Configuration
The setUp method defines how the tests will be executed:

    setUp(
        // Baseline Test Configuration
        baselineTest.injectOpen(atOnceUsers(10)),

        // High Concurrency Test Configuration
        highConcurrencyTest.injectOpen(rampUsers(50).during(300)),

        // Long Duration Test Configuration
        longDurationTest.injectOpen(constantUsersPerSec(10).during(900)),

        // Ramp-Up/Ramp-Down Test Configuration
        rampUpRampDownTest.injectOpen(
            rampUsers(10).during(300), // Ramp-Up
            rampUsers(10).during(300)  // Ramp-Down
        )
    ).protocols(httpProtocol);

Test 1 (Baseline Test): Injects 10 users simultaneously.
Test 2 (High Concurrency Test): Injects 50 users over a period of 300 seconds.
Test 3 (Long Duration Test): Executes 10 users per second for 900 seconds.
Test 4 (Ramp-Up/Ramp-Down Test): Gradually ramps up 10 users over 300 seconds and then ramps down 10 users over 300 seconds.

## 5. Summary of Tests
Baseline Test: Verifies that the endpoint works correctly with 10 simultaneous users.
High Concurrency Test: Simulates how the system handles 50 concurrent users over 5 minutes.
Long Duration Test: Evaluates system performance under a constant load over a long period.
Ramp-Up/Ramp-Down Test: Assesses how the system manages gradual increases and decreases in load.

## 6. How to use

To execute the tests you need to run the Engine.java this will automatically run the file since there is no more gatling configuration file.