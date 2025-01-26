# Fantasy Hockey Stats Tweeter 

This project aggregates daily player statistics for fantasy hockey and posts them to Twitter. The data is collected using various Python scripts, stored in a PostgreSQL database, and automated through Apache Airflow. The project is deployed on Google Cloud Platform (GCP) with Docker containers to manage dependencies and facilitate smooth operations.

## Features

- **Fetch player statistics**: The project fetches player statistics for the day before and the current season.
- **Post to Twitter**: The statistics are posted to Twitter for user engagement.
- **Database**: Player data is stored in a PostgreSQL database, which is running on Docker for containerization.
- **Task Scheduling**: Apache Airflow automates the tasks for scheduling data fetching and posting at regular intervals.

## Technologies Used

- **PostgreSQL**: Used for storing player statistics, including daily and season data.
- **Google Cloud Platform (GCP)**: The project is hosted on a virtual machine in GCP to ensure scalability and availability.
- **Docker**: Docker is used to containerize the PostgreSQL database, allowing for easy deployment and management.
- **Apache Airflow**: Task automation is handled through Apache Airflow, scheduling and running jobs such as fetching statistics and posting on Twitter.
- **Twitter API (Tweepy)**: Used for posting player statistics to Twitter.

## Fantasy Hockey Points Conversion

The points for each player are calculated based on the following fantasy hockey scoring system:

- **Goals (G)** = 6 points
- **Assists (A)** = 4 points
- **Plus/Minus (+/-)** = 1 point
- **Powerplay Points (PPP)** = 2 points
- **Shots on Goal (SOG)** = 0.9 points
- **Hits (HIT)** = 0.5 points
- **Blocks (BLK)** = 1 point

These stats are fetched for each player, converted into fantasy points, and shared on Twitter.

## Getting Started

To set up the project locally or on a server, follow the steps below:

### Prerequisites

- **PostgreSQL**: Dockerized database for storing player statistics.
- **Google Cloud Platform (GCP)**: VM for hosting the scripts and Airflow.
- **Docker**: Containerization for PostgreSQL.
- **Apache Airflow**: Task automation and scheduling.

