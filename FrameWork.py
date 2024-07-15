from machine import Pin,I2C,ADC,Timer
import network
import socket
import utime
import sgp30
import dht

co2para = 0
tvocpara = 0
temppara = 0
humpara = 0
soilpara = 0

#air sensor
air_sda = Pin(6)
air_scl = Pin(7)
air_i2cl = I2C(1,sda=air_sda,scl=air_scl)
air_sgp3O = sgp30.SGP30(air_i2cl)
air_sgp3O.iaq_init()

#temp and humidity sensor
dht = dht.DHT11(Pin(0))

#soil sensor
adc = ADC(Pin(26))

# You need to import dht library and upload sgp30 driver file. 
ssid = 'CPE-EEF4'
password = '12345678'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
wifi_status = network.WLAN(network.STA_IF)

def wificonnect():
    wifi_status.active(True)
    wifi_status.connect(ssid, password)
    utime.sleep(2)
    # check wifi connected
    while wifi_status.isconnected() == False:
       print('Wifi lost connect...')
       utime.sleep(1)
    print('Wifi connect successful')
    print(wifi_status.ifconfig())
    
def measure(timer):
    global co2para,tvocpara,temppara,humpara,soilpara
    # air sensor data
    co2para,tvocpara = air_sgp3O.iaq_measure()
    # temp and humidity data
    dht.measure()
    temppara = dht.temperature()
    humpara = dht.humidity()
    # soil sensor data
    soilpara = adc.read_u16()
    
def web_page(co2para,tvocpara,temppara,humpara,soilpara):
    html = """<html>
 <meta http-equiv="refresh" content="1"; URL="192.168.1.164">
 <head> <title>BIT Web Server</title> <meta name="viewport" content="width=device-width, initial-scale=1">
 <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
 h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}</style></head><body> <h1>LED Dashboard</h1>
 <p>CO2eq: <strong>"""+str(co2para)+"ppm"+"""</strong></p><p>TVOC:<strong>"""+str(tvocpara)+"""</p>
 <p>Temperature:<strong>"""+str(temppara)+"C"+"""</p>
 <p>Humidity:<strong>"""+str(humpara)+"%"+"""</p>
<p>Soil Moisture:<strong>"""+str(soilpara)+"%"+"""</p>
 </body></html>"""
    return html
tim0 = Timer(mode=Timer.PERIODIC, period=1000,callback=measure)

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    wifi_status = network.WLAN(network.STA_IF)
    wificonnect()
    s.bind(('', 80))
    s.listen(5)
    while True:
       conn, addr = s.accept()
       print('Connection: %s' % str(addr))
       req = conn.recv(1024)
       req = str(req)
       print('Connect = %s' % req)
       response = web_page(co2para,tvocpara,temppara,humpara,soilpara)
       conn.send('HTTP/1.1 200 OK\n')
       conn.send('Content-Type: text/html\n')
       conn.send('Connection: close\n\n')
       conn.sendall(response)
       conn.close()
    timer0.deinit()
if __name__ == "__main__":
    main()

