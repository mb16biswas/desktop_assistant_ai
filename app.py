import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
import numpy as np
import json
import sys
import webbrowser
import requests
from googlesearch import search
import random
import smtplib
import ssl
import os
from twilio.rest import Client

with open("Data.json") as file:
    data = json.load(file)
df = data
pattern = []
store = df["intents"]
for i in range(len(store)):
    PAT = store[i]["patterns"]
    for j in range(len(PAT)):
        pattern.append(PAT[j].lower())
tokenizer = Tokenizer(
    oov_token='OOV', filters='!"#$%&()*+,-./:;<=>@[\]^_`{|}~ ')
corpus = pattern
tokenizer.fit_on_texts(corpus)
total_words = len(tokenizer.word_index) + 1


def google():

    text = input("enter your quary....")
    if(len(text) == 0):
        return 0
    else:
        try:
            print("showing results ..")
            # open 5 tabs
            for i in search(text, tld="com", num=5, stop=5,  pause=2):
                webbrowser.open(i)
                print(i)
        except Exception as e:
            print(e)


def youtube():
    text = input("enter your quary....")
    if(len(text) == 0):
        return 0
    else:
        text1 = "".join(text.split())
        link = "https://www.youtube.com/results?search_query=" + text1
        try:
            webbrowser.open(link)
        except Exception as e:
            print(e)


def random_reply():
    reply = ["what??????????", "hahahahahah ???", "i am good ,but i dont understand",
             "okay nice but type something right", "hahahahahaha , what are you trying to say??",
             "pardon", "can you repeat master?",
             "hail hydra , can u repeat?", "counld not find any results regradung this", "sorry", "i am good", "thats nice", "hmmmmmmmmmmmm"]
    num = random.randint(0, len(reply))
    print(reply[num])


def message():

    # Your Account Sid and Auth Token from twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    TWILIO_ACCOUNT_SID = ""
    TWILIO_AUTH_TOKEN = ""
    # Trial accounts cannot send messages to unverified numbers
    my_number = ""
    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN
    text = input("enter your message..  ")
    if(len(text) == 0):
        return 0
    rec_number = input("enter the sender number .. ")
    rec_number = "+" + rec_number
    if(len(rec_number) == 0):
        return 0
    client = Client(account_sid, auth_token)

    try:
        message = client.messages \
            .create(
                body=text,
                from_=my_number,
                to=rec_number
            )

        print(message.sid)

    except Exception as e:
        print(e)


def email():
    text = input(
        "type 'd' to go the website or 's' to send a normal text email ")
    if(text == "d"):
        webbrowser.open("https://mail.google.com/")
    elif(text == "s"):

        port = 465   # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = input(" Enter your address  ")  # Enter your address
        # email id shold have less secure app access
        if(len(sender_email) == 0):
            return 0
        receiver_email = input(" Enter receiver address  ")
        if(len(receiver_email) == 0):
            return 0
        password = input("Type your password and press enter: ")
        if(len(password) == 0):
            return 0
        message = input("enter you message  ")

        context = ssl.create_default_context()
        try:

            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message)
        except Exception as e:
            print(e)
    else:
        return 0


def process(x):
    token_list = tokenizer.texts_to_sequences([x])
    input_sequences = np.array(pad_sequences(
        token_list, maxlen=7, padding='pre'))
    input_sequences = np.array([input_sequences[0]])
    return input_sequences


predict = {0: "google", 1: "youtube", 2: "email", 3: "random", 4: "text"}
new_model = tf.keras.models.load_model('friday_1.0.h5')

bot = True
while bot:
    text = input("hello...   ")
    if(len(text) == 0):
        break
    text = process(text)
    pred = new_model.predict(text)
    pred = np.argmax(pred)
    print(predict[pred])
    if(pred == 0):
        google()
    elif(pred == 1):
        youtube()
    elif(pred == 2):
        email()
    elif(pred == 3):
        random_reply()
    else:
        message()
