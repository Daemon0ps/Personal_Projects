#osbar_scrape.py

import numpy as np
import hashlib
import ssl
from pathlib import Path
import urllib.request
import urllib
import re
import logging
import traceback
import os, sys
from pathlib import Path
import concurrent.futures
from io import BytesIO
from PIL import Image
import codecs
from time import sleep
from random import randint
import unicodedata
from dataclasses import dataclass
from termcolor import cprint
import cv2
from unidecode import unidecode
import requests

save_path = "p:/amphibia_wiki/"

# https://www.osbar.org/_docs/ethics/2005-123.pdf

headers = {'User-Agent': "Mozilla/5.0 (Windows; U; Win98; en-US; rv:1.6) Gecko/20040206 Firefox/0.8",
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                'Accept-Encoding': 'none',
                'Accept-Language': 'en-US,en;q=0.8',
                'Connection': 'keep-alive'}

request_urls = [
                "https://amphibia.fandom.com/wiki/Special:AllPages?from=%22BFFs%22+photo",
                "https://amphibia.fandom.com/wiki/Special:AllPages?from=Commander+Anne",
                "https://amphibia.fandom.com/wiki/Special:AllPages?from=Jess",
                "https://amphibia.fandom.com/wiki/Special:AllPages?from=Quarreler%27s+Pass%2FGallery",
                "https://amphibia.fandom.com/wiki/Special:AllPages?from=The+Third+Temple%2FGallery"
                ]

base_url = "https://amphibia.fandom.com"

amphibia_links = []
pg_check = True
cprint("start","blue")
for x in request_urls:
    request_url = x
    cprint(request_url,"blue")
    r = requests.get(request_url)
    html = r.text
    links = re.findall(r'<li><a href="(.*?)" title="', codecs.decode(str(html).encode(encoding='utf-8',errors='ignore')))
    if len(links) > 0:
        link_list = [str(x) for x in links]
        for x in link_list:
            amphibia_links.append(x+'\n')

print(amphibia_links)

with open(save_path+"amphibia_links.txt","wt") as fi:
    fi.writelines(amphibia_links)