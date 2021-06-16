# Works with any video calling software as we are using the audio source.
# Let me know how it goes @ashutoshshukla__


import speech_recognition as sr
import sys
import requests
import pprint

pp = pprint.PrettyPrinter()

# Enter your discord webhook URL of the bot.
WEBURL = '<<---Enter Here-->>'

# Initialize the speech recognition module.
r = sr.Recognizer()

# Lists All the input and output audio devices.
pp.pprint(sr.Microphone.list_microphone_names())

# Selecting the Realtek Stereo Mix input.
# The Index number may vary, check the list from above and find the device index which starts from 0.
mic = sr.Microphone(device_index=2)

# Array of all the words we will match from the heard text, for example "present","attendance","student names",etc.
matches = ["attendance", "present", "present sir",
           "present ma'am", "Enter all your friends names XD"]

# These send a message to Discord that the bot is online and listening.
requests.post(WEBURL, data={"content": 'Im online and listening!'})
requests.post(
    WEBURL, data={"content": f'Listening for following - {matches}'})

# Infinite loop, can be broken by entering Ctrl+C in terminal.
while True:
    with mic as source:
        try:
            # Listening from the selected mics input.
            r.adjust_for_ambient_noise(source, duration=0.2)
            print('Listening...')

            # Setting the phrase limit to 6 and converting speech to text in lowercase because its easier to compare.
            audio = r.listen(source, phrase_time_limit=6)
            text = r.recognize_google(audio).lower()

            # Prints the matched line and sends the message to discord.
            print(f'Heard Text: {text}')
            if any(x in text for x in matches):
                print(f'Matched Text: {text}')
                requests.post(
                    WEBURL, data={"content": f'Shits going down!\nI heard: {text}'})

        # If no one is talking or input audio is not clear this message will be persistent until something is heard.
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")

        # Any other unkown error will be speciefed by this.
        except sr.RequestError as e:
            print(
                "Could not request results from Google Speech Recognition service; {0}".format(e))

        # To exit the program.
        except (KeyboardInterrupt, SystemExit):
            requests.post(WEBURL, data={"content": 'Offline now!'})
            sys.exit('User Ctrl+C quit')
