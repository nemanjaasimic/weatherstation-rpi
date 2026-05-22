from sensor.sht31_temp import get_temp_and_humidity_readings
from sensor.globe_temp import find_ds18b20, read_globe_temperature
from sensor.air_quality import read_air_quality_sensor
from sensor.gps import get_gps_data
from sensor.analog_sensors import get_wind_speed, get_uv_intensity
import csv
from datetime import datetime
import time
import os


def fetch_current_date_time_from_gps():
    gps_latitude, gps_longitude, gps_altitude, gps_altitude_units, gps_datetime = None, None, None, None, None
    while gps_latitude == None or gps_longitude == None or gps_altitude == None or gps_datetime == None:
        try:
            gps_latitude, gps_longitude, gps_altitude, gps_altitude_units, gps_datetime = get_gps_data()
            return gps_datetime
        except Exception as error:
            print(f'Failed to retrieve GPS data. Message: {error.args[0]}. Trying again!')
            continue


def fetch_values():
    gps_latitude, gps_longitude, gps_altitude, gps_altitude_units, gps_datetime = None, None, None, None, None
    while gps_latitude == None or gps_longitude == None or gps_altitude == None or gps_datetime == None:
        try:
            gps_latitude, gps_longitude, gps_altitude, gps_altitude_units, gps_datetime = get_gps_data()
        except Exception as error:
            print(f'Failed to retrieve GPS data. Message: {error.args[0]}. Trying again!')
            continue

    temp, humidity = None, None
    while temp == None or humidity == None:
        try:
            temp, humidity = get_temp_and_humidity_readings()
        except Exception as error:
            print(f'Failed to retrieve Temperature and Humidity data. Message: {error.args[0]}. Trying again!')
            continue

    wind_speed_m_s = None
    while wind_speed_m_s == None:
        try:
            wind_speed_m_s = get_wind_speed()
        except Exception as error:
            print(f'Failed to retrieve Wind Speed data. Message: {error.args[0]}. Trying again!')
            continue

    uv_intensity = None
    while uv_intensity == None:
        try:
            uv_intensity = get_uv_intensity()
        except Exception as error:
            print(f'Failed to retrieve UV Intensity data. Message: {error.args[0]}. Trying again!')
            continue

    globe_temp = None
    while globe_temp == None:
        try:
            globe_temp_sensor_name = find_ds18b20()
            globe_temp = read_globe_temperature(globe_temp_sensor_name)
        except Exception as error: 
            print(f'Failed to retrieve Globe temp data. Message: {error.args[0]}. Trying again!')
            continue

    pm25, pm10 = None, None
    while pm25 == None or pm10 == None:
        try:
            pm25, pm10 = read_air_quality_sensor()
            # time.sleep(60)
        except Exception as error:
            print(f'Failed to retrieve Air Quality PM data. Message: {error.args[0]}. Trying again!')
            continue
    
    return gps_datetime, gps_altitude, gps_altitude_units, gps_longitude, gps_latitude, temp, humidity, globe_temp, wind_speed_m_s, get_limited_wind_speed(wind_speed_m_s), pm25, pm10, uv_intensity


def get_limited_wind_speed(wind_speed_m_s):
    limited_wind_speed_m_s = wind_speed_m_s
    if limited_wind_speed_m_s > 17.0:
        limited_wind_speed_m_s = 17.0
    elif limited_wind_speed_m_s < 0.5:
        limited_wind_speed_m_s = 0.5
    return limited_wind_speed_m_s


def start_measuring(filename, iteration_pause=90):
    print("Active measuring started...\n")
    measurement_counter = 1
    while True:
        print(f"Obtaining new data for measurement #{measurement_counter}")
        
        gps_datetime, gps_altitude, gps_altitude_units, gps_longitude, gps_latitude, temp, humidity, globe_temp, wind_speed_m_s, limited_wind_speed_m_s, pm25, pm10, uv_intensity = fetch_values()
        print_measured_values(gps_datetime, gps_altitude, gps_altitude_units, gps_longitude, gps_latitude, temp, humidity, globe_temp, wind_speed_m_s, limited_wind_speed_m_s, pm25, pm10, uv_intensity)

        # field names 
        header = ['Date', 'Time', 'Altitude (m)', 'Longitude', 'Latitude', 't (°C)', 'RH (%)', 'Tg(°C)', 'v (m/s)', 'v [0.5-17] (m/s)', 'PM (2.5) ppm', 'PM (10) ppm', 'UV B (mW/cm^2)'] 
        write_header = False
        try:
            with open(filename, 'r') as csv_file:
                csv_dict = [row for row in csv.DictReader(csv_file)]
                if len(csv_dict) == 0:
                    write_header = True
        except FileNotFoundError:
            write_header = True


        with open(filename, 'a') as csv_file:
            # data rows of csv file 
            row = [gps_datetime.date(), gps_datetime.time().strftime('%H:%M:%S'), gps_altitude, gps_longitude, gps_latitude, temp, humidity, globe_temp, wind_speed_m_s, limited_wind_speed_m_s, pm25, pm10, uv_intensity]
        
            # using csv.writer method from CSV package
            write = csv.writer(csv_file)

            if write_header:
                write.writerow(header)
    
            write.writerow(row)
        
        print(f"Successfully obtained data for measurement #{measurement_counter}. Pausing for 90s for next iteration...\n")
        measurement_counter = measurement_counter + 1
        time.sleep(iteration_pause)


def print_measured_values(gps_datetime, gps_altitude, gps_altitude_units, gps_longitude, gps_latitude, temp, humidity, globe_temp, wind_speed_m_s, limited_wind_speed_m_s, pm25, pm10, uv_intensity):
    print('___________________________________________________________________________________________')
    print(f'Reading started at: {gps_latitude}, {gps_longitude}, {gps_altitude}{gps_altitude_units}, {gps_datetime}')
    print(f'Temp is : {temp} C, Humidity is: {humidity} %RH')
    print(f'Wind speed is : {wind_speed_m_s} m/s | Limited wind speed is: {limited_wind_speed_m_s} m/s')
    print(f'UV Intensity is : {uv_intensity} mW/cm^2')
    print(f'Globe temperature is : {globe_temp} C')
    print(f'PM2.5 {pm25} ug/m^3 | PM10 {pm10} ug/m^3')
    print('___________________________________________________________________________________________')



def debug():
    gps_datetime, gps_altitude, gps_altitude_units, gps_longitude, gps_latitude, temp, humidity, globe_temp, wind_speed_m_s, limited_wind_speed_m_s, pm25, pm10, uv_intensity = fetch_values()
    print("Measurements completed.\nPlease take a look at the results below:")
    print_measured_values(gps_datetime, gps_altitude, gps_altitude_units, gps_longitude, gps_latitude, temp, humidity, globe_temp, wind_speed_m_s, limited_wind_speed_m_s, pm25, pm10, uv_intensity)


if __name__ == "__main__":
    DEFAULT_ITERATION_PAUSE_SECONDS = 90

    print("\nRunning the first measurement to check the system...\n")
    debug()
    print("First measurement completed...System will pause for 5 seconds and then continue regular interval measurements.\n")  
    time.sleep(5)
    
    print("Getting system time from GPS...\n")
    current_date_time = fetch_current_date_time_from_gps()

    filename = f'/home/weatherstation/Desktop/measured-data/measurement_{current_date_time.date()}.csv'
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    start_measuring(filename, DEFAULT_ITERATION_PAUSE_SECONDS)
