# -*- coding: utf-8 -*-
import sys, os, csv, glob, time, shutil, platform

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from playsound import playsound
from ipaddress import IPv4Address  # for your IP address
from pyairmore.request import AirmoreSession  # to create an AirmoreSession
from pyairmore.services.messaging import MessagingService  # to send messages


ip = '192.168.1.77'
port = 2333
phoneNumber = "0613600787"
nbNotes_file = "nbNotes.txt"
login_file = "login.txt"
downloads_file = "downloads.txt"
oldFile_file = "oldFile.txt"
driver = webdriver.Chrome(ChromeDriverManager().install())
# driver = webdriver.Safari()
driver.get("https://webaurion.centralelille.fr/faces/Login.xhtml")


def createSession(ipAdr, port, msgContent):
    ipV = IPv4Address(ipAdr)  # let's create an IP address object
    # now create a session
    session = AirmoreSession(ipV)
    # if your port is not 2333
    session = AirmoreSession(ipV, port)  # assuming it is 2334
    session.is_server_running  # True if Airmore is running
    was_accepted = session.request_authorization()
    print(was_accepted)
    sendSms(session, msgContent)


def sendSms(session, msgContent):
    service = MessagingService(session)
    service.send_message(phoneNumber, msgContent)


def login():
    ids = getIds()
    pseudoinput = driver.find_element_by_xpath('//*[@id="username"]')
    pseudoinput.send_keys(ids[0])
    pwdinput = driver.find_element_by_xpath('//*[@id="password"]')
    pwdinput.send_keys(ids[1])
    loginBtn = driver.find_element_by_xpath('//*[@id="formulaireSpring"]/div[4]')
    loginBtn.click()
    

def getMyMarks():
    try:
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
    except Exception as e:
        print(e)
        notify("ERREUR", "Identifiant ou mot de passe incorrecte", "Fin du programme")
        print("Identifiant ou mot de passe incorrecte...")
        print("Fin du programme")
        driver.close()
        exit(-1)


def findMarks():
    answer = 'N'
    searchbtn = driver.find_element_by_xpath('//*[@id="form:search"]')
    # on renseigne un mot-clé pour rechercher une/des note(s) par matière
    if len(sys.argv) > 1:
        searchbox = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="form:search-texte"]'))
        ) 
        searchbox.send_keys(sys.argv[1])
        searchbtn.click()
        while answer == 'N':
            answer = input("Have you ended up ? [y/N] ")
    # on recherche une/des nouvelle(s) note(s)
    else:
        searchbtn.click()
        nbNotes = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="form:messages"]/div/ul/li/span'))
        )
        nbNotes = nbNotes.text
        nbNotes = nbNotes.split()
        nbNotes = nbNotes[0]
        checkMarksNumber(nbNotes)
    driver.close()



def exportCsvMarks():
    exportBtn = driver.find_element_by_xpath('//*[@id="form:exportButton"]/span[2]')
    exportBtn.click()
    exportCsvUtf = driver.find_element_by_xpath('//*[@id="form:j_idt158"]/ul/li[5]/a')
    exportCsvUtf.click()
    time.sleep(5)


def getIds():
    fichier = open(login_file, "r")
    res = fichier.read()
    result = res.split(" ")
    fichier.close()
    return result


def storeMarksNumber(nbNotes):
    fichier = open(nbNotes_file, "w")
    fichier.write(nbNotes)
    fichier.close()


def getPrevMarksNumber():
    fichier = open(nbNotes_file, "r")
    result = fichier.read()
    fichier.close()
    return result


def checkMarksNumber(nbNotes):
    if getPrevMarksNumber() < nbNotes:
        storeMarksNumber(nbNotes)
        exportCsvMarks()
        oldFile = "mesnotes.csv"
        newFile = getNewCsvFile()
        oldDictionnary = readCsvFile(oldFile, 1)
        newDictionnary = readCsvFile(newFile, 0)
        os.rename(newFile, oldFile)
        newMarks = compareOldMarksNewOnes(oldDictionnary, newDictionnary)
        print(newMarks)
        if len(newMarks) > 0:
            for k, newMark in newMarks.items():
                topic = newMark[1]
                mark = newMark[2]
                try:
                    createSession(ip, port, "NOUVELLE NOTE : " + str(topic) + " tu as obtenu la note de " + str(mark) + "")
                except:
                    print("0 session created")
                if platform.system() == 'Darwin':
                    playsound('notification.mp3')
                    notify("NOUVELLE NOTE", topic, mark)
                time.sleep(3)
        print("NOUVELLE NOTE !")
    else:
        if platform.system() == 'Darwin':
            notify("Aucune nouvelle NOTE" , "Fin du programme", "Bye !")
        print("Aucune nouvelle note ...")


def notify(title, subject, mark):
    t = '-title {!r}'.format(title)
    s = '-subtitle {!r}'.format(subject)
    m = '-message {!r}'.format(mark)
    os.system('terminal-notifier {}'.format(' '.join([m, t, s])))


def readCsvFile(filename, numRemove):
    tab = {}
    with open(filename, encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            line = []
            i = 0
            for elt in row.values():
                if i in [0, 1, 4]:
                    line.append(elt)
                i += 1
            tab[line_count] = line
            line_count += 1
        csv_file.close()
    if numRemove == 1: os.remove(filename) 
    return tab


def getDownloadPath():
    fichier = open(downloads_file, "r")
    result = fichier.read()
    fichier.close()
    return result


def getNewCsvFile():
    dlPath = getDownloadPath()
    dlPath_files = dlPath + "*"
    list_of_files = glob.glob(dlPath_files)
    latest_file = max(list_of_files, key=os.path.getctime)
    print("LATEST = " + latest_file)
    newOne = shutil.move(latest_file, './')
    return newOne


def differences(li1, li2):
    return (list(list(set(li1)-set(li2)) + list(set(li2)-set(li1))))


def compareOldMarksNewOnes(oldDict, newDict):
    result = {}
    line_count = 0
    list_id_oldDict = []
    list_id_newDict = []
    differences_list = []

    for kO, vO in oldDict.items():
        list_id_oldDict.append(vO[0])

    for kN, vN in newDict.items():
        list_id_newDict.append(vN[0])

    differences_list = differences(list_id_oldDict, list_id_newDict)

    for idMark in differences_list:
        for kN, vN in newDict.items(): 
            if idMark == vN[0]:
                result[line_count] = vN
                line_count += 1
    return result
    


if __name__ == "__main__":
    login()
    getMyMarks()
    findMarks() 