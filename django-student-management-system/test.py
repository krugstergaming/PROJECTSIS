import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

chromedriver_path = os.getenv('CHROMEDRIVER')

options = Options()
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')


service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

try:

    url = 'http://127.0.0.1:8000/'
    driver.get(url)

    try:
        print("Login form found, proceeding with login...")

        driver.find_element(By.ID, 'email').send_keys('admin@gmail.com')
        driver.find_element(By.ID, 'password').send_keys('admin')
        driver.find_element(By.CLASS_NAME, 'login-btn').click()

        print("Login successful!")

        driver.implicitly_wait(5)

        faculty_management_url = '/manage_staff/'
        driver.find_element(By.CSS_SELECTOR, f"a[href='{faculty_management_url}']").click()

        print("Navigated to Faculty Management.")

        driver.implicitly_wait(5)

        faculty_table = driver.find_element(By.XPATH, "//table[@class='table table-hover text-nowrap']")

        rows = faculty_table.find_elements(By.XPATH, ".//tbody/tr")

        print("\nFaculty Data:")
        for row in rows:
            name = row.find_element(By.XPATH, ".//td[1]").text
            username = row.find_element(By.XPATH, ".//td[2]").text
            email = row.find_element(By.XPATH, ".//td[3]").text

            print(f"Name: {name}, Username: {username}, Email: {email}")

        driver.implicitly_wait(5)

        dropdown_menu = driver.find_element(By.ID, 'menu_dropdown')
        ActionChains(driver).move_to_element(dropdown_menu).click().perform()

        # Find the logout link by its ID and click it
        logout_link = driver.find_element(By.ID, 'logout_user')
        logout_link.click()

        driver.implicitly_wait(5) 
        
        print("Logged out successfully.")

    except Exception as e:
        print(f"Failure: An error occurred while autotesting. Error: {e}")

except Exception as e:
    print(f"Failure: An error occurred while accessing the URL - {e}")

finally:
    # Quit the driver
    driver.quit()
