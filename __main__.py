import string
import time
from time import sleep
from time import strftime
import datetime
import os
import sys
import subprocess
import re
#speech recognition  / polly#
from tempfile import gettempdir
import speech_recognition as sr
from pygame import mixer
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import random
#facial recognition#
import face_recognition
import cv2
#URL / Song#
import requests
import vlc
import urllib
#converastion#
import conversations
import wikipedia

r = sr.Recognizer()
m = sr.Microphone()

session = Session(profile_name="adminuser")
polly = session.client("polly")
hello = False
searching = False
songactive = False
name = False
faceid = None

def run_once(f):
	def wrapper(*args, **kwargs):
		if not wrapper.has_run:
			wrapper.has_run = True
			return f(*args, **kwargs)
	wrapper.has_run = False
	return wrapper

def facerecognition():
	video_capture = cv2.VideoCapture(0)

	# Sample recognizer.
	tyler_image = face_recognition.load_image_file("tyler.jpg")
	tyler_face_encoding = face_recognition.face_encodings(tyler_image)[0]
	# Sample recognizer.
	#donna_image = face_recognition.load_image_file("donna.jpg")
	#donna_face_encoding = face_recognition.face_encodings(donna_image)[0]
	# Sample Recognizer.
	#justin_image = face_recognition.load_image_file("justin.jpg")
	#justin_face_encoding = face_recognition.face_encodings(justin_image)[0]
	# Known faces
	known_face_encodings = [
	    tyler_face_encoding,
	 #   donna_face_encoding,
	#   justin_face_encoding
	]
	known_face_names = [
	    "Tyler",
	    "Donna",
	    "Justin"
	]

	face_locations = []
	face_encodings = []
	face_names = []
	process_this_frame = True
	if video_capture != True:
		return;

	while True:
		try:
		    # Grab a single frame of video
		    ret, frame = video_capture.read()

		    # Resize frame of video to 1/4 size for faster face recognition processing
		    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

		    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
		    rgb_small_frame = small_frame[:, :, ::-1]

		    # Only process every other frame of video to save time
		    if process_this_frame:
			# Find all the faces and face encodings in the current frame of video
			face_locations = face_recognition.face_locations(rgb_small_frame)
			face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

			face_names = []
			for face_encoding in face_encodings:
			    # See if the face is a match for the known face(s)
			    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
			    name = "Unknown"
			    # If a match was found in known_face_encodings, just use the first one.
			    if True in matches:
				first_match_index = matches.index(True)
				name = known_face_names[first_match_index]
			        face_names.append(name)
			        facerecognition.name = name

		    	    if name == "Unknown":
				unknownface()

		    process_this_frame = not process_this_frame


		    # Display the results
		    for (top, right, bottom, left), name in zip(face_locations, face_names):
			# Scale back up face locations since the frame we detected in was scaled to 1/4 size
			top *= 4
			right *= 4
			bottom *= 4
			left *= 4

			# Draw a box around the face
			cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

			# Draw a label with a name below the face
			cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
			font = cv2.FONT_HERSHEY_DUPLEX
			cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

		    # Display the resulting image
		    cv2.imshow('Video', frame)

		    # Hit 'q' on the keyboard to quit
		    if True in matches:
			initspeech(facerecognition)
			break;
		    else:
			unknownface()
			return;

			# Release handle to the webcam
		    video_capture.release()
	   	    cv2.destroyAllWindows()
	        except Exception:
			unknownferror()
			continue;

	return name, matches;


class songcontroller:
	@staticmethod
	def songs(talk, polly):
		while True:
			#http://localhost:9999/get_by_search?type=song&artist=Daftpunk&title=Loseyourselftodance
			artistname = talk.replace('play', '')
			urllib.quote(artistname)
			#global requestsong
			payload = {'artist' : artistname}
			songcontroller.requestsong = requests.get('http://localhost:9999/get_by_search?type=song', params=payload)
			print(songcontroller.requestsong.url)
			response = polly.synthesize_speech(Text="Ok, playing your request of" + artistname, OutputFormat='mp3', VoiceId='Justin')
			respondmodule(response)
			time.sleep(3.5)
			break;
		


def playmusic(songcontroller):
	playmusic.Media = vlc.MediaPlayer(songcontroller.requestsong.url)
	playmusic.Media.play()


