import os
from requests_html import HTMLSession
from unidecode import unidecode
from ascii_html import ascii_html

ep_list = [
r"Anne_or_Beast?",
r"Best_Fronds",
r"Cane_Crazy",
r"Flood,_Sweat_%26_Tears",
r"Hop_Luck",
r"Stakeout",
r"The_Domino_Effect",
r"Taking_Charge",
r"Anne_Theft_Auto",
r"Breakout_Star",
r"Sprig_Vs._Hop_Pop",
r"Girl_Time",
r"Dating_Season",
r"Anne_Vs._Wild",
r"Contagi-Anne",
r"Family_Shrub",
r"Lily_Pad_Thai",
r"Plantar%27s_Last_Stand",
r"Toad_Tax",
r"Prison_Break",
r"Grubhog_Day",
r"Hop_Pop_and_Lock",
r"Civil_Wart",
r"Hop-Popular",
r"Croak_%26_Punishment",
r"Trip_to_the_Archives",
r"Snow_Day",
r"Cracking_Mrs._Croaker",
r"A_Night_at_the_Inn",
r"Wally_and_Anne",
r"Family_Fishing_Trip",
r"Bizarre_Bazaar",
r"Cursed!",
r"Fiddle_Me_This",
r"The_Big_Bugball_Game",
r"Combat_Camp",
r"Children_of_the_Spore",
r"Anne_of_the_Year",
r"Reunion",
r"Handy_Anne",
r"Fort_in_the_Road",
r"The_Ballad_of_Hopediah_Plantar",
r"Anne_Hunter",
r"Truck_Stop_Polly",
r"A_Caravan_Named_Desire",
r"Quarreler%27s_Pass",
r"Toadcatcher",
r"Swamp_and_Sensibility",
r"Wax_Museum",
r"Marcy_at_the_Gates",
r"Scavenger_Hunt",
r"The_Plantars_Check_In",
r"Lost_in_Newtopia",
r"Sprig_Gets_Schooled",
r"Little_Frogtown",
r"Hopping_Mall",
r"The_Sleepover_to_End_All_Sleepovers",
r"A_Day_at_the_Aquarium",
r"Night_Drivers",
r"Return_to_Wartwood",
r"The_Shut-In!",
r"Ivy_on_the_Run",
r"After_the_Rain",
r"The_First_Temple",
r"New_Wartwood",
r"Friend_or_Frobo?",
r"Toad_to_Redemption",
r"Maddie_%26_Marcy",
r"The_Second_Temple",
r"Barrel%27s_Warhammer",
r"Bessie_%26_MicroAngelo",
r"The_Third_Temple",
r"The_Dinner",
r"Battle_of_the_Bands",
r"True_Colors",
r"The_New_Normal",
r"Hop_%27Til_You_Drop",
r"Turning_Point",
r"Thai_Feud",
r"Adventures_in_Catsitting",
r"Fight_at_the_Museum",
r"Temple_Frogs",
r"Fixing_Frobo",
r"Anne-sterminator",
r"Mr._X",
r"Sprig%27s_Birthday",
r"Spider-Sprig",
r"Olivia_%26_Yunan",
r"Hollywood_Hop_Pop",
r"If_You_Give_a_Frog_a_Cookie",
r"Froggy_Little_Christmas",
r"Escape_to_Amphibia",
r"Commander_Anne",
r"Sprivy",
r"Sasha%27s_Angels",
r"Olm_Town_Road",
r"Mother_of_Olms",
r"Grime%27s_Pupil",
r"The_Root_of_Evil",
r"The_Core_%26_The_King",
r"Newts_in_Tights",
r"Fight_or_Flight",
r"The_Three_Armies",
r"The_Beginning_of_the_End",
r"All_In"
]
session = HTMLSession()

trans_save_path = "p:/amphibia_wiki/transcripts/"
file_path = "p:/amphibia_wiki/"

# transcript_list = []
# gallery_list = []
# all_pages_list = []

# with open(file_path+"amphibia_links.txt","rt") as fi:
#     all_pages_list = fi.readlines()

# base_url = "https://amphibia.fandom.com"

# transcript_list = [x.replace('\n','') for x in all_pages_list if x.find('Transcript') != -1]

# print(transcript_list)

# for t in transcript_list:
#     trans_text = str("")
#     f_name = t.replace('/Transcript','').replace('/wiki/','')
#     print(f_name)
#     r = session.get(base_url+t)
#     r.html.render(timeout=50)
#     sel = f'//*[@id="mw-content-text"]/div'
#     get_trans = r.html.find('p')
#     print(get_trans)
#     for i in range(0,len(get_trans)-1):
#         trans_text = trans_text + str(unidecode(get_trans[i].text)) + str('\n')
#         print(trans_text)
#     with open(trans_save_path+f_name+".txt","wt") as fi:
#         fi.write(unidecode(trans_text.replace('[','(').replace(']',')')))

# file_list = [f.lower().replace('.txt','') for f in ep_list if os.path.isfile(trans_save_path+f+".txt")]
# print(len(file_list))

