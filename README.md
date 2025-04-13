
# Engineering Project for Process Data Acquisition, Analysis, and Visualization

This project was created to implement an system that acquires, analyzes, and visualizes process data from two simultaneously simulated industrial processes.

---

## Projects Overview

### 1. **Data Generation for Visualization**
The first of the three projects, **data-generation-for-visualisation**, is responsible for downloading the data through communication interfaces (OPC_UA, S7comm) and timing them. The synchronized data is then sent to the Kafka platform, through which it passes and is ultimately stored in the **InfluxDB** database.

---

## Features
- **Real-time Data Acquisition**: Communication interfaces to download real-time process data.
- **Data Synchronization**: Ensures data is synchronized before sending it to the Apache Kafka platform.
- **Data Storage**: Uses Kafka for data streaming and InfluxDB for data storage.

---

## System Context  
Data originates from Siemens S7-1500 PLCs simulated in **TIA Portal** and **PLC-SIM Advanced**, operating in parallel via two communication protocols:  
- **S7comm**  
- **OPC UA**  

InfluxDB is deployed as a **Docker container** to store both raw error data and the results of the analysis.  

---


## System Diagram

Below is the system diagram implemented in the first project.

<img width="424" alt="PLC-Kafka_data_transfer" src="https://github.com/user-attachments/assets/f68dfd09-cfd6-4ca0-a909-8f4092270258" />

---

## Technologies Used  

### 🐍 Python Libraries  
- `influxdb_client` – communication with InfluxDB  
- `numpy`, `pandas` – data processing and statistical computation  
- `scipy` – numerical integration (IAE, ISE)  
- `dotenv` – environment variable management  
- `json` – config and data handling  
- `threading`, `time`, `datetime`, `uuid`, `os` – concurrency and scheduling  

### 💾 Data Communication & Integration  
- `kafka-python` – Kafka producer/consumer and admin client  
- `opcua` – OPC UA client communication  
- `snap7` – S7Comm communication with Siemens PLCs  

### 🧱 Other Components  
- **InfluxDB** – time-series database (Docker container)  
- **TIA Portal / PLC-SIM Advanced** – industrial simulation environment for Siemens S7-1500

---

## Usage  

1. **Start InfluxDB (Docker)**  
   Make sure the InfluxDB container is running and reachable.

2. **Set Environment Variables**  
   Create a `.env` file with the required variables:
   ```env
   INFLUXDB_URL=http://localhost:8086
   INFLUXDB_TOKEN=your_token
   INFLUXDB_ORG=your_org
   INFLUXDB_BUCKET=your_bucket
   
3. **Start Kafka Container**
Run Kafka in KRaft mode using the provided docker-compose.yml:

```bash
docker-compose up -d
```

4. **Run Analysis Script**
Launch the main analysis process:

```bash
python main.py
```