def pausemusic(playmusic):
	playmusic.Media.stop()
	global songactive
	songactive = False
	print(songactive)

def conversation():
	global hello
	hello = True

def songinit():
	global songactive
	songactive = True
	print(songactive)

def searchinit():
	global searching
	searching = True

def respondmodule(response):
	if "AudioStream" in response:
		with closing(response["AudioStream"]) as stream:
			output = os.path.join(gettempdir(), "speech.mpg")
			try:
				with open(output, "wb") as file:
					file.write(stream.read())
	 				opener = "open" if sys.platform == "darwin" else "xdg-open"
					subprocess.call([opener, output])

			except IOError as error:
				print(error)
				sys.exit(-1)
	return; 



#def mira (polly):
#	if "AudioStream" in response:
#		with closing(response["AudioStream"]) as stream:
#			output = os.path.join(gettempdir(), "speech.mpg")
#			try:
#				with open(output, "wb") as file:
#					file.write(stream.read())
#	 				opener = "open" if sys.platform == "darwin" else "xdg-open"
#  					SyntaxWarningsubprocess.call([opener, output])
#
#			except IOError as error:
#				print(error)
#				sys.exit(-1)
#	return;

def mira_time ():
	current = datetime.datetime.now().strftime('<speak>The current date is, %A, %B %d, %Y. And time is now, %l:%M %p .</speak>')
	response = polly.synthesize_speech(TextType='ssml', Text=current, OutputFormat='mp3', VoiceId='Justin')
	respondmodule(response)

@run_once
def unknownferror():
	time.sleep(6)
	response = polly.synthesize_speech(Text="Sorry, I can't recognize you. Please make sure the lights are on and I can see you!", OutputFormat='mp3', VoiceId='Justin')
	respondmodule(response)

@run_once
def unknownface():
	time.sleep(6)
	response = polly.synthesize_speech(Text="Hi there. I don't recognize you. What is your name?", OutputFormat='mp3', VoiceId='Justin')
	respondmodule(response)
	time.sleep(2)

def initspeech(facerecognition):
	#facerecognition()
	conversation()
	if facerecognition.name != "Unknown":
		replyname = facerecognition.name
		response = polly.synthesize_speech(Text="hello there" +replyname +random.choice(conversations.greeting_response), OutputFormat='mp3', VoiceId='Justin')
		respondmodule(response)

facerecognition()

