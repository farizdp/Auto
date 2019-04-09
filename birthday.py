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

def hut(date, id_telegram, user, pw):
	driver = webdriver.Chrome()
	driver.set_page_load_timeout(60)
	driver.get("***Link Web HCM***")
	username = driver.find_element_by_id('loginform-username')
	username.send_keys(user)
	password = driver.find_element_by_id('loginform-password')
	password.send_keys(pw)
	button = driver.find_element_by_name('login-button')
	button.click()
	wait = WebDriverWait(driver, 10)
	element = wait.until(element_has_css_class((By.ID, 'myCarousel'), "carousel slide"))
	hut = driver.find_element_by_xpath("//div[6]/div[2]/div[2]/div")
	source_code = hut.get_attribute('innerHTML')
	html_string = str(source_code).replace('							<div>','							<div class="nik">')
	html_page = BeautifulSoup(html_string, 'html.parser')
	nama = html_page.find_all('span', attrs={"class":"testimonials-name"})
	title = html_page.find_all('div', attrs={"style":"overflow:hidden;font-size:11px"})
	nik = html_page.find_all('div', attrs={"class":"nik"})
	driver.quit()
	text = "Rekan yang berulang tahun hari ini!\n" + date
	for i,j in enumerate(nama):
		temp = "\n\n" + str(i+1) + ". *" + j.string + "* - `" + nik[i].string + "`\n[" + title[i].string + "]"
		text = text + temp
	bot.sendMessage(id_telegram, text, 'Markdown')


id_telegram = '***ID Telegram***'
token = '***Toket BOT Telegram***'
user = '***Username***'
pw = '***Password***'

bot = telepot.Bot(token)
hari = datetime.datetime.now()
print('Starting...')
hut(hari.strftime("%b, %d %Y"), id_telegram, user, pw)

while 1:
	hari = datetime.datetime.now()
	if hari.strftime("%H:%M") == '09:00':
		hut(hari.strftime("%b, %d %Y"), id_telegram, user, pw)
	time.sleep(60)
