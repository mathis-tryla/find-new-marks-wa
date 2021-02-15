# -*- coding: utf-8 -*-
import sys, os, csv, codecs, json

#from selenium import webdriver
#from webdriver_manager.chrome import ChromeDriverManager
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.by import By

#driver = webdriver.Chrome(ChromeDriverManager().install())
#driver.get("https://webaurion.centralelille.fr/faces/Login.xhtml")

def login():
    pseudoinput = driver.find_element_by_xpath('//*[@id="username"]')
    pseudoinput.send_keys('mtryla')

    pwdinput = driver.find_element_by_xpath('//*[@id="password"]')
    pwdinput.send_keys('MWarrior62')

def getMyMarks():
    searchbtn = driver.find_element_by_xpath('//*[@id="j_idt29"]')
    searchbtn.click()
    resultsLink = driver.find_element_by_xpath('//*[@id="form:sidebar"]/div/div[2]/ul/li[2]/a')
    resultsLink.click()
    ig2iLink = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="form:sidebar"]/div/div[2]/ul/li[2]/ul/li/a'))
    )
    ig2iLink.click()
    mesNotesLink = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="form:sidebar"]/div/div[2]/ul/li[2]/ul/li/ul/li[1]/a'))
    )
    mesNotesLink.click()

def findMarks():
    try:
        searchbtn = driver.find_element_by_xpath('//*[@id="form:search"]')
        # on renseigne un mot-clé pour rechercher une/des note(s) par matière
        if len(sys.argv) > 1:
            searchbox = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="form:search-texte"]'))
            ) 
            searchbox.send_keys(sys.argv[1])
            searchbtn.click()
            return 0
        # on recherche une/des nouvelle(s) note(s)
        else:
            searchbtn.click()
            nbNotes = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="form:messages"]/div/ul/li/span'))
            )
            nbNotes = nbNotes.text
            nbNotes = nbNotes.split()
            nbNotes = nbNotes[0]
            readCsvFile("mesnotes.csv")
            checkMarksNumber(nbNotes)
    finally:
        pass
        driver.close()

def exportCsvMarks():
    exportBtn = driver.find_element_by_xpath('//*[@id="form:exportButton"]/span[2]')
    exportBtn.click()
    exportCsvUtf = driver.find_element_by_xpath('//*[@id="form:j_idt158"]/ul/li[5]/a')
    exportCsvUtf.click()

def storeMarksNumber(nbNotes):
    fichier = open("nbNotes.txt", "w")
    fichier.write(nbNotes)
    fichier.close()

def getPrevMarksNumber():
    fichier = open("nbNotes.txt", "r")
    result = fichier.read()
    fichier.close()
    return result

def checkMarksNumber(nbNotes):
    if getPrevMarksNumber() < nbNotes:
        storeMarksNumber(nbNotes)
        # TODO: modify argument of readCsvFile
        exportCsvMarks()
        dictionnary = readCsvFile("mesnotes.csv")
        newMarks = compareOldMarksCsvOnes()
        # if len(newMarks) > 1:
        # for newMark in newMarks:
        #     type = newMark.get(0)
        #     topic = newMark.get(1)
        #     mark = newMark.get(2)
        # notify("NOUVELLE NOTE:", topic, mark)
        print("NOUVELLE NOTE !")
    else:
        notify("Aucune nouvelle NOTE", "test", "test1")
        print("Aucune nouvelle note ...")

def notify(title, subject, mark):
    t = '-title {!r}'.format(title)
    s = '-subtitle {!r}'.format(subject)
    m = '-message {!r}'.format(mark)
    os.system('terminal-notifier {}'.format(' '.join([m, t, s])))

def readCsvFile(filename):
    tab = {}
    with open(filename) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            line = []
            i = 0
            for elt in row.values():
                if i in [0, 2, 6]:
                    line.append(elt)
                i += 1
            tab[line_count] = line
            line_count += 1
        csv_file.close()
    with open("notesListe.json", "w") as fichierToWrite:
        json.dump(tab, fichierToWrite, indent=4, sort_keys=True)
    with open("notesListe.json", "r") as fichierToWrite:
        data = json.load(fichierToWrite)
        fichierToWrite.close()
    # os.remove(filename)
    # os.remove(notesListe)
    return data


def compareOldMarksCsvOnes():
    dictionnary = {}
    with open("notesListe.json", "r") as fichier:
        result = json.load(fichier)
        
    fichier.close()
    return dictionnary
    


if __name__ == "__main__":
   #login()
   #getMyMarks()
   #findMarks() 
   dictionnary = readCsvFile("mesnotes.csv")
   compareOldMarksCsvOnes()

