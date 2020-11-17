import cv2
import numpy as np
from scipy.io import wavfile
import math
from audiotsm import phasevocoder
from shutil import copyfile, rmtree
import sys
import subprocess
from pytube import YouTube
import os
import glob
from bs4 import BeautifulSoup
import requests




 
def getPlaylistLinks(url):
    sourceCode = requests.get(url).text
    soup = BeautifulSoup(sourceCode, 'html.parser')
    returnlist=[]
    domain = 'https://www.youtube.com'
    for link in soup.find_all("a", {"dir": "ltr"}):
        href = link.get('href')
        if href.startswith('/watch?'):
            link = (domain + href + '\n')
            returnlist.append(link)
    return returnlist
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

deletePath("output")
deletePath("out")

createPath("output")
createPath("out")
nombre="procesado.mp4"
test = None
videoFile="archivo.mp4"

try:
    subprocess.call("python3 splitter.py -f "+videoFile+" -s 1000",shell=True)

    f = sorted(glob.glob("output/*.mp4"))
    for i in f:
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