try:
    print("A moment of silence, please...")
    with m as source: r.adjust_for_ambient_noise(source)
    print("Set minimum energy threshold to {}".format(r.energy_threshold))

    while True:
	print("Say something!")
	with m as source: audio = r.listen(source)
	print("Got it! Now to recognize it...")

	try:
	    # recognize speech using Google Speech Recognition
	    talk = r.recognize_google(audio).lower()
	    splitted = r.recognize_google(audio).lower().split()


	    while name == False:
		if talk in (conversations.name_list):
			name = talk
			response = polly.synthesize_speech(Text='Ok! I will keep your name in mind,' +name, OutputFormat='mp3', VoiceId='Justin')
			respondmodule(response)
			time.sleep(4)
			response = polly.synthesize_speech(Text='Can I take a photo of your face so that I can easily identify you next time?', OutputFormat='mp3', VoiceId='Justin')
			respondmodule(response)
			name = True
			faceid = False

		else:
			response = polly.synthesize_speech(Text='Sorry, but I am not willing to be of service to unauthorized users.', OutputFormat='mp3', VoiceId='Justin')
			respondmodule(response)
			name = True
	   		break;


	    while faceid == False:
	   	 if talk in {'okay', 'yes', 'sure', 'go for it', 'certainly'}:
			print('sucess')
			faceid = True
		 else:
		 	break;



	    if hello == True:
	    	if any(word in talk for word in conversations.statusgood_to):
			response = polly.synthesize_speech(TextType='ssml', Text="<speak><break time='1s'/>That's nice to hear!</speak>", OutputFormat='mp3', VoiceId='Justin')
			respondmodule(response)
			hello = False
			time.sleep(3)

		if any(word in talk for word in conversations.status_request):
			response = polly.synthesize_speech(Text="I'm very good, thank you for asking!", OutputFormat='mp3', VoiceId='Justin')
			respondmodule(response)
			time.sleep(4)

		
	   	#if any(word in talk for word in conversations.statusbad_to):
		#	response = polly.synthesize_speech(Text="I'm sorry to hear that! Is there anything I can do to cheer you up?", OutputFormat='mp3', VoiceId='Justin')
		#	respondmodule(response)
		#	statusbad = True

		#if talk in {'yes','okay','sure','yeah','i guess','yes please','please','ya','ok'}:
		#	response = polly.synthesize_speech(Text="Ok. Would you like to hear a good song or a joke?", OutputFormat='mp3', VoiceId='Justin')
		#	respondmodule(response)

		#elif talk in {'no','nope','nah','no thanks','im okay', "i'm okay",'absolutely not'}:
		#	response = polly.synthesize_speech(Text="Ok then.", OutputFormat='mp3', VoiceId='Justin')
		#	respondmodule(response)
		#	hello = False
		#	statusbad = False

		#if talk=='joke':
		#	response = polly.synthesize_speech(Text="Knock Knock, who is there", OutputFormat='mp3', VoiceId='Justin')
		#	respondmodule(response)
		#	statusbad = False
		#	hello = False

		#if talk=='song':
		#	response = polly.synthesize_speech(Text="Here is a good song", OutputFormat='mp3', VoiceId='Justin')
		#	respondmodule(response)
		#	statusbad = False
		#	hello = False
		
		while hello == False:
			time.sleep(1)
			response = polly.synthesize_speech(Text="So "+ facerecognition.name +",what can I do for you today?", OutputFormat='mp3', VoiceId='Justin')
			respondmodule(response)
			time.sleep(1)
			break;


	    if any(word in splitted for word in conversations.song_list):
		songinit()
		if songactive == True:
			songcontroller.songs(talk, polly)
			playmusic(songcontroller)

	    if talk in {'pause','stop'}:
		pausemusic(playmusic)

#	    if any(word in talk for word in {'play me a song by','play song by','song by'}):
#		playmusic(songcontroller)
#		talk = talk.replace('play me a song by', '')
#		print(talk)

	    if any(word in splitted for word in conversations.search_to):
		searchinit()
		if searching == True and songactive == False:
			query = talk.replace('search','')
			result = wikipedia.summary(query, chars=1, sentences=2)
			response = polly.synthesize_speech(Text= result, OutputFormat='mp3', VoiceId='Justin')
			respondmodule(response)
			searching = False


	    if talk=='test':
		response = polly.synthesize_speech(TextType='ssml', Text='<speak><emphasis level="strong">Okay then</emphasis> \
		Farewell for now.</speak>', OutputFormat='mp3', VoiceId='Justin')
		respondmodule(response)

	    if talk in {'exit', 'shut down', 'go away', 'stop listening', 'terminate'}:
		response = polly.synthesize_speech(Text="Okay. Farewell for now.", OutputFormat='mp3', VoiceId='Justin')
		respondmodule(response)
		#sys.exit()
	 
	    if talk in (conversations.time_to):
		mira_time()

	    if talk in {'what is my name', 'my name', "what's my name", "who am i"}:
		response = polly.synthesize_speech(Text="You said your name was," +name, OutputFormat='mp3', VoiceId='Justin')
		respondmodule(response)


	    if talk in (conversations.listen_list):
		response = polly.synthesize_speech(TextType='ssml', Text='<speak><prosody rate="slow">I am awake.</prosody><break time="30ms"/> \
		<amazon:effect vocal-tract-length="-5%">what can I do for you.</amazon:effect></speak>', OutputFormat='mp3', VoiceId='Justin')
		respondmodule(response)



	    # we need some special handling here to correctly print unicode characters to standard output
	    if str is bytes:  # this version of Python uses bytes for strings (Python 2)
	  	  print("You said {}".format(talk).encode("utf-8"))

       	    else:  # this version of Python uses unicode for strings (Python 3+)
	          print("You said {}".format(talk))

	except sr.UnknownValueError:
	    response = polly.synthesize_speech(Text='Sorry, I didnt quite understand...', OutputFormat='mp3', VoiceId='Justin')
	    respondmodule(response)

	except sr.RequestError as e:
	    print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))

except KeyboardInterrupt:
	pass
