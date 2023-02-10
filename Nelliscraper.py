import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from items import Items, Item
from jinja2 import Environment, FileSystemLoader

chromeOptions = Options()
chromeOptions.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2}) 
chromeOptions.add_argument("--no-sandbox") 
chromeOptions.add_argument("--disable-setuid-sandbox") 

chromeOptions.add_argument("--window-size=1920,1080")
chromeOptions.add_argument("--start-maximized")
# chromeOptions.add_argument("--headless")  # this
chromeOptions.add_argument("--remote-debugging-port=9222")  # this

chromeOptions.add_argument("--disable-dev-shm-using") 
chromeOptions.add_argument("--disable-extensions") 
chromeOptions.add_argument("--disable-gpu") 


environment = Environment(loader=FileSystemLoader("templates/"))
template = environment.get_template("results.html")


driver = webdriver.Chrome(options=chromeOptions)
driver.get("https://www.nellisauction.com")

loc = driver.find_element(By.XPATH, "//*[name()='svg' and @data-testid='ExpandMoreIcon']")

loc.click()
loc = driver.find_element(By.XPATH, "//button[@id='shopping-location-option-2']")
loc.click()

time.sleep(1)

loc = driver.find_elements(By.XPATH, "//button[@type='submit']")
loc[0].click()

all_items = Items()

search_terms = ['3d printer', 'cnc', 'shop vac', 'router', 'espresso machine']
for search in search_terms:
    search_input = driver.find_element(By.TAG_NAME, "input")
    search_input.send_keys(Keys.COMMAND + "a")
    search_input.send_keys(Keys.DELETE)
    search_input.send_keys(search)
    
    loc = driver.find_elements(By.XPATH, "//button[@type='submit']")
    loc[0].click()

    time.sleep(1)
    search_count = driver.find_element(By.CLASS_NAME, "__search-results-description")
    tx = search_count.find_element(By.TAG_NAME, "span").text

    count = re.findall(r'\d+', tx)[0]
    if int(count) > 500:
        continue
    items = driver.find_elements(By.CLASS_NAME, "__product-card-layout-container")
    for item in items:
        title = item.find_element(By.CLASS_NAME, "__product-card-title").text
        location = item.find_element(By.CLASS_NAME, "__product-card-header-location-container").text
        retail = item.find_element(By.CLASS_NAME, "__product-card-auction-detail-content").text
        price = item.find_element(By.CLASS_NAME, "__product-card-price-and-bid-count-price").text
        bid = item.find_element(By.CLASS_NAME, "__product-card-price-and-bid-count-bid-count").text
        time_left = item.find_element(By.CLASS_NAME, "__product-card-time-label-container").text
        img_cont = item.find_element(By.CLASS_NAME, "__product-card-image-container")
        link = item.find_element(By.TAG_NAME, "a")
        url = link.get_attribute('href')
        link = item.find_element(By.TAG_NAME, "img")
        img_url = link.get_attribute('src')
        all_items.add_item(search, Item(title, retail, location, price, bid, time_left, url, img_url ))


        # print(f"Price {price_and_bid[0].text} Bids {price_and_bid[1].text}")

    # for item in all_items.items:
        # print(item)

content = template.render(
        items=all_items.items
    )

with open("output.html", mode="w", encoding="utf-8") as results:
    results.write(content)
# In[ ]:




