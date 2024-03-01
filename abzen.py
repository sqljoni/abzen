from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import time


def load_env_variables(env_file=".env"):
    """Load variables from .env file."""
    with open(env_file, "r") as file:
        for line in file:
            # Ignore lines starting with '#' (comments) and empty lines
            if line.strip() and not line.strip().startswith("#"):
                key, value = line.strip().split("=")
                os.environ[key.strip()] = value.strip()


def login(driver, username, password):
    driver.get("https://akademik.polban.ac.id/")
    # driver.maximize_window()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="fm"]/div[1]/input'))
    ).send_keys(username)
    driver.find_element(By.XPATH, '//*[@id="fm"]/div[2]/input').send_keys(password)
    driver.find_element(By.XPATH, '//*[@id="fm"]/div[3]/div[2]/button').click()

    try:
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()
    except TimeoutException:
        print("No alert found within the specified timeout period.")
    except Exception as e:
        print("An error occurred:", str(e))


def absen(driver):
    driver.get("https://akademik.polban.ac.id/ajar/absen")
    temp = driver.find_elements(By.CLASS_NAME, "simpan_awal")
    if len(temp) == 0:
        print("sudah absen")
    else:
        for i in range(len(temp)):
            temp[i].click()


if __name__ == "__main__":
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--start-minimized")
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)

    load_env_variables()
    username = os.environ.get("USERNAME")
    password = os.environ.get("PASS")

    try:
        login(driver, username, password)
    except Exception as e:
        print(f"Failed to login: {str(e)}")
        driver.quit()
        exit()

    try:
        while True:
            absen(driver)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Process interrupted by user")
    finally:
        driver.quit()
