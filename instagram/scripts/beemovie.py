import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def launch():
    driver = webdriver.Chrome(executable_path="./resources/chromedriver_linux")
    driver.get("https://www.instagram.com/")

    return driver


driver = launch()


def locate(location):
    return WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(location)
    )


def main():
    with open("./resources/credentials.json") as f:
        credentials = json.load(f)

    # Login
    username = locate((By.NAME, "username"))
    password = locate((By.NAME, "password"))
    username.send_keys(credentials["username"])
    password.send_keys(credentials["password"] + "\n")

    # Dismiss notifications
    notifications = locate(
        (By.XPATH, "/html/body/div[4]/div/div/div[3]/button[2]"))
    notifications.click()

    # Navigate to dms
    dms = locate((By.CLASS_NAME, "xWeGp"))
    dms.click()

    # Search for user
    search = locate(
        (By.XPATH, "/html/body/div[1]/section/div/div[2]/div/div/div[1]/div[1]/div/div[3]/button"))
    search.click()
    query = locate((By.NAME, "queryBox"))
    query.send_keys("deanmyster18\n")
    user = locate(
        (By.XPATH, "/html/body/div[4]/div/div[2]/div[2]/div/div/div[3]/button"))
    user.click()
    select = locate(
        (By.XPATH, "/html/body/div[4]/div/div[1]/div/div[2]/div/button"))
    select.click()

    # Read in script
    file = open("./resources/beemoviescript.txt")
    script = file.read().split(" ")

    # Send message
    message_box = locate(
        (By.XPATH, "/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea"))
    message_box.send_keys("The Bee Movie: One glorious word at a time!\n")
    message_box.send_keys("Sit back, relax, and enjoy the show!\n")

    for word in script:
        message_box.send_keys(word + "\n")


main()
