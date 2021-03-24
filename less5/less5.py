from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()

driver.get('https://gb.ru/login')

elem = driver.find_element_by_id('user_email')
elem.send_keys('study.ai_172@mail.ru')

elem = driver.find_element_by_id('user_password')
elem.send_keys('Password172')

elem.send_keys(Keys.ENTER)

profile = driver.find_element_by_class_name('avatar')
driver.get(profile.get_attribute('href'))

profile = driver.find_element_by_class_name('text-sm')
a = driver.get(profile.get_attribute('href'))

gender = driver.find_element_by_name('user[gender]')
options = gender.find_elements_by_tag_name('option')

for option in options:
    if option.text == 'Женский':
        option.click()

gender.submit()
driver.quit()
