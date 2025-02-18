# BreakingCircuits - FLASHEAR MICROPYTHON EN ESP32(s2 mini)


## REQUISITOS DE INSTALACIÓN 📖

1º Para tener micropython en el esp32 primeramente deberemos tener python instalado en el ordenador.

	https://www.python.org/downloads/](https://www.python.org/downloads/)

2º Instalaremos la herramienta “ESPTOOL” con pip para poder comunicarnos con nuestro esp32 para flashearla e instalar micropython en ella

```
D:\ESP32> pip install esptool

	Collecting esptool
  Downloading esptool-4.8.1.tar.gz (409 kB)
  Installing build dependencies ... done
  Getting requirements to build wheel ... done
  Preparing metadata (pyproject.toml) ... done
  ...
```

3º Nos descargamos el último archivo que haya salido con extensión .uf2 de Micropython que posteriormente instalaremos en la esp32s2
	[https://downloads.circuitpython.org/bin/lolin_s2_mini/es/adafruit-circuitpython-lolin_s2_mini-es-9.2.4.bin](https://downloads.circuitpython.org/bin/lolin_s2_mini/es/adafruit-circuitpython-lolin_s2_mini-es-9.2.4.bin "https://downloads.circuitpython.org/bin/lolin_s2_mini/es/adafruit-circuitpython-lolin_s2_mini-es-9.2.4.bin")



## FLASHEAR LA TARJETA 📸💳
1º Conectamos la tarjeta al ordenador

	https://github.com/espressif/esp-win-usb-drivers/releases

2º Pondremos el modo Download en la tarjeta:
	Mantén presionado el botón BOOT y mientras presionas el BOOT, pulsa y suelta el otro botón RESET y por último, suelta el botón BOOT.

3º Nos dirigimos a administrador de dispositivos, comprobamos que aparece el esp32 en el puerto COM

	Si aparece en Otros dispositivos con un triángulo amarillo: 
		- 1º Identifica si es placa china o real de silicon labs
		- 2º a)  Descarga el CH340 si es china [https://www.wch-ic.com/search?q=CH340&t=downloads]
		- 2º b) Descarga el CP210 si es de silabs [https://www.silabs.com/developer-tools/usb-to-uart-bridge-vcp-drivers?tab=downloads]
		- 3º Pulsa en administración de dispositivos y actualiza el controlador del esp32 y selecciona el que te hayas instalado.	

4º Confirmamos que tenemos esptool en la terminal utilizando:
	
```
D:\ESP32> esptool -h

usage: esptool [-h]
[--chip {auto,esp8266,esp32,esp32s2,esp32s3beta2,esp32s3,esp32c3,esp32c6beta,esp32h2beta1,esp32h2beta2,esp32c2,esp32c6,esp32c61,esp32c5,esp32c5beta3,esp32h2,esp32p4}]
...
```


5º  Borramos lo que haya dentro del ESP32 primeramente: (recuerda que debes poner el puerto que te salga a ti en administración de dispositivos) 

```
D:\ESP32> esptool --port COM3 --baud 460800 erase_flash

esptool.py v4.8.1
Serial port COM3
Connecting....
Detecting chip type... Unsupported detection protocol, switching and trying again...
Detecting chip type... ESP32-S2
Chip is ESP32-S2FNR2 (revision v0.0)
Features: WiFi, Embedded Flash 4MB, Embedded PSRAM 2MB, ADC and temperature sensor calibration in BLK2 of efuse V2
Crystal is 40MHz
MAC: 70:04:1d:fe:e1:30
Uploading stub...
Running stub...
Stub running...
Erasing flash (this may take a while)...
Chip erase completed successfully in 17.1s
```

6º Instalamos el CircuitPython con el archivo que hemos descargado anteriormente junto a el siguiente comando

```
D:\ESP32> esptool --port COM3 --baud 460800 write_flash -z 0x0 [la ruta y tu fichero]

esptool.py v4.8.1
Serial port COM3
Connecting...
Detecting chip type... Unsupported detection protocol, switching and trying again...
Detecting chip type... ESP32-S2
Chip is ESP32-S2FNR2 (revision v0.0)
Features: WiFi, Embedded Flash 4MB, Embedded PSRAM 2MB, ADC and temperature sensor calibration in BLK2 of efuse V2
Crystal is 40MHz
MAC: 70:04:1d:fe:e1:30
Uploading stub...
Running stub...
Stub running...
Changing baud rate to 460800
Changed.
Configuring flash size...
Flash will be erased from 0x00001000 to 0x002b4fff...
Compressed 2832896 bytes to 1046858...
Wrote 2832896 bytes (1046858 compressed) at 0x00001000 in 43.3 seconds (effective 523.8 kbit/s)...
Hash of data verified.

Leaving...
```

7º Una vez instalado, reiniciaremos la placa pulsando el botón rst, se iluminará de color azul la placa y lo detectará el ordenador para poder insertar los ficheros correctamente.
## ⚠ POSIBLES FALLOS ⚠
- EN CASO DE NO APARECER EN EL ADMINISTRADOR DE DISPOSITIVOS:
	- MANTÉN PRESIONADO EL BOTÓN BOOT (O), Y MIENTRAS LO PRESIONAS, PULSA Y SUELTA EL OTRO BOTÓN RESET Y POSTERIORMENTE SUELTA EL BOTÓN BOOT

- EN CASO DE QUE APAREZCA EN EL ADMINISTRADOR DE DISPOSITIVOS COMO "Otros dispositivos":
	-  Instalar drivers de tu sistema operativo de la tarjeta: https://www.silabs.com/developer-tools/usb-to-uart-bridge-vcp-drivers?tab=downloads

- EN CASO DE QUE AL BORRAR  O FLASHEAR APAREZCA EL SIGUIENTE MENSAJE NO PASA NADA, SE EJECUTA CORRECTAMENTE IGUAL:

```
Error: ESP32-S2FNR2 (revision v0.0) chip was placed into download mode using GPIO0.
esptool.py can not exit the download mode over USB. To run the app, reset the chip manually.
To suppress this note, set --after option to 'no_reset'.
```

- INSTALAR EL FICHERO .bin, no .uf2

# TODO
- [ ] Add code (to the presentation too)
- [ ] Add drivers
- [ ] Python/pip .exe
- [ ] Esptool.py
- [ ] Add firmware