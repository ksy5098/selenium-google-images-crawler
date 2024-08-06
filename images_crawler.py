from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import urllib.request
import os
import time

# Selenium WebDriver setup
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://www.google.co.kr/imghp?hl=ko&ogbl")

# Get search query and number of images to download
search_query = input("Enter search term: ")
num_images_to_download = int(input("Enter number of images to download: "))

# Enter search query and execute search
input_element = driver.find_element(By.CLASS_NAME, "gLFyf")
input_element.send_keys(search_query + Keys.ENTER)

# Scroll down
elem = driver.find_element(By.TAG_NAME, 'body')
for i in range(60):
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.1)

# Click 'Show more results' button (if available)
try:
    view_more_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'mye4qd')))
    view_more_button.click()
    for i in range(80):
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.1)
except:
    pass

# Create folder based on search query
download_path = os.path.join(os.getcwd(), search_query)  # Create search query folder in current working directory
os.makedirs(download_path, exist_ok=True)

# Collect image links
thumbnails = driver.find_elements(By.CLASS_NAME, "F0uyec")
print(thumbnails)
print('Total number of downloadable images:', len(thumbnails))

# Download images
downloaded_count = 0
for index, thumbnail in enumerate(thumbnails):
    if downloaded_count >= num_images_to_download:
        break

    try:
        # Click thumbnail
        driver.execute_script("arguments[0].click();", thumbnail)

        # Wait for high-resolution image to load
        high_res_image = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "sFlh5c.pT0Scc.iPVvYb"))
        )

        # Get src attribute of high-resolution image
        high_res_src = high_res_image.get_attribute('src')

        # Download image
        if high_res_src and "http" in high_res_src:
            filepath = os.path.join(download_path, f'{search_query} image_{downloaded_count + 1}.jpg')
            urllib.request.urlretrieve(high_res_src, filepath)
            downloaded_count += 1
            print(f'Image {downloaded_count} downloaded successfully')

    # Handle exception if image download fails
    except Exception as e:
        print(f'Image {index + 1} download failed: {e}')
        continue

print(f'Successfully downloaded {downloaded_count} images.')
 
# Close driver
driver.quit()