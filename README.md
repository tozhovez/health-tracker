
# Health Tracker

The application allows users to track and analyze their health data, including Physical Activity, Sleep Activity, and Blood Tests.

- [Building a Health Tracker API.pdf](#/Home%20Assignment_%20Building%20a%20Health%20Tracker%20API.pdf)
------------------------------------------------------------

## Prerequisites

### If not installed:
#### To Install:
```bash
sudo apt install git wget curl
```

### How to install Docker Engine:
Follow the instructions from the official Docker documentation:
- [Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/)
- [Linux post-installation steps for Docker Engine](https://docs.docker.com/engine/install/linux-postinstall/)

## Setup Instructions

### Step 1: Clone GitHub Repository
```bash
git clone <repository-url>
cd health-tracker
```

### Step 2: Setup Infrastructure on Docker Compose
```bash
make run-infra
```

### Step 3: Start Health Tracker Service
```bash
make run-tracker
```
The health-tracker service will be running on:
- Application: [http://0.0.0.0:6565](http://0.0.0.0:6565)
- FastAPI - Swagger UI: [http://0.0.0.0:6565/docs](http://0.0.0.0:6565/docs)

-------------------------------------

## Faker Infrastructure

The `infra/faker` directory contains scripts and configurations to generate fake data for testing purposes.

### Step 1: Navigate to the Faker Directory
```bash
cd infra/faker
```

### Step 2: Install Faker Dependencies
Ensure you have the required dependencies installed:
```bash
pip install -r requirements.txt
```

### Step 3: Run the Faker Script
Execute the faker script to generate fake data:
```bash
python generate_fake_data.py
```

This will populate your database with fake data, which can be useful for testing and development purposes.

---------------------

The health-tracker project leverages PostgreSQL with the TimescaleDB extension as its database technology. This choice offers several advantages:

### 1. Efficient Time-Series Data Handling
- **PostgreSQL**: A robust, open-source relational database known for its reliability, feature richness, and performance.
- **TimescaleDB**: A time-series database built on PostgreSQL, optimized for handling time-series data efficiently. It provides powerful time-series capabilities such as continuous aggregates, data retention policies, and efficient querying.

### 2. Scalability
TimescaleDB allows for horizontal scaling, which is crucial for handling large volumes of data generated over time. This ensures the system can grow with the increasing amount of data without compromising performance.

### 3. Continuous Aggregates
The use of continuous aggregates in TimescaleDB allows for real-time aggregation of data, which is essential for generating insights and reports. This reduces the computational load and improves query performance.

### 4. Data Retention Policies
TimescaleDB supports data retention policies, enabling automatic data archiving and deletion based on predefined rules. This helps manage storage efficiently and ensures that only relevant data is retained.

### 5. Advanced SQL Features
PostgreSQL offers advanced SQL features such as window functions, common table expressions (CTEs), and JSON support, which are beneficial for complex queries and data manipulation required in applications.

### 6. Integration with Docker
The project uses Docker for infrastructure management, as seen in the docker-compose.infra.yml file. Docker ensures consistent environments across development, testing, and production, making it easier to manage dependencies and deployments.

### 7. Community and Support
Both PostgreSQL and TimescaleDB have strong community support and extensive documentation, making it easier to find solutions to potential issues and stay updated with the latest features and best practices.

In summary, using PostgreSQL with TimescaleDB for the health-tracker project provides a scalable, efficient, and feature-rich solution for managing and analyzing time-series health data. This combination ensures high performance, real-time insights, and ease of maintenance, making it an ideal choice for the project.


--------------------------------------------


- python 3.13.0 or dev
if it's not installed:
#### Step 1: Check Existing Python Version
Run the following command to check if Python 3.13 is already installed:
```bash
  python3 --version
```
If Python 3.13 is not listed, proceed to the next step.

#### Step 2: Install Python 3.13
For Linux (Ubuntu/Debian)
- 1. Add Python's PPA (Personal Package Archive):
```bash
sudo apt update
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa
```
- 2. Install Python 3.13:
```bash
sudo apt update
sudo apt install python3.13 python3.13-venv python3.13-dev -y
```

#### Step 3: Create a Virtual Environment
Once Python 3.13 is installed, create a virtual environment:
Create the environment:
```bash
python3.13 -m venv my_env
source my_env/bin/activate
```
#### Step 4: Install Required Packages
Within the virtual environment, you can now install packages using pip:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
#### Step 5: Verify Installation
Confirm the correct Python version and packages:
```bash
python --version
pip list
```

--------------------------------------------

## Health Tracker Frontend

The frontend of the health-tracker application is built using modern web technologies to provide a responsive and user-friendly interface for tracking and analyzing health data.

### Technologies Used
- **VUE**: A JavaScript library for building user interfaces.
- **TypeScript**: A typed superset of JavaScript that compiles to plain JavaScript.

### Prerequisites
- **Node.js**: Ensure you have Node.js installed. You can download it from [Node.js official website](https://nodejs.org/).
- **npm**: Node package manager, which comes with Node.js.

### Installation
Follow these steps to set up the frontend:

#### Step 1: Navigate to the Frontend Directory
```bash
cd work/health-tracker/frontend/healthapp
```

#### Step 2: Install Dependencies
Install the required dependencies using npm:
```bash
npm install
```

### Running the Frontend
To start the development server and run the frontend application, use the following command:
```bash
npm run dev
```
This will start the application on [http://localhost:5173/](http://localhost:5173/).


