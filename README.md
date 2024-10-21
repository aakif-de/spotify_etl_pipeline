# Spotify-ETL-Pipeline-Project

## Introduction
This project implements an ETL (Extract, Transform, Load) pipeline using the Spotify API on AWS. It extracts data from the Spotify API, transforms it, and loads it into an AWS data store for analysis and insights.

## Architecture
![image](https://github.com/user-attachments/assets/c2f1981d-eba0-4cba-8890-2180f0138de4)


# Dataset/API Used


# Project Execution Flow
Extract Data from API -> Lambda trigger every(1 hour) -> Run extract code -> Store raw data -> Trigger Transfom Function -> Transform Data and Load it -> Query using Athena
