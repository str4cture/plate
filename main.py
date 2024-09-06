import pyautogui
import time
import webbrowser
import sys
import requests
from bs4 import BeautifulSoup

# open ny dmv
webbrowser.open('https://transact3.dmv.ny.gov/platespersonalized/')
time.sleep(5)  # wait for ny dmv to load

pyautogui.click(383, 1017)  # click on the passenger button (adjust coordinates if needed)

# need to scroll down however amount

pyautogui.scroll(-5)

# this clicks the box to enter your desired plate
pyautogui.click(445, 992)

# this deletes whatever was there beforehand
pyautogui.hotkey('command', 'a')
pyautogui.hotkey('command', 'x')

def write_licenseplate(request):

    pyautogui.write(request)
    pyautogui.press('enter')

def read_plates_from_file(file_path):
    # read lines from the specified file
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines

def main():
    # path to the text file
    file_path = 'plate.txt'

    # read lines from the file
    lines = read_plates_from_file(file_path)

    # check if there is at least one line in the file
    if lines:
        # get the first line and strip any leading/trailing whitespace
        first_plate = lines[0].strip()
        
        # write the license plate and press Enter
        write_licenseplate(first_plate)
    else:
        print("No plates found in the file.")

def check_plate(plate):
    url = 'https://transact3.dmv.ny.gov/platespersonalized/'
    #form_data = {
      #  'plate': plate,
       # 'passenger': 'on',  # Adjust form field names based on actual form fields
   # }
    
    # Simulate form submission
    response = requests.get(url)
    #soup = BeautifulSoup(response.text, 'html.parser')
    
    # Check if the response indicates availability
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
