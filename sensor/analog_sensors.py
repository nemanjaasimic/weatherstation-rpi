import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import RPi.GPIO as GPIO
import sensor.gpio_pinout as gpio_pinout
import time

SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# Software SPI configuration:
# CLK  = 31
# MISO = 29
# MOSI = 18
# CS   = 16
# mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

R_TOP = 1000.0       # sensor output -> ADC input
R_BOTTOM = 2000.0    # ADC input -> GND

MCP_VREF = 3.3
MAX_SENSOR_V = 5.0
MAX_WIND_MPS = 60.0  

def get_wind_speed():
    adc = mcp.read_adc(0)

    v_adc = (adc / 1023.0) * 3.3

    divider_ratio = R_BOTTOM / (R_TOP + R_BOTTOM)
    v_sensor = v_adc / divider_ratio

    # Clamp voltage
    v_sensor = max(0.0, min(5.0, v_sensor))

    wind_speed = (v_sensor / 5.0) * 60.0

    return round(wind_speed, 3)

 
def get_uv_intensity():
    GPIO.output(gpio_pinout.ML_8511_UV_POWER_PIN, True)
    time.sleep(1)

    uv_intensity = [0]*5
    for i in range(5):
        uv_intensity_measured = mcp.read_adc(1)
        # 0-1023 = 0-3.3v
        # 310 = 1V --> min uv of 0 (mW/cm^2)
        # 885 = 2.85V --> max uv of 15 (mW/cm^2)
        # scaling real_value = measured_value - 310 which means offset is [0-575]
        uv_intensity[i] = (uv_intensity_measured - 310) / 575 * 15
        time.sleep(0.5)


    uv_intensity = round(sum(uv_intensity) / len(uv_intensity), 2)

    GPIO.output(gpio_pinout.ML_8511_UV_POWER_PIN, False)

    if uv_intensity < 0:
        uv_intensity = 0

    return uv_intensity
