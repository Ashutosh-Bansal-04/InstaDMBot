import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# === CONFIGURATION ===
MAX_DMS_PER_ACCOUNT = 10
DELAY_RANGE = (3, 7)  # Random delay between actions

# === Load Files ===
def load_accounts(file_path):
    with open(file_path, "r") as f:
        return [tuple(line.strip().split(":")) for line in f.readlines()]

def load_usernames(file_path):
    with open(file_path, "r") as f:
        return [line.strip() for line in f.readlines()]

def load_messages(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        raw = f.read()
        return [msg.strip() for msg in raw.split("===") if msg.strip()]

# === Setup Chrome ===
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    return driver

# === Instagram Login ===
def login_instagram(driver, username, password):
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(random.uniform(*DELAY_RANGE))

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )

    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)

    time.sleep(random.uniform(5, 10))  # Wait for login to complete

# === Message Sending Logic ===
def try_message_button(driver):
    try:
        # buttons = driver.find_elements(By.CLASS_NAME, "x1i10hfl")
        buttons = driver.find_element(By.XPATH, "//div[@class='x1i10hfl xjqpnuy xa49m3k xqeqjp1 x2hbi6w x972fbf xcfux6l x1qhh985 xm0m39n xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x18d9i69 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x1lku1pv x1a2a7pz x6s0dn4 xjyslct x1lq5wgf xgqcy7u x30kzoy x9jhf4c x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 x1ypdohk x78zum5 x1f6kntn xwhw2v2 x10w6t97 xl56j7k x17ydfre x1swvt13 x1pi30zi x1n2onr6 x2b8uid xlyipyv x87ps6o x14atkfc xcdnw81 x1i0vuye x1gjpkn9 x5n08af xsz8vos']").click()
        # for btn in buttons:
        #     if 'Message' in btn.text:
        #         btn.click()
        #         print("✅ Clicked primary message button (generic text scan).")
        print("✅ Clicked primary message button.")
        return True
    except:
        return False

def try_3dot_menu(driver):
    try:
        # menu = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Options')]")
        # menu.click()
        # time.sleep(random.uniform(2, 4))
        # message_btn = driver.find_element(By.XPATH, "//div[text()='Message']")
        # message_btn.click()
        # menu = driver.find_elements(By.CLASS_NAME, "x972fbf")
        menu = driver.find_element(By.XPATH, "//div[@class='x1i10hfl x972fbf xcfux6l x1qhh985 xm0m39n x9f619 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x6s0dn4 xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x1ypdohk x78zum5 xl56j7k x1y1aw1k x1sxyh0 xwib8y2 xurb0ha xcdnw81']").click()

        # for opt in menu:
        #     # if 'Message' in opt.text:
        #     opt.click()
        #     print("✅ Clicked menu button (generic text scan).")
        #     time.sleep(random.uniform(2, 4))
        message_btn = driver.find_element(By.XPATH, "//button[text()='Send message']")
        message_btn.click()
        return True
    except:
        return False

# def send_message(driver, username, message):
#     driver.get(f"https://www.instagram.com/{username}/")
#     time.sleep(random.uniform(*DELAY_RANGE))

#     if not try_message_button(driver):
#         if not try_3dot_menu(driver):
#             print(f"[!] Could not find message button for {username}")
#             return False

#     time.sleep(random.uniform(2, 4))
#     textarea = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.TAG_NAME, "textarea"))
#     )
#     textarea.send_keys(message)
#     time.sleep(1)
#     textarea.send_keys(Keys.RETURN)
#     print(f"[✓] Message sent to @{username}")
#     return True
def send_message(driver, username, message):
    try:
        driver.get(f"https://www.instagram.com/{username}/")
        time.sleep(random.uniform(3, 6))

        # Try primary and fallback message buttons
        if not try_message_button(driver):
            if not try_3dot_menu(driver):
                print(f"[!] Could not find message button for {username}")
                return False

        # Message section opened
        print(f"[i] Message window opened for @{username}")
        time.sleep(random.uniform(3, 5))

        # Just type the message directly (textarea usually auto-focused)
        actions = webdriver.ActionChains(driver)
        for line in message.split("\n"):
            actions.send_keys(line).send_keys(Keys.SHIFT, Keys.ENTER)
        actions.send_keys(Keys.RETURN)
        actions.perform()

        print(f"[✓] Message sent to @{username}")
        return True

    except Exception as e:
        print(f"[!] Failed to send message to @{username}: {str(e)}")
        driver.save_screenshot(f"screenshots/err_{username}.png")
        return False


# === Main Logic ===
def main():
    accounts = load_accounts("accounts.txt")
    usernames = load_usernames("usernames.txt")
    messages = load_messages("messages.txt")

    for acc_index, (username, password) in enumerate(accounts):
        print(f"\n[+] Logging in with @{username}")
        driver = setup_driver()
        try:
            login_instagram(driver, username, password)
            dms_sent = 0

            for target in usernames:
                if dms_sent >= MAX_DMS_PER_ACCOUNT:
                    print(f"[i] Reached DM limit for @{username}")
                    break

                message = random.choice(messages)
                success = send_message(driver, target, message)

                if success:
                    dms_sent += 1
                    time.sleep(random.uniform(5,20))
                else:
                    print(f"[!] Skipping {target}")

        except Exception as e:
            print(f"[!] Error with @{username}: {e}")
        finally:
            driver.quit()

if __name__ == "__main__":
    main()
