# Proyecto 1 - IC4302 Bases de Datos II

## Introduction
Following is the documentation for 'Proyecto 1' of the course IC4302 - Databases II.
This project assignment focuses on developing an application that integrates multiple technologies, including MariaDB, Elasticsearch, RabbitMQ, and the Hugging Face API. The application is designed to handle various tasks such as loading and processing datasets, generating text embeddings, and interacting with these databases. To optimize performance, the system includes caching using Memcached, and it is instrumented with Prometheus to monitor critical metrics such as HTTP request counts, query response times, object processing times, and cache efficiency.

The application is deployed in a Kubernetes environment using Helm Charts, ensuring scalability, manageability, and observability. Each component is containerized using Docker, packaging only the necessary dependencies and database interactions. For performance evaluation, the system collects Prometheus metrics and displays them on Grafana dashboards, enabling real-time monitoring and analysis of the system's performance under different workloads.

Additionally, a React-based UI is implemented, allowing users to interact with the system in a user-friendly way. The UI supports functionality such as user registration and login, submitting prompts to query songs using vector search on Elasticsearch, and interacting with friends through a social feed. Users can search for song-related prompts, follow friends, and manage their profiles and posts. The UI is deployed as a Kubernetes Deployment and exposed via NodePort for external access. The UI interacts with the backend API to perform various tasks, such as querying the database, processing text, and caching results.

## Team Members
- Victor Aymerich
- Anthony Barrantes
- Fabricio Solis 
- Melanie Wong
- Pavel Zamora 

Next up, you will find the requirements to run the application, the steps to execute it, testing examples and the recommendations and conclusions we have gathered from the homework.
## Requirements

The requirements for the project are the following:

