import sys

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://webaurion.centralelille.fr/faces/Login.xhtml")

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
			return nbNotes
	finally:
		pass
		#driver.close()

if __name__ == "__main__":
   login()
   getMyMarks()
   note = findMarks() 

