from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.webdriver.support.wait as wait
from selenium.webdriver.support.ui import Select
import sys
import os
#import undetected_chromedriver as uc
import time
from dotenv import load_dotenv


load_dotenv()
URL='https://login.sofi.com/u/login?state=hKFo2SBiMkxuWUxGckdxdVJ0c3BKLTlBdEk1dFgwQnZCcWo0ZKFur3VuaXZlcnNhbC1sb2dpbqN0aWTZIHdDekRxWk81cURTYWVZOVJleEJORE9vMExBVFVjMEw2o2NpZNkgNkxuc0xDc2ZGRUVMbDlTQzBDaWNPdkdlb2JvZXFab2I'
USERNAME=os.getenv('USER')
PASSWORD=os.getenv('PASSWORD')
print("USERNAME:", USERNAME, "PASSWORD:",PASSWORD)

chrome_options = Options()
#chrome_options.add_argument("--headless")
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument('--disable-notifications')
chrome_options.add_argument('--disable-popup-blocking')
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")



driver = webdriver.Chrome(options=chrome_options)
driver.get(URL)

def login():
    # Wait for the username field and enter the username
    username_field = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='username']")))
    username_field.send_keys(USERNAME)

    # Wait for the password field and enter the password
    password_field = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='password']")))
    password_field.send_keys(PASSWORD)


    login_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='widget_block']/div/div[2]/div/div/main/section/div/div/div/form/div[2]/button")))
    login_button.click()

    print("---------------------------------\n")
    code2fa=input('Please enter code and press ENTER to continue:')
    code_field = WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='code']")))
    code_field.send_keys(code2fa)



    code_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='widget_block']/div/div[2]/div/div/main/section/div/div/div/div[1]/div/form/div[3]/button")))
    code_button.click()

def investmentPage():

    investment_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='root']/div/header/nav/div[2]/a[4]")))
    investment_button.click()
def submittingOrders(ORDER, QUANTITY, TICKER, DRY):

    search_field = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='page-wrap']/div[1]/div/div/div/div/input")))
    search_field.send_keys(TICKER)
   
    WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id='page-wrap']/div[1]/div/div/div/ul/li")))
    dropdown_items = driver.find_elements(By.XPATH, "//*[@id='page-wrap']/div[1]/div/div/div/ul/li")
    total_items = len(dropdown_items)
    if total_items == 0:
        print("No stock found")
        return
    else:
        found_stock = False
        for item in dropdown_items:
            ticker_name = item.find_element(By.XPATH, "./a/div/p[1]").text
            if ticker_name == TICKER:
                found_stock = True
                item.click()
                Ordering(ORDER, QUANTITY, TICKER, DRY)
                break

        if not found_stock:
            print("SOFI DOESN'T HAVE THIS STOCK")
            return


def Ordering(ORDER, QUANTITY, TICKER, DRY):
    print("order")
    time.sleep(5)
    WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "SpanDollars-cAYUlQ")))
    dollars = driver.find_element(By.CLASS_NAME, "SpanDollars-cAYUlQ").text
    print("dollars", dollars)
    cents = driver.find_element(By.CLASS_NAME, "SpanCents-bUjKSs").text
    print("cents", cents)
    live_price = f"{dollars}.{cents}"
    if ORDER == "BUY":
        

        buy_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='mainContent']/div[2]/div[2]/div[2]/div[2]/div/button[1]")))
        buy_button.click()

        accounts_dropdown = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.NAME, "account")))
    
        select=Select(accounts_dropdown)
        #print("select", select)
        Options=select.options
        #print("options", Options)
        Options_length=len(Options)
        for index in range(Options_length):
            select = Select(WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located((By.NAME, "account"))))
            select.select_by_index(index)
            print("Selected account index:", index)
            time.sleep(3)
            quant=WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.NAME, "shares")))
            quant.send_keys(QUANTITY)

            limit_price=WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.NAME, "value")))
            limit_price.send_keys(str(float(live_price) + 0.01))
            time.sleep(3)

            
            review_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='mainContent']/div[2]/div[2]/div[3]/div/div[8]/button")))
            review_button.click()
           
            if(DRY=='FALSE'):
                submit_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='mainContent']/div[2]/div[2]/div[3]/div/div[4]/button[1]")))
                submit_button.click()
                print("LIVE MODE")
                done=WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='mainContent']/div[2]/div[2]/div[3]/div/div[2]/button")))
                done.click()
                print("Submitting order BUY for", QUANTITY, "shares of", TICKER, "at", str(float(live_price) + 0.01))
                index+=1
            elif(DRY=='TRUE'):
                
                print("testing before back")
                time.sleep(5)
                back_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='mainContent']/div[2]/div[2]/div[3]/div/div[4]/button[2]")))
                back_button.click()
                time.sleep(3)
                print("DRY MODE")
                print("Submitting order BUY for", QUANTITY, "shares of", TICKER, "at", str(float(live_price) + 0.01))
                index+=1

    elif ORDER == "SELL":

        sell = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='mainContent']/div[2]/div[2]/div[2]/div[2]/div/button[2]")))
        sell.click()
  
        accounts_dropdown = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.NAME, "account")))
      
        select=Select(accounts_dropdown)
        print("select", select)
        Options=select.options
        print("options", Options)
        Options_length=len(Options)
       

        for index in range(Options_length):
            select = Select(WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located((By.NAME, "account"))))
            select.select_by_index(index)
            #print("Selected account index:", index)
            time.sleep(3)
            quant=WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.NAME, "shares")))
            quant.send_keys(QUANTITY)

            limit_price=WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.NAME, "value")))
            limit_price.send_keys(str(float(live_price) + 0.01))
            time.sleep(3)

            
            review_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='mainContent']/div[2]/div[2]/div[3]/div/div[8]/button")))
            review_button.click()
           
            if(DRY=='FALSE'):
                submit_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='mainContent']/div[2]/div[2]/div[3]/div/div[4]/button[1]")))
                submit_button.click()
                print("LIVE MODE")
                done=WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='mainContent']/div[2]/div[2]/div[3]/div/div[2]/button")))
                done.click()
                print("Submitting order SELL for", QUANTITY, "shares of", TICKER, "at", str(float(live_price) + 0.01))
                index+=1
            elif(DRY=='TRUE'):
                
                print("testing before back")
                time.sleep(5)
                back_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='mainContent']/div[2]/div[2]/div[3]/div/div[4]/button[2]")))
                back_button.click()
                time.sleep(3)
                print("DRY MODE")
                print("Submitting order SELL for", QUANTITY, "shares of", TICKER, "at", str(float(live_price) + 0.01))
                index+=1

            
if __name__ == "__main__":
    if(len(sys.argv) < 5):
        print("Usage: python main.py <order> <quantity> <ticker> <dry>")
        sys.exit(1)
    ORDER=sys.argv[1]
    QUANTITY=sys.argv[2]
    TICKER=sys.argv[3]
    DRY=sys.argv[4]
    if DRY == "True" or 'TRUE' or 'true' or 'T' or 't':
        DRY = 'TRUE'
    elif DRY == "False" or 'FALSE' or 'false' or 'F' or 'f':
        DRY = 'FALSE'
    else:
        print("Invalid DRY MODE")
        sys.exit(1)
    print("ORDER:", ORDER, "QUANTITY:", QUANTITY, "TICKER:", TICKER, "DRY:", DRY)
    login()
    investmentPage()
    #accounts=get_accounts()
    submittingOrders(ORDER.upper(), QUANTITY, TICKER, DRY)
    driver.quit()
 


