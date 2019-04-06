from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import telepot
import time, os, sys, random
import datetime

link_hris = "***Link Login HRIS***"
id_telegram = '***ID Telegram***'
token = '***Token Telegram***'
menit_awal = 30
menit_akhir = 45

def presensi(tipe, link_hris, id_telegram):
	driver = webdriver.Chrome()
	driver.set_page_load_timeout(60)
	try :
		driver.get(link_hris)
		driver.get("***Link Clock***?_act=clock_" + tipe + "&captcha=1&captchaInput=1")
		element = driver.find_element_by_id('captcha')
		captcha = element.get_attribute('value')
		inputElement = driver.find_element_by_id("captchaInput")
		inputElement.send_keys(captcha)
		try :
			telat = Select(driver.find_element_by_id('reasonLate'))
			selected_option = telat.select_by_index(1)
		except :
			bot.sendMessage(id_telegram, 'Semangat pagi!', 'Markdown')
		inputElement.send_keys(Keys.ENTER)
		try :
			jsalert = driver.switch_to.alert
			jsalert.accept()
		except :
			bot.sendMessage(id_telegram, 'Semangat berkarya!', 'Markdown')
		try :
			 driver.find_element_by_name('clock_in_button').click()
		except :
			 bot.sendMessage(id_telegram, 'Selamat istirahat!', 'Markdown')
		text = 'Clock' + tipe + ' *' + datetime.datetime.now().strftime("%a, %b %d") + '* is successful!'
		print(text)
		driver.get("http://hrispappsnew.hrims.telkomsel.co.id:8000/OA_HTML/sshr/TSEL_ABSENSI/ViewFHist.jsp")
		driver.save_screenshot('history.png')
		driver.quit()
		bot.sendMessage(id_telegram, text, 'Markdown')
		bot.sendPhoto(id_telegram, open('history.png', 'rb'))
	except TimeoutException:
		driver.quit()
		bot.sendMessage(id_telegram, 'Timeout!', 'Markdown')	

print('Starting ...')
bot = telepot.Bot(token)
list_in = list(range(20, 24)) + list(range(0, 7))
list_out = list(range(8, 20))
list_day = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
hari = datetime.datetime.now()
menit = random.randint(menit_awal, menit_akhir)
jam = int(hari.strftime("%H"))
if hari.strftime("%a") in list_day :
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
print(text)
bot.sendMessage(id_telegram, text, 'Markdown')

while 1:
	ctime = time.strftime("%H:%M")
	menit = random.randint(menit_awal, menit_akhir)
	hari = datetime.datetime.now()
	if hari.strftime("%a") in list_day :
		if ctime == waktu :
			if waktu[:2] == '20' :
				presensi('out', link_hris, id_telegram)
				plan = '07:' + str(menit)
				hari = hari + datetime.timedelta(days = 1)
				if hari.strftime("%a") != 'Sat' :
					text = 'Next `clockin` at *' + hari.strftime("%a, %b %d") + '* / *' + plan + '*'
				else :
					text = 'Next `clockin` at *' + 'Mon' + '* / *' + plan + '*'
			if waktu[:2] == '07' :
				presensi('in', link_hris, id_telegram)
				plan = '20:' + str(menit)
				text = 'Next `clockout` at *' + hari.strftime("%a, %b %d") + '* / *' + plan + '*'
			waktu = plan
			print(text)
			bot.sendMessage(id_telegram, text, 'Markdown')
	time.sleep(10)
