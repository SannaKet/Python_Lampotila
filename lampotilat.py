import pyowm
import sqlite3
from datetime import datetime
from pyowm.exceptions import api_response_error
from texttable import Texttable
import os


def paikkakunnanLampotila():
    sql = "SELECT * FROM paikkakunnat"
    kursori.execute(sql)
    rows = kursori.fetchall()
    lkm = len(rows)

    table = Texttable()
    table.set_cols_dtype(['t','t'])
    table.set_cols_align(["l", "c"])
    table.add_row(['Paikkakunta', 'Lämpötila ' u'\N{DEGREE SIGN}''C'])


    for row in rows:
        paikka = row[0]
        Paikka = paikka.capitalize()
        degree_sign = u'\N{DEGREE SIGN}'
        owm = pyowm.OWM('9028ea04d593364b883b28032ffe5029')     #API-key sääpalveluun
        try:
            observation = owm.weather_at_place(paikka)
            weather = observation.get_weather()
            temperature = weather.get_temperature('celsius')['temp']
            print(f'Lämpötila ({Paikka}): {temperature} {degree_sign}C')
            table.add_row([Paikka, temperature])
        except api_response_error.NotFoundError:
            #Kirjoitetaan epäonnistunut haku lokiin
            kirjoita_lokiin(f"{paikka}: hakuvirhe!")

    # Tulostetaan lämpötilataulukko (vaihtoehto 2)
    print("\n--- Tulostusvaihtoehto nro 2 ---")
    print(table.draw())

    # Kirjoitetaan onnistunut haku lokiin
    kirjoita_lokiin(f"Haettiin {lkm} paikkakunnan lämpötila")
    kirjoita_lokiin("--- Haku päättyy ---")



def paikkakunnatTietokannasta():
    #Haetaan tiedot tietokannasta
    sql = "SELECT * FROM paikkakunnat"
    kursori.execute(sql)
    rows = kursori.fetchall()
    for row in rows:
        paikka = row[0]
        Paikka = paikka.capitalize()
        print(Paikka)


def haetaankoLampotilat():
    # Haetaan lämpötilatiedot, jos käyttäjä haluaa
    print(" ")
    haetaankoLampotila = input("Haetaanko paikkakuntien lämpötilatiedot? (K/E)")
    haetaankoLampotilaToUpper = haetaankoLampotila.upper()


    if haetaankoLampotilaToUpper == "K":
        print("\n--- Tulostusvaihtoehto nro 1 ---")
        paikkakunnanLampotila()

    elif haetaankoLampotilaToUpper == "E":
        pass

    else:
        print("Virhe -- Anna ystävällisesti vastaukseksi K tai E")



def kirjoita_lokiin(viesti):
    pvm = datetime.now()
    f = open("LampotilaLoki.txt", "a", encoding="UTF-8")
    tallennus = ("\n" + str(pvm) + ", " + viesti)
    f.write(tallennus)
    f.close


while True:

    os.system('cls')

    print("\n======== TERVETULOA SÄÄ-OHJELMAAN ========")
    print("\nEtsi lämpötiloja haluamiltasi paikkakunnilta.")

    aloitetaan = input("\nAloitetaanko? (K/E)")
    aloitetaanToUpper = aloitetaan.upper()
    #print("--- Aloitetaan ---")


    if aloitetaanToUpper == "K":
        #pass

        try:

            # Yhteys tietokantaan
            conn = sqlite3.connect('paikkakunnat.db')

            # Tietokannan rakenteen luonti
            sql = '''CREATE TABLE IF NOT EXISTS paikkakunnat (
                        Nimi text)'''
            kursori = conn.cursor()
            kursori.execute(sql)


            # Haetaan tietokannassa olevat tiedot
            print("\n--- Tällä hetkellä valittuna paikkakunnat: ---\n")
            paikkakunnatTietokannasta()


            # Paikkakuntien valinta
            vaihdetaanko = input("\nHaluatko muuttaa seurattavia paikkakuntia? (K/E)")
            vaihdetaankoToUpper = vaihdetaanko.upper()

            if vaihdetaankoToUpper == "K":
                
                # Tyhjennetään tietokannasta edelliset tiedot
                sql = 'DELETE FROM paikkakunnat'
                kursori.execute(sql)

                location = ""

                print('''
                ==============================================================
                Lopetus: Paina X, kun haluat lopettaa paikkakuntien antamisen.
                ==============================================================''')

                while location != "X" or location !="x":
                    location = input("\nAnna paikkakunta, jonka lämpötilan haluat tietää: ")
                    locationToUpper = location.upper()

                    if location == "X" or location == "x":
                        print("\n--- Kiitos, tietojen syöttö on päättynyt ---")
                        break

                    else:
                        #Tallennus tietokantaan
                        print("- Tallennetaan tietokantaan.... -")

                        sql = 'INSERT INTO paikkakunnat VALUES(?)'
                        kursori.execute(sql, (locationToUpper,))
                        conn.commit()

                # Tulostetaan tiedot kannasta
                print(" ")
                print("--- Tallennetut paikkakunnat ---")
                paikkakunnatTietokannasta()

                # Haetaan lämpötilatiedot, jos käyttäjä haluaa
                haetaankoLampotilat()

            elif vaihdetaankoToUpper == "E":
                # Jos käyttäjä ei halua vaihtaa paikkakuntia, haetaan kannassa olevien paikkakuntien tiedot
                haetaankoLampotilat()

            else:
                print("Virhe -- Anna ystävällisesti vastaukseksi K tai E")

        except sqlite3.Error as error:  # Jos tietokannan luku ei onnistu
            print("Tapahtui virhe: ", error)

        finally:
            if (conn):
                conn.close()
                #print("The SQLite connection is closed")

    elif aloitetaanToUpper == "E":
        pass

    else:
        print("Virhe -- Anna ystävällisesti vastaukseksi K tai E")


    while True:
        print(" ")
        lopetus = input('Haluatko jatkaa? (K/E): ')
        lopetusToUpper = lopetus.upper()

        if lopetusToUpper in ('K', 'E'):
            break
        else:         
            print("Virhe -- Anna ystävällisesti vastaukseksi K tai E")

    if lopetusToUpper == 'K':
        continue
    else:
        print('\n--- Kiitos. Ohjelman suoritus päättyi ---\n')
        break




