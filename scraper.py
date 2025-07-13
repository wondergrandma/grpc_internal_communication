from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

url = "https://www.themoviedb.org/"

driver = webdriver.Chrome()

driver.get(url)
wait = WebDriverWait(driver, 10)


search = driver.find_element(By.ID, "inner_search_v4")
search.send_keys("Blade runner 2049")
search.send_keys(Keys.RETURN)
cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.card.v4.tight')))

cards[0].find_element(By.TAG_NAME, "a").click()

film_title = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="original_header"]/div[2]/section/div[1]/h2/a')))
film_make_year = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="original_header"]/div[2]/section/div[1]/div/span[2]')))
age_restriction = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="original_header"]/div[2]/section/div[1]/div/span[1]')))
length = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="original_header"]/div[2]/section/div[1]/div/span[4]')))
overview = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="original_header"]/div[2]/section/div[3]/div/p')))


print(film_title.text)
print(film_make_year.text)
print(age_restriction.text)
print(length.text)
print(overview.text)

#for card in cards:
#   element = card.find_element(By.TAG_NAME, "h2")




driver.quit()