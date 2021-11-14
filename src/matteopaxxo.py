from bs4 import BeautifulSoup
import os, json

import mysql.connector

mydb = mysql.connector.connect(
		host = "localhost",
		user = "unibot",
		password = "password",
		database = 'unibot'
	)

mycursor = mydb.cursor()

def exFetch(cmd):
        mycursor.execute(cmd)
        return mycursor.fetchall()

def exCommit(cmd):
        mycursor.execute(cmd)
        mydb.commit()
        return


curricula = "/@@available_curricula?"
start = 'data-title="'
end = '"'
start2 = 'href="'

#File dal quale vado a leggere i Corsi di UniBo
f = open('corsi-di-studio.html', "r")
data = f.read()

soup = BeautifulSoup(data, 'html.parser')
vett = ""	#Vettore che vado a stampare nel file di output


cont = 0	#Conteggio per i corsi totali


seen = []

mysql1 = "INSERT INTO universita (ID, corso, url, shortUrl, durata) VALUES "
mysql2 = "INSERT INTO percorso (id_universita, curricula, nome) VALUES "
for a in soup.find_all("a", class_ = "umtrack"):
	if("data-title" in str(a)): # and ("elettro" in str(a) or "infor" in str(a)) ):
		var = str(a)
		nome = var.split(start)[1].split(end)[0]
		link = var.split(start2)[1].split(end)[0]
		short = var.split("https://corsi.unibo.it/")[1].split(end)[0]
		if(link in seen):
			continue
		seen.append(link)
		cont +=1

		vett += nome + " \n" + link + "\n" + short + "\n"
		quando = "/orario-lezioni"
		if("cycle" in var.split(start2)[1].split(end)[0]):
			quando = "/timetable"
		comando = "curl " + var.split(start2)[1].split(end)[0]+quando
		data2 = os.popen(comando).read()
		zuppa = BeautifulSoup(data2, 'html.parser')
		resp = str(zuppa.find_all("option"))
		max = 0
		for x in resp:
			if(x.isdigit()):
				max = x
		vett+= str(max) + "\n"

		mysql1 += '( ' + str(cont) + ', "' + nome +'","' + link + '","' + short + '", ' + str(max)+ '),'

		#Gets the CURRICULA
		comando += curricula
		print(comando)
		try:
			a = json.loads(os.popen(comando).read())
			print(a)
			campi = ['value', 'label']
			for x in range(len(a)):
				mysql2 += '( ' + str(cont) + ', '
				for y in range(len(campi)):
					vett += str(a[x][campi[y]]) + " | "
					mysql2 += '"'+str(a[x][campi[y]]) + '",'
				vett += "\n"
				mysql2 = mysql2[:-1]
				mysql2 +=  '),'
			vett += "\n\n"
#			print(vett)

		except :
			vett += "\nNon è stato possibile ricevere queste informazioni\n\n"
#		print(vett)
print(vett)
print(seen)

exCommit("delete from utente")
exCommit("delete from percorso")
exCommit("delete from universita")
exCommit("alter table utente AUTO_INCREMENT = 1;")
exCommit("alter table percorso AUTO_INCREMENT = 1;")
exCommit("alter table universita AUTO_INCREMENT = 1;")
exCommit(mysql1[:-1])
exCommit(mysql2[:-1])
print("Corsi Trovati: " + str(cont))

vett = "Corsi Totali: " + str(cont) + "\n\n" + vett
f = open("corsi.txt", "w")
f.write(vett)
f.close()
