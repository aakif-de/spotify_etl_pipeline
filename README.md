# Spotify-ETL-Pipeline-Project

## Introduction
This project involves implementing an ETL pipeline that utilizes the Spotify API, AWS, and Snowflake. The pipeline extracts data from the Spotify API, performs transformations using AWS Lambda, and loads the processed data into an AWS data store. From there, the data is ingested into Snowflake for further analysis and insights.

## Architecture
![image](https://github.com/user-attachments/assets/c2f1981d-eba0-4cba-8890-2180f0138de4)

## Business Problem : 
Client, who is deeply passionate about the music industry, wants to gather music data to identify patterns and trends that will help him create music. 
To start, he plans to focus on the top 50 Indian songs each week, allowing him to analyze trending genres, and determine which albums and artists are dominating the charts.

## Dataset/API Used
Spotify API: Utilized the Spotify Web API Spotify to retrieve data on songs, albums, and artists. The API provides access to detailed metadata and analytics for various music tracks, allowing for comprehensive data analysis and insights.

## Services Used

1. **S3 (Simple Storage Service)**: Amazon S3 is a scalable cloud storage solution by AWS that allows users to store and retrieve data from anywhere on the web, offering high durability, security features, and seamless integration with other AWS services.

2. **AWS Lambda**: AWS Lambda is a serverless computing service that allows you to run code without provisioning or managing servers. It automatically scales your applications by executing code in response to events, such as changes in data or HTTP requests, enabling you to build highly scalable and efficient applications with minimal overhead.

3. **CloudWatch**: Amazon CloudWatch is a monitoring and management service for AWS resources and applications. It provides real-time insights through metrics and logs, enabling you to track performance, set alarms, and automate actions based on defined thresholds, ensuring optimal operation and resource utilization.

4. **Snowpipe**: Snowpipe is a continuous data loading service by Snowflake that automates the process of loading data from external sources like AWS S3 into Snowflake. It listens for new data in S3 buckets and automatically ingests it in near real-time, providing a seamless integration for real-time analytics and reducing the need for manual data loading processes.

5. **Snowflake**: Snowflake is a cloud-based data warehousing platform that allows for scalable storage, querying, and analysis of large datasets. It supports structured and semi-structured data, making it ideal for high-performance analytics. With built-in capabilities for auto-scaling, Snowflake integrates seamlessly with AWS services, enabling efficient data storage, transformation, and analysis for insights.

## Installed Packages ( Refer requiremnets.txt)
Spotipy: A library for accessing the Spotify Web API.
Boto3: The AWS SDK for Python, for interacting with AWS services.
Pandas: A data manipulation and analysis library for Python.

## Project Execution Flow
Extract data from the API → Trigger AWS Lambda weekly → Run extraction code → Store raw data in S3 → Trigger transformation function → Transform data and load it into S3 → Snowpipe automatically ingests the data into designated tables in Snowflake for analysis and querying.
