import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
from keras.models import load_model
model = load_model('chatbot_model_chuc.h5')
import json
import random
# print(open('intents.json').read()[440:446])
# intents = json.loads(open('intents.json').read())
intents= json.loads(open('intents.json',"rb").read().decode("utf-8", "ignore"))
words = pickle.load(open('words_chuc.pkl','rb'))
classes = pickle.load(open('classes_chuc.pkl','rb'))

def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words
# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result


def chatbot_response(text):
    ints = predict_class(text, model)
    res = getResponse(ints, intents)
    return res

import tkinter
# from tkinter import *
# def send():
#     msg = EntryBox.get("1.0",'end-1c').strip()
#     EntryBox.delete("0.0",END)
#     if msg != '':
#             ChatLog.config(state=NORMAL)
#             ChatLog.insert(END, "You: " + msg + '\n\n')
#             ChatLog.config(foreground="#442265", font=("Verdana", 12 ))
#             res = chatbot_response(msg)
#             ChatLog.insert(END, "Bot: " + res + '\n\n')
#             ChatLog.config(state=DISABLED)
#             ChatLog.yview(END)
#
# base = Tk()
# base.title("Hello")
# base.geometry("400x500")
# base.resizable(width=FALSE, height=FALSE)
# #Create Chat window
# ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial",)
# ChatLog.config(state=DISABLED)
# #Bind scrollbar to Chat window
# scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
# ChatLog['yscrollcommand'] = scrollbar.set
# #Create Button to send message
# SendButton = Button(base, font=("Verdana",12,'bold'), text="Send", width="12", height=5,
#                     bd=0, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',
#                     command= send )
# #Create the box to enter message
# EntryBox = Text(base, bd=0, bg="white",width="29", height="5", font="Arial")
# #EntryBox.bind("<Return>", send)
# #Place all components on the screen
# scrollbar.place(x=376,y=6, height=386)
# ChatLog.place(x=6,y=6, height=386, width=370)
# EntryBox.place(x=128, y=401, height=90, width=265)
# SendButton.place(x=6, y=401, height=90)
# base.mainloop()

########################################################################################

import os
import random
import sys

from discord.ext import commands
# from dotenv import load_dotenv

# load_dotenv('.env')
# TOKEN = os.getenv('DISCORD_TOKEN')
TOKEN= 'NzE4NjUwNzQyMDU5MTcxOTUx.XtsB2g.lP1B-f_xE1rEmtEWgczVZbPUNBo'
# GUILD = os.getenv("DISCORD_GUILD")
GUILD= None
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    for guild in bot.guilds:
        if guild.name==GUILD:
            break

    print(f'{bot.user} is connected to the following guild:\n'
          f'{guild.name}(id: {guild.id})\n'
          )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')
@bot.event
async def on_message(ctx):
    if ctx.author == bot.user:
        return

    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    if ctx.content[0] != '!':
        # response = random.choice(brooklyn_99_quotes)
        await ctx.channel.send(chatbot_response(ctx.content))
        # ctx.send(chuc_function())
    await bot.process_commands(ctx)

@bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)

@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

@bot.command(name="stop")
async def stop_bot(ctx):
    await ctx.send("chương trình đang dừng")
    sys.exit()

# def chuc_function():
#     text=["xin chào"," ê cu", "chào bạn", " cho phép trình bày", "chào cc"]
#     res= random.choice(text)
#     return res

bot.run(TOKEN)