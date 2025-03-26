from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from scrappers.constants import CHROME_PATH
from .constants import (
    F1_BASE_URL,
    DRIVERS_TABLE_ENDPOINT,
    TEAMS_TABLE_ENDPOINT
)


def get_drivers_standings(driver):
    # TODO: to turn this function independent from others or the __main__
    F1_DRIVER_URL = F1_BASE_URL + DRIVERS_TABLE_ENDPOINT
    driver.get(F1_DRIVER_URL)
    # TODO: Use "WebDriverWait" and "Expected Conditions" instead of a hardcoded sleep
    sleep(8)

    table = driver.find_element(By.CLASS_NAME, "f1-table")
    rows = table.find_elements(By.TAG_NAME, "tr")

    driver_data = []
    for row in rows:
        columns = row.find_elements(By.TAG_NAME, "td")
        if len(columns) > 1:
            position = columns[0].text.strip()
            driver_name = columns[1].text.strip()
            # nationality = columns[2].text.strip()  # Not using this atm
            team = columns[3].text.strip()
            points = columns[4].text.strip()

            driver_data.append(
                {
                    "position": position,
                    "driver_name": driver_name,
                    "team": team,
                    "points": points
                }
            )
    return driver_data


def get_team_standings(driver):
    # TODO: to turn this function independent from others or the __main__
    F1_TEAM_URL = F1_BASE_URL + TEAMS_TABLE_ENDPOINT
    driver.get(F1_TEAM_URL)
    # TODO: Use "WebDriverWait" and "Expected Conditions" instead of a hardcoded sleep
    sleep(8)

    table = driver.find_element(By.CLASS_NAME, "f1-table")
    rows = table.find_elements(By.TAG_NAME, "tr")

    team_data = []
    for row in rows:
        columns = row.find_elements(By.TAG_NAME, "td")
        if len(columns) > 1:
            position = columns[0].text.strip()
            team = columns[1].text.strip()
            points = columns[2].text.strip()

            team_data.append(
                {
                    "position": position,
                    "team": team,
                    "points": points
                }
            )

    return team_data


def run_it_all():

    driver_standings = []
    team_standings = []

    service = Service(CHROME_PATH)
    driver = webdriver.Chrome(service=service)
    try:
        driver_standings = get_drivers_standings(driver)
        team_standings = get_team_standings(driver)

    finally:
        driver.quit()


    print("DRIVER'S CHAMPIONSHIP TABLE")
    for driver_row in driver_standings:
        print(driver_row)


    print("TEAM'S CHAMPIONSHIP TABLE")
    for team_row in team_standings:
        print(team_row)
