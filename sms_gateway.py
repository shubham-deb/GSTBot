from twilio import twiml
import nltk
from flask import Flask, request
import urllib2
import vlc
import glob
from difflib import SequenceMatcher
import time
from twilio.rest import TwilioRestClient
import requests
import pyowm

ACCOUNT_SID = "ACa7be370a093da413ffc38778e5365171" 
AUTH_TOKEN = "cf96f1247b96d64852db5f3c0db16175" 

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
app = Flask(__name__)

owm = pyowm.OWM('8b72480eda043d8228295d650b019a62')  # You MUST provide a valid API key

ngrok="0346baa5"
@app.route("/sms", methods=['POST'])
def hello():
	in_text = request.form["Body"]
	ph_number = request.form["From"]
	in_text = in_text.lower()
	out_text = get_response(in_text, ph_number)
	response = twiml.Response()
	response.message(out_text)
	return str(response)

def get_response(in_text, ph_number):
	'''
	Get the response output from input
	'''
	if "name" in in_text:
		words = in_text.split()
		word = words[words.index("name")+2]
		lst = [word[0].upper() + word[1:] for word in s.split()]
		index_name = " ".join(lst)
		if words[words.index("name")+1]=="is":
			out_text = "Hi "+index_name+"\
			, Tell me how can i assist you?"
	elif "how" in in_text and "you" in in_text:
		out_text = "I am fine, How could i help you ?"
	elif "light" in in_text and "off" in in_text and "all" in in_text:
		out_text = "All lights switched off."
		urllib2.urlopen("http://"+ngrok+".ngrok.io/LED1=OFF")
		urllib2.urlopen("http://"+ngrok+".ngrok.io/LED2=OFF")
		urllib2.urlopen("http://"+ngrok+".ngrok.io/LED3=OFF")
	elif "light" in in_text and "off" in in_text and "living" in in_text:
		out_text = "Lights switched off for living room."
		urllib2.urlopen("http://"+ngrok+".ngrok.io/LED1=OFF")
	elif "light" in in_text and "off" in in_text and "lobby" in in_text:
		out_text = "Lights switched off for lobby."
		urllib2.urlopen("http://"+ngrok+".ngrok.io/LED2=OFF")
	elif "light" in in_text and "off" in in_text and "bedr" in in_text:
		out_text = "Lights switched off for lobby."
		urllib2.urlopen("http://"+ngrok+".ngrok.io/LED3=OFF")
	elif "light" in in_text and "on" in in_text and "all" in in_text:
		out_text = "All lights switched off."
		urllib2.urlopen("http://"+ngrok+".ngrok.io/LED1=ON")
		urllib2.urlopen("http://"+ngrok+".ngrok.io/LED2=ON")
		urllib2.urlopen("http://"+ngrok+".ngrok.io/LED3=ON")
	elif "light" in in_text and "on" in in_text and "living" in in_text:
		out_text = "Lights switched off for living room."
		urllib2.urlopen("http://"+ngrok+".ngrok.io/LED1=ON")
	elif "light" in in_text and "on" in in_text and "lobby" in in_text:
		out_text = "Lights switched off for lobby."
		urllib2.urlopen("http://"+ngrok+".ngrok.io/LED2=ON")
	elif "light" in in_text and "on" in in_text and "bedr" in in_text:
		out_text = "Lights switched off for lobby."
		urllib2.urlopen("http://"+ngrok+".ngrok.io/LED3=ON")
	elif "music" in in_text and "play" in in_text:
		available = glob.glob("music/*.mp3")
		in_text = in_text.lstrip("music").lstrip("play")
		words = in_text.split()
		max_simi = [music for music in available if words[0] in music]
		p = vlc.MediaPlayer(max_simi[0])
		p.play()
		time.sleep(15)
		p.stop()
	elif "music" in in_text and "stop" in in_text:
		available = glob.glob("music/*.mp3")
		music_selected = available[1]
		p = vlc.MediaPlayer(music_selected)
		p.stop()
	elif ("good" in in_text and "bye" in in_text) or ("exit" in in_text):
		out_text = client.messages.create(
	    to=ph_number, 
	    from_="+17819718068", 
	    body=":)", 
	    media_url="http://smstosay.com/wp-content/uploads/2014/06/have-nice-day-sms.jpg")
	elif "weather" in in_text:
		place=in_text[-1]
		observation = owm.weather_at_place(place+',us')
		w = observation.get_weather()
		# Weather details
		wind_speed = w.get_wind()['speed']                  # {'speed': 4.6, 'deg': 330}
		humidity = w.get_humidity()              # 87
		temp = w.get_temperature('celsius')['temp']  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
		out_text = "The wind speed is "+str(wind_speed)+" and humidity is "+str(humidity)+". The temperature in your area is "+str(temp)+" degree celcius"
	else:
		out_text="How could I help you, you can say :\
		\n* switch off all lights\
		\n* switch on all lights\
		\n* switch off living room lights\
		\n* play music bethovan"
	return out_text


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

if __name__ == "__main__":
	hello.counter=0
	app.run(debug=True)