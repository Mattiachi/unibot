CREATE TABLE universita(
	ID int NOT NULL,
	corso TEXT,
	url TEXT,
	shortUrl TEXT,
	durata int,	
	PRIMARY KEY (ID)
);




CREATE TABLE percorso(
	ID INT NOT NULL AUTO_INCREMENT,
	curricula TEXT,
	nome TEXT,
	id_universita INT NOT NULL,
	PRIMARY KEY (ID),
	FOREIGN KEY (id_universita) REFERENCES universita(ID)
);
	
