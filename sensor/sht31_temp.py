import board
import adafruit_sht31d


def get_temp_and_humidity_readings():
    try:
        i2c = board.I2C()
        sht_device = adafruit_sht31d.SHT31D(i2c)
        temp, humidity = 0, 0
        temp, humidity = get_measures(sht_device)
        return temp, humidity
    except Exception as error:
        raise error


def get_measures(sht_device):
    temp = sht_device.temperature
    humidity = sht_device.relative_humidity
    
    while sht_device.temperature == None or sht_device.humidity == None:
        try:
            sht_device._reset()
            temp = sht_device.temperature
            humidity = sht_device.relative_humidity
        except Exception as error:
            print("SHT31 Device not ready yet")
            continue
    return temp, humidity