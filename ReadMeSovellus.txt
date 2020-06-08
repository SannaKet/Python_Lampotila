Python ohjelmointi, kevät 2020
Careeria
Sanna Ketomäki

SÄÄOHJELMA

Ohjelma hakee lämpötilatiedot Open Weathermap -palvelusta.
Tietokantaan tallennetaan käyttäjän antamat paikkakunnat.

Toimiakseen sovellus tarvitsee seuraavat kirjastot, jotka asennettiin pypi.org palvelusta:

pip install pyowm==2.10.0   => säätietoja varten
	* uusimmassa versiossa (3.0.0) oli ilmeisesti jokin bugi eikä se toiminut Python 3.8.2:sen kanssa.
pip install texttable 	=> tekstimuotoisen taulukon tulostamista varten (tulostusvaihtoehto 2)
(ver 1.6.2)


Lisäksi importattiin
import sqlite3	=> tietokantaa varten
from pyowm.exceptions import api_response_error	=> käsitellään paikkakunnat, joita ei löydy tietokannasta
import os	=> jotta konsoli voidaan tyhjentää, kun sovellus käynnistyy

Ohjelma kirjoittaa hakujen tulokset lokiin.

Sovelluksessa annetaan esitettyihin kysymyksiin K tai E vastaus, joka voidaan antaa joko pienillä tai ISOILLA kirjaimilla.
Jos käyttäjä antaa jonkin muun vastauksen, siitä tulee virheilmoitus ja käyttäjältä kysytään haluaako hän jatkaa.
Jos käyttäjä haluaa jatkaa, ohjelma alkaa alusta.
Jos käyttäjä vastaa, ettei halua jatkaa, kiitetään käyttäjää ja ohjelman suoritus päättyy.