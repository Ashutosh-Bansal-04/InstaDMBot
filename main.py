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
        buttons = driver.find_elements(By.CLASS_NAME, "x1i10hfl")
        for btn in buttons:
            if 'Message' in btn.text:
                btn.click()
                print("✅ Clicked primary message button (generic text scan).")
        print("✅ Clicked primary message button.")
        return True
    except:
        return False

def try_3dot_menu(driver):
    try:
        menu = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Options')]")
        menu.click()
        time.sleep(random.uniform(2, 4))
        message_btn = driver.find_element(By.XPATH, "//div[text()='Message']")
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
