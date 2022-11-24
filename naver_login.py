from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def naver_login(driver):
    chromedriver_file = './chromedriver'
    driver.get("https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com")

    id = "yourid"
    pw = "yourpw"

    WebDriverWait(driver,timeout=5).until(EC.presence_of_element_located((By.TAG_NAME, "button")))

    driver.execute_script(f"document.getElementsByName('id')[0].value='{id}'")  
    driver.execute_script(f"document.getElementsByName('pw')[0].value='{pw}'")  
    driver.find_elements(By.TAG_NAME,'button')[1].click()

    return driver