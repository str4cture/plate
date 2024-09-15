import time
import sys
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

chrome_driver_path = r'C:\Users\dany\Downloads\silly\chromedriver-win64\chromedriver.exe' 


service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)


driver.get('https://transact3.dmv.ny.gov/platespersonalized/')
time.sleep(25) 


wait = WebDriverWait(driver, 10)
passenger_button = wait.until(EC.element_to_be_clickable((By.ID, 'passenger'))) 
passenger_button.click()

driver.execute_script("window.scrollBy(0, 500);")
time.sleep(2)

plate_input_box = driver.find_element(By.NAME, 'plateText') 
plate_input_box.clear()

def write_licenseplate(plate):
    plate_input_box.send_keys(plate)
    plate_input_box.send_keys(Keys.RETURN)

# Read plates from the file
def read_plates_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines

def main():
    file_path = 'plate.txt'

    lines = read_plates_from_file(file_path)

    if lines:
    
        first_plate = lines[0].strip()

        write_licenseplate(first_plate)
    else:
        print("No plates found in the file.")

def check_plate(plate):
    url = 'https://transact3.dmv.ny.gov/platespersonalized/'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    if 'emppasplatedisplay' in response.url or 'available' in soup.text.lower():
        return True
    else:
        return False

if __name__ == "__main__":
    if sys.platform == "win32":
        import os
        os.system("danyal's plate checker for nys")

    with open('plate.txt') as f:
        plates = [line.rstrip() for line in f]

    available_plates = []
    for plate in plates:
        if check_plate(plate):
            available_plates.append(plate)
            print(f"The plate '{plate}' is available.")
            with open('available_plate.txt', 'a') as f:
                f.write(plate + '\n')
        else:
            print(f"The plate '{plate}' is not available.")

    main()

    driver.quit()
