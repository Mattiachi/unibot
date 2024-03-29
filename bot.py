'''
Author: Mattia&Matteo<3
Program: bot.py
Date: Apr. 16 2021
Version: 3.0, python3
'''

test = 0 #If zero does not run as test script

import telepot,re, schedule
from datetime import datetime,timedelta

import time as ttt, json
import textwrap
import locale

#Our libraries
from  lib.query_resolved import *
from  lib.messageHandler  import myHandle
from lib.core import *

#Telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from lib.inlineKey import makeKeyboard


bot = telepot.Bot(getToken(test))
# Sends message to the admins when (re)started
response = getAdmins()

debug = True
msg = str(__file__) + " just restarted"

# set locale to translate from english to another lenguage days
it = locale.setlocale(locale.LC_TIME, 'it_IT.UTF-8')

if(debug):
        msg = "I'm working on " + str(__file__)

for i in range(len(response)):
        bot.sendMessage(response[i][0], msg)

print("Imma listening")


def sendMessage(chat_id, message):
    # if utente nella lista
    bot.sendMessage(chat_id, message)

def giornata(chat_id, message):
                """ function to create daily time table 

                Args:
                    chat_id ([int]): [user id to send message]
                    message ([str]): [payload]

                Returns:
                    [str, str]: [keyboard to navigate, payload]
                """
                print("Executing GIORNATA " + datetime.now().strftime("%H:%M:%S"))
                now = datetime.now()
                today = now.strftime("%Y-%m-%d")
                tomorrow = now + timedelta(1,0)
                nextDay = tomorrow.strftime("%Y-%m-%d")
                a = nextDay
                if(message == "/oggi"):
                        a = today
                        text = "Ecco le lezioni di \n*" + now.strftime("%A").capitalize() + " "
                        text += str(a) + "*\n"
                else:
                        text = "Ecco le lezioni di \n*" + tomorrow.strftime("%A").capitalize() + " "
                        text += str(a) + "*\n"

                        
                ob = getJson(str(chat_id), a, a) 
                if(ob == " "):
                    bot.sendMessage(chat_id, "Qualcosa è andato storto con il tuo orario :^(\n Riprova più tardi") 
                ob = buildDict(ob)
                l = len(text)
                for x in range(len(ob)):
                        text += str(ob[x].to_string())

                if(len(text) == l):
                        text += "\n*Nessuna lezione*"

                tastiera = ["Oggi","/oggi","Domani","/domani","Settimana", "/settimana", "Menù", "/menu"]
                return text,tastiera


