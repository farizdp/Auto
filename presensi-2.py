from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import datetime
import time
import telepot
import telepot.api
import os
import random
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class element_has_css_class(object):
  def __init__(self, locator, css_class):
    self.locator = locator
    self.css_class = css_class

  def __call__(self, driver):
    element = driver.find_element(*self.locator)
    if self.css_class in element.get_attribute("class"):
        return element
    else:
        return False

def presensi(tipe, id_telegram, uname, pw):
	driver = webdriver.Chrome()
	driver.set_page_load_timeout(60)
	driver.get("***Web Link Login***")
	driver.find_element_by_id('loginform-username').send_keys(uname)
	driver.find_element_by_id('loginform-password').send_keys(pw)
	driver.find_element_by_name('login-button').click()
	wait = WebDriverWait(driver, 10)
	element = wait.until(element_has_css_class((By.ID, 'clock-in-button'), "btn btn-danger"))
	driver.find_element_by_link_text(tipe).click()
	if tipe == 'Clock In' :
		driver.get("***Web Link Clock In***")
		element_survey = wait.until(element_has_css_class((By.ID, 'question'), "question-label"))
		driver.find_element_by_css_selector("input[type='radio'][value='450']").click()
		driver.find_element_by_css_selector("input[type='radio'][value='455']").click()
		driver.find_element_by_tag_name("textarea").send_keys("                              ")
		driver.find_element_by_css_selector("button[type='submit'][class='btn btn-danger submission-button']").click()
	if tipe == 'Clock out' :
		jsalert = driver.switch_to.alert
		jsalert.accept()
	driver.get("***Web Link***")
	source_code = driver.page_source
	html_page = BeautifulSoup(source_code, 'html.parser')
	status = html_page.find_all('div', attrs={"class":"subtitle"})
	text = "Successfully " + status[0].string + " `" + status[1].string + "`"
	bot.sendMessage(id_telegram, text, 'Markdown')
	driver.quit()

id_telegram = '***ID Telegram***'
token = '***Token Telegram BOT***'
bot = telepot.Bot(token)
telepot.api.set_proxy(proxy)

cred = credentials.Certificate('***Directory Certificate***')
firebase_admin.initialize_app(cred)
db = firestore.client()

print('Starting...')

list_in = list(range(20, 24)) + list(range(0, 7))
list_out = list(range(8, 20))
list_day = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']

menit_awal = 30
menit_akhir = 45

hari = datetime.datetime.now()
if hari.strftime("%a") in list_day :
	menit = random.randint(menit_awal, menit_akhir)
	jam = int(hari.strftime("%H"))
 	if jam in list_out :
 		waktu = '20:' + str(menit)
 		text = 'Next `clockout` at *' + hari.strftime("%a, %b %d") + '* / *' + waktu + '*'
 	if jam in list_in :
 		waktu = '07:' + str(menit)
 		hari = hari + datetime.timedelta(days = 1)
 		if hari.strftime("%a") != 'Sat' :
 			text = 'Next `clockin` at *' + hari.strftime("%a, %b %d") + '* / *' + waktu + '*'
 		else :
 			text = 'Next `clockin` at *' + 'Mon' + '* / *' + waktu + '*'
 else :
 	waktu = '07:' + str(menit)
 	text = 'Next `clockin` at *' + 'Mon' + '* / *' + waktu + '*'
 bot.sendMessage(id_telegram, text, 'Markdown')

while 1:
	ctime = time.strftime("%H:%M")
	menit = random.randint(menit_awal, menit_akhir)
	hari = datetime.datetime.now()
	if hari.strftime("%a") in list_day :
		if ctime == waktu :
	 		doc = db.collection(u'***DB***').document(u'***Table***').get().to_dict()
	 		if waktu[:2] == '20' :
	 			presensi('Clock out', id_telegram, doc['username'], doc['password'])
	 			plan = '07:' + str(menit)
	 			hari = hari + datetime.timedelta(days = 1)
	 			if hari.strftime("%a") != 'Sat' :
	 				text = 'Next `clockin` at *' + hari.strftime("%a, %b %d") + '* / *' + plan + '*'
	 			else :
	 				text = 'Next `clockin` at *' + 'Mon' + '* / *' + plan + '*'
	 		if waktu[:2] == '07' :
	 			presensi('Clock In', id_telegram, doc['username'], doc['password'])
	 			plan = '20:' + str(menit)
	 			text = 'Next `clockout` at *' + hari.strftime("%a, %b %d") + '* / *' + plan + '*'
	 		waktu = plan
	 		bot.sendMessage(id_telegram, text, 'Markdown')
	 		time.sleep(60)
