# import os
# import pika
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# os.environ['PATH'] += r"C:\Users\davide\Downloads\chromedriver_win32"

# DOWNLOAD chromedriver
# https://chromedriver.chromium.org/downloads

wallbox_account = "xxxxxxxxxx@gmail.com"
wallbox_password = "xxxxxxxxxx"
mqtt_topic = "allarmi"
mqtt_hostname = "192.168.0.2"


def riavvia_wallbox():
    try:
        driver_Wallbox = webdriver.Chrome()
        driver_Wallbox.get("https://my.wallbox.com/chargers/210204")
        driver_Wallbox.implicitly_wait(4)
        # Accedi btn
        driver_Wallbox.find_element(By.CLASS_NAME, "login-button").click()
        # Nome
        driver_Wallbox.find_element(By.CLASS_NAME, "input").send_keys(wallbox_account)

        time.sleep(2)
        # Continue btn
        driver_Wallbox.find_element(By.CLASS_NAME, "button").click()
        time.sleep(2)
        #
        # Password
        p2 = driver_Wallbox.find_element(By.CLASS_NAME, "input")
        p2.send_keys(wallbox_password)
        time.sleep(2)
        # Continue btn
        driver_Wallbox.find_element(By.CLASS_NAME, "button").click()
        driver_Wallbox.get("https://my.wallbox.com/chargers/210204")
        # restart_button
        restart_button = driver_Wallbox.find_element(By.CLASS_NAME, "button")
        # print(restart_button.text)
        restart_button.click()
        time.sleep(2)

        confirm_button = driver_Wallbox.find_element(By.CLASS_NAME, "is-primary")
        confirm_button.click()
        driver_Wallbox.quit()
        pubblica("riavvia_wallbox")
    except e:
        pubblica("errore riavvia_wallbox")


def pubblica(valore):
    try:
        publish.single(topic=mqtt_topic, payload=valore, qos=0, retain=False, hostname=mqtt_hostname,
                       port=1883, client_id="red-", keepalive=60, will=None,
                       tls=None, protocol=mqtt.MQTTv311, transport="tcp")
        print(valore)
    except e:
        print("ERRORE in pubblica")


while True:
    try:
        riavvia_wallbox()
        time.sleep(120)
    except e:
        print("ERRORE in loop")