def getWeek(chat_id):
    """[gets the week timetable]
     
    Args:
        chat_id ([int]): [user id to send message]
    """
    tastiera = ["Oggi","/oggi","Domani","/domani","Settimana", "/settimana", "Menù", "/menu"]
    today = datetime.now()
    week = "Ecco le lezioni per la settimana corrente\n"
    for i in range(7):
        ob = getJson(str(chat_id), today.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d"))
        ob = buildDictWeek(ob)
        week += "\n*" + today.strftime("%A %D") + "*\n"
        for x in range(len(ob)):
            if(len(str(ob[x].to_stringWeek())) != 0):
                week += str(ob[x].to_stringWeek())
            else: 
                week += "\n*Nessuna lezione*"
        today = today + timedelta(1, 0)
    return week, tastiera

def getDay(department, anno, start, end):
    """[creates the http request]
     
    Args:
        department ([str]): [uinversita url]
        anno ([str]): [anno]
        start ([str]): [date to start reading]
        end ([str]): [date to stop reading]
     
    Returns:
        [dict]: [dictionary containg the information]
    """
    cmd = ""
    cmd += "curl \"" + department + "/@@orario_reale_json?&anno=" + str(anno)
    cmd += "&start=" + start + "&end=" + end + "\""
    print(cmd)
    data = json.load(os.popen(cmd))
    f = open("output.txt", "a")
    now = datetime.now()
    f.write(now.strftime("%Y-%m-%d %H:%M"))
    f.write("\n" + str(cmd) + "\n")
    f.write(str(data))
    f.write("\n")
    f.close()
    di = buildDict(data)
    return di


def mySendMessage(cchat_id, when):
        print("Executing mySendMessage for " + str(cchat_id) + " " + str(when) + " " + datetime.now().strftime("%H:%M:%S"))
        text, tastiera = giornata(cchat_id, when)
        bot.sendMessage(cchat_id, text, reply_markup = makeKeyboard(tastiera), parse_mode = 'Markdown')


def startSchedules():
        """[schedule utility]
        """
        if(test):
                print("This is a test, i won't execute this function")
                return

        variable = getSchedules()
        output = ""
        for chat_id, oggi, domani in variable:
                if(oggi): #Not null
                        if(len(oggi) == 5):
                                oggi = "0" + str(oggi)
                        else:
                                oggi = str(oggi)[0:5]
                        schedule.every().day.at(str(oggi)[0:5]).do(mySendMessage, cchat_id = chat_id, when = "/oggi").tag(str(chat_id)+"/oggi")
                        output += ("Scheduled oggi for chat_id = " + str(chat_id) + " every day at " + str(oggi)+"\n")
                if(domani):
                        if(len(domani) == 5):
                                domani = "0" + str(domani)
                        else:
                                domani = str(domani)[0:5]

                        domani = str(domani)[0:5]
                        schedule.every().day.at(domani).do(mySendMessage, cchat_id=chat_id, when = "/domani").tag(str(chat_id)+"/domani")
                        output +=("Scheduled domani" + " for chat_id = " + str(chat_id) + " every day at " + domani + "\n")
        print(output)

def addSchedule(chat_id, wwhen, hour):
        """[adds the schedule]

        Args:
            chat_id ([int]): [user id to send message]
            wwhen ([date]): [date]
            hour ([time]): [time]
        """
        if(test):
                print("This is a test, i won't execute this function")
                return
        if(len(hour) == 4):
                hour = "0" + str(hour)
        else:
                hour = str(hour)[0:5]
        print(hour)
        schedule.every().day.at(hour).do(mySendMessage, cchat_id=chat_id, when = wwhen).tag(str(chat_id)+wwhen)
        print("Scheduled "+ wwhen + " for chat_id = " + str(chat_id) + " every day at " + str(hour)+"\n")


def deleteSchedule(chat_id, when):
        """[delets schedule]

        Args:
            chat_id ([int]): [user id to send message]
            when ([date]): [date]
        """
        if(test):
                print("This is a test, i won't execute this function")
                return

        schedule.clear(str(chat_id)+when)
        print("Schedule " +when+ " clear for chat_id = " + str(chat_id))

def handle(chat_id,message):
        """[handle alle the scenarios to send timetables]

        Args:
            chat_id ([int]): [user id to send message]
            message ([str]): [payload]
        """
        print(chat_id, message,message_count)

        nuovoUtente(chat_id)
        state = getState(chat_id)
        updateLast_seen(chat_id)

        #take the cursor
        mycursor=mydb.cursor()
        if(message == "kicked"): # User blocks the bot
                print("Setting to -1 stato di  " + str(chat_id))
                sql = "update utente set stato = -1, curricula_id = NULL, anno = 1, oggi = NULL, domani = NULL where  chat_id =" + str(chat_id)
                mycursor.execute(sql)
                mydb.commit()
                state = -1
                deleteSchedule(chat_id, "/oggi")
                deleteSchedule(chat_id, "/domani")


        if(message == "member"): # Average chad bot user
                print("Setting to 0 stato di " + str(chat_id))
                sql = "update utente set stato = 0, curricula_id = NULL, anno = 1 where  chat_id =" + str(chat_id)
                mycursor.execute(sql)
                mydb.commit()
                state = 0

        if(message == "/start"): # New user turns on the bot
                sql = "update utente set stato = 0, anno = 1, oggi = NULL, curricula_ID = NULL, domani = NULL where  chat_id =" + str(chat_id)
                mycursor.execute(sql)
                mydb.commit()
                bot.sendMessage(chat_id, "Procediamo alla registrazione: che corso frequenti? \n(Basta una parola chiave contenuta nel nome del tuo corso di laurea, come ingegneria, med, ling)")
                state = 0
                updateNickname(chat_id, nickname)
                deleteSchedule(chat_id, "/oggi")
                deleteSchedule(chat_id, "/domani")

        if(state == 0): # Unkow user
                testo = "Ciao, sono unibot! Una volta impostato il tuo corso di laurea e anno, sarò in grado di mandarti l'orario odierno o del giorno seguente su richiesta. \n"
                print("Stato utente 0, procedo alla registrazione")
                testo += "Procediamo alla registrazione: che corso frequenti? \n(Basta una parola chiave contenuta nel nome del tuo corso di laurea, come ingegneria, med, ling, elettronica)"
                # state = 1
                upgradeStato(chat_id)
                bot.sendMessage(chat_id,testo)
                updateNickname(chat_id, nickname)
                return

        if(state == 1): # Select uni department
                results = likeString(message)
                text = "Quale tra questi è il tuo corso?\n"
                corsi = []
                for rows in results:
                        for x in rows:
                                corsi.append(x)
                print(corsi)
                if(len(results) == 0):
                        bot.sendMessage(chat_id, "Nessun corso riscontrato")
                        return
                bot.sendMessage(chat_id, text, reply_markup=makeKeyboard(corsi))
                upgradeStato(chat_id)
                return

        if(state == 2): # Insert uni department 
                sql = "select ID from universita"
                if(message.isnumeric() and [item for item in exFetch(sql) if item[0] == int(message)]):
                        upgradeStato(chat_id)
                        key = makeKeyboard(getCurricula(message))
                        text = "Quale tra questi è il tuo curricula?"
                        bot.sendMessage(chat_id, text,  reply_markup = key)
                        return

                else:
                        bot.sendMessage(chat_id,"Non è stato possibile trovare il tuo corsi di laurea. \nProcediamo alla registrazione: che corso frequenti?")
                        downgradeStato(chat_id)
                        return

        if(state == 3): #Found curricula
                if(message.isnumeric()):
                        #Se arrivo fino a qui, ho trovato il curricula ID
                        sql = "update utente set curricula_id = " + message + " where chat_id = " + str(chat_id)
                        exCommit(sql)
                        upgradeStato(chat_id) #Setto lo stato a 4
                        print("curricula_id aggiornato per utente " + str(chat_id))
                        text = "Un'ultima cosa... Che anno frequenti?"
                        key = getYear(chat_id, message)
                        bot.sendMessage(chat_id, text, reply_markup = makeKeyboard(key))
                        return
                else:
                        if(message == "-1"): #L'utente non ha trovato il proprio curricula, lo rimando allo stato 1!
                                bot.sendMessage(chat_id, "Procediamo alla registrazione: che corso frequenti?")
                                downgradeStato(chat_id)
                                downgradeStato(chat_id) #Da stato 3 arriva a stato 1
                                return
                        bot.sendMessage(chat_id, "Il curricula inserito non è valido")
                        return


        if(state == 4): #Insert year
                sql = 'select durata from universita where ID = (select id_universita from percorso where ID = (select curricula_id from utente where chat_id = "' + str(chat_id) + '"))'
                max = int(exFetch(sql)[0][0])
                if(message.isdigit() and 1 <= int(message) <= max):
                        sql = 'update utente set anno = "' + message + '\" where chat_id = ' + str(chat_id)
                        exCommit(sql)
                        print("Anno aggiornato per utente: " + str(chat_id))
                        tastiera = ["Oggi","/oggi","Domani","/domani","Menù", "/menu"]
                        bot.sendMessage(chat_id, "Registrazione completata! \nPuoi inoltre attivare tramite il menù la modalità ricorda, che ad un orario a tuo piacimento, ti invierà automaticamente gli orari delle lezioni odierne o del giorno seguente.", reply_markup=makeKeyboard(tastiera))
                        upgradeStato(chat_id)
                        return
                else:
                        bot.sendMessage(chat_id, "Anno di corso non valido")
                        return


        if(state == 6 or state == 7): # Set schedule

                try:
                        print(datetime.strptime(message, '%H:%M').time())
                except ValueError:
                        bot.sendMessage(chat_id, "Il formato che hai inviato non è corretto")
                        return

                if(state == 6):
                        sql = 'update utente set oggi ="' + str(message) + ' " where chat_id = ' + str(chat_id)
                        deleteSchedule(chat_id, "/oggi")
                        addSchedule(chat_id, "/oggi", message)
                else:
                        deleteSchedule(chat_id, "/domani")
                        addSchedule(chat_id, "/domani", message)
                        sql = 'update utente set domani ="' + str(message) + ' " where chat_id = ' + str(chat_id)

                mycursor.execute(sql)
                mydb.commit()
                print("Stato " + str(chat_id) + " = 5")
                sql = 'update utente set stato = 5 where chat_id = ' + str(chat_id)
                mycursor.execute(sql)
                mydb.commit()

                dday = "domani"
                if(state == 6):
                        dday = "oggi"
                testo = "Ogni giorno riceverai relativo alla giornata di *" +dday + "* alle ore *" +str(message) + "*"
                tastiera = ["Oggi","/oggi","Domani","/domani","Settimana", "/settimana", "Menù", "/menu"]
                bot.sendMessage(chat_id, testo, reply_markup = makeKeyboard(tastiera), parse_mode='Markdown')

        if(state == 8):
                tastiera = ["Oggi","/oggi","Domani","/domani", "Settimana", "/settimana", "Menù", "/menu"]
                if(message == "oggi"):
                        exCommit('update utente set stato=5, ' + message + ' = NULL where chat_id = ' + str(chat_id))
                        bot.sendMessage(chat_id, "Non riceverai più l'orario relativo alla giornata di " + message,reply_markup = makeKeyboard(tastiera))
                        deleteSchedule(chat_id, "/oggi")
                elif(message == "domani"):
                        exCommit('update utente set stato=5, ' + message + ' = NULL where chat_id = ' + str(chat_id))
                        bot.sendMessage(chat_id, "Non riceverai più l'orario relativo alla giornata di " + message, reply_markup = makeKeyboard(tastiera))
                        deleteSchedule(chat_id, "/domani")
                elif(message =="entrambi"):
                        exCommit('update utente set stato=5, oggi = NULL , domani = NULL where chat_id = ' + str(chat_id))
                        bot.sendMessage(chat_id, "Non riceverai più l'orario relativo alle giornate di oggi e domani", reply_markup = makeKeyboard(tastiera))
                        deleteSchedule(chat_id, "/oggi")
                        deleteSchedule(chat_id, "/domani")

        if(message == "/oggi" or message == "/domani"):
                """
                res = getUrl(chat_id)
                bot.sendMessage(chat_id, res)
                """
                text, tastiera = giornata(chat_id, message)
                bot.sendMessage(chat_id, text, reply_markup=makeKeyboard(tastiera), parse_mode='Markdown')
        if(message == "/goback"):
                tastiera = ["Oggi","/oggi","Domani","/domani","Menù", "/menu"]
                bot.sendMessage(chat_id, "Menù principale", reply_markup=makeKeyboard(tastiera), parse_mode='Markdown')

        if(message == "/settimana"):
            text,tastiera = getWeek(chat_id)
            print(len(text))
            if(len(text) > 4096):
                for i in range(0,int(len(text) / 4096) + (len(text) % 4096 > 0)):
                   bot.sendMessage(chat_id, text[i*4096:(i+1)*4096], parse_mode = 'Markdown')
                bot.sendMessage(chat_id, "Questa era la tua settimana:", reply_markup=makeKeyboard(tastiera), parse_mode='Markdown')
                return
            bot.sendMessage(chat_id, text, reply_markup=makeKeyboard(tastiera), parse_mode='Markdown')

        if(message == '/stats' and adminInfo(chat_id)):
                tastiera = ["Oggi","/oggi","Domani","/domani","Settimana", "/settimana", "Menù", "/menu"]
                text = ""
                text += os.popen("sudo supervisorctl status | awk '{print}'").read() + "\n\n"
                text += getStats()
                text += "\n\n"
                text += "ssh pi@"
                text += os.popen("curl ifconfig.me").read()
                text += "\n"
                bot.sendMessage(chat_id, text, reply_markup=makeKeyboard(tastiera) , parse_mode='Markdown')

        if(message == '/menu'): # Send menu
                tastiera = ["Reimposta corso/anno","/start" ]
                feature_in_beta = ["Ricordami oggi", "/ricordamioggi", "Ricordami domani","/ricordamidomani", "Non ricordarmi più", "/nonricordarmi", "Torna indietro", "/goback"]
                tastiera += feature_in_beta

                if(adminInfo(chat_id)):
                        tastiera += ["Jobs", "/jobs","Stats", "/stats"]

                text = "Menù:"
                bot.sendMessage(chat_id, text ,reply_markup = makeKeyboard(tastiera))

        if(message == '/ricordamioggi'): # Add daily schedule
                sql = 'update utente set stato=6 where chat_id = ' + str(chat_id)
                mycursor.execute(sql)
                mydb.commit()
                text = "A che orario vuoi ricevere l'orario relativo alla giornata di oggi?\nScrivilo nel formato hh:mm , per esempio 8:30 oppure 15:30"
                bot.sendMessage(chat_id, text)

        if(message == '/ricordamidomani'): # Add daily schedule
                sql = 'update utente set stato=7 where chat_id = ' + str(chat_id)
                mycursor.execute(sql)
                mydb.commit()
                text = "A che orario vuoi ricevere l'orario relativo alla giornata di domani?\nScrivilo nel formato hh:mm , per esempio 8:30 oppure 15:30"
                bot.sendMessage(chat_id, text)

        if(message == '/nonricordarmi'):
                text = "Vuoi annullare la funzionalità di ricordarmi relativa all'orario di oggi, domani o entrambe?"
                tastiera = ["Oggi", "oggi", "Domani", "domani", "Entrambi", "entrambi"]
                exCommit('update utente set stato=8 where chat_id = ' + str(chat_id))
                bot.sendMessage(chat_id, text, reply_markup = makeKeyboard(tastiera))

        if(message == '/jobs' and adminInfo(chat_id)):
                var = "ssh pi@"
                var += os.popen("curl ifconfig.me").read()
                var += "\n\n"
                var += str(schedule.get_jobs())
                if(len(var)>4000):
                    var = var[:3999]
                print(var)
                tastiera = ["Oggi","/oggi","Domani","/domani","Menù", "/menu"]
                bot.sendMessage(chat_id, var,reply_markup = makeKeyboard(tastiera))

        if(message == "/ornitorinco"): #Fa crashare il bot
                a = 2
                b = "cc"
                print(a+b)

        if(message == "/admin"):
                print("hai chiesto gli admin")
                print(getAdmins())

        mycursor.close()

startSchedules()

#Per non fare crashare il db..
schedule.every().minute.at(":45").do(getAdmins).tag("Anticrash")

while True:
        schedule.run_pending()
        ttt.sleep(0.35)
        if(bot.getUpdates()):
                chat_id, text, message_count, nickname = myHandle(test) #Test vale 1
                print(nickname)
                if(message_count != -1 ):
                        handle(chat_id, text)