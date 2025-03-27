import pyttsx3
import speech_recognition as sr
import eel
import time
from engine.camera import take_photo, take_photo1
from engine.datetime import get_current_time_and_date
from engine.translator import translate_text
from engine.api import get_joke, get_weather,get_news
import datetime


# engine = pyttsx3.init()
def speak(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 174)
    engine.say(text)
    engine.runAndWait()

@eel.expose
def takecommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print('listening....')
        eel.DisplayMessage('listening....')
        r.pause_threshold=3
        r.adjust_for_ambient_noise(source)

        audio=r.listen(source, 10, 6)
    try:
        print('recognizing.....')
        eel.DisplayMessage('recognizing.....')
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
        
       
    except Exception as e:
        return ""
    
    return query.lower()


@eel.expose
def allCommands(message=1):
    if message == 1:
        query = takecommand()
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)

    try:

        if "open" in query:
            from engine.features import openCommand
            openCommand(query)

        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)

        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp
            flag= ""
            contact_no, name = findContact(query)
            if(contact_no != 0):

                if "send message" in query:
                    flag= 'message'
                    speak("what message to send")
                    query = takecommand()
                    
                elif "phone call" in query:
                    flag = 'call'
                else:
                    flag= 'video call'
                    
                whatsApp(contact_no, query, flag, name)
            
        elif "translate" in query:
            query = query.replace("translate", "").strip()
            speak("Which language would you like to translate to?")
            dest_language = takecommand().strip()
            print(f"Destination language: {dest_language}")
            print(f"Query: {query}")
            source_language = 'auto'
            translated_text = translate_text(query, source_language, dest_language)
            print(f"Translated text: {translated_text}")
            speak(f"Translation to {dest_language}: {translated_text}")
        
        elif "weather" in query:
            city = query.split("in")[-1].strip()
            api_key = 'dc149ed8de1996cd28086c1e10c84130'
            weather_report = get_weather(city, api_key)
            speak(weather_report)

        elif "joke" in query:
            joke = get_joke()
            speak(joke)

        
        elif "click a photo" in query:
            speak("Which device would you like to use, desktop?")
            preference = takecommand().lower()

            if "mobile" in preference:
                take_photo1()  # Call the function for mobile
            elif "desktop" in preference:
                take_photo()  # Call the function for desktop
            else:
                speak("Sorry, I didn't understand. Please try again.")


        elif 'time' in query or 'date' in query:
            response = get_current_time_and_date()
            speak(response) 
        else:
            from engine.features import chatBot
            chatBot(query)
    except:
        print("error")

    eel.ShowHood()