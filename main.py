import time

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver

from cblades_combat_page import CryptoBladesCombatPage
from google_sheet import GoogleSheet
from mmask_page import MetaMaskPage


# This is the Chrome Script going to be using Heco Network.

# variables
sheet = GoogleSheet("Your Google Sheet")
net_row = 2
skill_row = 209
col = 0
net = 0
skill_net = 0
accounts_list = [
    'Account 2', 'Account 3', 'Account 4', 'Account 5', 'Account 6',
    'Account 7', 'Account 8', 'Account 9', 'Account 10'
    ]
net_row_list = [7, 12, 17, 22, 27, 32, 37, 42, 47]
skill_row_list = [214, 219, 224, 229, 234, 239, 244, 249, 254]

chrome_options = Options()
chrome_options.add_argument('--profile-directory=Profile 1')
chrome_options.add_argument(
    f"path\\to\\your\\chrome\\profile"
    )
exe_path = Service(
    'path\of\your\chromedriver'
    )
driver = webdriver.Chrome(options=chrome_options, service=exe_path)

# script
# driver.window_handles[0] = 'Metamask'
# driver.window_handles [1] = 'fiddle window'
#driver.window_handles [2] = 'Metamask pop-up'

driver.execute_script("window.open('about:blank', 'secondtab');")
driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#')
metamask = MetaMaskPage(driver=driver)
cryptoblades_combat = CryptoBladesCombatPage(driver=driver)
metamask.input_password()
time.sleep(10)
driver.switch_to.window(driver.window_handles[0])

# switch to the account you want to start on
# we'll get the prices of skill and of Heco
metamask.switch_account('Account 1')
metamask.switch_chain('HECO MAIN')
driver.switch_to.window(driver.window_handles[1])
heco_price, skill_price = cryptoblades_combat.earning_calculator()
driver.get('https://app.cryptoblades.io/#/?chain=HECO')
driver.maximize_window()
driver.switch_to.window(driver.window_handles[1])
time.sleep(5)
driver.get('https://app.cryptoblades.io/#/combat?chain=HECO')
time.sleep(20)
cryptoblades_combat.close_notifications()
time.sleep(5)


# now we are on the fight page so we can put fight logic into here

# feed the stamina you will allow characters to fight with into
# select character. I also put select weapon into select character
# so that the script doesn't break selecting a weapon when no character
# has stamina. I gave it a return of 0 if it finds a character to play, and
# 1 if it does not, so we can use this in a loop condition
# to fight all our characters.
keep_fighting = cryptoblades_combat.select_character(200)
if keep_fighting == 0:
    cryptoblades_combat.select_weapon()
while keep_fighting == 0:
    # now we will do the game logic of finding an enemy to fight and checking
    # whether this fight is actually worth skill such that we want to
    # take the fight.
    time.sleep(3)
    skill_amount = cryptoblades_combat.fight()
    print(f"The skill amount is: {skill_amount}")

    if (skill_amount == 0):
        break

    if (skill_amount > 0):

        print(f"Heco price is: {heco_price}")
        print(f"skill price is: {skill_price}")

        time.sleep(3)
        driver.switch_to.window(driver.window_handles[2])
        time.sleep(3)
        gas_amount = metamask.get_gas_amount()
        print(f"The gas amount is: {gas_amount} Heco")
        print(f"The gas cost is: {gas_amount * heco_price}")
        print(f"The skill value is: {skill_amount * skill_price}")
        if (skill_amount * skill_price >= gas_amount * heco_price):
            print(f"The profits earned are: {(skill_amount * skill_price) - (gas_amount * heco_price)}")
            metamask.confirm()
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(20)
            if (cryptoblades_combat.fight_result() == 0):  # you lost the fight
                col = sheet.find_empty_cell(net_row)
                net = 0 - (gas_amount * heco_price)
                sheet.update_cell(net_row, col, net)
                sheet.update_cell(skill_row, col, 0)
                net_row += 1
                skill_row += 1
                cryptoblades_combat.close_fight()
                time.sleep(20)

            else:  # you won the fight
                col = sheet.find_empty_cell(net_row)
                net = (skill_amount * skill_price) - (gas_amount * heco_price)
                sheet.update_cell(net_row, col, net)
                sheet.update_cell(skill_row, col, skill_amount)
                net_row += 1
                skill_row += 1
                cryptoblades_combat.close_fight()
                time.sleep(20)

        else:
            print(f"The loss would of been: {(skill_amount * skill_price) - (gas_amount * heco_price)}")
            metamask.reject()
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(3)
            break

        driver.switch_to.window(driver.window_handles[1])
        keep_fighting = cryptoblades_combat.select_character(200)

# next accnts
for i, account in enumerate(accounts_list):
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(1)
    metamask.switch_account(account)
    driver.switch_to.window(driver.window_handles[1])
    driver.get('https://app.cryptoblades.io/#/combat')
    net_row = net_row_list[i]
    skill_row = skill_row_list[i]
    time.sleep(20)

    keep_fighting = cryptoblades_combat.select_character(200)
    if keep_fighting == 0:
        cryptoblades_combat.select_weapon()
    else:
        pass
    while keep_fighting == 0:
        # now we will do the game logic of finding an enemy to fight and checking
        # whether or not this fight is actually worth skill such that we want to take
        # the fight.
        time.sleep(3)
        skill_amount = cryptoblades_combat.fight()
        print(f"The skill amount is: {skill_amount}")

        if (skill_amount == 0):
            break

        if (skill_amount > 0):
            print(f"Heco price is: {heco_price}")
            print(f"skill price is: {skill_price}")

            time.sleep(5)
            driver.switch_to.window(driver.window_handles[2])
            time.sleep(3)
            gas_amount = metamask.get_gas_amount()
            print(f"The gas amount is: {gas_amount} Heco")
            print(f"The gas cost is: {gas_amount * heco_price}")
            print(f"The skill value is: {skill_amount * skill_price}")
            if (skill_amount * skill_price >= gas_amount * heco_price):
                print(
                    f"The profits earned are: {(skill_amount * skill_price) - (gas_amount * heco_price)}")
                metamask.confirm()
                driver.switch_to.window(driver.window_handles[1])
                time.sleep(20)
                if (
                        cryptoblades_combat.fight_result() == 0):  # you lost the fight
                    col = sheet.find_empty_cell(net_row)
                    net = 0 - (gas_amount * heco_price)
                    sheet.update_cell(net_row, col, net)
                    sheet.update_cell(skill_row, col, 0)
                    net_row += 1
                    skill_row += 1
                    cryptoblades_combat.close_fight()
                    time.sleep(20)

                else:  # you won the fight
                    col = sheet.find_empty_cell(net_row)
                    net = (skill_amount * skill_price) - (
                            gas_amount * heco_price)
                    sheet.update_cell(net_row, col, net)
                    sheet.update_cell(skill_row, col, skill_amount)
                    net_row += 1
                    skill_row += 1
                    cryptoblades_combat.close_fight()
                    time.sleep(20)

            else:
                print(
                    f"The loss would of been: {(skill_amount * skill_price) - (gas_amount * heco_price)}")
                metamask.reject()
                driver.switch_to.window(driver.window_handles[1])
                time.sleep(3)
                break

            driver.switch_to.window(driver.window_handles[1])
            keep_fighting = cryptoblades_combat.select_character(200)