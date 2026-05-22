import serial
import pynmea2
import time
import pytz
from lat_lon_parser import to_str_deg_min_sec

def get_gps_data():
	port="/dev/ttyAMA0"
	neo_6m_gps_serial=serial.Serial(port, baudrate=9600, timeout=1)
	# dataout = pynmea2.NMEAStreamReader()
	time.sleep(2)

	gpgga_data = get_gps_message(neo_6m_gps_serial, '$GPGGA')
	gprmc_data = get_gps_message(neo_6m_gps_serial, '$GPRMC')

	
	if gpgga_data.startswith('$GPGGA') and gprmc_data.startswith('$GPRMC'):

		neo_gps_gpgga_reading = pynmea2.parse(gpgga_data)
		neo_gps_gprmc_reading = pynmea2.parse(gprmc_data)

		gps_latitude = neo_gps_gprmc_reading.latitude
		gps_longitude = neo_gps_gprmc_reading.longitude
		gps_datetime_utc = neo_gps_gprmc_reading.datetime
		belgrade_timezone = pytz.timezone('Europe/Belgrade')
		gps_datetime_belgrade = gps_datetime_utc.astimezone(belgrade_timezone)
		
		gps_altitude = neo_gps_gpgga_reading.altitude
		gps_altitude_unit = neo_gps_gpgga_reading.altitude_units

		neo_6m_gps_serial.close()
		return to_str_deg_min_sec(gps_latitude), to_str_deg_min_sec(gps_longitude), gps_altitude, gps_altitude_unit, gps_datetime_belgrade
	else:
		neo_6m_gps_serial.close()
		raise Exception('No GPS data found. Please wait for GPS to connect to satellites.')


def get_gps_message(gps_serial, message_type='$GPRMC'):
	gps_line = ''
	
	while not gps_line.startswith(message_type):
		gps_line = gps_serial.readline().decode('unicode_escape')

	return gps_line
