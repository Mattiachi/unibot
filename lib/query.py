import mysql.connector
from datetime import datetime

DEBUG = False

mydb = mysql.connector.connect(
	host = "localhost",
	user = "unibot",
	password = "password",
	database = "unibot"
	)

mycursor = mydb.cursor()

def exFetch(cmd):
	mycursor.execute(cmd)
	return mycursor.fetchall()

def exCommit(cmd):
	mycursor.execute(cmd)
	mydb.commit()
	return

def getToken(a = 0):
	"""
	Returns a string value corresponding of the telegram bot token found in
	the table "telegram" field token of the mysql DB
	"""
	token = exFetch("SELECT token FROM telegram") 
	token = str(token[a][0]) #Cast from list to string
	if(DEBUG):
		print("getToken() returned telegram bot")
	return token

def getState(id):
	"""
	Returns the int(stato) of a given chat_id found in its corresponding row of
	the mysql DB in field stato and table utente
	"""
	id = str(id)
	var = exFetch("SELECT stato FROM utente WHERE chat_id = " + id)
	var = int(var[0][0])
	if(DEBUG):
		print("chat_id " + id + " has now a stato of: " + str(var))
	return var

def upgradeStato(id):
	"""
	Increments by one the stato of a given chat_id found in its corresponding row of
	the mysql DB in field stato and table utente
	"""
	id = str(id)
	exCommit("UPDATE utente SET stato = stato + 1 WHERE chat_id = " + id)
	if(DEBUG):
		print("stato of " + id + " increased by one.")
	actual_stato = str(getState(id))
	return

def downgradeStato(id):
	"""
	Decrements by one the stato of a given chat_id found in its corresponding row of
	the mysql DB in field stato and table utente
	"""
	id = str(id)
	exCommit("UPDATE utente SET stato = stato -1 WHERE chat_id = " + id)
	if(DEBUG):
		print("Stato of " + id + " decreased by one.")
	actual_stato = str(getState(id))
	return

def getAdmins():
	"""
	Returns the list of all the chat_id in the table admin
	"""
	if(DEBUG):
		print("Retrieving the admins from the database")
	return exFetch("SELECT chat_id FROM admin")


def nuovoUtente(id):
	"""
	Check if a chat_id is known. In this case it increments the message count, otherwise
	it adds him to the table utente initializing stato = 0, anno = 0, messaggi = 1
	"""
	response = exFetch("SELECT chat_id FROM utente")
	for i in range(len(response)):
		if(int(id) == response[i][0]):
			if(DEBUG):
				print("chat_id " + str(id) + "is already known")
			exCommit("UPDATE utente SET messaggi = messaggi + 1 WHERE chat_id = " + str(id))
			if(DEBUG):
				print("Upgrading messaggi count for chat_id = " + str(id))
			return

	if(DEBUG):
		print("chat_id " + str(id) + "is unknown, adding him...")

	exCommit("INSERT INTO utente (chat_id,messaggi,stato,anno) VALUES ( " + str(id) + ",1,0,1)")
	if(DEBUG):
		print("Initialized messaggi = 1, stato = 0, anno = 0 for chat_id = " + str(id))
	return

def likeString(comando):	#Updated in V3
	count = 0
	for i in range(len(comando)):
		if(comando[i] == " "):
			count +=1
	x = comando.split(" ")
	sql = 'select corso,id from universita where corso like "%'

	for i in range(len(x)):
		if(i==0):
			sql += x[i]
		else:
			sql += '%" and url like "%'
			sql += x[i]
	sql +='%"'
	res = exFetch(sql)
	return res

def adminInfo(chat_id):
	'''
	Returns 1 wether the chat_id is an admin, otherwise returns 0
	'''
	a = exFetch("SELECT chat_id FROM admin")

	for i in range(len(a)):
		if(chat_id == a[i][0]):
			return 1
	return 0


def getStats():
#	utenti_attivi = exFetch("SELECT COUNT(chat_id) FROM utente WHERE stato > 3")
#	messaggi_totali = exFetch("SELECT SUM(messaggi) from utente")
#	return [utenti_attivi[0][0],int(messaggi_totali[0][0])]
	"""
	data =  exFetch("SELECT nick, messaggi, stato, oggi, domani, last_seen from utente")
	text = "Nome/t| messaggi/t| stato/t| oggi/t| domani/t| last_seen\n"
	for nick, messaggi,stato, oggi, domani, last_seen in data:
		text += nick + " " + str(messaggi) + " " +str(stato) + " "
		if(oggi):
			text += oggi
		else:
			text += "/ "
		if(domani):
			text += domani
		else:
			text += "/ "

		text += str(last_seen)
		text += "\n"

	return text
	"""
	from tabulate import tabulate
	data = exFetch("SELECT nick, messaggi, stato, oggi, domani, last_seen from utente order by last_seen desc")
	a = []
	for nick, messaggi,stato, oggi, domani, last_seen in data:
		t = [nick, str(messaggi), str(stato), str(last_seen)[2:10]]
		#if(oggi):
		#	t += [oggi]
		#else:
		#	t+= ['None']
		#if(domani):
		#	t+= ['None']
		a += [t]

	head = ['Nome', 'msg', 'Stato', 'Last']

	print(tabulate(a, headers = head,tablefmt='orgtbl'))
	return tabulate(a, headers = head, tablefmt='orgtbl')

def getYear(chat_id, message):
	sql = "select durata from universita where ID = (select id_universita from percorso where ID = " + str(message) + " )"
	key = []
	for x in range(exFetch(sql)[0][0]):
		key += [x+1]*2
	return key

def updateLast_seen(chat_id):
	now = datetime.now().strftime("%Y-%m-%d %H:%M")
	exCommit('update utente set last_seen = "' + str(now) + '" where chat_id=' +str(chat_id))


def updateNickname(chat_id, nickname):
	exCommit("update utente set nick = '" + str(nickname) + "' where  chat_id =" + str(chat_id))

def getSchedules():
	table = exFetch('select chat_id, oggi, domani from utente')
	return table
	print(type(table))

def getYears(corso):
	result = []
	var = exFetch("select anno from corsi where url = '" + corso + "'")
	print(type(var[0][0]), var[0][0])
	for x in range(var[0][0]):
		result += [x+1]*2
	return result


def getCurricula(id_uni):
	'''
	Dove id_uni e una stringa
	'''
	res = exFetch("select nome, ID from percorso where id_universita = " + id_uni)
	key = []
	for row in res:
		for x in row:
			key.append(str(x))
	key.append("Nessuno di questi")
	key.append("-1")
	print(key)
	return(key)


def getUrl(chat_id):
	sql1 = "select url from universita where ID = (select id_universita from percorso where ID = (select curricula_id from utente where chat_id = " + str(chat_id) + " ))"
	sql2 = "select anno from utente where chat_id = " + str(chat_id)
	sql3 = "select curricula from percorso where ID = (select curricula_id from utente where chat_id = " + str(chat_id) + " )"

	url = exFetch(sql1)[0][0]
	year = exFetch(sql2)[0][0]
	curricula = exFetch(sql3)[0][0]

	time = "/orario-lezioni"
	if("2cycle" in url):
		time = "/timetable"

	res = url + time + "/@@orario_reale_json?anno=" + str(year) + "&curricula=" + curricula
	#res += "&start=" + start + "&end=" + end + "\""
	print(res)
	return res