# t_file_list = [f.lower().replace('.txt','') for f in os.listdir(trans_save_path[:-1:]) if os.path.isfile(trans_save_path+f) and f[-(f[::-1].find('.')):] in ['txt']]

# for i in range(0,len(file_list)-1):
#     if file_list[i] in t_file_list:
#         popdex = t_file_list.index(file_list)
#         t_file_list.pop(popdex)

# print([t for t in t_file_list if t not in file_list])

# for f in file_list:
#     with open(trans_save_path+f,"rt") as fi:
#         f_clean = fi.read()
#     f_clean = f_clean.replace('[','(').replace(']',')').replace('\r\n','\n')
#     f_clean = f_clean.replace('\n\n','\n')
#     with open(trans_save_path+f,"wt") as fi:
#         fi.write('\n'+f_clean)


file_list = [f.lower().replace('.txt','') for f in ep_list]
t_file_list = [f.lower().replace('.txt','') for f in os.listdir(trans_save_path[:-1:]) if os.path.isfile(trans_save_path+f) and f[-(f[::-1].find('.')):] in ['txt']]
for x in file_list:

# //*[@id="mw-content-text"]/div/aside/section[2]/div[2]
# //*[@id="mw-content-text"]/div
# char info //*[@id="mw-content-text"]/div/aside/section[2]/h2
# /#/*[@id="mw-content-text"]/div/p[1]
#mw-content-text > div > p:nth-child(4)
# # /#/*[@id="mw-content-text"]/div
# # /#/*[@id="mw-content-text"]/div
# /html/body/div[4]/div[3]/div[2]/main/div[3]/div[1]/div
#mw-content-text > div
# /html/body/div[4]/div[3]/div[2]/main
# html.client-js.desktop.landscape.pxfcehb.idc0_347.ve-available body.mediawiki.ltr.sitedir-ltr.mw-hide-empty-elt.ns-0.ns-subject.page-A_Night_at_the_Inn_Transcript.rootpage-A_Night_at_the_Inn.skin-fandomdesktop.action-view.ooui-theme-fandomooui.wiki-amphibiapedia.theme-fandomdesktop-light.wikia-bar-visible.menu-dark.page-bright div.main-container div.resizable-container div.page.has-right-rail main.page__main div#content.page-content.ve-init-mw-desktopArticleTarget-targetContainer div#mw-content-text.mw-body-content.mw-content-ltr div.mw-parser-output table.color-main



for t in transcript_list:
    trans_text = str("")
    f_name = t.replace('/Transcript','').replace('/wiki/','')
    print(f_name)
    r = session.get(base_url+t)
    r.html.render(timeout=50)
    sel = f'//*[@id="mw-content-text"]/div'
    get_trans = r.html.find('p')
    print(get_trans)
    for i in range(0,len(get_trans)-1):
        trans_text = trans_text + str(unidecode(get_trans[i].text)) + str('\n')
        print(trans_text)
    with open(trans_save_path+f_name+".txt","wt") as fi:
        fi.write(unidecode(trans_text.replace('[','(').replace(']',')')))





#amphibia_fandom-py.py
# import numpy as np
# import hashlib
# import ssl
# from pathlib import Path
# import urllib.request
# import urllib
# import logging
# import traceback
# import os, sys
# from pathlib import Path
# import concurrent.futures
# from io import BytesIO
# from PIL import Image
# from random import randint
# import cv2
# import unicodedata
# from dataclasses import dataclass
# import re
# import requests
# from bs4 import BeautifulSoup
# from lxml import etree
# import codecs
# from time import sleep


# transcript_list = []
# all_pages_list = []
# with open(save_path+"amphibia_transcript_links.txt","rt") as fi:
#     transcript_list = fi.readlines()
# with open(save_path+"amphibia_links.txt","rt") as fi:
#     all_pages_list = fi.readlines()
# base_url = "https://amphibia.fandom.com"
# print(base_url+transcript_list[0])
# req_url = base_url+transcript_list[0]
# r = session.get("https://amphibia.fandom.com/wiki/A_Night_at_the_Inn/Transcript")
# r.html.render(timeout=50)
# print(r.html.xpath('/html/body/div[4]/div[3]/div[2]/main/div[3]/div/div/p'))
# get_trans = r.html.xpath('/html/body/div[4]/div[3]/div[2]/main/div[3]/div/div/p')
# for i in range(0,len(get_trans)-1):
#     x = get_trans[i].text
#     print(x)

# req_url = base_url+transcript_list[0]
# xp = "/html/body/div[4]/div[3]/div[2]/main/div[3]/div/div/table[3]/*"
# r = session.get("https://amphibia.fandom.com/wiki/A_Night_at_the_Inn/Transcript")
# r.html.render(timeout=50)
# print(r.html.xpath(xp))
# get_trans = r.html.xpath(xp)
# for i in range(0,len(get_trans)-1):
#     x = get_trans[i].text
#     print(x)

# /html/body/div[4]/div[3]/div[2]/main/div[3]/div/div/table[3]

# with open(save_path+"amphibia_tr0.txt","wb") as fi:
#     fi.write(str(r.html.html).encode(encoding='utf-8',errors='ignore'))