* Create an user in [DockerHub](https://hub.docker.com/)
* Install [Docker Desktop](https://docs.docker.com/desktop/install/windows-install/), if you are using MacOS, please make sure you select the right installer for your CPU architecture.
* Open Docker Desktop, go to **Settings > Kubernetes** and enable Kubernetes.
![K8s](./images/docker-desktop-k8s.png "K8s Docker Desktop")
* Install [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-macos/)
* Install [Helm](https://helm.sh/docs/intro/install/)
* Install [Visual Studio Code](https://code.visualstudio.com/)
* Install [Lens](https://k8slens.dev/)


## Building the docker images

There is a script to build the docker images, to execute it in a bash shell execute:

```bash
cd ./TC1/docker
./build.sh nereo08
```

Change **nereo08** to your DockerHub username

Please take a look on the script contents to make sure you understand what is done under the hood.
This script will build the images for the components of the homework, including the database, the API, the cache, and the monitoring components.

## Helm Charts

### Configure

* Open the file **TC1/charts/app/values.yaml**
* Replace **nereo08** by your DockerHub username

```yaml
config:
  docker_registry: nereo08
```

### Install

Execute:

```bash
cd ./TC1/charts
./install.sh
```

Here we are installing the components in the Kubernetes cluster. The script will install the databases, the API, the cache, the backend and fronted, plus the monitoring components. It is important to have the DockerHub username set correctly in the script to ensure the correct components are installed.

### Uninstall

Execute:

```bash
cd ./TC1/charts
./uninstall.sh
```

This script will uninstall the components from the Kubernetes cluster. It is important to have the DockerHub username set correctly in the script to ensure the correct components are removed.

## Access Debug Pod

```bash
# copy the name that says debug from the following command
kubectl get pods
# then replace debug-844bb45d6f-9jt45 by that name
kubectl exec --stdin --tty debug-844bb45d6f-9jt45 -- /bin/bash
```
In case you need to access the debug pod to check the logs or execute some commands, you can use the previous command to access it.


# How to Test

To test the whole project together, you can follow the next steps:
First you need to do the build and install steps, in this time you have to choose the components that will be used for this you have to change in TC1\charts\app\values.yaml, after that to verify that the project is working correctly you can follow the next steps:

- Check Docker images are running, you can check this in the Docker Desktop application. In this area it is important to check the different images, you can check the logs of the images to see if there are any errors. You should check the logs of the S3 Crawler, Backend API, Hugging Face API, Ingest, the MariaDB, Memcached, Prometheus, and Grafana images. You can check the logs of the images by clicking on the image and then clicking on the logs button. Y


- After that you can check in Lens that the pods are running correctly, here you can check the logs of the pods to see if there are any errors and the status of the pods.


- Once you have checked all the logs and the data is being processed correctly, you can consider to go to Grafana to see the metrics of the project. To do this you should forward the port of the Grafana service called **grafana-deployment** to you local machine. From here you can access the Grafana dashboards by going to http://localhost: (Port you decide) and logging in with the credentials **admin** and the password found in the GF_SECURITY_ADMIN_PASSWORD variable which can be found while observing the logs of the Grafana pod.


- Once you enter Grafana, you can see various dashboards displaying metrics for different components of the project. The databases being monitored include MariaDB, Elasticsearch, and Memcached, all of which are critical to the system's performance. These metrics provide insights into the behavior and efficiency of the databases and caching systems. Additionally, each of the Python components, such as the Hugging Face API, S3 Crawler, Backend API and Ingest service, have dedicated dashboards that track their respective metrics. These include the number of requests, object processing times, and error rates, providing full visibility into how each part of the system is functioning. This allows for thorough monitoring of all the critical processes in real time. These metrics are made possible by Prometheus, which continuously scrapes data from the components, stores it in its internal database, and then feeds this information to Grafana for visualization. Monitoring is a crucial part of this project, as it helps identify potential bottlenecks and areas for optimization, offering a real-time overview of the system's performance.

- The frontend is also available for testing, you can access it by forwarding the port of the frontend service called **frontend-deployment** to your local machine. From here you can access the frontend by going to http://localhost: (Port you decide) and interact with the UI. The frontend provides a user-friendly interface for users to interact with the system, including features such as user registration, login, and social feed. Users can submit prompts to query songs using vector search on Elasticsearch, follow friends, and manage their profiles and posts. The frontend interacts with the backend API to perform various tasks, such as querying the database, processing text, and caching results. 

# Recommendations and Conclusions

## Recommendations

To successfully complete the project, the following recommendations are provided to help you navigate the different components and technologies involved:

1. **Learn How to Use a Kubernetes Cluster**
   - **Recommendation**: It is very important to get a basic understanding of Kubernetes, what is their function and how it works, as the whole project is designed to run in a Kubernetes cluster.
   - **Reason**: Knowing how to deploy and manage the application in Kubernetes will help you run the project in a real-world environment.

2. **Learn How to Use Helm Charts**
   - **Recommendation**: Learn how to use Helm charts, which are used to deploy the application in Kubernetes. It is relevant to understand how they work and what it their function so you can deploy the application correctly.
   - **Reason**: The project uses Helm charts to deploy the application in Kubernetes. Knowing how to use Helm charts will help you manage the deployment of the application.

3. **Get Familiar with MariaDB**
   - **Recommendation**: Learn how to access and use MariaDB, which the the main database used. You should learn the basics, including knowing how to connect to it, view tables, and check data for example.
   - **Reason**: You will need to know how to connect to MariaDB to ensure certain components are working correctly, as well as to verify that data is being updated and stored properly.

4.  **Get Familiar with Elasticsearch Indexing**
   - **Recommendation**: Study the basics of Elasticsearch, focusing on how to create and manage indices where data will be stored.
   - **Reason**: Understanding how to create and manage indices in Elasticsearch is crucial for storing and retrieving data efficiently.
  
5.  **Monitor Resource Usage**
   - **Recommendation**: Keep an eye on resource usage (CPU, memory) while running the script to ensure it operates within acceptable limits.
   - **Reason**: Monitoring helps prevent performance bottlenecks and ensures that the script runs efficiently, particularly for large datasets.

6.  **Document Configuration and Steps**
    - **Recommendation**: Document the configuration parameters and execution steps clearly for future reference and ease of use.
    - **Reason**: Clear documentation helps users understand the setup and execution process, making it easier to troubleshoot and replicate the environment.
  
7.  **Understand the Data Schema**
    - **Recommendation**: Familiarize yourself with the data schema and relationships between tables to write efficient queries.
    - **Reason**: Understanding the data schema helps optimize queries and ensures accurate results when fetching data from the databases.

8. **Understand the Endpoints**
    - **Recommendation**: Learn how to use the endpoints to query data from the databases and understand the responses.
    - **Reason**: Understanding the endpoints helps you retrieve specific data from the databases and analyze the results effectively.
  
9.  **Familizarize with Gatling**
    - **Recommendation**: Learn how to use Gatling to run load tests and analyze the performance of the application under different conditions.
    - **Reason**: Gatling helps evaluate the performance of the application and identify potential bottlenecks or areas for optimization, by simulating real-world scenarios with varying loads.

10. **Understand Prometheus and how to use it**
    - **Recommendation**: Learn how to use Prometheus to monitor the different components of the project and how to scrape the metrics.
    - **Reason**: Prometheus is a key component of the project as it captures the metrics of the different components and stores them in its database. 

11. **Understand Grafana and the consequent Dashboards**
    - **Recommendation**: Learn how to use Grafana to visualize the metrics of the different components of the project.
    - **Reason**: Grafana is a key component of the project as it allows you to see the metrics of the different components and see how they are performing in real time.

12. **Understand Memcached**
    - **Recommendation**: Learn how to use Memcached, which is used as a cache system in the project.
    - **Reason**: Understanding how to use Memcached will help you cache data and understand how it impacts the performance of the application.
  
13. **Understand the loading scripts**
    - **Recommendation**: Understand how the loading scripts work and how they are used to load data into the databases.
    - **Reason**: The loading scripts are essential for the way the databases are loaded with data, and understanding how they work will help you manage the data effectively and understand the structure of the databases. Please note that the information is loaded from CSV files.

## Conclusions 

1. The structure of the relational database is designed to make queries efficient, with tables separated by categories. This allows searches using indexes and foreign keys.

2. The use of MariaDB allows handling large volumes of data. Additionally, integrating Elasticsearch into the project provides options for fast and scalable searches in even larger or distributed databases.

3. The API offers direct and simple access to data through well-structured SQL queries. The relationships between tables allow obtaining details of races, times, and rankings, which is essential for analyzing the performance of drivers and constructors.

4. The database and API are designed in a way that facilitates the incorporation of new data (future drivers, additional circuits, etc.) without interrupting current operations.

5. The data source is configured to connect to Prometheus using an internal URL and is set as the default and editable data source, making it easy to adjust in the environment.

6. The dashboard-loader.yaml configuration allows the automatic creation of dashboards for multiple services (Elasticsearch, MariaDB and Memcached).

7. Each of these dashboards is enabled or disabled through the values.yaml file, allowing for flexible deployment based on monitoring needs.

8. The dashboards are based on pre-existing Grafana configurations, making it easier to adopt best practices for monitoring.

9. The dashboards follow a standard Grafana structure, using panels like Graph and Singlestat, which are essential for metric visualizations and alerts.

10. Each dashboard's JSON file defines inputs such as DS_PROMETHEUS to connect to the Prometheus data source.

11. The project is designed to provide a comprehensive monitoring solution for the different components, allowing users to visualize key metrics and identify performance bottlenecks or areas for optimization.

12. The integration of diverse technologies, helps create a application that uses optimal solutions for different tasks, such as data storage, retrieval, caching, and monitoring.

# Components

## Databases:

The databases used in the project are MariaDB and ElasticSearch. These databases are widely used in the industry and offer features for storing and managing data. 

MariaDB is a popular open-source relational database management system that is compatible with MySQL. It provides excellent performance, scalability, and reliability. MariaDB ensures data integrity and consistency. It also offers advanced features such as replication, clustering, and high availability, making it suitable for handling large volumes of data.

Elasticsearch is also a popular NoSQL database that is used for full-text search and analytics. It is designed for real-time search and analysis of large volumes of data. It offers features like full-text search, aggregations, and spatial search, making it suitable for handling complex data structures and performing advanced queries.

MariaDB is well-suited for handling complex data structures and performing complex queries. They offer strong data consistency, reliability, and security. The choice between the two databases depends on specific project requirements, familiarity with the technology, and the need for specific features or compatibility with existing systems. On the other hand, Elasticsearch is ideal for full-text search and analytics, providing fast and scalable search capabilities for large volumes of data.

Overall, the combination of MariaDB and ElasticSearch in this project ensures efficient and reliable data storage and retrieval, enabling the application to handle large amounts of data effectively.

The structure of the databases is designed to store data related to songs, users, and objects. The MariaDB database stores user information and object data, while the Elasticsearch database stores song titles, artists, and lyrics. 

MariaDB has the following tables:

# ADD TABLES

## Data Loading Scripts:

As mentioned before, Elasticsearch and MariaDB are populated with certain data each. Elasticsearch is populated with songs and MariaDB is populated with Users and Objects data. The data inserting scripts are written in Python and use the Elasticsearch and MariaDB Python libraries to interact with the databases. Elasticsearch is populated with song data, which includes song titles, artists, and lyrics, allowing for efficient retrieval and search capabilities. In contrast, MariaDB is populated with user and object data, such as login information, user profiles, and object details.The scripts encharge of loading the data into the databases are optimized to handle large volumes of data efficiently, ensuring data integrity throughout the loading process. The scripts help assure that both databases are populated with the necessary data for the application to function correctly.

## S3 Crawler: 

## Hugging Face API: (MODIFY)

The API developed in Flask allows users to access Formula 1 data stored in MariaDB databases. Routes are built that execute SQL queries on various tables related to races, drivers, teams, circuits, and Formula 1 events. The main routes include:

1. Routes for obtaining drivers and constructors:

/drivers: Returns a list of all drivers.
/constructors: Returns a list of all constructors.

2. Routes for obtaining laps and times:

/circuit/<int:id>/laps: Provides the laps recorded at a specific circuit.
/drivers/<int:id>/laps: Provides the laps completed by a driver in all races.

3. Other routes:

/driver/<int:id>/total_races: Returns the total number of races a specific driver has participated in.
/driver/<int:id>/pitstops: Details the pit stops of a driver in different races.

## Ingest:

The Ingest application is a Python component responsible for processing data from RabbitMQ messages. When it receives a message, it first checks MariaDB to see if the object has been previously processed; if so, the message is ignored. If the object is new, it downloads the data from an S3 bucket and processes it as a CSV file. For each row in the CSV, an embedding for the “lyrics” field is generated using the Hugging Face API and added to each row as a new field named “embeddings,” formatted as a dense vector for Elasticsearch. The document, including the embeddings, is then added to Elasticsearch in the index named “songs,” and MariaDB is updated to indicate that the object has been processed. This application runs as a Kubernetes deployment and all necessary configurations are injected as environment variables. Additionally, it exposes various metrics for Prometheus monitoring, including the maximum, minimum, and average processing times for both objects and rows, as well as the total number of objects and rows processed, and the number of rows with errors.The ingest is a critical component of the project, as it processes incoming data from RabbitMQ messages, generates embeddings for the lyrics field using the Hugging Face API, and updates the data in both Elasticsearch and MariaDB. The ingest ensures that new data is processed efficiently and accurately, enabling users to search and retrieve song data effectively. 

## Backend API:

## UI:

## Prometheus

Prometheus is an open-source monitoring and alerting software that is used to collect and store metrics from various components of the project. Prometheus scrapes metrics from the different components, such as databases, API, cache systems, and monitoring tools, and stores them in a time-series database. It provides a specific query language, called PromQL, to retrieve and analyze metrics, enabling users to monitor the performance and health of the system. Prometheus offers features like service discovery, multi-dimensional data model, and powerful queries, making it suitable for monitoring complex environments. In this case Prometheus is used to monitor the different components of the project and store the metrics in its database. It is configured to scrape the metrics with the goal of visualizing them in Grafana. It is configured with automatic service discovery due to the use of technologies like MariaDB which for example count with an integrated exporter that allows Prometheus to scrape the metrics of the databases automatically. In the route TC1/charts/databases/values.yaml you can see the configuration of the databases to be scraped by Prometheus. The servicemonitor resource is used to configure the scraping of the metrics of the different components of the project. As this is enabled in the Helm chart, Prometheus will automatically scrape the metrics of the different components of the project.

## Grafana

Grafana is an open-source analytics and monitoring platform that is used to visualize the metrics collected by Prometheus. Grafana provides a user-friendly interface to create dashboards and panels that display the metrics in a visually appealing way. It offers a wide range of visualization options, such as graphs, tables, and gauges, allowing users to customize the dashboards according to their needs. Grafana supports various data sources, including Prometheus, Elasticsearch, and InfluxDB, making it versatile for monitoring different systems. In this project, Grafana is used to create dashboards that display the metrics of the different components, such as databases, API and  cache systems. The dashboards provide insights into the performance and health of the system, allowing users to identify bottlenecks, anomalies, or areas for optimization. Grafana is configured to connect to Prometheus as a data source, enabling it to retrieve the metrics stored in the Prometheus database and visualize them in the dashboards. The dashboards are designed to display key performance indicators, such as HTTP request counts, query response times, cache efficiency, and resource usage, helping users monitor the system in real time and make informed decisions based on the data.

In this project, talking specifically about Grafana we can find seven main dashboards, which are:

- **MariaDB Dashboard:** This dashboard provides a comprehensive view of MariaDB's performance and health. It tracks various metrics, helping users monitor database activity, identify potential bottlenecks, and optimize overall efficiency.

- **Elasticsearch Dashboard:** Designed to give insights into Elasticsearch’s health, this dashboard presents a range of performance metrics. Users can easily track the system's efficiency and address potential issues.

- **Memcached Dashboard:** Focused on the health of the Memcached system, this dashboard offers a variety of performance metrics, enabling users to monitor and enhance caching effectiveness.

- **Hugging Face API Dashboard:** This dashboard provides a detailed view of the Hugging Face API's performance, including request count and maximum, minimum, and average embedding generation time.

- **S3 Crawler Dashboard:** This dashboard tracks the performance of the S3 Crawler, displaying metrics such as total processing time and objects processed. 

- **Backend API Dashboard:** This dashboard offers insights into the Backend API's performance, including cache hits, cache misses, maximum, minimum, and average request processing time, and total request count per endpoint.

- **Ingest Service Dashboard:** This dashboard provides a detailed view of the Ingest Service's performance, including object and row processing times, request counts, and error rates.

## Tests

For the project we did the necessary tests to the databases now we are gonna show the results based on grafana dashboards:
# MariaDB
## Without cache

![Prueba](Tests/maria1.jpeg) 
![Prueba](Tests/maria2.jpeg)
![Prueba](Tests/maria3.jpeg)
![Prueba](Tests/maria4.jpeg)
![Prueba](Tests/maria5.jpeg)
![Prueba](Tests/maria6.jpeg)

The following pictures are proof the dashboards implementation in grafana 

## Memcached

![Prueba](Tests/memcached.jpeg)

## Prometheus 

![Prueba](Tests/prometheus.jpeg)

## Elastic search

![Prueba](Tests/elastic.jpeg)

# References

- [1] "Dockerfile reference," Docker Documentation. [Online]. Available: https://docs.docker.com/reference/dockerfile/#overview. [Accessed: Sep. 4, 2024].

- [2] "kubectl commands," Kubernetes Documentation. [Online]. Available: https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands. [Accessed: Sep. 4, 2024].

- [3] "MariaDB Documentation," MariaDB Knowledge Base. [Online]. Available: https://mariadb.com/kb/en/documentation/. [Accessed: Sep. 4, 2024].

- [4] "Elasticsearch Documentation," Elasticsearch Documentation. [Online]. Available: https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html. [Accessed: Sep. 4, 2024].

- [5] "Grafana Documentation," Grafana Documentation. [Online]. Available: https://grafana.com/docs/. [Accessed: Sep. 4, 2024].