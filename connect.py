from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os, time

BASE_DIR = os.path.dirname(__file__)
ITENS_FILE = os.path.join(BASE_DIR, "itens.txt")

def read_itens(file_path):
	with open(file_path, 'r') as f:
		file_text = f.read()

	itens_list = file_text.split("\n")
	return itens_list

def search_item(item, browser):
	#time.sleep(1)
	#Find the Search textbox
	search_element = browser.find_element_by_css_selector("input[name='field-keywords']")
	#Clean the query
	search_element.send_keys(Keys.CONTROL, 'a')
	search_element.send_keys(Keys.BACKSPACE)
	#Search for something
	search_element.send_keys(item)

	#Find the Search button
	time.sleep(1)
	search_btn_element = browser.find_element_by_css_selector("input[type='submit']")
	search_btn_element.click()


if __name__ == "__main__":
	to_search_itens_list = read_itens(ITENS_FILE)

	browser = webdriver.Chrome()

	url = "https://www.amazon.com.br/"
	browser.get(url)

	for to_search_item in to_search_itens_list:
	#to_search_item = to_search_itens_list[1]
		search_item(to_search_item, browser)
		
		common_itens = browser.find_elements_by_css_selector("div[class='sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20']")
		sponsored_itens = browser.find_elements_by_css_selector("div[class='sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 AdHolder sg-col s-widget-spacing-small sg-col-4-of-20']") 

		itens = sponsored_itens + common_itens

		prices = []
		names = []
		for item in itens[:4]:
			text = item.text
			coin_index = text.find('R$')
			if coin_index != -1:
				prices.append(float(text[coin_index+2:coin_index+6].replace('\n','.')))
			else:
				prices.append('out of stock')

			name_index = text.find('\n')
			name = text[:name_index]
			if name == 'Patrocinados':
				new_name_index = text.find('\n',name_index+1)
				name = text[name_index+1:new_name_index]
			names.append(name)

		for i,n in enumerate(names):
			print(n)
			print(prices[i])
			print('-----------')

