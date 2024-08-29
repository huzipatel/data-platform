import requests
from influxdb_client import InfluxDBClient, Point, WriteOptions

# Configuration
INFLUXDB_URL = "http://influxdb-service.monitoring.svc.cluster.local:8086"
INFLUXDB_TOKEN = "sL0JLLOmld1bN1kBWpWx3RZ3Scd6ZeOOYVbWkeKRPkGqKI7-0sehEzH05Xlm9r6zeqvYyCH0DmalpYlgOCfJxA=="
INFLUXDB_ORG = "HuziPersonal"
INFLUXDB_BUCKET = "WeatherAPI"
API_URL = "https://api.marketstack.com/v1/eod?symbols=AAPL"
API_KEY = "18d39a0626eaf7cdd4a23b2e9c962150"

client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = client.write_api(write_options=WriteOptions(batch_size=1))

def fetch_end_of_day_data():
    response = requests.get(API_URL, API_KEY)
    data = response.json()
    return data
    print(data)




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
    data = fetch_air_quality_data()
    process_and_store_data(data)
