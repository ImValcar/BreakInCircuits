# BreakingCircuits - FLASHEAR MICROPYTHON EN ESP32(s2 mini)


## REQUISITOS DE INSTALACIÓN 📖
1º Para tener micropython en el esp32 primeramente deberemos tener python instalado en el ordenador. 
[Python downloads](https://www.python.org/downloads/)

	
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

Tambien tenemos la opción de instalar esptool en nuestro OS


En el caso de linux:
```
$> sudo apt install esptool
```


3º Nos descargamos el último archivo que haya salido con extensión .bin de Micropython que posteriormente instalaremos en la esp32s2.
	[adafruit-circuitpython-lolin_s2_mini-es-9.2.4.bin](https://downloads.circuitpython.org/bin/lolin_s2_mini/es/adafruit-circuitpython-lolin_s2_mini-es-9.2.4.bin)



## FLASHEAR LA TARJETA 📸💳

1º Conectamos la tarjeta al ordenador, en caso de no detectarla podeis descargar los drivers en el siguiente enlace:
	https://github.com/espressif/esp-win-usb-drivers/releases

2º Pondremos el modo Download en la tarjeta:
	Mantén presionado el botón BOOT y mientras presionas el BOOT, pulsa y suelta el otro botón RESET, por último, suelta el botón BOOT.

3aº	WINDOWS
		  Nos dirigimos a administrador de dispositivos, comprobamos que aparece el esp32 en el puerto COM

	Si aparece en Otros dispositivos con un triángulo amarillo: 
		- 1º Identifica si es placa clon o real de silicon labs
		- 2º a) Descarga el CH340 si es clon [https://www.wch-ic.com/search?q=CH340&t=downloads]
		- 2º b) Descarga el CP210 si es de silabs [https://www.silabs.com/developer-tools/usb-to-uart-bridge-vcp-drivers?tab=downloads]
		- 3º Pulsa en administración de dispositivos y actualiza el controlador del esp32 y selecciona el que te hayas instalado.`

3bº LINUX
		
		
		
		
		
		
  - 3.1º Identificamos si reconoce la placa en nuestro equipo. Debe aparecer algo como esto:  
		 
 ```
$> lsusb

[...]
Bus 003 Device 010: ID XXXX Lolin S2 Mini
[...]
```

   - 3.2º Identificamos el puerto en el que está, en el ejemplo se encuentra en ttyACM0 como se puede observar: 
		
```
$> sudo dmesg | tail -30

[...]  
[77573.041149] usb 3-1: Product: S2 Mini
[77573.041151] usb 3-1: Manufacturer: Lolin
[77573.041153] usb 3-1: SerialNumber: 0856990F6740
[77573.049333] cdc_acm 3-1:1.0: ttyACM0: USB ACM device
[...]
```
4º Confirmamos que tenemos esptool en la terminal utilizando:
	
```
D:\ESP32> esptool -h

usage: esptool [-h]
[--chip {auto,esp8266,esp32,esp32s2,esp32s3beta2,esp32s3,esp32c3,esp32c6beta,esp32h2beta1,esp32h2beta2,esp32c2,esp32c6,esp32c61,esp32c5,esp32c5beta3,esp32h2,esp32p4}]
...
```


5º \[OPCIONAL\] Algo que se puede realizar es eliminar lo que haya dentro del ESP32 primeramente aunque si no habia nada  es probable que de error. En ese caso, no te preocupes: (recuerda sustituir &lt;COM_N&gt; por el puerto que te salga a ti en administración de dispositivos, COM3, COM5,ACM0,ACM1...) 

```
D:\ESP32> esptool --chip esp32s2 --port <PORT_COM> --baud 460800 erase_flash

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
D:\ESP32> esptool --chip esp32s2 --port <PORT_COM> --baud 460800 write_flash -z 0x0 [la ruta y tu fichero]

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


## INTRODUCIR LOS ARCHIVOS Y CORRER 📄🚀

Primero de todo debemos saber que el código se divide en dos carpetas,

	- Donde server es todo lo que utilizaremos para crear el servidor donde recibiremos y mandaremos las instrucciones
	- Y pycode, lo que corresponde con los archivos que tendremos que introducir al esp32

1º Introducimos los ficheros y carpetas de pycode en los ficheros del ESP32, donde los ficheros principales son el boot.py, el code.py y el settings.toml


2º Abrimos el settings.toml y cambiamos los parametros que vienen entre <> por los de nuestra red.


3aº En el caso de utilizar el `main.py` simplemente es lanzar el servidor y se pondrá a la escucha en el puerto 1337
	
	
	$> python3 main.py


3bº En el caso de utilizar un bot de discord tendremos que abrir el fichero .env que se encuentra en la carpeta y rellenarlo con los siguientes datos:


3b.1 - Tendremos que utilizar un token del bot
		`https://discord.com/developers/applications`
		<img src="https://github.com/user-attachments/assets/48b5621c-91ae-4d4e-a59b-b64649793625" alt="image" width="1146"   height="273"/>


3b.2- Nuestra IP 


3b.3 - El id del canal que va a enviar los datos 
		
	
		
<img width="402" height="504" alt="image" src="https://github.com/user-attachments/assets/146a41ec-9613-4de7-8088-ad309dd65a74" />


3b.4- procederemos a instalarnos la lista de requisitos 


3b.5 - Una vez hecho todo esto simplemente lanzaremos el bot de discord con 

		
	$> python3 discord_bot.py
		

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
