# data-generation-for-visualization

This project is a preliminary version of a project created to send process data from an automation system. The final version will download data using the OPC-UA standard from the TIA Portal environment. The data will be generated based on the actual automation system and plant for heat generation and distribution. The initial version allows you to generate a function (in this case, a sine function) and send it to the InfluxDB time database. It uses the `influxdb-client` library to write and query data from an InfluxDB bucket. Also it is able to visualise the results after uncomment "# data_get.get_values()" funcion (for preliminary purposes). There will be also project that retrives the data and visualises it.

## Features

- **Initialize InfluxDB Connection**: Handles connecting to the InfluxDB instance and manages write/query operations.
- **Write Sample Data**: Generates a series of sample data points to an InfluxDB bucket.
- **Write Sinusoidal Data**: Generates and stores sine wave data points at regular intervals.
- **Query Data and Visualization**: In this preliminary version it queries the stored data from InfluxDB and plots the results using `matplotlib`.

## Project Structure

- **`init_db_conn.py`**: Contains the `InitDB` class responsible for connecting to InfluxDB using environment variables for configuration.
- **`get_data.py`**: Implements the `GetData` class for writing and querying data. It includes methods to generate and visualize data (for preliminary version).
- **`main.py`**: The entry point of the project. Writes data, sends it into InfluxDB time database. (In addition it retrieves and visualizes the stored data, but it is for tests and preliminary project purposes - There will be added project that retrives the data and visualises it.). 

## Dependencies

- Python 3.x
- InfluxDB (best to run it as a docker image)
- Required Python libraries:
  - `influxdb-client`
  - `numpy`
  - `pandas`
  - `matplotlib`
  - `python-dotenv`
  - `streamlit-autorefresh`


Install the required libraries using:

```bash
pip install influxdb-client numpy pandas matplotlib python-dotenv streamlit-autorefresh
