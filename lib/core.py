#!/usr/bin/env python3

import os 

from datetime import  *
from lib.query_resolved import *

import json 

class LessonClass:
    lessonName: str
    day: str
    dayTime: str
    docente: str
    current : str
    place: str
    room: str
    
    def __init__(self, lessonName: str, day: str, dayTime: str, docente: str, place: str, room: str) -> None:
        self.lessonName = lessonName
        self.day = day
        self.dayTime = dayTime
        self.docente = docente
        self.place = place
        self.room = room

    def to_stringWeek(self) -> str:
        response = "\nOrario: " + self.dayTime + "\n"
        response += "Materia: " + self.lessonName
        response += "\n"
        return response


    def to_string(self) -> str:
        response = ""
        response += "\nOrario: " + self.dayTime 
        ##response += "\nMateria: " + self.lessonName 
        #response += "\nData: " + str(self.day).split(' ')[0] 
        ##response += "\nDocente: " + self.docente 
        ##response += "\nLuogo: " + self.place 
        response += "\n*Materia: " + self.lessonName + "*"
        #response += "\nData: " + str(self.day).split(' ')[-1]
        response += "\nDocente: " + self.docente
        if(self.place):
              response += "\nLuogo: " + self.place 
        response += "\nAula: [" + self.room + "]\n"
        return response

def getJson(chat_id, start, end):
    # date format: YYYY-mm-DD
    #cmd += "curl \"" + department + "@@orario_reale_json?&anno=" + str(anno)
    cmd = "curl \"" + getUrl(chat_id)
    #print(cmd)
    cmd += "&start=" + start + "&end=" + end + "\""
    print(cmd)
    #return json.load(os.popen(cmd))
    while True:
        try:
            enc = json.load(os.popen(cmd))
            #print(enc)
            return enc
        except json.decoder.JSONDecodeError:
            print("errorLMAO")
            f = open("error.txt", "a")
            f.write("ErrorLMAO")
            f.close
            return " "


def buildDict(json_enc):
    ll = []
    place = ""
    if(json_enc == " "):
        print("json_enc is empty")
        return ll

    for i in range(len(json_enc)):
#        if(type(json_enc[i]['start']) is str  and type(json_enc[i]['time']) is str and type(json_enc[i]['aule'][0]['des_edificio']) is str and type(json_enc[i]['aule'][0]['des_indirizzo']) is str and type(json_enc[i]['title']) is str and type(json_enc[i]['docente']) is str):
            date = datetime.strptime(json_enc[i]['start'].split('T')[0], '%Y-%m-%d')#TODO
            clock = json_enc[i]['time']
            lessonRoom = ""
            if(json_enc[i]['teledidattica']):
                lessonRoom = "online"
            else:
                 if(json_enc[i]['aule']):
                     if(json_enc[i]['aule'][0]['des_edificio']):
                          lessonRoom = json_enc[i]['aule'][0]['des_edificio']
                     if(json_enc[i]['aule'][0]['des_indirizzo']):
                          place = json_enc[i]['aule'][0]['des_indirizzo'] #AGGIUNTA 
            if(json_enc[i]['docente']):
                     ll.append(LessonClass(json_enc[i]['title'], date, clock, 
                     json_enc[i]['docente'], place ,lessonRoom))
    return ll

def buildDictWeek(json_enc):
    ll = []
    place = ""
    
    for i in range(len(json_enc)):
#        if(type(json_enc[i]['start']) is str  and type(json_enc[i]['time']) is str and type(json_enc[i]['aule'][0]['des_edificio']) is str and type(json_enc[i]['aule'][0]['des_indirizzo']) is str and type(json_enc[i]['title']) is str and type(json_enc[i]['docente']) is str):
            date = datetime.strptime(json_enc[i]['start'].split('T')[0], '%Y-%m-%d')#TODO
            clock = json_enc[i]['time']
            lessonRoom = ""
            if(json_enc[i]['teledidattica']):
                lessonRoom = "online"
            else:
                if(json_enc[i]['aule']):
                     if(json_enc[i]['aule'][0]['des_edificio']):
                          lessonRoom = json_enc[i]['aule'][0]['des_edificio']
                     if(json_enc[i]['aule'][0]['des_indirizzo']):
                          place = json_enc[i]['aule'][0]['des_indirizzo'] #AGGIUNTA 
            if(json_enc[i]['docente']):
                     ll.append(LessonClass(json_enc[i]['title'], date, clock, " ", " ", lessonRoom))
    return ll
