# bot.py
import os
import random
import discord
import logging
import requests
import re
import time
import asyncio
import json
import dropbox
import pathlib
import subprocess
import numpy as np
from scipy.io import wavfile
import math
from audiotsm import phasevocoder
from shutil import copyfile, rmtree
import sys
from pytube import YouTube
import glob
from bs4 import BeautifulSoup
import string
import gdown
adsasdads=1

def createPath(s):
    #assert (not os.path.exists(s)), "The filepath "+s+" already exists. Don't want to overwrite it. Aborting."

    try:  
        os.mkdir(s)
    except OSError:  
        assert False, "Creation of the directory %s failed. (The TEMP folder may already exist. Delete or rename it, and try again.)"

def deletePath(s): # Dangerous! Watch out!
    try:  
        rmtree(s,ignore_errors=False)
    except OSError:  
        adsasdads=1

token = "discord token"

client = discord.Client()
d = dropbox.Dropbox("dropbox token")

    # located in this folder


working=False
def downloadFile(url):
    if YouTube(url).streams.get_by_itag(22):
        name = YouTube(url).streams.get_by_itag(22).download()
    else:
        name = YouTube(url).streams.first().download()
    name2 = name.split('/')
    name = name2[-1]
    newname = name.replace(' ','_')
    os.rename(name,newname)
    newname=newname.split("/")
    return newname[-1]
async def gd(link,message,nombre,filepath,targetfile):
    try:
        gdown.download(link,"archivo.mp4",quiet=False)
        await message.edit(content="Se descargo tu archivo")
        await message.edit(content="Se procesara tu archivo")
        await testmain(message,nombre)
        await message.edit(content="Espere mientras se genera el link de descarga")
        with filepath.open("rb") as f:
            meta = d.files_upload(f.read(), targetfile, mode=dropbox.files.WriteMode("overwrite"))
        link = d.sharing_create_shared_link(targetfile)
        url = link.url
        dl_url = re.sub(r"\?dl\=0", "?dl=1", url)
        return dl_url
    except:
        await message.edit(content="Ocurrio un error: Por favor verifique el que link es publicamente accesible")


async def dropD(link,message,nombre,filepath,targetfile):
    d.sharing_get_shared_link_file_to_file("archivo.mp4",link)
    await message.edit(content="Se descargo tu archivo")
    await message.edit(content="Se procesara tu archivo")
    await testmain(message,nombre)
    await message.edit(content="Espere mientras se genera el link de descarga")
    with filepath.open("rb") as f:
        meta = d.files_upload(f.read(), targetfile, mode=dropbox.files.WriteMode("overwrite"))
    link = d.sharing_create_shared_link(targetfile)
    url = link.url
    dl_url = re.sub(r"\?dl\=0", "?dl=1", url)
    return dl_url
async def yt(link,message,nombre,filepath,targetfile):
    await message.edit(content="Se descargara tu archivo")
    dir=downloadFile(link)
    await asyncio.sleep(10)
    await message.edit(content="Se procesara tu archivo")
    await testmainyt(message,nombre,dir)
    await message.edit(content="Espere mientras se genera el link de descarga")
    with filepath.open("rb") as f:
        meta = d.files_upload(f.read(), targetfile, mode=dropbox.files.WriteMode("overwrite"))
    link = d.sharing_create_shared_link(targetfile)
    url = link.url
    dl_url = re.sub(r"\?dl\=0", "?dl=1", url)
    return dl_url
async def testmain(message,nombre):
    deletePath("output")
    deletePath("out")
    createPath("output")
    createPath("out")
    test = None
    videoFile="archivo.mp4"
    subprocess.call("ffmpeg -y  -i archivo.mp4 -filter:v fps=fps=25 archivo25.mp4",shell=True)
    videoFile="archivo25.mp4"
    try:
        subprocess.call("python3 splitter.py -f "+videoFile+" -s 60 -v h264 ",shell=True)

        f = sorted(glob.glob("output/*.mp4"))
        await message.edit(content="<@"+ str(message.author.id) + "> Se procesaran "+str(len(f))+" segmentos")
        porcentaje=100/len(f)
        for i in f:
            await message.edit(content='{0:.2f}%'.format(porcentaje*f.index(i))+" completado")
            subprocess.call("python3 jump.py --input_file "+i+" --output_file out/"+i.strip("output/")+" --sounded_speed 1 --silent_speed 999999 --frame_margin 4 --frame_rate 25", shell=True)

        outfiles= sorted(glob.glob("out/*.mp4"))
        f= open("mylist.txt","w+")
        for i in outfiles:
            linea="file '"+i+"'\n"
            f.write(linea)
        f.close()
        subprocess.call("ffmpeg -f concat -safe 0 -i mylist.txt -c copy "+nombre,shell=True)
    except OSError:
        subprocess.call("python3 jump.py --input_file "+videoFile+" --output_file "+nombre+" --sounded_speed 1 --silent_speed 999999 --frame_margin 4 --frame_rate 25", shell=True)
    deletePath("output")
    deletePath("out")
