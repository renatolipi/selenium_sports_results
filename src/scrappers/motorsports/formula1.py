from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from scrappers.constants import CHROME_PATH
from .constants import (
    F1_BASE_URL,
    DRIVERS_TABLE_ENDPOINT,
    TEAMS_TABLE_ENDPOINT
)


def get_drivers_standings(driver, wait):
    F1_DRIVER_URL = F1_BASE_URL + DRIVERS_TABLE_ENDPOINT
    driver.get(F1_DRIVER_URL)

    try:
        wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".f1-table tr"))
        )

        table = driver.find_element(By.CLASS_NAME, "f1-table")
        rows = table.find_elements(By.TAG_NAME, "tr")

        driver_data = []
        for row in rows:
            columns = row.find_elements(By.TAG_NAME, "td")
            if len(columns) == 5:
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
    except Exception as err:
        print(f"Error occurred while getting driver standings: {err}")
        return []


def get_team_standings(driver, wait):
    F1_TEAM_URL = F1_BASE_URL + TEAMS_TABLE_ENDPOINT
    driver.get(F1_TEAM_URL)

    try:
        wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".f1-table tr"))
        )

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
    except Exception as err:
        print(f"Error occurred while getting team standings: {err}")
        return []


def retrieve_tables(drivers, teams):

    driver_standings = []
    team_standings = []

    service = Service(CHROME_PATH)
    driver = webdriver.Chrome(service=service)

    wait = WebDriverWait(driver, 10)

    # NOTE: Below, we could run them both in parallel using "concurrent.futures"
    # but I'm going to use it earlier, when I have more sports to scrap
    try:
        if drivers:
            driver_standings = get_drivers_standings(driver, wait)
        if teams:
            team_standings = get_team_standings(driver, wait)

    finally:
        driver.quit()


    if drivers:
        print("DRIVER'S CHAMPIONSHIP TABLE")
        for driver_row in driver_standings:
            print(driver_row)

    if teams:
        print("TEAM'S CHAMPIONSHIP TABLE")
        for team_row in team_standings:
            print(team_row)
