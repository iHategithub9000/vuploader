import argparse
import requests
import random
import os
import base64
import json

parser = argparse.ArgumentParser(description="Python script for uploading a voice message from a file to a Discord channel", epilog="Discord Token is taken from USER_TOKEN.txt in pwd")
parser.add_argument("filename", type=str, help="Filename")
parser.add_argument("channel_id", type=int, help="The Channel ID")
parser.add_argument("--duration", type=float, default=0, help="The shown voice message duration. Can be any float between 0 and 2147483647. Defaults to 0")
parser.add_argument("--noisetype", type=str, default='cone', help="Determines the waveform displayed in the message. Can be 'random', 'reversecone', 'cone', 'silence', 'wall', 'specified'. Defaults to 'cone'.")
parser.add_argument("--nspec", type=str, help="A 256 element long byte array encoded in base64. This will be sent to Discord as waveform data if you specify 'specified' in noisetype, otherwise this is ignored.")
args = parser.parse_args()

with open("USER_TOKEN.txt", "r", encoding="utf-8") as f:
	USER_TOKEN = f.read().strip()

CHANNEL_ID = args.channel_id
VOICE_FILE = args.filename


def noise():
	match args.noisetype:
		case 'wall':
			return base64.b64encode(bytes([255 for _ in range(256)])).decode()
		case 'silence':
			return base64.b64encode(bytes([0 for _ in range(256)])).decode()
		case 'reversecone':
			return base64.b64encode(bytes([255-i for i in range(256)])).decode()
		case 'cone':
			return base64.b64encode(bytes([i for i in range(256)])).decode()
		case 'random':
			return base64.b64encode(bytes([random.randint(0, 255) for _ in range(256)])).decode()
		case 'specified':
			return args.nspec
		case _:
			raise ValueError(f"i'm gonna be real with you: i don't know what the fuck {args.noisetype} means.")
	

def send_request(url, method='POST', data=None, headers=None):
	if headers is None:
		headers = {}
	method = method.upper()
	if isinstance(data, bytes):
		response = requests.request(method, url, data=data, headers=headers)
	else:
		response = requests.request(method, url, json=data, headers=headers)
	return response

print("sending request to generate an upload URL")

uploadData = send_request(f"https://discord.com/api/v10/channels/{CHANNEL_ID}/attachments", data={
	"files": [
		{
			"filename": "voice-message.ogg",
			"file_size": os.path.getsize(VOICE_FILE),
			"id": "2"
		}
	]
}, headers={
	"Content-Type": "application/json",
	"Authorization": USER_TOKEN
})

uploadData = uploadData.json()
print(f"../channels/{CHANNEL_ID}/attachments returned", uploadData)

with open(VOICE_FILE, "rb") as f:
	voiceData = f.read()

print("sending raw voice bytes at", uploadData['attachments'][0]['upload_url'])
uploadResponse = send_request(uploadData['attachments'][0]['upload_url'], method="PUT", data=voiceData, headers={
	"Content-Type": "audio/ogg",
	"Authorization": USER_TOKEN
})

print("so we just got done sending all that bullshit - time to send a message to the", f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages")
waveform = noise()
print('wave is ',waveform)
that_fucker = send_request(f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages", data={
	"flags": 8192,
	"attachments": [
		{
			"id": 0,
			"filename": "voice-message.ogg",
			"uploaded_filename": uploadData['attachments'][0]['upload_filename'],
			"duration_secs": args.duration,
			"waveform": waveform
		}
	]
}, headers={
	"Content-Type": "application/json",
	"Authorization": USER_TOKEN
})
print("done, here's the response to sending a message:")
print("that_fucker.text =",that_fucker.text.strip())
print("that_fucker.status_code =",that_fucker.status_code)