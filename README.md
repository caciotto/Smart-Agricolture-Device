# Smart-Agricolture-Device
In this experiment, we use the Pico W microcontroller and environmental sensors. The goal is to monitor environmental conditions and display the sensor data on a webpage hosted by the Pico W.

Here's a summary of the process:
1. Set Up Sensors: Connect environmental sensors to the Pico W.
2. Configure Timer: Use the Timer to periodically read sensor data. The Timer acts like an alarm, triggering an Interrupt Service Routine (ISR) to handle tasks at set intervals.
3. Host Webpage: Display the sensor data on a webpage hosted by the Pico W.

We are going to use:
- DHT11 Sensor (Temperature and Humidity sensor.)
- SR04 (Ultrasonic Distance Finder)
- SGP30 (Air Sensor)
- Soil Moisture Sensor (ADC-based)

You will find the Python code on the Framework.py file
The drivers to upload on the Picoboard for the SGP30 Air Sensor are in the sgp30.py file


