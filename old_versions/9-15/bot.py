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

debug = False
msg = str(__file__) + " just restarted"
if(debug):
        msg = "I'm working on " + str(__file__)

for i in range(len(response)):
        bot.sendMessage(response[i][0], msg)

print("Imma listening")


def sendMessage(chat_id, message):
    # if utente nella lista
    bot.sendMessage(chat_id, message)

def giornata(chat_id, message):
                print("Executing GIORNATA " + datetime.now().strftime("%H:%M:%S"))
                now = datetime.now()
                today = now.strftime("%Y-%m-%d")
                tomorrow = now + timedelta(1,0)
                nextDay = tomorrow.strftime("%Y-%m-%d")
                """
                sql = 'select corso,anno from utente where chat_id = ' + str(chat_id)
                mycursor.execute(sql)
                response = mycursor.fetchall()
                """
                a = nextDay
                if(message == "/oggi"):
                        a = today
                ob = getJson(str(chat_id), a, a) #Gli ultimi due campi della funzione sono la data di inizio e di fine di quando si vuole ricevere la lezione
                ob = buildDict(ob)
                text = "Ecco le lezioni di " + message[1:] + "\n"
                text += "*" + str(a) + "*\n"

                l = len(text)
                for x in range(len(ob)):
                        text += str(ob[x].to_string())

                if(len(text) == l):
                        text += "\n*Nessuna lezione*"
                tastiera = ["Oggi","/oggi","Domani","/domani","Menù", "/menu"]

                return text,tastiera

def getDay(department, anno, start, end):
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
        if(test):
                print("This is a test, i won't execute this function")
                return

        schedule.clear(str(chat_id)+when)
        print("Schedule " +when+ " clear for chat_id = " + str(chat_id))

def handle(chat_id,message):
        print(chat_id, message,message_count)

        nuovoUtente(chat_id)
        state = getState(chat_id)
        updateLast_seen(chat_id)

        #prendo il cursor
        mycursor=mydb.cursor()
        #alla fine della funzione lo chiudo
        if(message == "kicked"):
                print("Setting to -1 stato di  " + str(chat_id))
                sql = "update utente set stato = -1, curricula_id = NULL, anno = 1, oggi = NULL, domani = NULL where  chat_id =" + str(chat_id)
                mycursor.execute(sql)
                mydb.commit()
                state = -1
                deleteSchedule(chat_id, "/oggi")
                deleteSchedule(chat_id, "/domani")


        if(message == "member"):
                print("Setting to 0 stato di " + str(chat_id))
                sql = "update utente set stato = 0, curricula_id = NULL, anno = 1 where  chat_id =" + str(chat_id)
                mycursor.execute(sql)
                mydb.commit()
                state = 0

        if(message == "/start"):
                sql = "update utente set stato = 0, anno = 1, oggi = NULL, curricula_ID = NULL, domani = NULL where  chat_id =" + str(chat_id)
                mycursor.execute(sql)
                mydb.commit()
                bot.sendMessage(chat_id, "Procediamo alla registrazione: che corso frequenti? \n(Basta una parola chiave contenuta nel nome del tuo corso di laurea, come ingegneria, med, ling)")
                state = 0
                updateNickname(chat_id, nickname)
                deleteSchedule(chat_id, "/oggi")
                deleteSchedule(chat_id, "/domani")
                #response = getAdmins()
                #msg = nickname + " joined the gang"
                #for i in range(len(response)):
                #       bot.sendMessage(response[i][0], msg)

        if(state == 0): #Utente sconociuto
                testo = "Ciao, sono unibot! Una volta impostato il tuo corso di laurea e anno, sarò in grado di mandarti l'orario odierno o del giorno seguente su richiesta. \n"
                print("Stato utente 0, procedo alla registrazione")
                testo += "Procediamo alla registrazione: che corso frequenti? \n(Basta una parola chiave contenuta nel nome del tuo corso di laurea, come ingegneria, med, ling, elettronica)"
                #Passo allo stato = 1
                upgradeStato(chat_id)
                bot.sendMessage(chat_id,testo)
                updateNickname(chat_id, nickname)
                return

        if(state == 1): #Chiedendo il corso di laurea
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

        if(state == 2): #Inserendo il corso di laurea
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

        if(state == 3):
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


        if(state == 4): #Inserendo anno di frequentazione
                if(message.isdigit()):
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


        if(state == 6 or state == 7):

                try:
                        print(datetime.strptime(message, '%H:%M').time())
                except ValueError:
                        bot.sendMessage(chat_id, "Il formato che hai inviato non è corretto")
                        return

                if(state == 6):
                        sql = 'update utente set oggi ="' + str(message) + ' " where chat_id = ' + str(chat_id)
                        #def addSchedule(chat_id, when, hour):
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
                tastiera = ["Oggi","/oggi","Domani","/domani","Menù", "/menu"]
                bot.sendMessage(chat_id, testo, reply_markup = makeKeyboard(tastiera), parse_mode='Markdown')

        if(state == 8):
                tastiera = ["Oggi","/oggi","Domani","/domani","Menù", "/menu"]
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


        if(message == '/stats' and adminInfo(chat_id)):
                #[utenti_attivi,messaggi] = getStats()
                #text = "*Utenti attivi*: " + str(utenti_attivi) + "\n*Messaggi ricevuti*: " + str(messaggi)
                tastiera = ["Oggi","/oggi","Domani","/domani","Menù", "/menu"]
                text = ""
                text += os.popen("sudo supervisorctl status | awk '{print}'").read() + "\n\n"
                text += getStats()
                #print(text)
                bot.sendMessage(chat_id, text, reply_markup=makeKeyboard(tastiera)) #, parse_mode='Markdown')

        if(message == '/menu'):
                tastiera = ["Reimposta corso/anno","/start" ]
                feature_in_beta = ["Ricordami oggi", "/ricordamioggi", "Ricordami domani","/ricordamidomani", "Non ricordarmi più", "/nonricordarmi", "Torna indietro", "/goback"]
                tastiera += feature_in_beta

                if(adminInfo(chat_id)):
                #       tastiera += feature_in_beta
                        tastiera += ["Jobs", "/jobs","Stats", "/stats"]

                text = "Menù:"
                bot.sendMessage(chat_id, text ,reply_markup = makeKeyboard(tastiera))

        if(message == '/ricordamioggi'): #and adminInfo(chat_id)):
                sql = 'update utente set stato=6 where chat_id = ' + str(chat_id)
                mycursor.execute(sql)
                mydb.commit()
                text = "A che orario vuoi ricevere l'orario relativo alla giornata di oggi?\nScrivilo nel formato hh:mm , per esempio 8:30 oppure 15:30"
                bot.sendMessage(chat_id, text)

        if(message == '/ricordamidomani'): # and adminInfo(chat_id)):
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
                var = schedule.get_jobs()
                print(var)
                tastiera = ["Oggi","/oggi","Domani","/domani","Menù", "/menu"]
                bot.sendMessage(chat_id, str(var),reply_markup = makeKeyboard(tastiera))

        if(message == "/ornitorinco"): #Fa crashare il bot
                a = 2
                b = "cc"
                print(a+b)

        if(message == "/admin"):
                print("hai chiesto gli admin")
                print(getAdmins())

        mycursor.close()

startSchedules()
#mycursor.close()

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
