''' A script to check cars available for purchase '''

import smtplib, ssl

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
    driver = webdriver.Chrome(executable_path='../resources/chromedriver')
    driver.get(URL)

    return driver

# Global variable to prevent browser from automatically closing at end of main method

def send_email(content):
    port = 465
    smtp_server = "smtp.gmail.com"
    message = f"Subject: Car Update\n\n{content}\nClick here to view: {URL}"

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(SENDER_EMAIL, SENDER_EMAIL_PASS)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message)

def main():
    driver = launch()
    # Wait for matches to load and locate them
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'inventory-tile'))
    )
    matches = driver.find_elements(By.CLASS_NAME, 'inventory-tile')

    # Create car objects to keep track of
    cars = []
    for i in range(len(matches)):
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
                    print("Diff")
                    send_email(car.get_info())

    # Write any updates
    with open("cars.txt", "w") as f:
        for car in cars:
            f.write(car.get_info() + "\n")

main()
