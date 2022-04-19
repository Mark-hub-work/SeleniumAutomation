import time

import selenium.common.exceptions
from selenium.common.exceptions import TimeoutException as TE
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

from base_element import BaseElement
from slow_element import SlowElement


class CryptoBladesCombatPage:
    def __init__(self, driver):
        self.driver = driver

    def close_notifications(self):
        try:
            notifications = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "button[class='close']"))
            )
        except selenium.common.exceptions.ElementClickInterceptedException:
            print("no notifications found")
            pass
        except:
            print("unknown error regarding notification closing")
            pass
        else:
            for notification in notifications:
                try:
                    notification.click()
                except:
                    print("can't close this element")

    def close_fight(self):
        try:
            close_btn_loc = By.XPATH, "//span[contains(@class, 'tap')]"
            close_btn = SlowElement(
                driver=self.driver, by=close_btn_loc[0],
                value=close_btn_loc[1]
            )
        except TE:
            print("TimeoutException error!")
            time.sleep(30)
            pass
        except:
            pass
        else:
            close_btn.click()

    def earning_calculator(self):

        self.driver.get('https://coinmarketcap.com/currencies/cryptoblades/')

        loc = By.XPATH, "//div[contains(@class, 'priceValue')]"
        skill_value = BaseElement(
            driver=self.driver, by=loc[0], value=loc[1]
        )

        skill_value = float(
            str(skill_value.get_attribute("innerText").split("$")[1])
        )

        self.driver.get('https://coinmarketcap.com/currencies/huobi-token/')

        chain_value = BaseElement(
            driver=self.driver, by=loc[0], value=loc[1]
        )

        chain_value = float(
            str(chain_value.get_attribute("innerText").split("$")[1])
        )

        return chain_value, skill_value

    # fight
    def fight(self):
        # chance of victory between enemies 1-4
        # We will examine this first and then check how much skill
        # to determine which enemy to fight

        # choice variable holds which enemy we will fight
        # max_skill variable holds the highest skill enemy of very likely or
        # of likely if there are no very likely fights
        choice = -1
        max_skill = 0

        vic_chance_list = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//div[contains(@class, 'chance-winning')]"))
        )


        # we get the html elements containing the skill of the 4 enemies
        skill_gain_list = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//div[contains (@class, 'skill-gain mb-1')]"))
        )

        # we parse the elements to put the actual strings of the skill
        # into a list
        skill_list = []
        for i in range(4):
            skill_list.append(
                float(skill_gain_list[i].get_attribute('outerText')[3:11]))

        print("The skill list is: " + str(skill_list))
        # logic goes here where we click fight on the one that
        # has the best result
        fight_list = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//div[contains (@class, 'enemy-character')]"))
        )

        enemy1 = fight_list[0]
        enemy2 = fight_list[1]
        enemy3 = fight_list[2]
        enemy4 = fight_list[3]

        # Very Likely Victory
        # Likely Victory
        # we want to check for Very Likely Victory in our enemies, and
        # whoever is Very Likely we want to check the amount of skill
        # and select the larger amount
        # if we don't find any Very Likely we do the same thing for Likely
        very_likely_list = []
        likely_list = []
        for vic_chance in vic_chance_list:
            if str(vic_chance.get_attribute(
                    'outerText').lower()) == "very likely victory":
                very_likely_list.append(1)
            else:
                very_likely_list.append(0)
            print(str(vic_chance.get_attribute('outerText').lower()))

            if (str(vic_chance.get_attribute('outerText').lower()) ==
                    "likely victory"):
                likely_list.append(1)
            else:
                likely_list.append(0)
            print(str(vic_chance.get_attribute('outerText').lower()))

        # if there is a very likely win we'll find the one with the
        # highest skill
        if very_likely_list != [0, 0, 0, 0]:
            very_likely_skill_list = []
            for num1, num2 in zip(very_likely_list, skill_list):
                very_likely_skill_list.append(num1 * num2)
            print(very_likely_skill_list)
            for i in range(len(very_likely_skill_list)):
                print(very_likely_skill_list[i])
                # look for any very likely fights and check if they
                # are the max skill
                if very_likely_skill_list[i] > max_skill:
                    choice = i
                    max_skill = very_likely_skill_list[i]
                    print(max_skill)
        elif likely_list != [0, 0, 0, 0]:
            likely_skill_list = []
            for num1, num2 in zip(likely_list, skill_list):
                likely_skill_list.append(num1 * num2)
            print(likely_skill_list)
            for i in range(len(likely_skill_list)):
                print(likely_skill_list[i])
                # look for any very likely fights and check
                # if they are the max skill
                if likely_skill_list[i] > max_skill:
                    choice = i
                    max_skill = likely_skill_list[i]
        else:
            return 0

        print(f"The choice is enemy: {choice}")

        # now we click fight on the choice
        if choice == 0:
            enemy1.click()
        elif choice == 1:
            enemy2.click()
        elif choice == 2:
            enemy3.click()
        elif choice == 3:
            enemy4.click()
        else:
            return 0

        return max_skill

    # return 1 on a win, and 0 on a lose
    def fight_result(self):
        result_loc = By.XPATH, "//h1"
        result_info = SlowElement(
            driver=self.driver, by=result_loc[0], value=result_loc[1]
        )
        result = result_info.get_attribute("innerText").lower()
        if result == "you lost the fight!":
            return 0
        else:
            return 1

    def select_character(self, stamina):
        character_list = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//div[contains(@class, 'character-details')]"))
        )

        print(character_list[0].get_attribute('innerText').split()[5])
        print(character_list[1].get_attribute('innerText').split()[5])
        print(character_list[2].get_attribute('innerText').split()[5])
        print(character_list[3].get_attribute('innerText').split()[5])

        stamina_list = [0, 0, 0, 0]

        character1_select = character_list[0]
        character2_select = character_list[1]
        character3_select = character_list[2]
        character4_select = character_list[3]

        stamina_list[0] = character_list[0].get_attribute('innerText') \
            .split()[5]
        stamina_list[1] = character_list[1].get_attribute('innerText') \
            .split()[5]
        stamina_list[2] = character_list[2].get_attribute('innerText') \
            .split()[5]
        stamina_list[3] = character_list[3].get_attribute('innerText') \
            .split()[5]

        if int(stamina_list[0]) >= stamina:
            character1_select.click()
            self.select_stamina(stamina)
            return 0
        elif int(stamina_list[1]) >= stamina:
            character2_select.click()
            self.select_stamina(stamina)
            return 0
        elif int(stamina_list[2]) >= stamina:
            character3_select.click()
            self.select_stamina(stamina)
            return 0
        elif int(stamina_list[3]) >= stamina:
            character4_select.click()
            self.select_stamina(stamina)
            return 0
        else:
            return 1

    def select_stamina(self, stamina):
        stamina_select = Select(self.driver.find_element_by_css_selector(
            "select[class='custom-select']")
        )
        stamina_select.select_by_visible_text(str(stamina))

    def select_weapon(self):
        time.sleep(3)
        weapons_btn_loc = By.XPATH, \
                          "//button[contains (@class, 'ml-3 ct-btn ml-2')]"

        weapons_btn = BaseElement(
            driver=self.driver, by=weapons_btn_loc[0],
            value=weapons_btn_loc[1]
        )

        weapons_btn.click()

        weapons = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//div[contains (@class, 'weapon-icon-wrapper')]"))
        )

        weapons[0].click()
