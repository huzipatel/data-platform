from dotenv import load_dotenv
import os 
import requests
from influxdb_client import InfluxDBClient, Point, WriteOptions

# Configuration
load_dotenv()
INFLUXDB_URL = os.getenv('INFLUXDB_URL')
INFLUXDB_TOKEN = os.getenv('INFLUXDB_TOKEN')
INFLUXDB_ORG = os.getenv('INFLUXDB_ORG')
INFLUXDB_BUCKET = os.getenv('INFLUXDB_BUCKET')
API_URL = os.getenv('API_URL')
API_KEY = os.getenv('API_KEY')

#Define parameters as a dictionary


client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = client.write_api(write_options=WriteOptions(batch_size=1))


def fetch_end_of_day_data():
    # Create a loop to fetch all pages
    while True:
        offset = 0
        limit = 100
        # Define the parameters, including the offset and limit
        params = {
    'access_key': API_KEY,
    'symbols': 'AAPL',
    'offset':offset,
    'limit':limit
}
        #Make the GET request
        response = requests.get(API_URL, params = params)
        data = response.json
        #Check if the response contains data
        if 'data' in data and data['data']:
            # Process the data on this page
            for item in data['data']:

                #Processing code here
                print(item)
         
        #C
        #if data.get()
        print(response)
        
        data = response.json()
        
        print(data)
        
        return data
    


def process_and_store_data(data):
    # Example: Suppose data contains "pm2.5" and "pm10" values
    pm25 = data['pm25']
    pm10 = data['pm10']

    point = Point("air_quality") \
        .tag("location", "Your_Location") \
        .field("pm25", pm25) \
        .field("pm10", pm10)

    write_api.write(INFLUXDB_BUCKET, INFLUXDB_ORG, point)

if __name__ == "__main__":
    data = fetch_end_of_day_data()
    print(data)
    #process_and_store_data(data)
