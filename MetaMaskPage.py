from base_element import BaseElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MetaMaskPage:
    def __init__(self, driver):
        self.driver = driver

    def get_gas_amount(self):
        spans = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span[class='currency-display-component__text']"))
        )

        gas_text = spans[0].get_attribute('textContent')
        gas = float(gas_text)

        return gas

    # this is for logging in using a pre-made profile
    def input_password(self):
        input_loc = By.CSS_SELECTOR, "input"
        input = BaseElement(
            driver=self.driver, by=input_loc[0], value=input_loc[1]
        )

        input.send_keys("DogDog214")

        unlock_btn_loc = By.XPATH, "//button[text()='Unlock']"
        unlock_btn = BaseElement(
            driver=self.driver, by=unlock_btn_loc[0], value=unlock_btn_loc[1]
        )

        unlock_btn.click()

    # check
    def reject(self):
        reject_btn_loc = By.XPATH, "//button[text()='Reject']"
        reject_btn = BaseElement(
            driver=self.driver, by=reject_btn_loc[0], value=reject_btn_loc[1]
        )

        reject_btn.click()

    def switch_account(self, account_name):
        account_name = "\'" + account_name + "\'"
        acct_menu_loc = (By.CSS_SELECTOR, "div[class='account-menu__icon']")
        acct_loc = (By.XPATH, "//div[text()=" + account_name + "]")

        acct_menu = BaseElement(
            driver=self.driver, by=acct_menu_loc[0], value=acct_menu_loc[1]
        )

        # click the account menu drop down
        acct_menu.click()

        acct = BaseElement(
            driver=self.driver, by=acct_loc[0], value=acct_loc[1]
        )

        # click on the chosen account, we will choose it by text
        acct.click()

    def switch_chain(self, chain_name):
        chain_name = "\'" + chain_name + "\'"

        networks_btn_loc = By.CSS_SELECTOR, "div[class='network-display network-display--clickable chip chip--with-left-icon chip--with-right-icon chip--border-color-ui-3 chip--background-color-undefined chip--max-content']"
        networks_btn = BaseElement(
            driver=self.driver, by=networks_btn_loc[0], value=networks_btn_loc[1]
        )

        networks_btn.click()

        chain_select_loc = By.XPATH, f"//span[text()={chain_name} and @class='network-name-item']"
        chain_select = BaseElement(
            driver=self.driver, by=chain_select_loc[0], value=chain_select_loc[1]
        )

        chain_select.click()