async def testmainyt(message,nombre,path):
    
    deletePath("output")
    deletePath("out")
    createPath("output")
    createPath("out")
    test = None
    videoFile=path
    subprocess.call("ffmpeg -y -i "+videoFile+" -filter:v fps=fps=25 archivo25.mp4",shell=True)
    videoFile="archivo25.mp4"
    try:
        subprocess.call("python3 splitter.py -f "+videoFile+" -s 60 -v h264",shell=True)

        f = sorted(glob.glob("output/*.mp4"))
        await message.edit(content="<@"+ str(message.author.id) + "> Se procesaran "+str(len(f))+" segmentos")
        porcentaje=100/len(f)
        for i in f:
            await message.edit(content='{0:.2f}%'.format(porcentaje*f.index(i))+" completado")
            subprocess.call("python3 jump.py --input_file "+i+" --output_file out/"+i.strip("output/")+" --sounded_speed 1 --silent_speed 999999 --frame_margin 4 --frame_rate 25", shell=True)

        outfiles= sorted(glob.glob("out/*.mp4"))
        f= open("mylist.txt","w+")
        for i in outfiles:
            linea="file '"+i+"'\n"
            f.write(linea)
        f.close()
        subprocess.call("ffmpeg -f concat -safe 0 -i mylist.txt -c copy "+nombre,shell=True)
    except OSError:
        subprocess.call("python3 jump.py --input_file "+videoFile+" --output_file "+nombre+" --sounded_speed 1 --silent_speed 999999 --frame_margin 4 --frame_rate 25", shell=True)
    deletePath("output")
    deletePath("out")



@client.event
async def on_ready():
    print(f'{client.user} se conecto sin problemas')

@client.event
async def on_message(message):
    folder = pathlib.Path(".")
    pre=''.join(random.choices(string.ascii_uppercase + string.digits, k= 10))
    filename = pre+".mp4"
    filepath = folder / filename
    target = "/Descargas/"              # the target folder
    targetfile = target + filename
    global working
    if message.author.bot:
        return

    if  '!zoomD' in message.content:
        if working==False:
            working=True
            msg = await message.channel.send("<@"+ str(message.author.id) + "> Se va a descargar tu archivo")
            menlist= message.content.split(" ")
            link = menlist[1]
            Url = await dropD(link,msg,filename,filepath,targetfile)
            response = "Se proceso tu archivo, este es el link de descarga: "+Url
            await msg.edit(content=response)
            working=False
        else:
            msg=await message.channel.send("<@"+ str(message.author.id) + "> Me encuentro procesando otro video en este momento. Volvere a intentarlo cada minuto a partir de ahora")
            while working==True:
                await asyncio.sleep(60)
                print("reitentando")
            print("ahora se puede ejecutar")
            working=True
            await msg.edit(content="<@"+ str(message.author.id) + "> Se va a descargar tu archivo")
            menlist= message.content.split(" ")
            link = menlist[1]
            Url = await dropD(link,msg,filename,filepath,targetfile)
            response = "Se proceso tu archivo, este es el link de descarga: "+Url
            await msg.edit(content=response)
            working=False

    if  '!zoomY' in message.content:
        if working==False:
            working=True
            msg=await message.channel.send("<@"+ str(message.author.id)  + "> Se va a descargar tu archivo")
            menlist= message.content.split(" ")
            link = menlist[1]
            Url = await yt(link,msg,filename,filepath,targetfile)
            response = "Se proceso tu archivo, este es el link de descarga: "+Url
            await msg.edit(content=response)
            working=False
        else:
            msg=await message.channel.send("<@"+ str(message.author.id) + "> Me encuentro procesando otro video en este momento. Volvere a intentarlo cada minuto a partir de ahora")
            while working==True:
                await asyncio.sleep(60)
                print("reitentando")
            working=True
            await msg.edit(content="<@"+ str(message.author.id) + "> Se va a descargar tu archivo")
            menlist= message.content.split(" ")
            link = menlist[1]
            Url = await yt(link,msg,filename,filepath,targetfile)
            response = "Se proceso tu archivo, este es el link de descarga: "+Url
            await msg.edit(content=response)
            working=False
    if '!zoomG' in message.content:
        print("entro")
        if working==False:
            working=True
            msg=await message.channel.send("<@"+ str(message.author.id) + "> Se va a descargar tu archivo")
            menlist= message.content.split(" ")
            link = menlist[1]
            link=link.replace("https://drive.google.com/file/d/","https://drive.google.com/uc?export=download&id=")
            link = link.replace("/view?usp=sharing","")
            Url = await gd(link,msg,filename,filepath,targetfile)
            response = "Se proceso tu archivo, este es el link de descarga: "+Url
            await msg.edit(content=response)
            working=False
        else:
            msg=await message.channel.send("<@"+ str(message.author.id) + "> Me encuentro procesando otro video en este momento. Volvere a intentarlo cada minuto a partir de ahora")
            while working==True:
                await asyncio.sleep(60)
                print("reitentando")
            working=True
            await msg.edit(content="<@"+ str(message.author.id) + "> Se va a descargar tu archivo")
            menlist= message.content.split(" ")
            link = menlist[1]  
            link=link.replace("https://drive.google.com/file/d/","https://drive.google.com/uc?export=download&id=")
            link = link.replace("/view?usp=sharing","")
            Url = await gd(link,msg,filename,filepath,targetfile)
            response = "Se proceso tu archivo, este es el link de descarga: "+Url
            await msg.edit(content=response)
            working=False
    if "!test" in message.content:
        await message.channel.send("<@"+ str(message.author.id) + "> funciona")



logging.basicConfig(level=logging.INFO)
client.run(token)
