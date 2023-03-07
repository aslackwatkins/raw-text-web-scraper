import re
import html5lib
import inputs as inp
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from bs4.diagnose import diagnose
from time import sleep
from random import uniform


driver = webdriver.Chrome(ChromeDriverManager().install())
actions = ActionChains(driver)

options = Options()
options.add_argument("--window-size=1920,1200")


current_page = inp.FIRST_PAGE
num_of_pages = inp.TOTAL_PAGES
url = inp.URL
target_class = inp.TARGET_CLASS
href_link_beginning = inp.HREF_BEGINNING
final_values = []


driver.get(url)

while current_page <= num_of_pages:
  sleep(round(uniform(10,20,),5))
  driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
  soup = BeautifulSoup(driver.page_source, "html5lib")
  target_data = soup.select(f"[class='{target_class}']")


  output_values = [target.text for target in target_data]


  for value in output_values:
    if "k" in value:
      if "." in value:
        item_len = len(value)
        dot_index = value.index(".")
        decimals = (item_len - 2) - dot_index
        final_values.append( value[0:dot_index] + value[dot_index + 1:item_len - 1] + ("0" * (3 - decimals)))
      else:
        final_values.append( value[0:dot_index] + value[dot_index + 1:item_len - 1] + ("000"))
    else:
      final_values.append(value)

  driver.find_element(By.CSS_SELECTOR, f"a[href='{href_link_beginning}{current_page + 1}']")
  actions.click()
  driver.get(url + f"{current_page + 1}")
  driver.execute_script("window.scrollTo(document.body.scrollHeight, 0);")
  current_page += 1


driver.quit()

with open("text.txt", "w") as f:
  for value in final_values:
    f.write(value + "\n")
  f.close()