from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.webdriver.support.wait as wait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException

import sys
import os
#import undetected_chromedriver as uc
import time
from dotenv import load_dotenv


load_dotenv()
URL='https://login.sofi.com/u/login?state=hKFo2SBiMkxuWUxGckdxdVJ0c3BKLTlBdEk1dFgwQnZCcWo0ZKFur3VuaXZlcnNhbC1sb2dpbqN0aWTZIHdDekRxWk81cURTYWVZOVJleEJORE9vMExBVFVjMEw2o2NpZNkgNkxuc0xDc2ZGRUVMbDlTQzBDaWNPdkdlb2JvZXFab2I'
USERNAME=os.getenv('USER')
PASSWORD=os.getenv('PASSWORD')

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
def submittingOrders(ORDER, QUANTITY, TICKERS, DRY):
    for TICKER in TICKERS:
        #//*[@id="mainContent"]/div[2]/div[2]/div[2]/div[1]/div/div/div/input
        try:
            search_field = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='page-wrap']/div[1]/div/div/div/div/input")))
            search_field.send_keys(TICKER)
            WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id='page-wrap']/div[1]/div/div/div/ul/li")))
            dropdown_items = driver.find_elements(By.XPATH, "//*[@id='page-wrap']/div[1]/div/div/div/ul/li")
            total_items = len(dropdown_items)
        except TimeoutException:
            try:
                invest_search_field=WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='mainContent']/div[2]/div[2]/div[2]/div[1]/div/div/div/input")))
                invest_search_field.send_keys(TICKER)
                WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id='mainContent']/div[2]/div[2]/div[2]/div[1]/div/div/ul/li")))
                dropdown_items = driver.find_elements(By.XPATH, "//*[@id='mainContent']/div[2]/div[2]/div[2]/div[1]/div/div/ul/li")
                total_items = len(dropdown_items)
            except TimeoutException:
                print("Search field not found")
                return
        #//*[@id="mainContent"]/div[2]/div[2]/div[2]/div[1]/div/div/ul/li

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
    if ORDER == "BUY":
        clicked_values = set()  # Set to keep track of processed accounts

        while True:
            # Click the buy button
            time.sleep(5)
            buy_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='mainContent']/div[2]/div[2]/div[2]/div[2]/div/button[1]")))
            driver.execute_script("arguments[0].click();", buy_button)
            print("BUY BUTTON CLICKED")

            # Fetch the live price
            live_price = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='mainContent']/div[2]/div[2]/div[3]/div/p"))).text
            live_price = live_price.split('$')[1]
            print("LIVE PRICE:", live_price)

            # Handle account selection
            accounts_dropdown = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.NAME, "account")))
            select = Select(accounts_dropdown)

            # Find an unclicked account
            for option in select.options:
                value = option.get_attribute('value')
                if value not in clicked_values:
                    select.select_by_value(value)
                    #print("Selected account:", value)
                    clicked_values.add(value)
                    break
            else:
                print("All accounts have been processed.")
                break  # Exit the while loop if all accounts are processed

            # Input quantity and price
            print("Inputting quantity and price")
            time.sleep(5)
            quant = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.NAME, "shares")))
            quant.send_keys(QUANTITY)
            time.sleep(5)
            limit_price = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.NAME, "value")))
            limit_price.send_keys(str(float(live_price) + 0.01))

            # Review and submit the order
            review_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='mainContent']/div[2]/div[2]/div[3]/div/div[8]/button")))
            review_button.click()
            
            if DRY == 'FALSE':
                submit_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='mainContent']/div[2]/div[2]/div[3]/div/div[4]/button[1]")))
                submit_button.click()
                print("Order submitted for", QUANTITY, "shares of", TICKER, "at", str(float(live_price) + 0.01))
                
                # Confirm the order
                done_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='mainContent']/div[2]/div[2]/div[3]/div/div[2]/button")))
                done_button.click()
                print("Order completed and confirmed.")
            elif(DRY=='TRUE'):
                print("testing before back")
                time.sleep(5)
                back_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='mainContent']/div[2]/div[2]/div[3]/div/div[4]/button[2]")))
                back_button.click()
                time.sleep(3)
                print("DRY MODE")
                print("Submitting order BUY for", QUANTITY, "shares of", TICKER, "at", str(float(live_price) + 0.01))

    elif ORDER == "SELL":

        sell = WebDriverWait(driver, 50).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='mainContent']/div[2]/div[2]/div[2]/div[2]/div/button[2]")))
        sell.click()
  
        accounts_dropdown = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.NAME, "account")))
      
        select=Select(accounts_dropdown)
        #print("select", select)
        Options=select.options
        #print("options", Options)
        Options_length=len(Options)
       

        for index in range(Options_length):
            if index !=0:
                sell = WebDriverWait(driver, 50).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='mainContent']/div[2]/div[2]/div[2]/div[2]/div/button[2]")))
                sell.click()
                quant=WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.NAME, "shares")))
                quant.send_keys(QUANTITY)
                #print('Quant sent')
                #//*[@id="mainContent"]/div[2]/div[2]/div[3]/div/div[6]/button
                sell_button_INDEX = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='mainContent']/div[2]/div[2]/div[3]/div/div[6]/button")))
                sell_button_INDEX.click()
            else:
                wait=WebDriverWait(driver,10)
                wait.until(EC.presence_of_all_elements_located((By.NAME, "account")))
                select = Select(WebDriverWait(driver, 20).until(
                                EC.presence_of_element_located((By.NAME, "account"))))
                select.select_by_index(index)
                #print("Selected account index:", index)
                #time.sleep(3)
                
                quant=WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.NAME, "shares")))
                quant.send_keys(QUANTITY)
                #print('Quant sent')
                #//*[@id="mainContent"]/div[2]/div[2]/div[3]/div/div[6]/button
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='mainContent']/div[2]/div[2]/div[3]/div/div[6]/button")))
                sell_button=driver.find_element(By.XPATH, "//*[@id='mainContent']/div[2]/div[2]/div[3]/div/div[6]/button")
                driver.execute_script("arguments[0].click();", sell_button)

            #limit_price=WebDriverWait(driver, 20).until(
               # EC.element_to_be_clickable((By.NAME, "value")))
            #limit_price.send_keys(str(float(live_price) + 0.01))
            #print('Limit price sent')
            #time.sleep(3)

            
            #review_button = WebDriverWait(driver, 20).until(
                #EC.element_to_be_clickable((By.XPATH, "//*[@id='mainContent']/div[2]/div[2]/div[3]/div/div[8]/button")))
            #review_button.click()
           
            if(DRY=='FALSE'):
                #//*[@id="mainContent"]/div[2]/div[2]/div[3]/div/div[4]/button[1]
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
                #time.sleep(5)
                try:
                    # Try to find and click the back_button
                    back_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//*[@id='mainContent']/div[2]/div[2]/div[3]/div/div[4]/button[2]")))
                    back_button.click()
                except TimeoutException:
                    try:
                        # If back_button is not found, try to find and click the Out_of_market_back_button
                        Out_of_market_back_button = WebDriverWait(driver, 20).until(
                            EC.element_to_be_clickable((By.XPATH, "//*[@id='mainContent']/div[2]/div[2]/div[3]/div/div[6]/div/button[2]")))
                        Out_of_market_back_button.click()
                    except TimeoutException:
                        print("Neither button was found.")
                    #time.sleep(3)
                    print("DRY MODE")
                    print("Submitting order SELL for", QUANTITY, "shares of", TICKER, "at", str(float(live_price) + 0.01))
                    #//*[@id="mainContent"]/div[2]/div[2]/div[3]/a
                    cancel_button = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.XPATH, "//*[@id='mainContent']/div[2]/div[2]/div[3]/a")))
                    cancel_button.click()
                    index+=1

            
if __name__ == "__main__":
    if(len(sys.argv) < 5):
        print("Usage: python main.py <order> <quantity> <ticker> <dry>")
        sys.exit(1)
    ORDER=sys.argv[1]
    QUANTITY=sys.argv[2]
    TICKER=sys.argv[3].split(',')
    DRY=sys.argv[4]
    if DRY == "True" or DRY == 'TRUE' or DRY== 'true' or DRY=='T' or DRY=='t':
        DRY = 'TRUE'
        print(DRY)
    elif DRY == "False" or DRY== 'FALSE' or DRY=='false' or DRY=='F' or DRY=='f':
        DRY = 'FALSE'
        print(DRY)
    else:
        print("Invalid DRY MODE")
        sys.exit(1)
    print("ORDER:", ORDER, "QUANTITY:", QUANTITY, "TICKER:", TICKER, "DRY:", DRY)
    login()
    investmentPage()
    #accounts=get_accounts()
    submittingOrders(ORDER.upper(), QUANTITY, TICKER, DRY)
    driver.quit()
 


