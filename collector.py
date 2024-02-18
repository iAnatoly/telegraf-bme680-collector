#!/home/avi/src/BME68X_Environmental_Sensor_code/RaspberryPi/Python/test/bin/python3

import bme680
import time
from telegraf.client import TelegrafClient

try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except (RuntimeError, IOError):
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

client = TelegrafClient(host='192.168.1.32', port=8092)

# These oversampling settings can be tweaked to
# change the balance between accuracy and noise in
# the data.

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

# Up to 10 heater profiles can be configured, each
# with their own temperature and duration.
# sensor.set_gas_heater_profile(200, 150, nb_profile=1)
# sensor.select_gas_heater_profile(1)

try:
    while True:
        if sensor.get_sensor_data():
            metric_data = { 
                'temp': sensor.data.temperature, 
                'pressure': sensor.data.pressure, 
                'humidity': sensor.data.humidity, 
                'gas_index': sensor.data.gas_index, 
                'gas_resistance': sensor.data.gas_resistance
            }; 
            client.metric('bme680', metric_data, tags={'server_name': 'zero-x'})
        else:
            print("failed to read metrics from the sensor; will try again in 10s")
            time.sleep(10)
            continue

        time.sleep(20)

except KeyboardInterrupt:
    pass
