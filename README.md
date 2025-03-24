
# Engineering Project for Process Data Acquisition, Analysis, and Visualization

This project was created to implement an system that acquires, analyzes, and visualizes process data from two simultaneously simulated industrial processes.

## Projects Overview

### 1. **Data Generation for Visualization**
The first of the three projects, **data-generation-for-visualisation**, is responsible for downloading the data through communication interfaces (OPC_UA, S7comm) and timing them. The synchronized data is then sent to the Kafka platform, through which it passes and is ultimately stored in the **InfluxDB** database.

## Features
- **Real-time Data Acquisition**: Communication interfaces to download real-time process data.
- **Data Synchronization**: Ensures data is synchronized before sending it to the Apache Kafka platform.
- **Data Storage**: Uses Kafka for data streaming and InfluxDB for data storage.

## System Diagram

Below is the system diagram implemented in the first project.

<img width="424" alt="PLC-Kafka_data_transfer" src="https://github.com/user-attachments/assets/f68dfd09-cfd6-4ca0-a909-8f4092270258" />
