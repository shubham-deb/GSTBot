#!/usr/bin/env

import pyttsx
import speech_recognition as sr
import os
import time
from os import system
import urllib2

# Record Audio
r=sr.Recognizer()
ngrok="0346baa5"

# Speech recognition using Google Speech Recognition
try:
	output = "none"
	while "exit" not in output:
		with sr.Microphone() as source:
			print("Say something!")
			audio = r.listen(source)
			output = r.recognize_google(audio)
			if "how" in output and "you" in output:
				reply = "I am fine Raxesh"
			elif "uber" in output:
				reply = "So do you want to go to"+output[-1]
			elif "of" in output:
				urllib2.urlopen("http://"+ngrok+".ngrok.io/LED1=OFF")
				urllib2.urlopen("http://"+ngrok+".ngrok.io/LED2=OFF")
				urllib2.urlopen("http://"+ngrok+".ngrok.io/LED3=OFF")
				reply = "All room lights switched off."
			elif "on" in output:
				urllib2.urlopen("http://"+ngrok+".ngrok.io/LED1=ON")
				urllib2.urlopen("http://"+ngrok+".ngrok.io/LED2=ON")
				urllib2.urlopen("http://"+ngrok+".ngrok.io/LED3=ON")
				reply = "All room lights switched on."
			else:
				reply = "Sorry, I did not understand you"
			system('say '+reply+' &')
			print("You said: " + r.recognize_google(audio))
except sr.UnknownValueError:
	print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
	print("Could not request results from Google Speech Recognition service; {0}".format(e))
