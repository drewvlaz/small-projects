''' A script to check cars available for purchase '''

import smtplib
import ssl
import time

from bs4 import BeautifulSoup, re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from secrets import (
    URL,
    SENDER_EMAIL,
    SENDER_EMAIL_PASS,
    RECEIVER_EMAIL
)

class Car:
    def __init__(self, source):
        self.source = source

    def parse(self):
        soup = BeautifulSoup(self.source, 'html.parser')

        self.name = soup.find('h2').string
        raw_price = str(soup.find('h3'))
        loc = raw_price.index('$')
        self.price = raw_price[loc:loc+7]
        self.distance = soup.find('span', text=re.compile('mi\)')).string

    def get_info(self):
        return f"{self.name} for {self.price} at {self.distance}"

def launch():
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.get(URL)

    return driver

def send_email(subject, content, recipient):
    port = 465
    smtp_server = "smtp.gmail.com"
    message = f"Subject: {subject}\n\n{content}\nClick here to view: {URL}"

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(SENDER_EMAIL, SENDER_EMAIL_PASS)
        server.sendmail(SENDER_EMAIL, recipient, message)

def main():
    driver = launch()
    # Accept cookies
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, '_evidon-decline-button'))
    )
    cookie_accept = driver.find_element(By.ID, '_evidon-decline-button')
    cookie_accept.click()

    # Adjust radius of search
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'dropdown__icon'))
    )
    radius = driver.find_element(By.CLASS_NAME, 'dropdown__list')
    driver.execute_script("arguments[0].setAttribute('style','')", radius)
    driver.find_elements(By.CLASS_NAME, 'dropdown__list-item')[3].click()
    # Wait for new results to load
    time.sleep(30)

    # Find matches
    num_of_matches = int(driver.find_element(By.CLASS_NAME, 'inventory-results__content__heading').get_attribute('innerHTML').strip()[1])
    matches = driver.find_elements(By.CLASS_NAME, 'inventory-tile')

    # Create car objects to keep track of
    cars = []
    for i in range(num_of_matches):
        cars.append(Car(matches[i].get_attribute('innerHTML')))
        cars[i].parse()

    # Write to file or compare to old
    try:
        with open("cars.txt", "x") as f:
            for car in cars:
                f.write(car.get_info() + "\n")

    except FileExistsError:
        with open("cars.txt", "r+") as f:
            prev_cars = f.read()

            for car in cars:
                if car.get_info() not in prev_cars:
                    send_email("Car Update", car.get_info(), RECEIVER_EMAIL)

    # Write any updates
    with open("cars.txt", "w") as f:
        car_content = ""
        for car in cars:
            car_content += car.get_info() + "\n"

        f.write(car_content.strip())
        send_email("Working", car_content, "314dsv@gmail.com")

    driver.close()

main()
