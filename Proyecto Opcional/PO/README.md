# Optional Project

## Requirements

* Create an user in [DockerHub](https://hub.docker.com/)
* Install [Docker Desktop](https://docs.docker.com/desktop/install/windows-install/), if you are using MacOS, please make sure you select the right installer for your CPU architecture.
* Open Docker Desktop, go to **Settings > Kubernetes** and enable Kubernetes.
![K8s](./images/docker-desktop-k8s.png "K8s Docker Desktop")
* Install [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-macos/)
* Install [Helm](https://helm.sh/docs/intro/install/)
* Install [Visual Studio Code](https://code.visualstudio.com/)
* Install [Lens](https://k8slens.dev/)


## AWS Access Information

**Bucket:** 2024-02-ic4302-gr1

**Access Key:** AKIAQ2VOGXQDTWAX4PUY

**Secret Key:** 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


## Building the docker images

There is a script to build the docker images, to execute it in a bash shell execute:

```bash
cd ./PO/docker
./build.sh nereo08
```

Change **nereo08** by your DockerHub username

Please take a look on the script contents to make sure you understand what is done under the hood.


## Helm Charts

### Configure

* Open the file **PO/charts/application/values.yaml**
* Replace **nereo08** by your DockerHub username

```yaml
config:
  docker_registry: nereo08
```

### Install

Execute:

```bash
cd ./PO/charts
./install.sh
```


### Uninstall

Execute:

```bash
cd ./PO/charts
./uninstall.sh
```

## Access Debug Pod

```bash
# copy the name that says debug from the following command
kubectl get pods
# then replace debug-844bb45d6f-9jt45 by that name
kubectl exec --stdin --tty debug-844bb45d6f-9jt45 -- /bin/bash
```

### Execute Spark

```bash
cd /opt/spark/
bin/spark-shell
```

Now that Spark Shell is up and running, you can execute the contents of the file **PO/charts/application/scala/app.scala**


# Recommendations and Conclusions

## Recommendations

1. **Learn Python Programming**
   - **Recommendation**: It is important to start by learning Python programming, knowing how to run scripts and understand code structures will help you follow and understand what is being done.
   - **Reason**: The S3 Spider component and the Downloader component are written in Python, so understanding the basics will help you follow the code and make minor adjustments if any change is needed.

2. **Familiarize Yourself with Environment Variables**
   - **Recommendation**: You also should understand what environment variables are, how they work and how to set them up. You will need to set certain environment variables for the components of the project to work correctly, for example, some database credentials and API URLs.
   - **Reason**: Environment variables are used to pass important configuration settings to the application without hardcoding them into the script.

3. **Learn the Basics of SQL**
   - **Recommendation**: Getting a basic understanding of SQL is highly recommended, it is the language used to interact with the databases. You should learn how to run queries, such as selecting data from tables or updating records and understand the functioning of them.
   - **Reason**: The project in multiple sections interacts with databases, mainly MariaDB, and understanding SQL will help you see how it inserts, retrieves and updates data.

4. **Get Familiar with MariaDB**
   - **Recommendation**: Learn how to access and use MariaDB, which the the main database used. You should learn the basics, including knowing how to connect to it, view tables, and check data for example.
   - **Reason**: You will need to know how to connect to MariaDB to ensure certain components are working correctly, as well as to verify that data is being updated and stored properly.

5. **Understand RabbitMQ Basics**
   - **Recommendation**: Learn what RabbitMQ is, what is it used for and how it works as a message broker that passes messages between different parts of an application.
   - **Reason**: The S3 Spider and Downloader both work beside RabbitMQ, sending and consuming messages with RabbitMQ, so understanding this process will help you see how jobs are being processed.

6. **Learn How to Use a Kubernetes Cluster**
   - **Recommendation**: It is very important to get a basic understanding of Kubernetes, what is their function and how it works, as the whole project is designed to run in a Kubernetes cluster.
   - **Reason**: Knowing how to deploy and manage the application in Kubernetes will help you run the project in a real-world environment.

7. **Understand API Interactions**
   - **Recommendation**: It is important to learn what an API (Application Programming Interface) is, and understand how a component uses it to fetch data from the CrossRef API.
   - **Reason**: The downloader interacts with the CrossRef API to retrieve information for each DOI. Understanding this process is key to seeing how the component works.
  
8. **Learn How to Use Helm Charts**
   - **Recommendation**: Learn how to use Helm charts, which are used to deploy the application in Kubernetes. It is relevant to understand how they work and what it their function so you can deploy the application correctly.
   - **Reason**: The project uses Helm charts to deploy the application in Kubernetes. Knowing how to use Helm charts will help you manage the deployment of the application.
  
9. **Understand Spark and Scala Basics**
   - **Recommendation**: Learn the basics of SparkSQL and Scala, as the project uses Spark to process data and Scala is the language used to write the SparkJob consequently. Basic knowledge of these technologies will help you understand the code and make changes if necessary.
   - **Reason**: In the SparkJob component, the code is written in Scala so for you to understand the structure and how everything works basic knowledge is needed. 
  
10. **Get Familiar with Elasticsearch Indexing**
   - **Recommendation**: Study the basics of Elasticsearch, focusing on how to create and manage indices where data will be stored.
   - **Reason**: After transforming the data with Spark SQL, the results are saved in an Elasticsearch index. Understanding Elasticsearch indexing will help you verify that the data is being stored correctly and know how to retrieve it.
  
11. **Learning the difference between CronJob and a Deployment**
   - **Recommendation**: Understand the difference between a CronJob and a Deployment in Kubernetes, as the project uses both to run the components.
   - **Reason**: The project uses a CronJob to run the S3 Spider and SparkJob components at specific times, and a Deployment to run the Downloader component. Knowing the difference between the two will help you understand how the components are being executed.

## Conclusions 

1. **Optional Projects Enhance Learning and Skill Development**
   Projects being part of a course make learning much more rewarding, as they allow practical applications of the theoretical knowledge gained. However, optional projects like this one provide an additional layer of complexity and challenge, which can significantly enhance learning and skill development. This project, in particular, covers a wide range of technologies and concepts we had not seen before, consequently not having knowledge about them, making it an excellent opportunity for us to develop our understanding and expertise in various areas.

2. **Diverse Databases Require Specialized Skills and Techniques**
   The project highlights the necessity of acquiring distinct skills and techniques to manage various types of databases effectively. By working with various databases, we gained valuable experience in handling different database systems, understanding their unique features, and optimizing data storage and retrieval processes. This exposure to diverse databases can help us develop a well-rounded skill set and adapt to different data management requirements in our future careers. 

3. **Spider/Crawler Tools Simplify Data Acquisition from Multiple Sources**
   The use of Spider/Crawler tools within the project demonstrates their effectiveness in automating data collection from various sources such as APIs, web pages, and data storage buckets. These tools significantly reduce the time and effort required for data gathering, making them indispensable for large-scale data processing tasks.

4. **Collaboration Across Technologies Enhances Project Outcomes**
   Integrating various technologies, such as RabbitMQ for messaging, Kubernetes for deployment, and Elasticsearch for data indexing, demonstrates the importance of cross-technology collaboration. This project demonstrated to us how combining different tools and platforms can result in a more appropiate and efficient system all together.

5. **Scalability is Essential for Modern Applications**
   The project emphasizes the need for scalability in modern applications. By leveraging Kubernetes and containerization, the project ensures that the system can handle increased loads and expand as needed, which has been demonstrated, is vital for maintaining performance in dynamic environments.

6. **Continuous Learning and Adaptation are Key to Success**
   Learning and adapting to new technologies and methodologies are essential for success in the rapidly evolving field of data science and software development, which is exactly our degree. This project provides an excellent opportunity for us to enhance skills, explore new technologies, and learn about the latest trends in the industry.

7. **Real-World Applications Provide Valuable Experience**
   Working on projects that simulate real-world scenarios provides valuable experience and prepares students like us for the challenges we may face in our professional careers. This project offers a practical learning experience that can help develop skills and knowledge needed to succeed in the field of data science and software development. In our professional careers we will face similar challenges where a application uses multiple technologies we do not know about to learning will be constant, for that reason this project is a great opportunity to learn how to solve them.

8.  **Feedback and Iteration Improve Project Outcomes**
   Working together and getting feedback from your teammates are key elements to making any project a success. When classmates team up, we can mix our habilities, share ideas, and tackle the challenges. Receiving feedback from our colleagues and teachers can help us identify areas for improvement and refine our work to achieve better outcomes. This iterative process of working together and improvement is essential for developing high-quality projects and achieving success in the project. 

9. **Reading and Understanding Code is Essential**
   Reading and understanding code is an essential skill for Computer Science majors as us. By reviewing and analyzing the codebase of this project, we could gain insights into best practices, coding standards on the technologies we did not know about, and design patterns used in real-world applications. This experience helped us improve our coding skills, learning new techniques, and developing a deeper understanding of various components of the project.

10. **Documentation and Learning to Search are Key**
   Documentation and learning how to navigate the internet in search of solutions are essential skills for students like us. By documenting the work, we can keep track of our progress, plus it helps with sharing our knowledge with others, and refering back to previous solutions if needed. Additionally, knowing how to search for information online may help us find solutions to problems we encounter, learn information about technologies we are not familiar with, and integrating new tools into our projects. The more information we can find, the more we can learn and apply to our projects.


# Components

## Downloader

### Overview

The downloader is a Python application designed to process jobs from a message queue, interact with a database, retrieve data from an external API, and store the results. It operates within a Kubernetes environment and performs the following key steps:

1. **Message Consumption**:
   - The downloader connects to a RabbitMQ queue, where it waits for messages. Each message represents a job that needs to be processed.

2. **Database Interaction**:
   - When a job message is received, the downloader connects to a MariaDB database and updates the job status to "in-progress". This ensures that the job is marked as active while it is being processed.
   - It then retrieves a list of DOIs (Digital Object Identifiers) associated with the job from the database.

3. **API Data Retrieval**:
   - For each DOI, the downloader makes a call to the CrossRef API using the DOI as a parameter. This API returns metadata about academic articles, books, or other scholarly content in JSON format.
   - The JSON response from the API is then saved to disk as a file, with the filename being an MD5 hash of the DOI.

4. **Handling Missing Data**:
   - If the API call does not return data for a particular DOI, that DOI is ignored, and its information is recorded in a "skipped" list within the MariaDB database.

5. **Job Completion**:
   - After processing all DOIs associated with a job, the downloader updates the job status in MariaDB to "done" and records the completion time.

6. **Environment Configuration**:
   - The downloader relies on environment variables for configuration. These variables specify important details like RabbitMQ credentials, MariaDB credentials, and the file storage path.


### Configuration

The Downloader component requires the following environment variables to be set:

* **RABBITMQ_HOST**: The hostname of the RabbitMQ server.
* **RABBITMQ_USER**: The username for authenticating with the RabbitMQ server.
* **RABBITMQ_PASS**: The password for authenticating with the RabbitMQ server.
* **RABBITMQ_QUEUE**: The name of the RabbitMQ queue to consume messages from.
* **DB_HOST**: The hostname of the MariaDB server.
* **DB_PORT**: The port number of the MariaDB server.
* **DB_USER**: The username for authenticating with the MariaDB server.
* **DB_PASS**: The password for authenticating with the MariaDB server.
* **DB_NAME**: The name of the MariaDB database to store the data in.

### Usage

To run the Downloader component, execute the following command:

```bash
python downloader.py
```



