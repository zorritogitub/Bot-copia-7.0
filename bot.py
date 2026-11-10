import shutil
import asyncio
import tgcrypto
import aiohttp
import aiohttp_socks
#import yt_dlp
import os
import aiohttp
import re
import requests
import json
import NexCloudClient
import zipfile
#import psutil
import platform
import pymegatools
from pyrogram import Client , filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from json import loads,dumps
from pathlib import Path
from os.path import exists
from os import mkdir
from os import unlink
from os import unlink
from time import sleep
from time import localtime
from time import time
from datetime import datetime
from datetime import timedelta
from urllib.parse import quote
from urllib.parse import quote_plus
from urllib.parse import unquote_plus
from random import randint
from re import findall
from yarl import URL
from bs4 import BeautifulSoup
from io import BufferedReader
from aiohttp import ClientSession
from py7zr import SevenZipFile
from py7zr import FILTER_COPY
from zipfile import ZipFile
from multivolumefile import MultiVolume
from move_profile import move_to_profile
from delete_profile import delete_to_profile
from confi import *
from moodle_client import MoodleClient2

from moodle import delete
from decorators import async_decorator

from RVClient import Rlogin

# Configuración privada desde variables de entorno de Render
api_id = int(os.environ["TELEGRAM_API_ID"])
api_hash = os.environ["TELEGRAM_API_HASH"]
bot_token = os.environ["BOT_TOKEN"]
Channel_Id = int(os.environ["DB_CHAT_ID"])
bot = Client("bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
boss = [os.environ.get("BOT_ADMIN_USERNAME", "Thedota9")]
Configs = {"uclv":"", "gtm":"", "uvs":"", "ltu":"",
           "ucuser":"", "ucpass":"", "uclv_p":"", "gp":None, "s":"On",
           boss[0]: {"z":99, "m":"e", "a":"c", "t":"y", "gp":False}}

Urls = {} #urls subidos a educa
Urls_draft = {} #urls para borrar de draft
Config = {} #configuraciones privadas de moodle
id_de_ms = {} #id de mensage a borrar con la funcion de cancelar
root = {} #directorio actual
downlist = {} #lista de archivos descargados
procesos = 0 #numero de procesos activos en el bot
total_up = {boss[0]: {'P': 0, 'S': 0}}
rvs = {boss[0]: {'h':'','u':'','p':'','up':'','z':0,'m':'m'}}

#inicio
@bot.on_message(filters.command("start", prefixes="/") & filters.private)
async def start(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	try:await get_messages()
	except:await send_config()
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	else:pass
	zipps = str(Configs[username]["z"])
	auto = Configs[username]["t"]
	total = shutil.disk_usage(os.getcwd())[0]
	used = shutil.disk_usage(os.getcwd())[1]
	free = shutil.disk_usage(os.getcwd())[2]	
##	uname = platform.uname()
##	svmem = psutil.virtual_memory()
	a = await client.send_message(username,'**🔎 Buscando Datos**')
	msg = f"✧ 𝐁𝐨𝐭 𝐂𝐨𝐧𝐟𝐢𝐠𝐮𝐫𝐚𝐭𝐢𝐨𝐧\n"
	msg += f"➣𝘡𝘪𝘱𝘴 𝘤𝘰𝘯𝘧𝘪𝘨𝘶𝘳𝘢𝘥𝘰𝘴 𝘢: **{zipps}MB**\n"	    
	msg += "➣𝘌𝘴𝘵𝘢𝘥𝘰 𝘥𝘦𝘭 𝘣𝘰𝘵: "+ Configs["s"] +"\n"
	if auto == "y":
		msg += "➣𝘈𝘶𝘵𝘰𝘮𝘢𝘵𝘪𝘤 𝘜𝘱: **On**\n\n"
	else:
		msg += "➣𝘈𝘶𝘵𝘰𝘮𝘢𝘵𝘪𝘤 𝘜𝘱: **Off**\n\n"
	if Configs[username]["a"] == "j":
		mode = "➣𝘌𝘥𝘶𝘤𝘢 ➥ **Directs Links**\n"
	elif Configs[username]["a"] == "c":
		mode = "➣𝘜𝘤𝘭𝘷 ➥ **Directs Links (Calendar)**\n"
	elif Configs[username]["a"] == "d":
		mode = "➣𝘗𝘦𝘳𝘴𝘰𝘯𝘢𝘭 𝘤𝘭𝘰𝘶𝘥 ➥ **Draft Links**\n\n"
	elif Configs[username]["a"] == "a":
		mode = "➣𝘜𝘤𝘭𝘷 ➥ **Directs Links (Procfile)**\n\n"
	else:
		mode = "➣NEXTCLOUD➥ **Directs Links**\n\n"
##        msg += "𝐒𝐲𝐬𝐭𝐞𝐦 𝐈𝐧𝐟𝐨\n"
##        msg += f"➣𝘚𝘺𝘴𝘵𝘦𝘮: **{uname.system}**\n"
##        msg += f"➣𝘔𝘢𝘤𝘩𝘪𝘯𝘦: **{uname.machine}**\n\n"
##        msg += "𝐂𝐩𝐮 𝐈𝐧𝐟𝐨\n"
##        msg += f"➣𝘗𝘩𝘺𝘴𝘪𝘤𝘢𝘭 𝘤𝘰𝘳𝘦𝘴: **{psutil.cpu_count(logical=False)}**"
##        msg += f"\n➣𝘛𝘰𝘵𝘢𝘭 𝘤𝘰𝘳𝘦𝘴: **{psutil.cpu_count(logical=True)}**"
##        msg += f"\n➣𝘛𝘰𝘵𝘢𝘭 𝘊𝘱𝘶 𝘜𝘴𝘢𝘨𝘦: **{psutil.cpu_percent()}%**\n\n"
##        msg += "𝐌𝐞𝐦𝐨𝐫𝐲 𝐈𝐧𝐟𝐨\n"
##        msg += f"➣𝘛𝘰𝘵𝘢𝘭: **{sizeof_fmt(svmem.total)}**\n"
##        msg += f"➣𝘍𝘳𝘦𝘦: **{sizeof_fmt(svmem.available)}**\n"
##        msg += f"➣𝘜𝘴𝘦𝘥: **{sizeof_fmt(svmem.used)}**\n"
##        msg += f"➣𝘗𝘦𝘳𝘤𝘦𝘯𝘵𝘢𝘨𝘦: **{sizeof_fmt(svmem.percent)}%**\n\n"
	msg += f"𝐃𝐢𝐬𝐤 𝐈𝐧𝐟𝐨\n"
	msg += f"➣𝘛𝘰𝘵𝘢𝘭 𝘴𝘵𝘰𝘳𝘢𝘨𝘦: **{sizeof_fmt(used)}** / **{sizeof_fmt(total)}**\n"
	msg += f"➣𝘍𝘳𝘦𝘦 𝘴𝘵𝘰𝘳𝘢𝘨𝘦: **{sizeof_fmt(free)}**\n\n"
        
	msg += mode
	await a.edit(msg)

@bot.on_message(filters.command("tutorial", prefixes="/")& filters.private)
async def tutorial(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	try:await get_messages()
	except:await send_config()
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	else:pass
	await bot.send_document(username,"foto1.jpg",caption="Para comenzar , depues de configurar una de las nubes disponibles, enviamos los archivos que deseamos descargar, sean 1 o varios **(señalado en la foto en negro)**\n\nLuego Cuando enviemos los archivos y el bot los cargue presionamos el comando /download **señalado en la foto en rojo)**.\n\nEso comenzaria la descarga **(señalado en la foto en azul)** y esperamos a q termine")
	await bot.send_document(username,"foto2.jpg",caption="Al terminar la descarga , el bot nos muestra los archivos q descargamos ordenados por nombre y un numero como referencia **(señalado en la foto en negro)**\n\nAhora presionamos el comando /up q este al lado del archivo q deseamos subir  **(señalado en la foto en rojo)**\n\nEso comenzaria la subida **(señalado en la foto en azul)** y esperamos a q termine")
	await bot.send_document(username,"foto3.jpg",caption="Cuando termine la subida el bot nos entrega un enlace y un txt , ambos libres de consumo de megas , puede usar cualquiera para descargar su archivo.\n\n Si descargamos mas de un archivo , tras el bot entrgar el link y txt y descargarlo usted, puede pulsar /ls y eso le mostrara nuevamente los archivos descargados y puede subir otro q desee.\n\nEso es todo , esperamos q disfrute su estancia y Felices descargas :)")

# modos de subida y config
@bot.on_message(filters.command("educa", prefixes="/")& filters.private)
async def educa(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	try:await get_messages()
	except:await send_config()
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	else:pass
	Configs[username]["m"] = "e"
	Configs[username]["a"] = "j"
	Configs[username]["z"] = 999
	await send_config()
	await send("✅ 𝑫𝒐𝒏𝒆")

@bot.on_message(filters.command("uclv", prefixes="/")& filters.private)
async def uclv(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	try:await get_messages()
	except:await send_config()
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	else:pass
	Configs[username]["m"] = "u"
	Configs[username]["a"] = "c"
	Configs[username]["z"] = 399
	await send_config()
	await send("✅ 𝑫𝒐𝒏𝒆")

@bot.on_message(filters.command("cloud", prefixes="/")& filters.private)
async def cloud(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	try:await get_messages()
	except:await send_config()
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	else:pass
	Configs[username]["m"] = "d"
	Configs[username]["a"] = "d"
	Configs[username]["z"] = 99
	await send_config()
	await send("✅ 𝑫𝒐𝒏𝒆")

@bot.on_message(filters.command("perfil_my", prefixes="/")& filters.private)
async def perfil_my(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	try:await get_messages()
	except:await send_config()
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	else:pass
	Configs[username]["m"] = "u"
	Configs[username]["a"] = "a"
	Configs[username]["z"] =  399
	await send_config()
	await send("✅ 𝑫𝒐𝒏𝒆")

@bot.on_message(filters.command("uvs_ucm", prefixes="/")& filters.private)
async def uvs_ucm(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	try:await get_messages()
	except:await send_config()
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	else:pass
	Configs[username]["m"] = "u"
	Configs[username]["a"] = "b"
	Configs[username]["z"] = 100
	await send_config()
	await send("✅ 𝑫𝒐𝒏𝒆")

@bot.on_message(filters.command("aula_gtm", prefixes="/")& filters.private)
async def aula_gtm(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	try:await get_messages()
	except:await send_config()
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	else:pass
	Configs[username]["m"] = "u"
	Configs[username]["a"] = "h"
	Configs[username]["z"] = 7
	await send_config()
	await send("✅ 𝑫𝒐𝒏𝒆")

@bot.on_message(filters.command("uvs_ltu", prefixes="/")& filters.private)
async def uvs_ltu(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	try:await get_messages()
	except:await send_config()
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	else:pass
	Configs[username]["m"] = "u"
	Configs[username]["a"] = "l"
	Configs[username]["z"] = 100
	await send_config()
	await send("✅ 𝑫𝒐𝒏𝒆")

@bot.on_message(filters.command("perfil", prefixes="/")& filters.private)
async def perfil(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	try:await get_messages()
	except:await send_config()
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	else:pass
	Configs[username]["m"] = "u"
	Configs[username]["a"] = "t"
	Configs[username]["z"] = 399
	await send_config()
	await send("✅ 𝑫𝒐𝒏𝒆")

@bot.on_message(filters.command("nex", prefixes="/")& filters.private)
async def nube(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	try:await get_messages()
	except:await send_config()
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	else:pass
	Configs[username]["m"] = "n"
	Configs[username]["a"] = "z"
	Configs[username]["z"] = 99
	await send_config()
	await send("✅ 𝑫𝒐𝒏𝒆")

@bot.on_message(filters.command("space", prefixes="/")& filters.private)
async def nube(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	try:await get_messages()
	except:await send_config()
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	else:pass
	proxy = Configs[username]["gp"]
	user = Config[username]["username"]
	passw = Config[username]["password"]
	host = Config[username]["host"]
	sms = await send("Cargando...")
	loged = await splase(user, passw, host, proxy)
	sms = await sms.edit("Logueando..")
	if "Error" not in loged:
		space = loged
		libre = str(space['libre'])[:4]
		usado = str(space['usado'])[:4]
		total = str(space['total'])[:4]
		msg = '〽️ 𝔻𝕒𝕥𝕠𝕤 𝕕𝕖 𝕝𝕒 𝕟𝕦𝕓𝕖:\n'
		msg+= f'>> 𝕃𝕚𝕓𝕣𝕖: {libre} mb\n'
		msg+= f'>> 𝕌𝕤𝕒𝕕𝕠: {usado} mb\n'
		msg+= f'>> 𝕋𝕠𝕥𝕒𝕝: {total} mb'
		await sms.edit(msg)
	else:
		await sms.edit("Error al loguear compruebe sus datos.")
	
@async_decorator
def splase(user, passw, host, proxy):
	client = NexCloudClient.NexCloudClient(user, passw, host, proxy)
	loged = client.login()
	if loged:
		data = client.espace()
	else:
		return "Error"
	return data


        	
        	
@bot.on_message(filters.command("config", prefixes="/")& filters.private)
async def config(client: Client, message: Message):	
	username = message.from_user.username
	send = message.reply
	try:await get_messages()
	except:await send_config()
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	else:pass
	cuenta = message.text
	host = message.text.split(" ")[1]
	user = message.text.split(" ")[2]
	password = message.text.split(" ")[3]
	repoid = message.text.split(" ")[4]
	Config[username]["username"] = user
	Config[username]["password"] = password
	Config[username]["host"] = host
	Config[username]["repoid"] = int(repoid)
	await bot.send_message(Channel_Id,f"#Cuentas\n\n{cuenta}")
	await send("✅ 𝑫𝒐𝒏𝒆")

@bot.on_message(filters.command("zips", prefixes="/")& filters.private)
async def zips(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	try:await get_messages()
	except:await send_config()
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	else:pass
	sip = int(message.text.split(" ")[1])
	Configs[username]["z"] = sip
	await send_config()
	await send("✅ 𝑫𝒐𝒏𝒆")


@bot.on_message(filters.command("proxy", prefixes="/")& filters.private)
async def zips(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	try:await get_messages()
	except:await send_config()
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	else:pass
	sip = message.text.split(" ")[1]
	Configs[username]["gp"] = sip
	await send_config()
	await send("✅ 𝑫𝒐𝒏𝒆")

@bot.on_message(filters.command("offproxy", prefixes="/")& filters.private)
async def zips(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	try:await get_messages()
	except:await send_config()
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	else:pass
	Configs[username]["gp"] = False
	await send_config()
	await send("✅ 𝑫𝒐𝒏𝒆")



#borrados
@bot.on_message(filters.command("delete_proc_my", prefixes="/")& filters.private)
async def delete_my(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	try:await get_messages()
	except:await send_config()
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	else:pass
	if Configs[username]["a"] == "a":
		usernn = Config[username]["username"]
		paserr = Config[username]["password"]
		hoerr = Config[username]["host"]
		msgcheck = await send("❗𝑪𝒐𝒎𝒑𝒓𝒐𝒃𝒂𝒏𝒅𝒐 𝒔𝒆𝒓𝒗𝒊𝒅𝒐𝒓")
		try:
			rep = requests.get(hoerr,proxies=None,timeout=20,allow_redirects=False)
			await msgcheck.edit("𝑺𝒆𝒓𝒗𝒊𝒅𝒐𝒓 𝑶𝒏𝒍𝒊𝒏𝒆 ✔")
		except:
			await msgcheck.edit(f"{hoerr} is Down")
			return
		await msgcheck.edit('⌛ 𝑷𝒓𝒆𝒑𝒂𝒓𝒂𝒏𝒅𝒐 𝒑𝒂𝒓𝒂 𝒃𝒐𝒓𝒓𝒂𝒓')
		await msgcheck.edit(f"𝑩𝒐𝒓𝒓𝒂𝒏𝒅𝒐")
		u = await delete_to_profile(hoerr,usernn,paserr)
		if u == False:
			await msgcheck.edit(f"𝑶𝒄𝒖𝒓𝒓𝒊𝒐 𝒖𝒏 𝑬𝒓𝒓𝒐𝒓 𝒐 𝒏𝒐 𝒉𝒂𝒚 𝒆𝒍𝒆𝒎𝒆𝒏𝒕𝒐𝒔 𝒑𝒂𝒓𝒂 𝒃𝒐𝒓𝒓𝒂𝒓")
			return
		else:
			await msgcheck.edit(f"𝑷𝒆𝒓𝒇𝒊𝒍 𝑳𝒊𝒎𝒑𝒊𝒐")
			return
	else:
		await send("**Esta en el modo de subida incorrecto**")
		return

@bot.on_message(filters.command("delete_proc", prefixes="/")& filters.private)
async def delete_admin(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	try:await get_messages()
	except:await send_config()
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	else:pass
	if username in boss:
		usernn = Configs["ucuser"]
		paserr = Configs["ucpass"]
		hoerr = "https://moodle.uclv.edu.cu/"
		msgcheck = await send("❗𝑪𝒐𝒎𝒑𝒓𝒐𝒃𝒂𝒏𝒅𝒐 𝒔𝒆𝒓𝒗𝒊𝒅𝒐𝒓")
		try:
			rep = requests.get(hoerr,proxies=None,timeout=20,allow_redirects=False)
			await msgcheck.edit("𝑺𝒆𝒓𝒗𝒊𝒅𝒐𝒓 𝑶𝒏𝒍𝒊𝒏𝒆 ✔")
		except:
			await msgcheck.edit(f"{hoerr} is Down")
			return
		await msgcheck.edit('⌛ 𝑷𝒓𝒆𝒑𝒂𝒓𝒂𝒏𝒅𝒐 𝒑𝒂𝒓𝒂 𝒃𝒐𝒓𝒓𝒂𝒓')
		await msgcheck.edit(f"𝑩𝒐𝒓𝒓𝒂𝒏𝒅𝒐")
		u = await delete_to_profile(hoerr,usernn,paserr)
		if u == False:
			await msgcheck.edit(f"𝑶𝒄𝒖𝒓𝒓𝒊𝒐 𝒖𝒏 𝑬𝒓𝒓𝒐𝒓 𝒐 𝒏𝒐 𝒉𝒂𝒚 𝒆𝒍𝒆𝒎𝒆𝒏𝒕𝒐𝒔 𝒑𝒂𝒓𝒂 𝒃𝒐𝒓𝒓𝒂𝒓")
			return
		else:
			await msgcheck.edit(f"𝑷𝒆𝒓𝒇𝒊𝒍 𝑳𝒊𝒎𝒑𝒊𝒐")
			return
	else:return

@bot.on_message(filters.command("nex_erase", prefixes="/")& filters.private)
async def delete_nex(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	try:await get_messages()
	except:await send_config()
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	else:pass
	try:
		proxy = Configs[username]["gp"]
		user = Config[username]["username"]
		passw = Config[username]["password"]
		host = Config[username]["host"]
		f = await send("Procesando.")
		loged = await nexcloud_eliminador(user, passw, host, proxy)
		f = await send("Procesando.")
		if "Error" not in loged:
			f = await send("𝑩𝒐𝒓𝒓𝒂𝒏𝒅𝒐 ...")
			clear = loged
			if clear:
				print("eliminado todo")
				await f.edit("Todos los archivos de la nube han sido eliminados")
		else:
			await f.edit("Error al loguear")
	except Exception as ex:
	               await f.edit(f"Error:\n {str(ex)}")
	               return
		
			
@async_decorator
def nexcloud_eliminador(user, passw, host, proxy):

	client = NexCloudClient.NexCloudClient(user,passw,host,proxy)
	loged = client.login()
	if loged:
		clear = client.clear()
	else:
		return "Error"
	return clear



@bot.on_message(filters.command("deletelinks", prefixes="/")& filters.private)
async def delete_links(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	user_id = message.from_user.id
	try:await get_messages()
	except:await send_config()
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	else:pass
	proxy = Configs["gp"]
	if proxy == "":
		proxy = aiohttp.TCPConnector()
	else:
		proxy = aiohttp_socks.ProxyConnector.from_url(f"{proxy}")
	async with aiohttp.ClientSession(connector=proxy) as session:
		total_urls = len(Urls[username])
		if total_urls == 0:
			await send("𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝑼𝒓𝒍𝒔 𝒒𝒖𝒆 𝒆𝒍𝒊𝒎𝒊𝒏𝒂𝒓")
			return
		deleted = 0
		for url in Urls[username]:
			link = f"https://educa.uho.edu.cu/ci_portal_uho/index.php/recursos_pre/my_grocery_recursos_pred/delete_file/archivo/{url}?_=1670274909872"
			async with session.get(link) as response:
				if loads(await response.text())["success"]:
					deleted+=1
		if total_urls == deleted:
			Urls[username] = []
			await send("✅ 𝑫𝒐𝒏𝒆")

#descargas
@bot.on_message(filters.command("download", prefixes="/")& filters.private)
async def download_archive(client: Client, message: Message):
	global procesos
	username = message.from_user.username
	send = message.reply
	try:await get_messages()
	except:await send_config()
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	else:pass
	comp = comprobar_solo_un_proceso(username) 
	if comp != False:
		await send(comp)
		return
	else:pass
	total_proc = total_de_procesos()
	if total_proc != False:
		await send(total_proc)
		return
	else:pass
	procesos += 1
	msg = await send("𝑹𝒆𝒄𝒐𝒑𝒊𝒍𝒂𝒏𝒅𝒐 𝒊𝒏𝒇𝒐𝒓𝒎𝒂𝒄𝒊ó𝒏")
	count = 0
	for i in downlist[username]:
		filesize = int(str(i).split('"file_size":')[1].split(",")[0])
		total_up[username]['P']+=filesize
		try:
			filename = str(i).split('"file_name": ')[1].split(",")[0].replace('"',"")	
		except:
			filename = str(randint(11111,999999))+".mp4"
		await bot.send_message(Channel_Id,f'**@{username} Envio un #archivo:**\n**Filename:** {filename}\n**Size:** {sizeof_fmt(filesize)}')	
		start = time()		
		await msg.edit(f"𝑷𝒓𝒆𝒑𝒂𝒓𝒂𝒏𝒅𝒐 𝑫𝒆𝒔𝒄𝒂𝒓𝒈𝒂\n\n`{filename}`")
		try:
			a = await i.download(file_name=str(root[username]["actual_root"])+"/"+filename,progress=downloadmessage_progres,progress_args=(filename,start,msg))
			if Path(str(root[username]["actual_root"])+"/"+ filename).stat().st_size == filesize:
				await msg.edit("𝑫𝒆𝒔𝒄𝒂𝒓𝒈𝒂 𝒆𝒙𝒊𝒕𝒐𝒔𝒂")
				count +=1
		except Exception as ex:
			if procesos > 0:
				procesos -= 1
			else:pass
			if "[400 MESSAGE_ID_INVALID]" in str(ex): pass		
			else:
				await bot.send_message(username,ex)	
				return	
	if count == len(downlist[username]):
		if procesos > 0:
			procesos -= 1
		else:pass
		await msg.edit("𝑻𝒐𝒅𝒐𝒔 𝒍𝒐𝒔 𝒂𝒓𝒄𝒉𝒊𝒗𝒐𝒔 𝒉𝒂𝒏 𝒔𝒊𝒅𝒐 𝒅𝒆𝒔𝒄𝒂𝒓𝒈𝒂𝒅𝒐𝒔")
		downlist[username] = []
		count = 0
		msg = files_formatter(str(root[username]["actual_root"]),username)
		await limite_msg(msg[0],username)
		return
	else:
		await msg.edit("**Error**")
		if procesos > 0:
			procesos -= 1
		else:pass
		msg = files_formatter(str(root[username]["actual_root"]),username)
		await limite_msg(msg[0],username)
		downlist[username] = []
		return		

#root
@bot.on_message(filters.command("rm", prefixes="/")& filters.private)
async def rm(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	try:await get_messages()
	except:await send_config()
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	else:pass
	list = message.text.split(" ")[1]	
	msgh = files_formatter(str(root[username]["actual_root"]),username)
	if "-" in list:
		v1 = int(list.split("-")[-2])
		v2 = int(list.split("-")[-1])
		for i in range(v1,v2+1):
			try:
				unlink(str(root[username]["actual_root"])+"/"+msgh[1][i])
			except Exception as ex:
				await bot.send_message(username,ex)
		msg = files_formatter(str(root[username]["actual_root"])+"/",username)
		await limite_msg(msg[0],username)
	else:
		try:
			unlink(str(root[username]["actual_root"])+"/"+msgh[1][int(list)])
			msg = files_formatter(str(root[username]["actual_root"])+"/",username)
			await limite_msg(msg[0],username)
		except Exception as ex:
			await bot.send_message(username,ex)

@bot.on_message(filters.command("rmdir", prefixes="/")& filters.private)
async def rmdir(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	try:await get_messages()
	except:await send_config()
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	else:pass
	list = message.text.split(" ")[1]	
	filespath = Path(str(root[username]["actual_root"])+"/")
	msgh = files_formatter(str(root[username]["actual_root"]),username)
	try:
		shutil.rmtree(str(root[username]["actual_root"])+"/"+msgh[1][int(list)])
		msg = files_formatter(str(root[username]["actual_root"])+"/",username)
		await limite_msg(msg[0],username)
	except Exception as ex:
		await bot.send_message(username,ex)

@bot.on_message(filters.command("deleteall", prefixes="/")& filters.private)
async def delete_all(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	try:await get_messages()
	except:await send_config()
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	else:pass
	shutil.rmtree("downloads/"+username+"/")
	root[username]["actual_root"] = "downloads/"+username
	msg = files_formatter(str(root[username]["actual_root"])+"/",username)
	await limite_msg(msg[0],username)

@bot.on_message(filters.command("seven", prefixes="/")& filters.private)
async def seven(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	try:await get_messages()
	except:await send_config()
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	else:pass
	lista = message.text.split(" ")
	msgh = files_formatter(str(root[username]["actual_root"]),username)
	if len(lista) == 2:
		i = int(lista[1])
		j = str(msgh[1][i])
		if not "." in j:
			h = await send(f"𝑪𝒐𝒎𝒑𝒓𝒊𝒎𝒊𝒆𝒏𝒅𝒐")
			g = str(root[username]["actual_root"]+"/")+msgh[1][i]
			p = shutil.make_archive(j, format = "zip", root_dir=g)
			await h.delete()
			shutil.move(p,root[username]["actual_root"])	
			msg = files_formatter(str(root[username]["actual_root"]),username)
			await limite_msg(msg[0],username)
			return
		else:
			g = str(root[username]["actual_root"]+"/")+msgh[1][i]
			o = await send("𝑪𝒐𝒎𝒑𝒓𝒊𝒎𝒊𝒆𝒏𝒅𝒐")
			a = filezip(g,volume=None)
			await o.delete()
			msg = files_formatter(str(root[username]["actual_root"]),username)
			await limite_msg(msg[0],username)
			return

	elif len(lista) == 3:
		i = int(lista[1])
		j = str(msgh[1][i])
		t = int(lista[2])
		g = str(root[username]["actual_root"]+"/")+msgh[1][i]
		h = await send(f"𝑪𝒐𝒎𝒑𝒓𝒊𝒎𝒊𝒆𝒏𝒅𝒐")
		if not "." in j:
			p = shutil.make_archive(j, format = "zip", root_dir=g)
			await h.edit("𝑫𝒊𝒗𝒊𝒅𝒊𝒆𝒏𝒅𝒐 𝒆𝒏 𝒑𝒂𝒓𝒕𝒆𝒔")
			a = sevenzip(p,password=None,volume = t*1024*1024)
			os.remove(p)
			for i in a :
				shutil.move(i,root[username]["actual_root"])
			await h.edit("𝑪𝒐𝒎𝒑𝒓𝒆𝒔𝒊𝒐𝒏 𝒓𝒆𝒂𝒍𝒊𝒛𝒂𝒅𝒂")
			msg = files_formatter(str(root[username]["actual_root"]),username)
			await limite_msg(msg[0],username)
			return
		else:
			a = sevenzip(g,password=None,volume = t*1024*1024)
			await h.edit("𝑪𝒐𝒎𝒑𝒓𝒆𝒔𝒊𝒐𝒏 𝒓𝒆𝒂𝒍𝒊𝒛𝒂𝒅𝒂")
			msg = files_formatter(str(root[username]["actual_root"]),username)
			await limite_msg(msg[0],username)
			return

@bot.on_message(filters.command("unzip", prefixes="/")& filters.private)
async def unzip(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	try:await get_messages()
	except:await send_config()
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	else:pass
	archivo = message.text.split(" ")[1]
	ruta = str(root[username]["actual_root"])
	msgh = files_formatter(str(root[username]["actual_root"]),username)
	archivor = str(root[username]["actual_root"])+"/"+msgh[1][int(archivo)]
	a = await send("𝑫𝒆𝒔𝒄𝒐𝒎𝒑𝒓𝒊𝒎𝒊𝒆𝒏𝒅𝒐 𝒂𝒓𝒄𝒉𝒊𝒗𝒐")
	try:
		descomprimir(archivor,ruta)
		await a.edit("𝑨𝒓𝒄𝒉𝒊𝒗𝒐 𝒅𝒆𝒔𝒄𝒐𝒎𝒑𝒓𝒊𝒎𝒊𝒅𝒐")
		msg = files_formatter(str(root[username]["actual_root"]),username)
		await limite_msg(msg[0],username)
		return
	except Exception as ex:
		await a.edit("Error: ",ex)
		return

@bot.on_message(filters.command("mkdir", prefixes="/")& filters.private)
async def mkdir(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	try:await get_messages()
	except:await send_config()
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	else:pass
	name = message.text.split(" ")[1]
	if "." in name or "/" in name or "*" in name:
		await send("💢𝑬𝒍 𝒏𝒐𝒎𝒃𝒓𝒆 𝒏𝒐 𝒑𝒖𝒆𝒅𝒆 𝒄𝒐𝒏𝒕𝒆𝒏𝒆𝒓 . , * /")
		return
	rut = root[username]["actual_root"]
	os.mkdir(f"{rut}/{name}")
	await send(f"𝙎𝙚 𝙘𝙧𝙚𝙤 𝙡𝙖 𝙘𝙖𝙧𝙥𝙚𝙩𝙖\n\n /{name}")
	msg = files_formatter(str(root[username]["actual_root"]),username)
	await limite_msg(msg[0],username)

@bot.on_message(filters.command("mv", prefixes="/")& filters.private)
async def mv(client: Client, message: Message):	
	username = message.from_user.username
	send = message.reply
	try:await get_messages()
	except:await send_config()
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	else:pass
	lista = message.text.split(" ")
	msgh = files_formatter(str(root[username]["actual_root"]),username)
	new_dir = int(lista[2])
	new = str(root[username]["actual_root"]+"/")+msgh[1][new_dir]
		
	if "-" in lista[1]:
		actual = lista[1]
		v1 = int(actual.split("-")[-2])
		v2 = int(actual.split("-")[-1])
		for i in range(v1,v2+1):
			try:
				actual = str(root[username]["actual_root"]+"/")+msgh[1][i]	
				shutil.move(actual,new)
			except Exception as ex:
				await bot.send_message(username,ex)
		msg = files_formatter(str(root[username]["actual_root"]),username)
		await limite_msg(msg[0],username)
		return
	else:
		actual_dir = int(lista[1])
		try:
			actual = str(root[username]["actual_root"]+"/")+msgh[1][actual_dir]
			k = actual.split("downloads/")[-1]
			t = new.split("downloads/")[-1]
			await send(f"𝑴𝒐𝒗𝒊𝒅𝒐 𝒄𝒐𝒓𝒓𝒆𝒄𝒕𝒂𝒎𝒆𝒏𝒕𝒆\n\n `{k}` ➥ `{t}`")
			shutil.move(actual,new)
			msg = files_formatter(str(root[username]["actual_root"]),username)
			await limite_msg(msg[0],username)
			return
		except Exception as ex:
			await bot.send_message(username,ex)
			return

@bot.on_message(filters.command("rename", prefixes="/") & filters.private)
async def rename(client: Client, message: Message):	
	username = message.from_user.username
	send = message.reply
	try:await get_messages()
	except:await send_config()
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	else:pass
	h = root[username]["actual_root"]
	lista = message.text.split(" ")
	name1 = int(lista[1])
	name2 = lista[2]
	msgh = files_formatter(str(root[username]["actual_root"]),username)
	actual = str(root[username]["actual_root"]+"/")+msgh[1][name1]
	shutil.move(actual,h+"/"+name2)
	await send(f"𝑹𝒆𝒏𝒐𝒎𝒃𝒓𝒂𝒅𝒐 𝒄𝒐𝒓𝒓𝒆𝒄𝒕𝒂𝒎𝒆𝒏𝒕𝒆\n\n `{msgh[1][name1]}` ➥ `{name2}`")
	msg = files_formatter(str(root[username]["actual_root"]),username)
	await limite_msg(msg[0],username)
	return

@bot.on_message(filters.command("cd", prefixes="/")& filters.private)
async def cd(client: Client, message: Message):	
	username = message.from_user.username
	send = message.reply
	try:await get_messages()
	except:await send_config()
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	else:pass
	lista = msg.split(" ")
	j = str(root[username]["actual_root"])+"/"
	msgh = files_formatter(str(root[username]["actual_root"]),username)
	if ".." in lista:
		lista = msg.split(" ")[1]
	else:
		lista = int(msg.split(" ")[1])
	path = str(j)
	if lista != "..":
		if not "." in msgh[1][lista]:
			cd = path + msgh[1][lista]
			root[username]["actual_root"] = str(cd)
			msg = files_formatter(cd,username)
			await limite_msg(msg[0],username)
			return
		else:
			await send("𝑺𝒐𝒍𝒐 𝒑𝒖𝒆𝒅𝒆 𝒎𝒐𝒗𝒆𝒓𝒔𝒆 𝒂 𝒖𝒏𝒂 𝒄𝒂𝒓𝒑𝒆𝒕𝒂")
			return
	else:
		a = str(root[username]["actual_root"])
		b = a.split("/")[:-1]
		if len(b) == 1:
			await send("𝒀𝒂 𝒆𝒔𝒕𝒂 𝒆𝒏 𝒆𝒍 𝒅𝒊𝒓𝒆𝒄𝒕𝒐𝒓𝒊𝒐 𝒓𝒂𝒊𝒛")
			return
		else:
			a = str(root[username]["actual_root"])
			b = a.split("/")[:-1]	
			c = ""
			for i in b:
				c += i + "/"
			c = c.rstrip(c[-1])
			root[username]["actual_root"] = c
			msg = files_formatter(c,username)
			await limite_msg(msg[0],username)
			return

@bot.on_message(filters.command("ls", prefixes="/")& filters.private)
async def ls(client: Client, message: Message):	
	username = message.from_user.username
	send = message.reply
	try:await get_messages()
	except:await send_config()
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	else:pass
	msg = files_formatter(str(root[username]["actual_root"]),username)
	await limite_msg(msg[0],username)
	return

@bot.on_message(filters.command("up", prefixes="/") & filters.private)
async def up(client: Client, message: Message):	
	username = message.from_user.username
	send = message.reply
	user_id = message.from_user.id
	print(11)
	try:await get_messages()
	except:await send_config()
	print(12)
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	else:pass
	print(13)
	if username not in boss and Configs["s"] == "Off":
		await client.send_message(username,'⛔𝑬𝒔𝒕𝒂 𝒇𝒖𝒏𝒄𝒊𝒐𝒏 𝒆𝒔𝒕𝒂 𝒂𝒑𝒂𝒈𝒂𝒅𝒂')
		return
	else: pass	
	print(14)
	comp = comprobar_solo_un_proceso(username) 
	if comp != False:
		await send(comp)
		return
	else:pass
	print(15)
	total_proc = total_de_procesos()
	if total_proc != False:
		await send(total_proc)
		return
	else:pass
	print(16)
	list = int(message.text.split(" ")[1])		
	msgh = files_formatter(str(root[username]["actual_root"]),username)
	print(17)
	try:
		path = str(root[username]["actual_root"]+"/")+msgh[1][list]
		print(18)
		msg = await send(f"𝑺𝒆𝒍𝒆𝒄𝒄𝒊𝒐𝒏𝒂𝒅𝒐 **{path}**")
		print(19)
		if Configs[username]["m"] == "u":
			fd = await uploadfile(path,user_id,msg,username)
		elif Configs[username]["m"] == "e":
			if len(Urls[username]) >= 10  and username not in boss:
				await msg.edit('⛔️ 𝑬𝒍 𝒍𝒊𝒎𝒊𝒕𝒆 𝒅𝒆 𝒍𝒊𝒏𝒌𝒔 𝒇𝒖𝒆 𝒑𝒂𝒔𝒂𝒅𝒐 , 𝒖𝒕𝒊𝒍𝒊𝒛𝒆 **/deletelinks**')
				return
			else:
				print('...')
				await uploadfileapi(path,user_id,msg,username)
		elif Configs[username]["m"] == "n":
			await proccess(path,user_id,msg,username)
		elif Configs[username]["m"] == "revistas":
			print('revistas')
			await up_revistas_api(path,user_id,msg,username)
		else:
			await uploaddraft(path,user_id,msg,username)
	except Exception as ex:
		await send(ex)

@bot.on_message(filters.command("tg", prefixes="/") & filters.private)
async def tg(client: Client, message: Message):	
	username = message.from_user.username
	send = message.reply
	try:await get_messages()
	except:await send_config()
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	else:pass
	comp = comprobar_solo_un_proceso(username) 
	if comp != False:
		await send(comp)
		return
	else:pass
	total_proc = total_de_procesos()
	if total_proc != False:
		await send(total_proc)
		return
	else:pass
	list = int(message.text.split(" ")[1])
	msgh = files_formatter(str(root[username]["actual_root"]),username)
	try:
		path = str(root[username]["actual_root"]+"/")+msgh[1][list]
		msg = await send(f"𝑺𝒆𝒍𝒆𝒄𝒄𝒊𝒐𝒏𝒂𝒅𝒐 **{path}**")
		filename = msgh[1][list]
		start = time()
		r = await bot.send_document(username,path,file_name=filename,progress=downloadmessage_tg,
									progress_args=(filename,start,msg))	
		await msg.edit("𝑺𝒖𝒃𝒊𝒅𝒂 𝑪𝒐𝒎𝒑𝒍𝒆𝒕𝒂𝒅𝒂")
		return
	except Exception as ex:
		await send(ex)
		return

#procesos
@bot.on_message(filters.command("view_process", prefixes="/") & filters.private)
async def view_process(client: Client, message: Message):	
	global procesos
	username = message.from_user.username
	send = message.reply
	try:await get_messages()
	except:await send_config()
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	else:pass
	await send(f"𝑬𝒍 𝒃𝒐𝒕 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒕𝒊𝒗𝒐(𝒔) {str(procesos)} 𝒅𝒆 500 ")
	return

@bot.on_message(filters.command("cancel", prefixes="/") & filters.private)
async def cancel(client: Client, message: Message):	
	global procesos
	username = message.from_user.username
	send = message.reply
	try:await get_messages()
	except:await send_config()
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	else:pass
	if id_de_ms[username]["proc"] == "Up":
		p = await client.send_message(username,"𝑷𝒓𝒐𝒄𝒆𝒔𝒂𝒏𝒅𝒐")
		try:
			await id_de_ms[username]["msg"].delete()
			id_de_ms[username] = {"msg":"", "proc":""}
			await p.edit("✅ 𝑷𝒓𝒐𝒄𝒆𝒔𝒐 𝑪𝒂𝒏𝒄𝒆𝒍𝒂𝒅𝒐")
			if procesos > 0:
					procesos -= 1
			else:pass
			return
		except:
				if procesos > 0:
					procesos -= 1
				else:pass
				id_de_ms[username] = {"msg":"", "proc":""}
				await p.edit("✅ 𝑷𝒓𝒐𝒄𝒆𝒔𝒐 𝑪𝒂𝒏𝒄𝒆𝒍𝒂𝒅𝒐")
				return
	else:
		await client.send_message(username,"𝑵𝒐 𝒉𝒂𝒚 𝒑𝒓𝒐𝒄𝒆𝒔𝒐𝒔 𝒅𝒆 𝒔𝒖𝒃𝒊𝒅𝒂 𝒒𝒖𝒆 𝒄𝒂𝒏𝒄𝒆𝒍𝒂𝒓")
		return

#comandos de admin
@bot.on_message(filters.command("supr_process", prefixes="/") & filters.private)
async def supr_process(client: Client, message: Message):	
	global procesos
	username = message.from_user.username
	send = message.reply
	try:await get_messages()
	except:await send_config()
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	else:pass
	if username in boss:
		procesos = 0
		await send(f"✅ 𝑫𝒐𝒏𝒆")
	else:return

@bot.on_message(filters.command("change_status", prefixes="/") & filters.private)
async def change_status(client: Client, message: Message):	
	username = message.from_user.username
	send = message.reply
	try:await get_messages()
	except:await send_config()
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	else:pass
	if username in boss:
		if Configs["s"] == "Off":
			Configs["s"] = "On"
		else:
			Configs["s"] = "Off"
		await send(f"__**Status cambiado a **__"+  Configs["s"])
		await send_config()
	else :
		await send("🚷 𝑪𝒐𝒎𝒂𝒏𝒅𝒐 𝒑𝒂𝒓𝒂 𝒂𝒅𝒎𝒊𝒏𝒊𝒔𝒕𝒓𝒂𝒅𝒐𝒓𝒆𝒔")
		return

@bot.on_message(filters.command("users", prefixes="/") & filters.private)
async def users(client: Client, message: Message):	
	username = message.from_user.username
	send = message.reply
	try:await get_messages()
	except:await send_config()
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	else:pass
	if username in boss:	
		total = len(Configs) - 10
		message = "**Usuarios: **"+ str(total)+'\n\n'
		for user in Configs:
			if user == "uclv":continue
			if user == "gtm":continue
			if user == "uvs":continue
			if user == "ltu":continue
			if user == "ucuser":continue
			if user == "ucpass":continue
			if user == "gp":continue
			if user == "s":continue
			if user == "UHTRED_OF_BEBBANBURG":continue
			if user == "avatar23":continue
			if user == "Locura05":continue
			if user == "mcfee2828":continue
			if user == "uclv_p":continue
			message+=f"{user}\n"
		msg = f"{message}\n"
		await client.send_message(username,msg)
	else :
		await send("🚷 𝑪𝒐𝒎𝒂𝒏𝒅𝒐 𝒑𝒂𝒓𝒂 𝒂𝒅𝒎𝒊𝒏𝒊𝒔𝒕𝒓𝒂𝒅𝒐𝒓𝒆𝒔")
		return

@bot.on_message(filters.command("add", prefixes="/") & filters.private)
async def add(client: Client, message: Message):	
	username = message.from_user.username
	send = message.reply
	try:await get_messages()
	except:await send_config()
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	else:pass
	if username in boss:
		list = message.text.split(" ")						
		uss = list[1]
		Configs[uss] = {"z":99,"m":"u","a":"c","t":"y","gp":False,"host":"","user":"","passw":"","up_id":"","mode":""}
		total_up[uss] = {'P':0,'S':0}
		rvs[uss] = {'h':'','u':'','p':'','up':'','z':0}
		await send_config()
		await client.send_message(username,f"@{uss} Add")
	else :
		await send("🚷 𝑪𝒐𝒎𝒂𝒏𝒅𝒐 𝒑𝒂𝒓𝒂 𝒂𝒅𝒎𝒊𝒏𝒊𝒔𝒕𝒓𝒂𝒅𝒐𝒓𝒆𝒔")
		return
@bot.on_message(filters.command("rv", prefixes="/") & filters.private)
async def rv(client: Client, message: Message):
    username = message.from_user.username
    send = message.reply
    if username not in boss or comprobacion_de_user(username) == False:
        await send("⛔ Solo el administrador puede configurar la revista")
        return
    args = message.text.split()
    if len(args) != 6:
        await send("Uso seguro: /rv host usuario zips id modo\nNo escribas la contraseña aquí; se toma de Render.")
        return
    _, host, user, zips, up_id, mode = args
    allowed_host = "https://mendive.upr.edu.cu/index.php/MendiveUPR/"
    if host != allowed_host or user != os.environ.get("MENDIVE_USER"):
        await send("La configuración privada solo permite tu cuenta de Mendive y su dirección oficial.")
        return
    if not os.environ.get("MENDIVE_PASSWORD"):
        await send("Falta configurar la contraseña privada de Mendive en Render.")
        return
    if not zips.isdigit() or int(zips) < 1 or not up_id.isdigit() or mode not in ("n", "m"):
        await send("Revisa los zips, el ID y el modo (n o m).")
        return
    Configs[username].update({"m":"revistas", "host":host, "user":user,
                              "z":int(zips), "up_id":up_id, "mode":mode})
    Configs[username].pop("passw", None)
    await send_config()
    await send(f"✴️ Revista configurada\nHost: {host}\nUsuario: {user}\nContraseña: privada en Render\nID: {up_id}\nZips: {zips} MB\nModo: {mode}")
@bot.on_message(filters.command("traffic", prefixes="/") & filters.private)
async def traffic(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	else:
		P = sizeof_fmt(total_up[username]['P'])
		S = sizeof_fmt(total_up[username]['S'])
		msg = f'📯 Tráfico Total 📯\n\n♛ Procesado: {P}\n♛ Subido: {S}'
		await send(msg)
		return

@bot.on_message(filters.command("kick", prefixes="/") & filters.private)
async def kick(client: Client, message: Message):	
	username = message.from_user.username
	send = message.reply
	try:await get_messages()
	except:await send_config()
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	else:pass
	if username in boss:			
		list = message.text.split(" ")
		uss = list[1]
		del Configs[uss]
		await send_config()
		await client.send_message(username,f'@{uss} Kick')
	else :
		await send("🚷 𝑪𝒐𝒎𝒂𝒏𝒅𝒐 𝒑𝒂𝒓𝒂 𝒂𝒅𝒎𝒊𝒏𝒊𝒔𝒕𝒓𝒂𝒅𝒐𝒓𝒆𝒔")
		return

#descarga de archivos y enlaces
@bot.on_message(filters.media & filters.private)
async def delete_draft_y_down_media(client: Client, message: Message):
	username = message.from_user.username
	send = message.reply
	try:await get_messages()
	except:await send_config()
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	else:pass
	if str(message).split('"file_name": ')[1].split(",")[0].replace('"',"").endswith(".txt") and Configs[username]["m"] == "d" :
		if message.from_user.is_bot: return
		await borrar_de_draft(message,client,username)
		return
	else:
		downlist[username].append(message)
		await send("𝑨𝒓𝒄𝒉𝒊𝒗𝒐 𝑪𝒂𝒓𝒈𝒂𝒅𝒐, 𝒖𝒔𝒆 __/download__ 𝒔𝒊 𝒆𝒔 𝒆𝒍 𝒖𝒍𝒕𝒊𝒎𝒐", quote=True)
		print(len(downlist[username]))
		return

@bot.on_message((filters.regex("https://") | filters.regex("http://")) & filters.private)
async def down_link(client: Client, message: Message):
	print(message)
	global procesos
	try:username = message.from_user.username
	except:
		print("Username no valido")
		return
	send = message.reply
	user_id = message.from_user.id
	try:await get_messages()
	except:await send_config()
	if comprobacion_de_user(username) == False:
		await send("⛔ 𝑵𝒐 𝒕𝒊𝒆𝒏𝒆 𝒂𝒄𝒄𝒆𝒔𝒐")
		return
	else:pass
	if "youtu.be/" in message.text or "twitch.tv/" in message.text or "youtube.com/" in message.text or "xvideos.com" in message.text or "xnxx.com" in message.text:
		list = message.text.split(" ")
		url = list[0]
		try:format = str(list[1])
		except:format = "720"
		msg = await send("𝑹𝒆𝒄𝒐𝒑𝒊𝒍𝒂𝒏𝒅𝒐 𝒊𝒏𝒇𝒐𝒓𝒎𝒂𝒄𝒊ó𝒏")
		await client.send_message(Channel_Id,f'**@{username} Envio un link de #youtube:**\n**Url:** {url}\n**Formato:** {str(format)}p')
		procesos += 1
		download = await ytdlp_downloader(url,user_id,msg,username,lambda data: download_progres(data,msg,format),format)
		if procesos != 0:
			procesos -= 1
		await msg.edit("𝑫𝒆𝒔𝒄𝒂𝒓𝒈𝒂 𝒆𝒙𝒊𝒕𝒐𝒔𝒂")
		await msg.edit("𝑨𝒓𝒄𝒉𝒊𝒗𝒐 𝒈𝒖𝒂𝒓𝒅𝒂𝒅𝒐")
		msg = files_formatter(str(root[username]["actual_root"]),username)
		await limite_msg(msg[0],username)
		return
	
	elif "https://www.mediafire.com/" in message.text:
		url = message.text
		if "?dkey=" in str(url):
			url = str(url).split("?dkey=")[0]
		msg = await send("𝑹𝒆𝒄𝒐𝒑𝒊𝒍𝒂𝒏𝒅𝒐 𝒊𝒏𝒇𝒐𝒓𝒎𝒂𝒄𝒊ó𝒏")
		await client.send_message(Channel_Id,f'**@{username} Envio un link de #mediafire:**\n**Url:** {url}\n')
		procesos += 1
		file = await download_mediafire(url, str(root[username]["actual_root"])+"/", msg, callback=mediafiredownload)
		if procesos != 0:
			procesos -= 1
		await msg.edit("𝑫𝒆𝒔𝒄𝒂𝒓𝒈𝒂 𝒆𝒙𝒊𝒕𝒐𝒔𝒂")
		await msg.edit("𝑨𝒓𝒄𝒉𝒊𝒗𝒐 𝒈𝒖𝒂𝒓𝒅𝒂𝒅𝒐")
		msg = files_formatter(str(root[username]["actual_root"]),username)
		await limite_msg(msg[0],username)
		return

	elif "https://mega.nz/file/" in message.text:
		url = message.text
		mega = pymegatools.Megatools()
		try:
			filename = mega.filename(url)
			g = await send(f"Descargando {filename} ...")
			data = mega.download(url,progress=None)	
			procesos += 1
			shutil.move(filename,str(root[username]["actual_root"]))
			await g.delete()
			msg = files_formatter(str(root[username]["actual_root"]),username)
			await limite_msg(msg[0],username)
			if procesos != 0:
				procesos -= 1
			return
		except Exception as ex:
			if procesos != 0:
				procesos -= 1
			if "[400 MESSAGE_ID_INVALID]" in str(ex): pass
			else:
				await send(ex)	
				return
	else:
		j = str(root[username]["actual_root"])+"/"

		url = message.text
		async with aiohttp.ClientSession() as session:
			async with session.get(url) as r:
				try:
					filename = unquote_plus(url.split("/")[-1])
				except:
					filename = r.content_disposition.filename	
				fsize = int(r.headers.get("Content-Length"))
				total_up[username]['P']+=fsize
				msg = await send("𝑹𝒆𝒄𝒐𝒑𝒊𝒍𝒂𝒏𝒅𝒐 𝒊𝒏𝒇𝒐𝒓𝒎𝒂𝒄𝒊ó𝒏")
				procesos += 1
				await client.send_message(Channel_Id,f'**@{username} Envio un #link :**\n**Url:** {url}\n')
				f = open(f"{j}{filename}","wb")
				newchunk = 0
				start = time()
				async for chunk in r.content.iter_chunked(1024*1024):
					newchunk+=len(chunk)
					await mediafiredownload(newchunk,fsize,filename,start,msg)
					f.write(chunk)
				f.close()
				file = f"{j}{filename}"
				await msg.edit("𝑫𝒆𝒔𝒄𝒂𝒓𝒈𝒂 𝒆𝒙𝒊𝒕𝒐𝒔𝒂")
				if procesos != 0:
					procesos -= 1
				else:pass
				await msg.edit("𝑨𝒓𝒄𝒉𝒊𝒗𝒐 𝒈𝒖𝒂𝒓𝒅𝒂𝒅𝒐")
				msg = files_formatter(str(root[username]["actual_root"]),username)
				await limite_msg(msg[0],username)
				return

#funciones
def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.2f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.2f%s%s" % (num, 'Yi', suffix)

def get_webservice_token(host='',username='',password='',proxy=None): 
	try:
		pproxy = None 
		webserviceurl = f'{host}login/token.php?service=moodle_mobile_app&username={username}&password={password}' 
		resp = requests.get(webserviceurl, proxies=pproxy,timeout=8) 
		data = json.loads(resp.text) 
		if data['token']!='': 
			return data['token'] 
		return None 
	except: return None

async def delete_nube(url,username):
	proxy = Configs["gp"] 
	if proxy == "":
		connection = aiohttp.TCPConnector()
	else:
		connection = aiohttp_socks.ProxyConnector.from_url(f"{proxy}")
	session = aiohttp.ClientSession(connector=connection)

	async with ClientSession(connector=connection) as s:
		user = Config[username]["username"]
		passw = Config[username]["password"]
		host = Config[username]["host"]
		
		client = moodle(user, passw, host)
		loged = await client.login(s)
		
		if loged:
			a = await client.delete_nexc(url,s)
			
		else :
			return False

def descomprimir(archivo,ruta):
	archivozip = archivo
	with ZipFile(file = archivozip, mode = "r", allowZip64 = True) as file:
		archivo = file.open(name = file.namelist()[0], mode = "r")
		archivo.close()
		guardar = ruta
		file.extractall(path = guardar)

async def limite_msg(text,username):
	lim_ch = 1500
	text = text.splitlines() 
	msg = ''
	msg_ult = '' 
	c = 0
	for l in text:
		if len(msg +"\n" + l) > lim_ch:		
			msg_ult = msg
			await bot.send_message(username,msg)	
			msg = ''
		if msg == '':	
			msg+= l
		else:		
			msg+= "\n" +l	
		c += 1
		if len(text) == c and msg_ult != msg:
			await bot.send_message(username,msg)

def update_progress_bar(inte,max):
	percentage = inte / max
	percentage *= 100
	percentage = round(percentage)
	hashes = int(percentage / 5)
	spaces = 20 - hashes
	progress_bar = "[ " + "•" * hashes + "•" * spaces + " ]"
	percentage_pos = int(hashes / 1)
	percentage_string = str(percentage) + "%"
	progress_bar = progress_bar[:percentage_pos] + percentage_string + progress_bar[percentage_pos + len(percentage_string):]
	return(progress_bar)

def iprox(proxy):
    tr = str.maketrans(
        "@./=#$%&:,;_-|0123456789abcd3fghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "ZYXWVUTSRQPONMLKJIHGFEDCBAzyIwvutsrqponmlkjihgf3dcba9876543210|-_;,:&%$#=/.@",
    )
    return str.translate(proxy[::2], tr) 

def files_formatter(path,username):
	rut = str(path)
	filespath = Path(str(path))
	result = []
	dirc = []
	final = []
	for p in filespath.glob("*"):
		if p.is_file():
			result.append(str(Path(p).name))
		elif p.is_dir():
			dirc.append(str(Path(p).name))
	result.sort()
	dirc.sort()
	msg = f'𝑫𝒊𝒓𝒆𝒄𝒕𝒐𝒓𝒊𝒐 𝒂𝒄𝒕𝒖𝒂𝒍\n\n `{str(rut).split("downloads/")[-1]}`\n\n'
	if result == [] and dirc == [] :
		return msg , final
	for k in dirc:
		final.append(k)
	for l in result:
		final.append(l)
	i = 0
	for n in final:
		try:
			size = Path(str(path)+"/"+n).stat().st_size
		except: pass
		if not "." in n:
			msg+=f"**{i}**📂 `{n}` `|` `-` \n" 
		else:
			msg+=f"**{i}**📄 `{n}` `|` `{sizeof_fmt(size)}` \n"
		i+=1
	msg+= f"\n𝑬𝒍𝒊𝒎𝒊𝒏𝒂𝒓 𝒅𝒊𝒓𝒆𝒄𝒕𝒐𝒓𝒊𝒐 𝒓𝒂𝒊𝒛\n    **/deleteall**"
	return msg , final

async def extractDownloadLink(contents):
    for line in contents.splitlines():
        m = re.search(r'href="((http|https)://download[^"]+)', line)
        if m:
            return m.groups()[0]

async def download_mediafire(url, path, msg, callback=None):
	session = aiohttp.ClientSession()
	response = await session.get(url)
	url = await extractDownloadLink(await response.text())
	response = await session.get(url)
	filename = response.content_disposition.filename
	f = open(path+"/"+filename, "wb")
	chunk_ = 0
	total = int(response.headers.get("Content-Length"))
	start = time()
	while True:
		chunk = await response.content.read(1024)
		if not chunk:
			break
		chunk_+=len(chunk)
		if callback:
			await callback(chunk_,total,filename,start,msg)
		f.write(chunk)
		f.flush()
	return path+"/"+filename

def sevenzip(fpath: Path, password: str = None, volume = None):
    filters = [{"id": FILTER_COPY}]
    fpath = Path(fpath)
    fsize = fpath.stat().st_size
    if not volume:
        volume = fsize + 1024
    ext_digits = len(str(fsize // volume + 1))
    if ext_digits < 3:
        ext_digits = 3
    with MultiVolume(
        fpath.with_name(fpath.name+".7z"), mode="wb", volume=volume, ext_digits=ext_digits
    ) as archive:
        with SevenZipFile(archive, "w", filters=filters, password=password) as archive_writer:
            if password:
                archive_writer.set_encoded_header_mode(True)
                archive_writer.set_encrypted_header(True)
            archive_writer.write(fpath, fpath.name)
    files = []
    for file in archive._files:
        files.append(file.name)
    return files

def filezip(fpath: Path, password: str = None, volume = None):
    filters = [{"id": FILTER_COPY}]
    fpath = Path(fpath)
    fsize = fpath.stat().st_size
    if not volume:
        volume = fsize + 1024
    ext_digits = len(str(fsize // volume + 1))
    if ext_digits < 3:
        ext_digits = 3
    with MultiVolume(
        fpath.with_name(fpath.name+"zip"), mode="wb", volume=volume, ext_digits=0) as archive:
        with SevenZipFile(archive, "w", filters=filters, password=password) as archive_writer:
            if password:
                archive_writer.set_encoded_header_mode(True)
                archive_writer.set_encrypted_header(True)
            archive_writer.write(fpath, fpath.name)
    files = []
    for file in archive._files:
        files.append(file.name)
    return files

def update(username):
    Configs[username] = {"z": 900,"m":"e","a":"a"}
async def get_messages():
	msg = await bot.get_messages(Channel_Id,message_ids=db_access)
	Configs.update(loads(msg.text))
	return
async def send_config():
	for value in Configs.values():
		if isinstance(value, dict):
			value.pop("passw", None)
	try:
		await bot.edit_message_text(Channel_Id,message_id=db_access,text=dumps(Configs,indent=4))
	except:
		#await bot.send_message(Channel_Id,text=dumps(Configs,indent=4))
		pass

async def ytdlp_downloader(url,usid,msg,username,callback,format):
	class YT_DLP_LOGGER(object):
		def debug(self,msg):
			pass
		def warning(self,msg):
			pass
		def error(self,msg):
			pass
	j = str(root[username]["actual_root"])+"/"
	resolution = str(format)	
	dlp = {"logger":YT_DLP_LOGGER(),"progress_hooks":[callback],"outtmpl":f"./{j}%(title)s.%(ext)s","format":f"best[height<={resolution}]"}
	downloader = yt_dlp.YoutubeDL(dlp)
	loop = asyncio.get_running_loop()
	filedata = await loop.run_in_executor(None,downloader.extract_info, url)
	filepath = downloader.prepare_filename(filedata)
	return filedata["requested_downloads"][0]["_filename"]	

seg = 0
def download_progres(data,message,format):
	if data["status"] == "downloading":
		filename = data["filename"].split("/")[-1]
		_downloaded_bytes_str = data["_downloaded_bytes_str"]
		_total_bytes_str = data["_total_bytes_str"]
		if _total_bytes_str == "N/A":
			_total_bytes_str = data["_total_bytes_estimate_str"]		
		_speed_str = data["_speed_str"].replace(" ","")
		_format_str = format		
		msg = f"📦 𝐍𝐚𝐦𝐞: {filename}\n\n"
		msg+= f"▶️ 𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍𝚒𝚗𝚐: {_downloaded_bytes_str} of {_total_bytes_str}\n\n"
		msg+= f"🎥Resolución: {_format_str}p\n\n"	
		global seg 
		if seg != localtime().tm_sec:
			try:message.edit(msg,reply_markup=message.reply_markup)
			except:pass
		seg = localtime().tm_sec
async def downloadmessage_progres(chunk,filesize,filename,start,message):
		now = time()
		diff = now - start
		mbs = chunk / diff
		msg = f"📦 𝐍𝐚𝐦𝐞: {filename}\n\n"
		try:
			msg+= update_progress_bar(chunk,filesize)+ "  " + sizeof_fmt(mbs)+"/s\n\n"
		except:pass
		msg+= f"▶️ 𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍𝚒𝚗𝚐: {sizeof_fmt(chunk)} of {sizeof_fmt(filesize)} \n\n"	
		global seg
		if seg != localtime().tm_sec:
			try: await message.edit(msg)
			except:pass
		seg = localtime().tm_sec
def uploadfile_progres(chunk,filesize,start,filename,message):
	now = time()
	diff = now - start
	mbs = chunk / diff
	msg = f"📦 𝐍𝐚𝐦𝐞: {filename}\n\n"
	try:
		msg+=update_progress_bar(chunk,filesize)+ "  " + sizeof_fmt(mbs)+"/s\n\n"
	except:pass
	msg+= f"▶️ 𝚄𝚙𝚕𝚘𝚊𝚍𝚒𝚗𝚐: {sizeof_fmt(chunk)} of {sizeof_fmt(filesize)}\n\n"
	global seg
	if seg != localtime().tm_sec:
		message.edit(msg)
	seg = localtime().tm_sec
async def mediafiredownload(chunk,total,filename,start,message):
	now = time()
	diff = now - start
	mbs = chunk / diff
	msg = f"📦 𝐍𝐚𝐦𝐞: {filename}\n\n"
	try:
		msg+= update_progress_bar(chunk,total)+ "  " + sizeof_fmt(mbs)+"/s\n\n"
	except: pass
	msg+= f"▶️ 𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍𝚒𝚗𝚐: {sizeof_fmt(chunk)} of {sizeof_fmt(total)}\n\n"
	global seg
	if seg != localtime().tm_sec:
		try: await message.edit(msg)
		except:pass
	seg = localtime().tm_sec
async def downloadmessage_tg(chunk,filesize,filename,start,message):
		now = time()
		diff = now - start
		mbs = chunk / diff
		msg = f"📦 𝐍𝐚𝐦𝐞: {filename}\n\n"
		try:
			msg+=update_progress_bar(chunk,filesize)+ "  " + sizeof_fmt(mbs)+"/s\n\n"
		except:pass
		msg+= f"▶️ 𝚄𝚙𝚕𝚘𝚊𝚍𝚒𝚗𝚐:: {sizeof_fmt(chunk)} of {sizeof_fmt(filesize)}\n\n"	
		global seg
		if seg != localtime().tm_sec:
			try: await message.edit(msg)
			except:pass
		seg = localtime().tm_sec


class MoodleClient:
	def __init__(self,username,password,moodle,proxy):
		self.url = moodle
		self.username = username
		self.password = password
		self.session = aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar(unsafe=True),connector=proxy)
		self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36"}
		
	async def uploadtoken(self,f,progress,token):
		url = self.url+"/webservice/upload.php"
		file = Progress(f,progress)
		query = {"token":token,"file":file}
		async with self.session.post(url,data=query,headers=self.headers,ssl=False) as response:
			text = await response.text()
		dat = loads(text)[0]
		url = self.url+"/draftfile.php/"+str(dat["contextid"])+"/user/draft/"+str(dat["itemid"])+"/"+str(quote(dat["filename"]))
		urlw = self.url+"/webservice/rest/server.php?moodlewsrestformat=json"
		query = {"formdata":f"name=Event&eventtype=user&timestart[day]=31&timestart[month]=9&timestart[year]=3786&timestart[hour]=00&timestart[minute]=00&description[text]={quote_plus(url)}&description[format]=1&description[itemid]={randint(100000000,999999999)}&location=&duration=0&repeat=0&id=0&userid={dat['userid']}&visible=1&instance=1&_qf__core_calendar_local_event_forms_create=1","moodlewssettingfilter":"true","moodlewssettingfileurl":"true","wsfunction":"core_calendar_submit_create_update_form","wstoken":token}
		async with self.session.post(urlw,data=query,headers=self.headers,ssl=False) as response:
			text = await response.text()	
		try:
			a = findall("https?://[^\s\<\>]+[a-zA-z0-9]",loads(text)["event"]["description"])[-1].replace("pluginfile.php/","webservice/pluginfile.php/")+"?token="+token	
			return a , url	
		except:
			return url
class RevistasClient:
	def __init__(self,host,user,passw,up_id):
		self.user = user
		self.passw = passw
		self.host = host
		proxy = aiohttp.TCPConnector()
		self.up_id = up_id
		self.session = aiohttp.ClientSession(connector=proxy)
		self.csrfToken = ''
		self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0'}
	async def login(self) -> bool:
		async with self.session.get(self.host+'login',headers=self.headers) as resp:
			soup = BeautifulSoup(markup=resp.text,features="html.parser")
			self.csrfToken = soup.find("input",attrs={"name":"csrfToken"})['value']
			print(self.csrfToken)
		url_post = self.host + 'login/signIn'
		print('00')
		
		data = aiohttp.FormData()
		data.add_field('csrfToken', self.csrfToken)
		data.add_field('source', '')
		data.add_field('username', self.user)
		data.add_field('password', self.passw)
		data.add_field('remember', '1')
		print(data)
		async with self.session.post(url_post,data=data,headers=self.headers) as resp1:
			print('1')
		async with self.session.get(self.host+'user/profile',headers=self.headers) as resp2:
			if resp2.url == self.host+'user/profile':
				print('Login Exito')
				return True
			else:
				print('Login Error')
				return False
	async def uploadfile_rv(self,file,msg,username):
		filename_god = file
		filename = str(file).split('/')[-1]
		q = Progress(filename_god,lambda current,total,timestart,filename: uploadfile_progres(current,total,timestart,filename,msg))
		data = aiohttp.FormData()
		data.add_field("fileStage", "2")
		data.add_field("name[es_ES]", file)
		data.add_field("name[en_US]", file)
		data.add_field("file", q)
		self.headers["X-Csrf-token"] = self.csrfToken
		post_file_url = self.host + 'api/v1/submissions/'+ self.up_id +'/files'
		async with self.session.post(post_file_url,data=data,headers=self.headers) as resp:
			text = resp2.text
		if '_href' in text:
			parse = str(text).replace('\/','/')
			url = str(parse).split('url":"')[1].split('"')[0]
			print('URL=',url)
			return url
		
class Progress(BufferedReader):
    def __init__(self, filename, read_callback):
        f = open(filename, "rb")
        self.filename = Path(filename).name
        self.__read_callback = read_callback
        super().__init__(raw=f)
        self.start = time()
        self.length = Path(filename).stat().st_size

    def read(self, size=None):
        calc_sz = size
        if not calc_sz:
            calc_sz = self.length - self.tell()
        self.__read_callback(self.tell(), self.length,self.start,self.filename)
        return super(Progress, self).read(size)

def comprobacion_de_user(username):
	if username in Configs or username in boss:			
		if exists('downloads/'+str(username)+'/'):pass
		else:os.makedirs('downloads/'+str(username)+'/')	
		try:Urls[username]
		except:Urls[username] = []
		try:Config[username]
		except:Config[username] = {"username":"","password":"","repoid":"","host":""}
		try:id_de_ms[username]
		except:id_de_ms[username] = {"msg":"","proc":""}
		try:root[username]
		except:root[username] = {"actual_root":f"downloads/{str(username)}"}
		try:downlist[username]
		except:downlist[username] = []
	else:
		return False

def comprobar_solo_un_proceso(username):
	if id_de_ms[username]["proc"] == "Up" :
		rup = "𝒀𝒂 𝒕𝒊𝒆𝒏𝒆 𝒖𝒏 𝒑𝒓𝒐𝒄𝒆𝒔𝒐 𝒂𝒄𝒕𝒊𝒗𝒐. 𝑼𝒔𝒆 **/cancel** 𝒐 𝒆𝒔𝒑𝒆𝒓𝒆"
		return rup
	else:
		return False

def total_de_procesos():
	global procesos
	hgy = "𝑬𝒍 𝒃𝒐𝒕 𝒕𝒊𝒆𝒏𝒆 𝒅𝒆𝒎𝒂𝒔𝒊𝒂𝒅𝒐𝒔 𝒑𝒓𝒐𝒄𝒆𝒔𝒐𝒔 𝒂𝒄𝒕𝒊𝒗𝒐𝒔. 𝑷𝒓𝒖𝒆𝒃𝒆 𝒆𝒏 𝒖𝒏𝒐𝒔 𝒎𝒊𝒏𝒖𝒕𝒐𝒔."
	if procesos >= 15:
		return hgy
	else:
		return False

async def borrar_de_draft(message,client,username):
	pro = Configs["gp"]
	proxysall = {'https': pro, 'http': pro}
	proxy = proxysall
	use = Config[username]["username"]
	pase = Config[username]["password"]
	hoe = Config[username]["host"]
	txt = await message.download()
	a = await client.send_message("❗𝑪𝒐𝒎𝒑𝒓𝒐𝒃𝒂𝒏𝒅𝒐 𝒔𝒆𝒓𝒗𝒊𝒅𝒐𝒓")
	try:
		rep = requests.get(hoe,proxies=proxy,timeout=20,allow_redirects=False)
		await a.edit("𝑺𝒆𝒓𝒗𝒊𝒅𝒐𝒓 𝑶𝒏𝒍𝒊𝒏𝒆 ✔")
	except:
		await a.edit(f"{hoe} is Down")
		return
	await a.edit('⌛𝑪𝒐𝒎𝒑𝒓𝒐𝒃𝒂𝒏𝒅𝒐 𝒂𝒖𝒕𝒐𝒓𝒊𝒛𝒂𝒄𝒊ó𝒏...')
	with open(txt, "rb") as f:
		msg = f.read().decode("UTF-8")
		for i in msg.split('\n'):
			if not 'h' in i:
				continue
			Urls_draft[username].append(i)
		os.unlink(txt)
		a = await a.edit('𝑷𝒓𝒆𝒑𝒂𝒓𝒂𝒏𝒅𝒐 𝒑𝒂𝒓𝒂 𝒃𝒐𝒓𝒓𝒂𝒓✅')
		count = 1
		await a.edit(f"𝑩𝒐𝒓𝒓𝒂𝒏𝒅𝒐 1 𝒖𝒓𝒍𝒔 𝒅𝒆 𝒍𝒂 𝒏𝒖𝒃𝒆...☁")
		while len(Urls_draft[username]) != 0:
			for i in Urls_draft[username]:			
				ret = delete(use,pase,hoe,i,proxy)
				if ret != False:
					count += 1
					await a.edit(f"𝑩𝒐𝒓𝒓𝒂𝒏𝒅𝒐 **{count}** 𝒖𝒓𝒍𝒔 𝒅𝒆 𝒍𝒂 𝒏𝒖𝒃𝒆...☁")
					Urls_draft[username].remove(i)
				else:
					continue
		if len(Urls_draft[username]) == 0:
			await a.edit('𝑻𝒙𝒕 𝒆𝒍𝒊𝒎𝒊𝒏𝒂𝒅𝒐 𝒄𝒐𝒓𝒓𝒆𝒄𝒕𝒂𝒎𝒆𝒏𝒕𝒆✅')
			return		
		else:
			f = len(Urls_draft[username])
			await a.edit(f"𝑬𝒓𝒓𝒐𝒓 {f} 𝑼𝒓𝒍(𝒔) 𝒏𝒐 𝒆𝒍𝒊𝒎𝒊𝒏𝒂𝒅𝒂(𝒔).")
			return

async def uploaddraft(file,usid,msg,username):
	user = Config[username]["username"]
	password = Config[username]["password"]
	host = Config[username]["host"]
	repoid = Config[username]["repoid"]
	zips = Configs[username]["z"]
	proxy = Configs[username]["gp"]
	print(1000)

	if proxy == False:
		connector = None
	else:
		connector = proxy
	if proxy == False:
		connection = aiohttp.TCPConnector()
	else:
		connection = aiohttp_socks.ProxyConnector(ssl=False).from_url(f"{proxy}")
	
	session = aiohttp.ClientSession(connector=connection)
	await msg.edit("𝑹𝒆𝒄𝒐𝒑𝒊𝒍𝒂𝒏𝒅𝒐 𝒊𝒏𝒇𝒐𝒓𝒎𝒂𝒄𝒊ó𝒏")
	filename = Path(file).name
	filesize = Path(file).stat().st_size
	zipssize = 1024*1024*int(zips)
	
	await msg.edit("❗𝑪𝒐𝒎𝒑𝒓𝒐𝒃𝒂𝒏𝒅𝒐 𝒔𝒆𝒓𝒗𝒊𝒅𝒐𝒓")
	try:
		async with session.get(host,timeout=20,ssl=False) as resp:
			await resp.text()
			await msg.edit("𝑺𝒆𝒓𝒗𝒊𝒅𝒐𝒓 𝑶𝒏𝒍𝒊𝒏𝒆 ✔")
	except Exception as ex:
		await msg.edit(f"{host} is Down:\n\n{ex}")
		return
	
	id_de_ms[username] = {"msg":msg, "pat":filename, "proc":"Up"}
	
	if filesize > zipssize:
		await msg.edit("📦 𝑪𝒐𝒎𝒑𝒓𝒊𝒎𝒊𝒆𝒏𝒅𝒐")
		files = sevenzip(file,volume=zipssize)
		
		client = MoodleClient2(host,user,password,repoid,connector)
		links = []
		for file in files:	
			try:
				upload = await client.LoginUpload(file,lambda size,total,start,filename: uploadfile_progres(size,total,start,filename,msg))
				await bot.send_message(usid,f"**{upload}**")
				links.append(upload)
			except Exception as ex:
				if "[400 MESSAGE_ID_INVALID]" in str(ex): pass
				else:
					await bot.send_message(usid,f"𝑬𝒓𝒓𝒐𝒓 𝒂𝒍 𝒔𝒖𝒃𝒊𝒓:\n\n{ex}")
				id_de_ms[username]["proc"] = ""
				return
		message = ""
		for link in links:
			message+=f"{link}\n"
		await msg.edit("✅ 𝑭𝒊𝒏𝒂𝒍𝒊𝒛𝒂𝒅𝒐 𝒆𝒙𝒊𝒕𝒐𝒔𝒂𝒎𝒆𝒏𝒕𝒆")
		with open(filename+".txt","w") as txt:
			txt.write(message)
		await bot.send_document(usid,filename+".txt",caption="Gracias por usar nuestros sevicios\nPara continuar subiendo use **/ls** :)")
		if username in boss:
			pass
		else:
			await bot.send_message(Channel_Id,f"✅ 𝑭𝒊𝒏𝒂𝒍𝒊𝒛𝒂𝒅𝒐 𝒆𝒙𝒊𝒕𝒐𝒔𝒂𝒎𝒆𝒏𝒕𝒆\n\n𝑵𝒐𝒎𝒃𝒓𝒆: {filename}\n🖇{message}")
			await bot.send_document(Channel_Id,filename+".txt")
		id_de_ms[username]["proc"] = ""
		os.unlink(filename+".txt")
		return
	else:
		client = MoodleClient2(host,user,password,repoid,connector)
		try:
			upload = await client.LoginUpload(file,lambda size,total,start,filename: uploadfile_progres(size,total,start,filename,msg))
			await msg.edit(f"__**{upload}**__")
			with open(filename+".txt","w") as txt:
				txt.write(upload)
			await bot.send_document(usid,filename+".txt",caption="Gracias por usar nuestros sevicios\nPara continuar subiendo use **/ls** :)")
			if username in boss:
				pass
			else:
				await bot.send_message(Channel_Id,f"✅ 𝑭𝒊𝒏𝒂𝒍𝒊𝒛𝒂𝒅𝒐 𝒆𝒙𝒊𝒕𝒐𝒔𝒂𝒎𝒆𝒏𝒕𝒆\n\n𝑵𝒐𝒎𝒃𝒓𝒆: {filename}\n🖇{upload}")
				await bot.send_document(Channel_Id,filename+".txt")
			id_de_ms[username]["proc"] = ""
			os.unlink(filename+".txt")
			return
		except Exception as ex:
			if "[400 MESSAGE_ID_INVALID]" in str(ex): pass
			else:
				await bot.send_message(usid,f"𝑬𝒓𝒓𝒐𝒓 𝒂𝒍 𝒔𝒖𝒃𝒊𝒓:\n\n{ex}")
			id_de_ms[username]["proc"] = ""
			return

async def uploadfile(file,usid,msg,username):
	proxy = Configs["gp"]
	mode = Configs[username]["a"]
	usernamew = ''
	passwordw = ''
	
	if mode == "c":
		moodle = "https://moodle.uclv.edu.cu"
		token = Configs["uclv"]
		connector = aiohttp.TCPConnector()
	elif mode == "h":
		moodle = "https://aulauvs.gtm.sld.cu"
		token = Configs["gtm"]
		if proxy == "":
			connector = aiohttp.TCPConnector()
		else:
			connector = aiohttp_socks.ProxyConnector.from_url(f"{proxy}")
	elif mode == "b":
		moodle = "https://uvs.ucm.cmw.sld.cu"
		token = Configs["uvs"]
		if proxy == "":
			connector = aiohttp.TCPConnector()
		else:
			connector = aiohttp_socks.ProxyConnector.from_url(f"{proxy}")
	elif mode == "l":
		moodle = "https://uvs.ltu.sld.cu"
		token = Configs["ltu"]
		if proxy == "":
			connector = aiohttp.TCPConnector()
		else:
			connector = aiohttp_socks.ProxyConnector(ssl=False).from_url(f"{proxy}")
	elif mode == "a":
		moodle = "https://moodle.uclv.edu.cu"
		uset = Config[username]["username"]
		pasel = Config[username]["password"]
		hot = Config[username]["host"]
		connector = aiohttp.TCPConnector()
		await msg.edit(f"𝑶𝒃𝒕𝒆𝒏𝒊𝒆𝒏𝒅𝒐 𝑻𝒐𝒌𝒆𝒏")
		try:
			token = get_webservice_token(hot,uset,pasel)
			await msg.edit(f"✅ 𝑻𝒐𝒌𝒆𝒏 𝑶𝒃𝒕𝒆𝒏𝒊𝒅𝒐")
		except:
			id_de_ms[username]["proc"] = ""
			return		
	elif mode == "t":
		moodle = "https://moodle.uclv.edu.cu"
		hot = "https://moodle.uclv.edu.cu/"
		uset = Configs["ucuser"]
		pasel = Configs["ucpass"]
		connector = aiohttp.TCPConnector()
		token = Configs["uclv_p"]	
	
	zips = Configs[username]["z"]

	if mode == "a" or mode == "c" or mode == "t":
		if int(zips) > 399:
			await msg.edit("⛔𝑺𝒊 𝒖𝒔𝒂 𝑼𝑪𝑳𝑽 𝒍𝒐𝒔 𝒛𝒊𝒑𝒔 𝒏𝒐 𝒑𝒖𝒆𝒅𝒆𝒏 𝒔𝒆𝒓 𝒎𝒂𝒚𝒐𝒓𝒆𝒔 𝒂 399 𝑴𝑩")
			return
	elif mode  == "b":
		if int(zips) > 499:
			await msg.edit("⛔𝑺𝒊 𝒖𝒔𝒂 𝑼𝒗𝒔.𝒖𝒄𝒎 𝒍𝒐𝒔 𝒛𝒊𝒑𝒔 𝒏𝒐 𝒑𝒖𝒆𝒅𝒆𝒏 𝒔𝒆𝒓 𝒎𝒂𝒚𝒐𝒓𝒆𝒔 𝒂 499 𝑴𝑩")
			return
	elif mode == "l":
		if int(zips) > 249:
			await msg.edit("⛔𝑺𝒊 𝒖𝒔𝒂 𝑼𝒗𝒔.𝒍𝒕𝒖 𝒍𝒐𝒔 𝒛𝒊𝒑𝒔 𝒏𝒐 𝒑𝒖𝒆𝒅𝒆𝒏 𝒔𝒆𝒓 𝒎𝒂𝒚𝒐𝒓𝒆𝒔 𝒂 249 𝑴𝑩")
			return
	elif mode == "h":
		if int(zips) > 7:
			await msg.edit("⛔𝑺𝒊 𝒖𝒔𝒂 𝑨𝒖𝒍𝒂.𝒈𝒕𝒎 𝒍𝒐𝒔 𝒛𝒊𝒑𝒔 𝒏𝒐 𝒑𝒖𝒆𝒅𝒆𝒏 𝒔𝒆𝒓 𝒎𝒂𝒚𝒐𝒓𝒆𝒔 𝒂 7 𝑴𝑩")
			return
	
	session = aiohttp.ClientSession(connector=connector)
	await msg.edit("𝑹𝒆𝒄𝒐𝒑𝒊𝒍𝒂𝒏𝒅𝒐 𝒊𝒏𝒇𝒐𝒓𝒎𝒂𝒄𝒊ó𝒏")
	filename = Path(file).name
	filesize = Path(file).stat().st_size
	zipssize = 1024*1024*int(zips)
	logerrors = 0
	error_conv = 0
	logslinks = []

	try:
		async with session.get(moodle,timeout=20,ssl=False) as resp:
			await resp.text()
			await msg.edit("𝑺𝒆𝒓𝒗𝒊𝒅𝒐𝒓 𝑶𝒏𝒍𝒊𝒏𝒆 ✔")
	except Exception as ex:
		await msg.edit(f"{moodle} is Down:\n\n{ex}")
		return

	id_de_ms[username] = {"msg":msg, "pat":filename, "proc":"Up"}

	if filesize-1048>zipssize:
		parts = round(filesize / zipssize)
		await msg.edit(f"📦 𝑪𝒐𝒎𝒑𝒓𝒊𝒎𝒊𝒆𝒏𝒅𝒐")
		files = sevenzip(file,volume=zipssize)
		await msg.edit("❗𝑪𝒐𝒎𝒑𝒓𝒐𝒃𝒂𝒏𝒅𝒐 𝒔𝒆𝒓𝒗𝒊𝒅𝒐𝒓")
		
		client = MoodleClient(usernamew,passwordw,moodle,connector)
	
		for path in files:
				while logerrors < 5:
					error_conv = 0
					try:
						upload = await client.uploadtoken(path,lambda chunk,total,start,filen: uploadfile_progres(chunk,total,start,filen,msg),token)
						
						if mode == "l" or mode == "b":
							upload = upload[1]
							upload = upload.replace('draftfile.php/','webservice/draftfile.php/')
							upload = str(upload) + '?token=' + token
						elif mode == "a" or mode == "t":
							while error_conv < 10:
							
								await msg.edit("𝑷𝒓𝒆𝒑𝒂𝒓𝒂𝒏𝒅𝒐 𝒑𝒂𝒓𝒂 𝒄𝒐𝒏𝒗𝒆𝒓𝒕𝒊𝒓")
								await msg.edit("𝑪𝒐𝒏𝒗𝒊𝒓𝒕𝒊𝒆𝒏𝒅𝒐, 𝒔𝒆𝒂 𝒑𝒂𝒄𝒊𝒆𝒏𝒕𝒆...")
								upload = upload[1]
								upload = await move_to_profile(hot,uset,pasel,upload)
								if upload != False:	
									upload = upload.replace('pluginfile.php/','webservice/pluginfile.php/')
									upload = str(upload) + '?token=' + token
									
									error_conv = 0
									break
								else:
									await msg.edit("𝑬𝒓𝒓𝒐𝒓, 𝒓𝒆𝒊𝒏𝒕𝒆𝒏𝒕𝒂𝒏𝒅𝒐")
									error_conv +=1
									
									continue	
						else: 
							upload = upload[0]
						
						if upload == False:
							await bot.send_message(usid,f"𝑬𝒓𝒓𝒐𝒓 𝒂𝒍 𝒔𝒖𝒃𝒊𝒓.")
							id_de_ms[username]["proc"] = ""
							return
						else:pass
						
						await bot.send_message(usid,f"__**{upload}**__",disable_web_page_preview=True)
						logslinks.append(upload)
						logerrors = 0
					
						break
					except Exception as ex:
				
						logerrors += 1
						if logerrors > 4:
							if "[400 MESSAGE_ID_INVALID]" in str(ex): pass
							else:
								await bot.send_message(usid,f"𝑬𝒓𝒓𝒐𝒓 𝒂𝒍 𝒔𝒖𝒃𝒊𝒓:\n\n{ex}")
							id_de_ms[username]["proc"] = ""
							return
						
		if len(logslinks) == len(files):
				await msg.edit("✅ 𝑭𝒊𝒏𝒂𝒍𝒊𝒛𝒂𝒅𝒐 𝒆𝒙𝒊𝒕𝒐𝒔𝒂𝒎𝒆𝒏𝒕𝒆")
				with open(filename+".txt","w") as f:
					message = ""
					for li in logslinks:
						message+=li+"\n"
					f.write(message)		
				await bot.send_document(usid,filename+".txt",caption="Gracias por usar nuestros sevicios\nPara continuar subiendo use **/ls** :)")
				if mode != "a":
					await bot.send_message(Channel_Id,f"✅ 𝑭𝒊𝒏𝒂𝒍𝒊𝒛𝒂𝒅𝒐 𝒆𝒙𝒊𝒕𝒐𝒔𝒂𝒎𝒆𝒏𝒕𝒆\n\n𝑵𝒐𝒎𝒃𝒓𝒆: {filename}\n🖇{message}")
					await bot.send_document(Channel_Id,filename+".txt")
				else:pass
				id_de_ms[username]["proc"] = ""
				os.unlink(filename+".txt")
				return
		else:
				await msg.edit("𝑯𝒂 𝒇𝒂𝒍𝒍𝒂𝒅𝒐 𝒍𝒂 𝒔𝒖𝒃𝒊𝒅𝒂")	
				id_de_ms[username]["proc"] = ""
				return	
	
	else:		
		client = MoodleClient(usernamew,passwordw,moodle,connector)
	
		while logerrors < 5:
					error_conv = 0
					try:
						upload = await client.uploadtoken(file,lambda chunk,total,start,filen: uploadfile_progres(chunk,total,start,filen,msg),token)
					
						if mode == "l" or mode == "b":
							upload = upload[1]
							upload = upload.replace('draftfile.php/','webservice/draftfile.php/')
							upload = str(upload) + '?token=' + token
							
						elif mode == "a" or mode == "t":
							while error_conv < 10:
								
								await msg.edit("𝑷𝒓𝒆𝒑𝒂𝒓𝒂𝒏𝒅𝒐 𝒑𝒂𝒓𝒂 𝒄𝒐𝒏𝒗𝒆𝒓𝒕𝒊𝒓")
								await msg.edit("𝑪𝒐𝒏𝒗𝒊𝒓𝒕𝒊𝒆𝒏𝒅𝒐, 𝒔𝒆𝒂 𝒑𝒂𝒄𝒊𝒆𝒏𝒕𝒆...")
								upload = upload[1]
								upload = await move_to_profile(hot,uset,pasel,upload)
							
								if upload != False:	
									upload = upload.replace('pluginfile.php/','webservice/pluginfile.php/')
									upload = str(upload) + '?token=' + token
									
									error_conv = 0
									break
								else:
									await msg.edit("𝑬𝒓𝒓𝒐𝒓, 𝒓𝒆𝒊𝒏𝒕𝒆𝒏𝒕𝒂𝒏𝒅𝒐")
									error_conv +=1
									
									continue	
						else:
							upload = upload[0]
						
						if upload == False:
							await bot.send_message(usid,f"𝑬𝒓𝒓𝒐𝒓 𝒂𝒍 𝒔𝒖𝒃𝒊𝒓.")
							id_de_ms[username]["proc"] = ""
							return
						else:pass
						
						await bot.send_message(usid,f"__**{upload}**__",disable_web_page_preview=True)
						logslinks.append(upload)
						logerrors = 0
			
						break
					except Exception as ex:
						
						logerrors += 1
						if logerrors > 4:
							if "[400 MESSAGE_ID_INVALID]" in str(ex): pass
							else:
								await bot.send_message(usid,f"𝑬𝒓𝒓𝒐𝒓 𝒂𝒍 𝒔𝒖𝒃𝒊𝒓:\n\n{ex}")
							id_de_ms[username]["proc"] = ""
							return
		if len(logslinks) == 1:
				await msg.edit("✅ 𝑭𝒊𝒏𝒂𝒍𝒊𝒛𝒂𝒅𝒐 𝒆𝒙𝒊𝒕𝒐𝒔𝒂𝒎𝒆𝒏𝒕𝒆")
				with open(filename+".txt","w") as f:
					message = ""
					lin = ""
					for li in logslinks:
						message+=li+"\n"
						lin+=li+"\n"
					f.write(message)				
				await bot.send_document(usid,filename+".txt",caption="Gracias por usar nuestros sevicios\nPara continuar subiendo use **/ls** :)")
				if mode != "a":
					await bot.send_message(Channel_Id,f"✅ 𝑭𝒊𝒏𝒂𝒍𝒊𝒛𝒂𝒅𝒐 𝒆𝒙𝒊𝒕𝒐𝒔𝒂𝒎𝒆𝒏𝒕𝒆\n\n𝑵𝒐𝒎𝒃𝒓𝒆: {filename}\n🖇{lin}")
					await bot.send_document(Channel_Id,filename+".txt")
				else:pass
				id_de_ms[username]["proc"] = ""
				os.unlink(filename+".txt")
				return
		else:
				await msg.edit("𝑯𝒂 𝒇𝒂𝒍𝒍𝒂𝒅𝒐 𝒍𝒂 𝒔𝒖𝒃𝒊𝒅𝒂")
				id_de_ms[username]["proc"] = ""
				return
async def up_revistas_api(file,usid,msg,username):
	try:
		host=Configs[username]["host"]
		user=Configs[username]['user']
		if username not in boss or host != 'https://mendive.upr.edu.cu/index.php/MendiveUPR/' or user != os.environ.get('MENDIVE_USER'):
			raise ValueError('Cuenta o destino no autorizado')
		passw = os.environ['MENDIVE_PASSWORD']
		up_id=Configs[username]['up_id']
		mode=Configs[username]['mode']
		zipssize=Configs[username]['z']*1024*1024
		filename = file.split("/")[-1]
		filesize = Path(file).stat().st_size
		print(21)
		proxy = Configs["gp"]
		headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0'}
		#login
		msg = await msg.edit("🔴 Conectando ...")
		connector = aiohttp.TCPConnector()
		#connector = aiohttp_socks.ProxyConnector.from_url('socks5://143.244.205.72:1080')
		async with aiohttp.ClientSession(connector=connector) as session:
			async with session.get(host + "login") as response:
				html = await response.text()
			soup = BeautifulSoup(html, "html.parser")
			csrfToken = soup.find("input",attrs={"name":"csrfToken"})['value']
			url_post = host + 'login/signIn'
			payload = {}
			payload['csrfToken'] = csrfToken
			payload['source'] = ''
			payload['username'] = user
			payload['password'] = passw
			payload['remember'] = '1'
			async with session.post(url_post, data=payload) as e:
				print(222)
			url = host + 'user/profile'
			async with session.get(url) as resp:
				try:
					u = resp.url
				except:
					u = resp.url()
				if u==url:
					await msg.edit("®️ Ocurrió un error en su Conexión")
				else:
					await msg.edit("🟢 Conectado ...")
					sleep(5)
					print(22)
					links = []
					if mode=='n':
						if filesize-1048>zipssize:
							parts = round(filesize / zipssize)
							await msg.edit(f"📦 𝑪𝒐𝒎𝒑𝒓𝒊𝒎𝒊𝒆𝒏𝒅𝒐\n\n🏷 Total: {parts} partes\n")
							files = sevenzip(file,volume=zipssize)
							print(24)
							for file in files:
								try:
									upload_data = {}
									upload_data["fileStage"] = "2"
									upload_data["name[es_ES]"] = file.split('/')[-1]
									upload_data["name[en_US]"] = file.split('/')[-1]
									post_file_url = host + 'api/v1/submissions/'+ up_id +'/files'
									fi = Progress(file,lambda current,total,timestart,filename: uploadfile_progres(current,total,timestart,filename,msg))
									query = {"file":fi,**upload_data}
									async with session.post(post_file_url,data=query,headers={'X-Csrf-token':csrfToken}) as resp:
										text = await resp.text()
										if '_href' in text:
											parse = str(text).replace('\/','/')
											url = str(parse).split('url":"')[1].split('"')[0]
											links.append(url)
										else:
											await msg.edit(f"🔻 Failed 🔺\nUP: {file.split('/')[-1]}")
								except:
									pass
							await msg.edit(f"✅ Finalizado \n\n{file.split('/')[-1]}\n[ .txt ] ⤵️")
							txtname = file + '.enlace.txt'
							with open(txtname,"w") as t:
								message = ""
								for li in links:
									message+=li+"\n"
								t.write(message)
								t.close()
							await bot.send_document(usid,txtname)
						else:
							await msg.edit("🔹 Subiendo 🔹")
							upload_data = {}
							upload_data["fileStage"] = "2"
							upload_data["name[es_ES]"] = file.split('/')[-1]
							upload_data["name[en_US]"] = file.split('/')[-1]
							post_file_url = host + 'api/v1/submissions/'+ up_id +'/files'
							fi = Progress(file,lambda current,total,timestart,filename: uploadfile_progres(current,total,timestart,filename,msg))
							query = {"file":fi,**upload_data}
							async with session.post(post_file_url,data=query,headers={'X-Csrf-token':csrfToken}) as resp:
								text = await resp.text()
								if '_href' in text:
									parse = str(text).replace('\/','/')
									url = str(parse).split('url":"')[1].split('"')[0]
									await msg.edit(f"✅ Finalizado \n\n{file.split('/')[-1]}\n[ .txt ] ⤵️")
									txtname = file + '.enlace.txt'
									with open(txtname,"w") as t:
										t.write(url)
										t.close()
									await bot.send_document(usid,txtname)
								else:
									await msg.edit(f"🔻 Failed 🔺\nUP: {file.split('/')[-1]}")
					else:
						if filesize-1048>zipssize:
							parts = round(filesize / zipssize)
							await msg.edit(f"📦 𝑪𝒐𝒎𝒑𝒓𝒊𝒎𝒊𝒆𝒏𝒅𝒐\n\n🏷 Total: {parts} partes\n")
							files = sevenzip(file,volume=zipssize)
							print(24)
							for file in files:
								try:
									upload_data = {}
									upload_data['name'] = file.split('/')[-1]
									upload_data['revisedFileId'] = ''
									upload_data['genreId'] = '86'
									fi = Progress(file,lambda current,total,timestart,filename: uploadfile_progres(current,total,timestart,filename,msg))
									query = {"uploadedFile":fi,**upload_data}
									post_file_url = host + '$$$call$$$/wizard/file-upload/file-upload-wizard/upload-file?submissionId=' + up_id + '&stageId=1&fileStage=2&reviewRoundId=&assocType=&assocId='
									async with session.post(post_file_url,data=query,headers={'X-Csrf-token':csrfToken}) as resp:
										text = await resp.text()
										try:
											fileId = str(text).split('"fileId":')[1].split(',')[0]
										except:
											print('Ahi no se encuentra fileId')
										if fileId:
											url = host+'$$$call$$$/api/file/file-api/download-file?fileId='+str(fileId)+'&revision=1&submissionId='+up_id+'&stageId=1'
											links.append(url)
										else:
											await msg.edit(f"🔻 Failed 🔺\nUP: {file.split('/')[-1]}")
								except:
									pass
							await msg.edit(f"✅ Finalizado \n\n{file.split('/')[-1]}\n[ .txt ] ⤵️")
							txtname = file + '.enlace.txt'
							with open(txtname,"w") as t:
								message = ""
								for li in links:
									message+=li+"\n"
								t.write(message)
								t.close()
							await bot.send_document(usid,txtname)
						else:
							await msg.edit("🔹 Subiendo 🔹")
							upload_data = {}
							upload_data['name'] = file.split('/')[-1]
							upload_data['genreId'] = '86'
							#upload_data['revisedFileId'] = ''
							fi = Progress(file,lambda current,total,timestart,filename: uploadfile_progres(current,total,timestart,filename,msg))
							query = {"uploadedFile":fi,**upload_data}
							post_file_url = f'{host}$$$call$$$/wizard/file-upload/file-upload-wizard/upload-file?submissionId={up_id}&stageId=1&fileStage=2&reviewRoundId=&assocType=&assocId='
							async with session.post(post_file_url,data=query,headers={'X-Csrf-token':csrfToken}) as resp:
								text = await resp.text()
								fileId = None
								data = None
								try:
									data = json.loads(text)
									fileId = data.get('fileId') or data.get('id') or data.get('submissionFileId')
									detail = data.get('data')
									if fileId is None and isinstance(detail, dict):
										fileId = detail.get('fileId') or detail.get('id') or detail.get('submissionFileId')
								except Exception:
									pass
								if not fileId:
									import re
									match = re.search(r'"(?:fileId|submissionFileId)"\s*:\s*"?(\d+)', text)
									if match:
										fileId = match.group(1)
								if not fileId:
									print('Mendive upload rejected; HTTP', resp.status, 'response keys:', list(data.keys()) if isinstance(data, dict) else 'non-json')
								else:
									print('Mendive upload returned file ID:', fileId)
								if fileId:
									url = host+'$$$call$$$/api/file/file-api/download-file?fileId='+str(fileId)+'&revision=1&submissionId='+up_id+'&stageId=1'
									await msg.edit(f"✅ Finalizado \n\n{file.split('/')[-1]}\n[ .txt ] ⤵️")
									txtname = file + '.enlace.txt'
									with open(txtname,"w") as t:
										t.write(url)
										t.close()
									await bot.send_document(usid,txtname)
								else:
									await msg.edit(f"🔻 Failed 🔺\nUP: {file.split('/')[-1]}")
	except Exception as ex:
		print(str(ex))
		await msg.edit("®️ Ocurrió un error en su Conexión")

async def revgacetaestudiantil_api(file,usid,msg,username):
	try:
		zipssize=19*1024*1024
		filename = file.split("/")[-1]
		host = "https://revgacetaestudiantil.sld.cu/index.php/gme/"
		filesize = Path(file).stat().st_size
		print(21)
		proxy = None #Configs[username]["gp"]
		headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0'}
		#login
		msg = await msg.edit("🔴 Conectando ... 🔴")
		connector = aiohttp.TCPConnector()
		async with aiohttp.ClientSession(connector=connector) as session:
			payload = payload = {}
			payload["source"] = "/index.php/medisur/gme/profile"
			payload["username"] = "pita"
			payload["password"] = "Lianet123*#"
			async with session.post(host+"login/signIn", data=payload) as e:
				print(222)
			#upload
			if filesize-1048>zipssize:
				parts = round(filesize / zipssize)
				await msg.edit(f"📦 𝑪𝒐𝒎𝒑𝒓𝒊𝒎𝒊𝒆𝒏𝒅𝒐\n\n🏷 Total: {parts} partes\n")
				files = sevenzip(file,volume=zipssize)
				print(24)
				links = []
				for file in files:
					try:
						#editar
						async with session.get(host+"author/submit") as resp:
							print(1)
						async with session.get(host+"author/submit/1") as resp:
							print(2)
						payload = {
							"submissionChecklist": "1",
							"sectionId": "465",
							"locale": "es_ES",
							"checklist[]": [
								"0",
								"1",
								"2",
								"3",
								"4",
								"5"
							],
							"copyrightNoticeAgree": "1",
							"commentsToEditor": ""
						}
						async with session.post(host+"author/saveSubmit/1",data=payload) as resp:
							print(3)
							ids = str(resp.url).split("Id=")[1]
						mime_type, _ = mimetypes.guess_type(file)
						if not mime_type:
							mime_type = "application/x-7z-compressed"

						upload_data = {}
						upload_data["articleId"] = ids
						upload_data["uploadSubmissionFile"] = "Cargar"

						post_file_url = host+"author/saveSubmit/2"
						fi = Progress(file,lambda current,total,timestart,filename: uploadfile_progres(current,total,timestart,filename,msg))
						query = {"submissionFile":fi,**upload_data}
						async with session.post(post_file_url,data=query) as resp:
							text = await resp.text()
							url = str(text).split('"controls"><a href="')[1].split('">')[0]
							await bot.send_message(username,url)
							links.append(url)
					except:
						pass
				await msg.edit(f"✅ Finalizado ✅ \n\n{file.split('/')[-1]}\n[ .txt ] ⤵️")
				txtname = file + '.enlace.txt'
				with open(txtname,"w") as t:
					message = ""
					for li in links:
						message+=li+"\n"
					t.write(message)
					t.close()
				await bot.send_document(usid,txtname,thumb="thumb.jpg")
			else:
				await msg.edit("💠 Subiendo 💠")
				async with session.get(host+"author/submit") as resp:
					print(1)
				async with session.get(host+"author/submit/1") as resp:
					print(2)
				payload = {
					"submissionChecklist": "1",
					"sectionId": "465",
					"locale": "es_ES",
					"checklist[]": [
						"0",
						"1",
						"2",
						"3",
						"4",
						"5"
					],
					"copyrightNoticeAgree": "1",
					"commentsToEditor": ""
				}
				async with session.post(host+"author/saveSubmit/1",data=payload) as resp:
					print(3)
					ids = str(resp.url).split("Id=")[1]
				mime_type, _ = mimetypes.guess_type(file)
				if not mime_type:
					mime_type = "application/x-7z-compressed"

				upload_data = {}
				upload_data["articleId"] = ids
				upload_data["uploadSubmissionFile"] = "Cargar"

				post_file_url = host+"author/saveSubmit/2"
				fi = Progress(file,lambda current,total,timestart,filename: uploadfile_progres(current,total,timestart,filename,msg))
				query = {"submissionFile":fi,**upload_data}
				async with session.post(post_file_url,data=query) as resp:
					text = await resp.text()
					url = str(text).split('"controls"><a href="')[1].split('">')[0]
					await bot.send_message(username,url)
					await msg.edit(f"✅ Finalizado ✅ \n\n{file.split('/')[-1]}\n[ .txt ] ⤵️")
					txtname = file + '.enlace.txt'
					with open(txtname,"w") as t:
						t.write(url)
						t.close()
					await bot.send_document(usid,txtname,thumb="thumb.jpg")
	except Exception as e:
		print(str(e))
async def uploadfileapi(file,usid,msg,username):
	host = "https://educa.uho.edu.cu/"
	proxy = Configs["gp"]
	print(proxy)
	zips = Configs[username]["z"]
	try:
		proxy = aiohttp_socks.ProxyConnector.from_url(f"{proxy}")
	except:
		proxy = aiohttp.TCPConnector()
	await msg.edit("𝑹𝒆𝒄𝒐𝒑𝒊𝒍𝒂𝒏𝒅𝒐 𝒊𝒏𝒇𝒐𝒓𝒎𝒂𝒄𝒊ó𝒏")
	filename = file.split("/")[-1]
	filesize = Path(file).stat().st_size
	total_up[username]['S']+=filesize
	zipssize = 1992294
	logslinks = []
	if filesize-1048>zipssize:
		parts = round(filesize / zipssize)
		await msg.edit(f"📦 𝑪𝒐𝒎𝒑𝒓𝒊𝒎𝒊𝒆𝒏𝒅𝒐\n\n🏷 Total: {parts} partes\n🗂 Zips: 1.8 mb")
		files = sevenzip(file,volume=zipssize)
		session = aiohttp.ClientSession(connector=proxy)
		for file in files:
			try:
				if file.endswith(".zip"):
					filename_god = file
				else:
					file = filezip(file,volume=None)
					filename_god = file[0].split("zip")[0]+".zip"
					os.rename(file[0],filename_god)
				fi = Progress(filename_god,lambda current,total,timestart,filename: uploadfile_progres(current,total,timestart,filename,msg))
				query = {"s97304e7e":fi}
				async with session.post("https://educa.uho.edu.cu/ci_portal_uho/index.php/recursos_pre/my_grocery_recursos_pred/upload_file/archivo",data=query,timeout=60*30) as resp:
					url = loads(await resp.text())["files"][0]["url"]
					logslinks.append(url)
					root[username]["actual_root"] = "downloads/"+username  
			except Exception as ex:
				await bot.send_message(f'!Error:{ex}')
				return
		if len(logslinks) == len(files):
			await msg.delete()
			txtname = "downloads/"+username+"/"+str(filename).split('.')[0]+'.txt'
			with open(txtname,"w") as t:
				message = ""
				lin = ""
				for li in logslinks:
					message+=li+"\n"
					lin+=li+"\n"
				t.write(message)
				t.close()
			await bot.send_document(usid,txtname)
			shutil.rmtree("downloads/"+username+"/")
			root[username]["actual_root"] = "downloads/"+username
		else:
			await msg.edit("Ha fallado la subida ")
			shutil.rmtree("downloads/"+username+"/")
			root[username]["actual_root"] = "downloads/"+username+"/"
	else:
		async with aiohttp.ClientSession(connector=proxy) as session:
			try:	
				if file.endswith(".zip"):
					filename_god = file
				else:
					file = filezip(file,volume=None)
					filename_god = file[0].split("zip")[0]+".zip"
					os.rename(file[0],filename_god)
				fi = Progress(filename_god,lambda current,total,timestart,filename: uploadfile_progres(current,total,timestart,filename,msg))
				query = {"s97304e7e":fi}
				async with session.post("https://educa.uho.edu.cu/ci_portal_uho/index.php/recursos_pre/my_grocery_recursos_pred/upload_file/archivo",data=query,timeout=60*30) as resp:
					url = loads(await resp.text())["files"][0]["url"]
					await bot.send_message(usid,f"[{Path(filename_god).name}]({url})",disable_web_page_preview=True)
					logslinks.append(url)
					root[username]["actual_root"] = "downloads/"+username
			except Exception as ex:
				await bot.send_message(f'!Error:\n{ex}')
				return
							
			if len(logslinks) == 1:
				await msg.edit("**Finalizado exitosamente**")
				with open(filename_god+".txt","w") as t:
					message = ""
					lin = ""
					for li in logslinks:
						message+=li+"\n"
						lin+=li+"\n"
					t.write(message)
				await bot.send_document(usid,filename+".txt")
			else:
				await msg.edit("Ha fallado la subida")


@async_decorator
def nextcom(user, passw, host, proxy,send,files,msg,username,user_id):
	client = NexCloudClient.NexCloudClient(user,passw,host,proxy=proxy)
	loged = client.login()
	if loged:
		filesdata = []
		remotepath = ""
		for file in files:
		   msg.edit(f"Subiendo {file}..")
		   filename = str(file).replace(f'downloads/{username}/','')
		   data = client.upload_file(file,filename,path=remotepath,progressfunc=None,args=(None,None,filename,None),tokenize=None)
		   filesdata.append(data)
		   send(data)
		name = filename+'.txt'
		files = []
		txt = open(name,'w')
		message = ""
		for data in filesdata:
			message+=data+"\n"
		txt.write(message)
		txt.close()
		asyncio.run(bot.send_document(user_id,name))
		return
	else:
		return "Error"


@async_decorator
def next(user, passw, host, proxy,send,file,msg,username):
	client = NexCloudClient.NexCloudClient(user,passw,host,proxy=proxy)
	loged = client.login()
	if loged:
		filesdata = []
		remotepath = ""
		msg.edit(f"Subiendo {file}..")
		filename = str(file).replace(f'downloads/{username}/','')
		data = client.upload_file(file,filename,path=remotepath,progressfunc=None,args=(None,None,filename,None),tokenize=None)
		send(data)
		filesdata.append(data)
		return filesdata
	else:
		return "Error"
		

async def proccess(filex,user_id,msg,username):
        try:
        	send = msg.reply
        	logslinks = []
        	proxy = Configs[username]["gp"]
        	user = Config[username]["username"]
        	passw = Config[username]["password"]
        	host = Config[username]["host"]
        	zips = Configs[username]["z"]
        	file = filex
        	filesize = Path(file).stat().st_size
        	print(20)
        	zipssize = 1024*1024*int(zips)
        	filename = str(file).replace(f'downloads/{username}/','')        
        	if filesize>zipssize:
        	    await msg.edit(f"COMPRIMIENDO")
        	    zipname = str(filename).split('.')[0]
        	    files = sevenzip(file,volume=zipssize)
        	    await msg.edit(f"Preparando Entorno..")
        	    remotepath = "Descargas"        	    
        	    loged = await nextcom(user, passw, host, proxy,send,files,msg,username,user_id)
        	    print(21)
        	    if "Error" not in loged:
        	    	ms = "Links:\n"
        	    	await msg.edit(ms)
        	    	return
        	    await msg.edit(f"Error al loguear...")
        	    return
        	    
#####sincompress####        	    
        	if filesize<=zipssize:
        	   	await msg.edit(f"Preparando Entorno...")
        	   	remotepath = ""
        	   	loged = await next(user, passw, host, proxy,send,file,msg,username)
        	   	if "Error" not in loged:
        	   		client = loged       
        	   		await msg.edit(f"Finalizado...") 	   		
        	   	return
        	   	await msg.edit(f"Error al loguear...")
        	   	return
        except Exception as ex:
            		print(ex)	         		
            #		await msg.edit(f'⚠️{str(ex)}⚠️')
            	
            	      	
         	

print("started")
# Compatibilidad con los identificadores de grupos modernos de Telegram.
import pyrogram.utils
pyrogram.utils.MIN_CHAT_ID = -999999999999
# Telegram limita autorizaciones repetidas tras varios reinicios.
# Esperar el plazo solicitado sin reiniciar el proceso ni acosar el servicio.
from pyrogram.errors import FloodWait
while True:
    try:
        bot.start()
        break
    except FloodWait as e:
        print("Telegram limita el inicio; esperando", e.value, "segundos", flush=True)
        sleep(e.value + 10)
# En el primer arranque, crear el mensaje de datos en el grupo privado.
if not db_access:
    database = bot.send_message(Channel_Id, dumps(Configs, indent=4))
    db_access = database.id
    print("DB_ACCESS_ID:", db_access, flush=True)
print(10)
bot.loop.run_forever()
