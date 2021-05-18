#!/usr/bin/env python3
import telepot, time

from  lib.query import getToken


bot = telepot.Bot(getToken())

def myHandle(test = 0):
    bot = telepot.Bot(getToken(test))
    a = (bot.getUpdates()[-1])
    if( "my_chat_member" in a):
        chat_id = a['my_chat_member']['chat']['id'] #Class int
        status = a['my_chat_member']['new_chat_member']['status']
        nick = a['my_chat_member']['chat']['first_name']
        print(str(chat_id) + " updated Bot status to: " + status)
        bot.getUpdates(offset =bot.getUpdates()[-1]['update_id']+1)
        return [chat_id,status,0,nick]
    if ("message" in a and "text" in a["message"]):
        chat_id = a['message']['chat']['id'] #Class int
        text = a['message']['text']	#Class str
        message_count = a['message']['message_id']	#Class int
        nick = a['message']['chat']['first_name']
#        print(chat_id,text,message_count)
        bot.getUpdates(offset =bot.getUpdates()[-1]['update_id']+1)
        return [chat_id,text,message_count,nick]
    if("callback_query" in a):
        chat_id = a['callback_query']['from']['id']
        text = a['callback_query']['data']
        message_count = a['callback_query']['message']['message_id']
        bot.getUpdates(offset =bot.getUpdates()[-1]['update_id']+1)
        nick = a['callback_query']['from']['first_name']
        return [chat_id,text,message_count,nick]
    return [-1,-1,-1,-1]
