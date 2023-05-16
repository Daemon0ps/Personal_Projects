from __future__ import annotations
import discord
import os, sys
import random
import keyring
from aiomcrcon import Client as MC_Client
import asyncio
import string
from unidecode import unidecode
import pyinotify
import subprocess
import struct
import random
import enum
import typing as t
import re
from time import sleep
from discord.ext import tasks

# user@hostname:/home$ sudo apt install gnome-keyring
# user@hostname:/home$ ./home/username/miniconda3/envs/minecraft_bot/bin/python
# >>> import keyring
# >>> keyring.get_keyring()
# <keyring.backends.SecretService.Keyring object at 0x0c0c0c0c0c0c>
# >>> #if you see the object above, keyring should be good to go
# keyring.set_password("mc_bot", "mc", "DISCORD_TOKEN")
# keyring.set_password("mc_bot", "mc_rcon", "PASSWORD")

# keyring.get_password("mc_bot", "mc_rcon")
# keyring.get_password("mc_bot", "mc")

mcf = [ #Minecraft_Format_Strings
        "§0","§1","§2","§3",\
        "§4","§5","§6","§7",\
        "§8","§9","§a","§b",\
        "§c","§d","§e","§f",\
        "§g","§h","§i","§j",\
        "§m","§n","§p","§q",\
        "§s","§t","§u","§k",\
        "§l","§m","§n","§o","§r"]

def rm_white(s)->str:
    return  " ".join(str(s).split())

def re_srch(s, srch):
    s = str(s)
    r_s = re.search(str(srch),string=str(s),flags=(re.IGNORECASE|re.M|re.ASCII))
    if r_s is None:
        return s
    if r_s is not None:
        s_start = r_s.start()
        s_end = r_s.end()
        return s.replace(str([[s[-(len(s)-s_start):]][0][:s_end-s_start]][0]),chr(32)+str([[s[-(len(s)-s_start):]][0][:s_end-s_start]][0]).replace(chr(32),''))

class RCONConnectionError(Exception):
    """Raised when the Client.connect() method fails."""

    def __init__(self, msg: t.Optional[str] = None, error: t.Optional[Exception] = None) -> None:
        super().__init__(msg)

        self.message = msg
        self.error = error


class ClientNotConnectedError(Exception):
    """Raised when an IO method is used when the Client isn't connected."""

    def __init__(self) -> None:
        super().__init__(
            "The client isn't connected. (Looks like you forgot to call the connect() coroutine!)"
        )


class IncorrectPasswordError(Exception):
    """Raised when the RCON authentication / password is incorrect."""

    def __init__(self) -> None:
        super().__init__(
            "The password provided to the client was incorrect according to the server."
        )


class MessageType(enum.IntEnum):
    LOGIN = 3
    COMMAND = 2
    RESPONSE = 0
    INVALID_AUTH = -1


class Client:
    """The base class for creating an RCON client."""

    def __init__(self, host: str, port: int, password: str) -> None:
        self.host = host
        self.port = port
        self.password = password

        self._reader = None
        self._writer = None

        self._ready = False

    async def __aenter__(self, timeout=2) -> Client:
        await self.connect(timeout)
        return self

    async def __aexit__(self, exc_type: type, exc: Exception, tb: t.Any) -> None:
        await self.close()

    async def connect(self, timeout: float = 2.0) -> None:
        """Sets up the connection between the client and server."""

        if self._ready:
            return

        try:
            self._reader, self._writer = await asyncio.wait_for(
                asyncio.open_connection(self.host, self.port), timeout
            )
        except (asyncio.TimeoutError, TimeoutError) as e:
            raise RCONConnectionError(
                "A timeout occurred whilst attempting to connect to the server.", e
            )
        except ConnectionRefusedError as e:
            raise RCONConnectionError("The remote server refused the connection.", e)
        except Exception as e:
            raise RCONConnectionError("The connection failed for an unknown reason.", e)

        await self._send_msg(MessageType.LOGIN, self.password)

        self._ready = True

    async def _send_msg(self, type_: int, msg: str) -> t.Tuple[str, int]:
        req_id = random.randint(0, 2147483647)
        packet_data = struct.pack("<ii", req_id, type_) + msg.encode("utf8") + b"\x00\x00"
        packet = struct.pack("<i", len(packet_data)) + packet_data
        self._writer.write(packet)
        await self._writer.drain()
        in_len = struct.unpack("<i", (await self._reader.read(4)))[0]
        in_arr = []
        in_tlen = 0

        while in_tlen < in_len:
            in_tmp = await self._reader.read(in_len - in_tlen)

            if not in_tmp:
                break

            in_tlen += len(in_tmp)
            in_arr.append(in_tmp)

        in_data = b"".join(in_arr)

        if len(in_data) != in_len or not in_data.endswith(b"\x00\x00"):
            raise ValueError("Invalid data received from server.")

        in_type, in_req_id = struct.unpack("<ii", in_data[0:8])

        if in_type == MessageType.INVALID_AUTH:
            raise IncorrectPasswordError

        in_msg = in_data[8:-2].decode("utf8")

        return in_msg, in_type

    async def send_cmd(self, cmd: str, timeout: float = 2.0) -> t.Tuple[str, int]:

        if not self._ready:
            raise ClientNotConnectedError

        return await asyncio.wait_for(self._send_msg(MessageType.COMMAND, cmd), timeout)

    async def close(self) -> None:

        if self._ready:
            self._writer.close()
            await self._writer.wait_closed()

            self._reader = None
            self._writer = None

            self._ready = False

with open('/home/user/logs/latest.log','rt') as fi:
    server_log_init = fi.readlines()
chat_log = [x for x in server_log_init if str(x).find('Async Chat Thread') != -1]
connect_log = [x for x in server_log_init if str(x).find('left the game') != -1 or str(x).find('joined the game') != -1]

