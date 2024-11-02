import io.gatling.javaapi.core.*;
import io.gatling.javaapi.http.*;
import static io.gatling.javaapi.core.CoreDsl.*;
import static io.gatling.javaapi.http.HttpDsl.*;
import static io.gatling.javaapi.http.HttpDsl.http;
import static io.gatling.javaapi.http.HttpDsl.status;
import java.util.Random;

public class DatabasePerformanceSimulation extends Simulation {

    HttpProtocolBuilder httpProtocol = http
            .baseUrl("http://localhost:63614")
            .acceptHeader("application/json");

    private String getRandomApiEndpoint() {
        String[] endpoints = {
                "/drivers", // API 1: Obtain drivers
                "/constructors", // API 2: Obtain constructors
                "/circuits", // API 3: Obtain laps by circuit
                "/races" // API 4: Obtain laps by driver
        };

        // Selects a random endpoint
        Random random = new Random();
        int randomIndex = random.nextInt(endpoints.length); // get a random index
        return endpoints[randomIndex]; // return the random endpoint
    }

    // Test 1: (Baseline Test)
    ScenarioBuilder baselineTest = scenario("Baseline Test")
            .exec(session -> {
                // Get a random API endpoint
                String randomEndpoint = getRandomApiEndpoint();

                // Save the random endpoint in the session
                return session.set("randomEndpoint", randomEndpoint);
            })
            .exec(http("Random API Call")
                    .get(session -> session.getString("randomEndpoint")) // Get the random endpoint from the session
                    .check(status().is(200)));

    // Test 2: (High Concurrency Test)
    ScenarioBuilder highConcurrencyTest = scenario("High Concurrency Test")
            .exec(session -> {
                // Get a random API endpoint
                String randomEndpoint = getRandomApiEndpoint();

                // Save the random endpoint in the session
                return session.set("randomEndpoint", randomEndpoint);
            })
            .exec(http("Random API Call")
                    .get(session -> session.getString("randomEndpoint")) // Get the random endpoint from the session
                    .check(status().is(200)));

    // Test 3: (Long Duration Test)
    ScenarioBuilder longDurationTest = scenario("Long Duration Test")
            .exec(session -> {
                // Get a random API endpoint
                String randomEndpoint = getRandomApiEndpoint();

                // Save the random endpoint in the session
                return session.set("randomEndpoint", randomEndpoint);
            })
            .exec(http("Random API Call")
                    .get(session -> session.getString("randomEndpoint")) // Get the random endpoint from the session
                    .check(status().is(200)));

    // Test 4: (Ramp-Up/Ramp-Down Test)
    ScenarioBuilder rampUpRampDownTest = scenario("Ramp-Up/Ramp-Down Test")
            .exec(session -> {
                // Get a random API endpoint
                String randomEndpoint = getRandomApiEndpoint();
                System.out.println("Calling API: " + randomEndpoint); // Opcional: Para debugging

                // Save the random endpoint in the session
                return session.set("randomEndpoint", randomEndpoint);
            })
            .exec(http("Random API Call")
                    .get(session -> session.getString("randomEndpoint")) // Get the random endpoint from the session
                    .check(status().is(200)));

    {
        setUp(
                // Configuration of Test 1: Baseline Test
                baselineTest.injectOpen(atOnceUsers(10)),

                // Configuration of Test 2: High Concurrency Test
                highConcurrencyTest.injectOpen(rampUsers(50).during(300)),

                // Configuration of Test 3: Long Duration Test
                longDurationTest.injectOpen(constantUsersPerSec(10).during(900)),

                // Configuration of Test 4: Ramp-Up/Ramp-Down Test
                rampUpRampDownTest.injectOpen(
                        rampUsers(10).during(300), // Ramp-Up
                        rampUsers(10).during(300) // Ramp-Down
                )).protocols(httpProtocol);
    }
}
