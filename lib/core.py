#!/usr/bin/env python3

import os 

from datetime import  *
from lib.query import *

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

    def to_string(self) -> str:
        response = ""
        response += "\nOrario: " + self.dayTime 
        ##response += "\nMateria: " + self.lessonName 
        #response += "\nData: " + str(self.day).split(' ')[0] 
        ##response += "\nDocente: " + self.docente 
        ##response += "\nLuogo: " + self.place 
        response += "\n*Materia: " + self.lessonName + "*"
        #response += "\nData: " + str(self.day).split(' ')[0]
        response += "\nDocente: " + self.docente
        if(self.place):
              response += "\nLuogo: " + self.place 
        response += "\nAula: [" + self.room + "]\n"
        return response

def getJson(chat_id, start, end):
    # date format: YYYY-mm-DD
    #cmd += "curl \"" + department + "@@orario_reale_json?&anno=" + str(anno)
    cmd = "curl \"" + getUrl(chat_id)
    print(cmd)
    cmd += "&start=" + start + "&end=" + end + "\""
    #return json.load(os.popen(cmd))
    while True:
        try:
            enc = json.load(os.popen(cmd))
            return enc
        except JSONDecodeError:
            print("error")
            f = open("error.txt", "a")
            f.write("Error")
            f.close

def buildDict(json_enc):
    ll = []
    place = ""
    for i in range(len(json_enc)):
        date = datetime.strptime(json_enc[i]['start'].split('T')[0], '%Y-%m-%d')#TODO
        clock = json_enc[i]['time']
        
        if(json_enc[i]['teledidattica']):
            lessonRoom = "online"
        else:
            lessonRoom = json_enc[i]['aule'][0]['des_edificio']
            place = json_enc[i]['aule'][0]['des_indirizzo'] #AGGIUNTA 

        ll.append(LessonClass(json_enc[i]['title'], date, clock, 
        json_enc[i]['docente'], place ,lessonRoom))
    return ll