if os.path.isfile('/home/user/logs/chat.log'):
    with open('/home/user/logs/chat.log','a') as fi:
        for x in chat_log:
            fi.write(str(x)+'\n')
elif not os.path.isfile('/home/user/logs/chat.log'):
    with open('/home/user/logs/chat.log','wt') as fi:
        for x in chat_log:
            fi.write(str(x)+'\n')

if os.path.isfile('/home/user/logs/connect.log'):
    with open('/home/user/logs/connect.log','a') as fi:
        for x in connect_log:
            fi.write(str(x)+'\n')
elif not os.path.isfile('/home/user/logs/connect.log'):
    with open('/home/user/logs/connect.log','wt') as fi:
        for x in connect_log:
            fi.write(str(x)+'\n')

class MyClient(discord.Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        self.chat_loop.start()
        self.connect_loop.start()

    @tasks.loop(seconds = 3)
    async def chat_loop(self):
        try:
            new_chat_log = []
            new_chat_log.clear()
            server_log_init = []
            server_log_init.clear()
            channel = self.get_channel(__CHANNEL_NO__)  # channel ID goes here
            with open('/home/user/logs/latest.log','rt') as fi:
                server_log_init = fi.readlines()
            new_chat_log = [x for x in server_log_init if str(x).find('Async Chat Thread') != -1 and x not in chat_log]
            for x in new_chat_log:
                chat_name = re.findall(r"INFO]: <(.*?)>",x)
                chat_msg = re.findall(r"> (.*?)\n",x)
                await channel.send("__**"+str(chat_name[0])+"**__: *"+str(chat_msg[0])+"*")
                chat_log.append(x)
                sleep(0.5)
            if os.path.isfile('/home/user/logs/chat.log'):
                with open('/home/user/logs/chat.log','a') as fi:
                    for x in new_chat_log:
                        fi.write(str(x)+'\n') 
        except Exception as e:
            print(e)
            pass

    @tasks.loop(seconds = 7)
    async def connect_loop(self):
        try:
            in_connect_log = []
            in_connect_log.clear()
            out_connect_log = []
            out_connect_log.clear()
            server_log_init = []
            server_log_init.clear()
            channel = self.get_channel(__CHANNEL_NO__)  # channel ID goes here
            with open('/home/user/logs/latest.log','rt') as fi:
                server_log_init = fi.readlines()
            in_connect_log = [x for x in server_log_init if str(x).find('joined the game')>1 and x not in connect_log]
            out_connect_log = [x for x in server_log_init if str(x).find('left the game')>1 and x not in connect_log]
            print("in: ",len(in_connect_log))
            print("out: ",len(out_connect_log))
            for x in in_connect_log:
                connect_log.append(x)
                cxn_in = re.findall(r"/INFO]: (.*?) joined the game",x)         
                in_send = str("`"+str(cxn_in[0])+" has joined the game`")
                await channel.send(in_send)
            for x in out_connect_log:
                connect_log.append(x)
                cxn_out = re.findall(r"/INFO]: (.*?) left the game",x)
                out_send = str("`"+str(cxn_out[0])+" has left the game`")
                await channel.send(out_send)
                sleep(0.5)
            if os.path.isfile('/home/user/logs/connect.log'):
                with open('/home/user/logs/connect.log','a') as fi:
                    for x in out_connect_log:
                        fi.write(str(x)+'\n')
                    for x in in_connect_log:
                        fi.write(str(x)+'\n')                       
        except Exception as e:
            print(e)
            pass

    async def on_message(self, message):
        rcon_response = ""
        rcon_cmd = ""
        # don't respond to ourselves
        if message.author == self.user:
            return
        
        if message.channel.id == __CHANNEL_NO__:
            if message.content[:4] == '!srv':
                if str(message.author) in admin_list:
                    rcon_cmd = str(message.content[4:]).strip()
                    mc_client = MC_Client("127.0.0.1", 25575, rcon_pass)
                    await mc_client.connect()
                    rcon_response = await mc_client.send_cmd(rcon_cmd)
                    rcon_parse = str(rcon_response[0])
                    for i in mcf:
                        rcon_parse = rcon_parse.replace(str(i),"")
                    rcon_parse = rcon_parse.replace("\\n","\n")
                    await mc_client.close()
                    await message.channel.send(rcon_parse)
            if message.content == 'ping':
                await message.channel.send('pong')
                await message.channel.send("Author: " + str(message.author))
                await message.channel.send("Channel ID: " + str(message.channel.id))
                channel = self.get_channel(__CHANNEL_NO__)
                await channel.send("Author: " + str(message.author))
                await channel.send("Channel ID: " + str(message.channel.id))

        if message.channel.id == __CHANNEL_NO__:
            if message.content == 'ping':
                await message.channel.send('pong')
                await message.channel.send("Author: " + str(message.author))
                await message.channel.send("Channel ID: " + str(message.channel.id))
                channel = self.get_channel(__CHANNEL_NO__)
                await channel.send("Author: " + str(message.author))
                await channel.send("Channel ID: " + str(message.channel.id))

  
discord_token = keyring.get_password("mc_bot","mc")
rcon_pass = keyring.get_password("mcC_bot","mc_rcon")
admin_list = ["DISCORD_NAME","DISCORD_NAME","DISCORD_NAME"]
server_log = []
mcf = [
        "§x","§0","§1","§2","§3",\
        "§4","§5","§6","§7",\
        "§8","§9","§a","§b",\
        "§c","§d","§e","§f",\
        "§g","§h","§i","§j",\
        "§m","§n","§p","§q",\
        "§s","§t","§u","§k",\
        "§l","§m","§n","§o","§r","m]"]

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(discord_token)



