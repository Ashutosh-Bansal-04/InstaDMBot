import time
import random
import requests
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

# # === Load Files ===
# def load_accounts(file_path):
#     with open(file_path, "r") as f:
#         return [tuple(line.strip().split(":")) for line in f.readlines()]

# def load_usernames(file_path):
#     with open(file_path, "r") as f:
#         return [line.strip() for line in f.readlines()]

# def load_messages(file_path):
#     with open(file_path, "r", encoding="utf-8") as f:
#         raw = f.read()
#         return [msg.strip() for msg in raw.split("===") if msg.strip()]
# === Load Files ===
def load_accounts(file_path):
    with open(file_path, "r") as f:
        return [tuple(line.strip().split(":")) for line in f.readlines()]

def load_personalized_messages(file_path):
    personalized = {}
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if "-" in line:
                username, msg = line.split("-", 1)
                personalized[username.strip()] = msg.strip()
    return personalized

def log_successful_dm(username, log_file="successful_dms.txt"):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(username + "\n")


# # Replace with your real API key
# DOLPHIN_API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiODM1OTAzNGNjODc1MGI5OWI1N2U2YjZhZWZlZDg1Y2ZjOWQxODMzYjgwMDY1ODkzOWFmYjhhOGJkMjBlNzhiYWRmNmU4NDA3M2FjMWQzZjMiLCJpYXQiOjE3NDg0NjE1ODYuODE1MjA3LCJuYmYiOjE3NDg0NjE1ODYuODE1MjA4LCJleHAiOjE3NTEwNTM1ODYuODA3OTk2LCJzdWIiOiI0NDA0MzgzIiwic2NvcGVzIjpbXSwidGVhbV9pZCI6NDMxMjA0OSwidGVhbV9wbGFuIjoiZnJlZSIsInRlYW1fcGxhbl9leHBpcmF0aW9uIjoxNzQ4MjYwOTQwfQ.qN-zQZeA51h8rHQxAo-yRkFXRCkeM93ncoSQYOew2Ew8R-SLyyLWic7-njB8CatlQDg8zW6GXEeR7Wk5rSKPxnRa8yYpsu8YSbgiO2xZ38xYKAy8rpSzc3kYJgVZEu-mNC0NV2BMNKxVD1jl-2mCi9JjjCdoRli08J8aZL8XMJICIN3ErSSXN6zrjhP9wZejyCrOyq4iMZUMe3z17wInbjl6bVYR_WYZUtv5vtCkLgGZwuNuDLKieUQBvgWF-3vzB-2qBreqDKBwER0TTv_3zFPGSBzNv8ggM_vWm8MiiXLcXupRQJzunrJcpcllTZv_wy-zy5-LyJPp_lYd6j6hzIcPUfaVh8pHvQQ4-oV3fpVTo9GWpLbCuj9rZ-ugbUuSGejfwFQtsDpLW9RzG3Ky1vF7i0dnjQHqGGN6uucMZaGiABOZFgk7xQFnF_mMZsWpbQ-I9e2CSAOMzUPieVWKIg0o2paUkqFqjXjt5WlHkoD8RAewd9wdE22N9wphPXc0phcurErmrmXm49sMHnQoQCBCUeOsEv_G7VathTvlHFfWctUKw-zQ9fsDKsqEb3D0qg5ESkWbZc4mzX9WJeS41Ne-nBhnyss4yKLUoeaddB03RP_sdDaNGaGxlUSz5siauvjSM-EsJKCpsnjHMHVcoQYZmlEZZ9p3V5ipL5_XGoU"

# def start_dolphin_profile(profile_id):
#     url = "http://localhost:3001/browser/start"
#     payload = {
#         "profile_id": profile_id,
#     }
#     headers = {
#         "Authorization": f"Bearer {DOLPHIN_API_KEY}"
#     }
#     response = requests.post(url, json=payload, headers=headers)
#     data = response.json()
#     if not data.get("success"):
#         raise Exception(f"Failed to start profile: {data}")
#     return data["automation"]["port"]
# def start_dolphin_profile(profile_id):
#     url = "http://localhost:3001/browser/start"
#     payload = {
#         "profile_id": profile_id,
#     }
#     headers = {
#         "Authorization": f"Bearer " + DOLPHIN_API_KEY
#     }

#     response = requests.post(url, json=payload, headers=headers)

#     print("Status code:", response.status_code)
#     print("Raw response text:", response.text)

#     try:
#         data = response.json()
#         if not data.get("success"):
#             raise Exception(f"Failed to start profile: {data}")
#         return data["automation"]["port"]
#     except Exception as e:
#         print("[!] Failed to parse JSON.")
#         raise es

DOLPHIN_API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiM2MwYmU3NTdlMTQ5YzY1NDRlNDBkOTUxOTA0YTgwY2I1MWU0OWNmM2YxMjNmZWZjYTNjOTMxM2Q1OGQ4MWYwMmE3YjNmZmM1MjRmODM3OGMiLCJpYXQiOjE3NDg1MTA4OTkuNTEzMTY4LCJuYmYiOjE3NDg1MTA4OTkuNTEzMTcsImV4cCI6MTc1MTEwMjg5OS41MDYyNjgsInN1YiI6IjQ0MDQzODMiLCJzY29wZXMiOltdLCJ0ZWFtX2lkIjo0MzEyMDQ5LCJ0ZWFtX3BsYW4iOiJmcmVlIiwidGVhbV9wbGFuX2V4cGlyYXRpb24iOjE3NDgyNjA5NDB9.JzQWgsWUQB2tLi7pKcs5EgpxUYedxW7qqGpvenMRRgcegtMdYpFT5lLO3sQA6UrLvSosFdw7SvZIeYbvIFyy2UgHYJm1UrGht9cyP678PJUz7R1hsoavyqkRs1akGnYnpUxGE3cUQqX77rkoh5xsZVnpQUxPZiJqTbZvPKllDHfw_gYsk3qlNVzBPvwl0sT72ARkrX04XgOF-wdIU-yby6Vb2Xd-9ElFnO6OoNPre93ov2_GXx6ojWrr9DNDw2N9zv5P93T_iZPrYCKVdLwiGSEszyn0fey1xCRrPr9rkZMu9467FHEuoCbngnRy2A8EvW0SgW23Hl8VoRltOFpLmR7Kiw3Ofv4MH-vCUBxWHt7fysOQkl7r2oV5RV-eiNyy8DkvX7QFeYCRQoE75jfRhAbvxfNy4la4csM1skWr8YA-izQksuFwBt_wisIqB8Aax8Mmqw3UCKAUUkJoAZj2GNCQmfweFeED8xpmyTnRxXjBCuxEtIL6goUBgJ4HU11KrAE11hxEDErmvJ64XK8gVvhryz86xQbsnCSvz_jI1ePqOdJH9AgNCafWkvnLx8khdFfr7yx2M6fxQnD4qSx1593_0gwd-e-vB77lOrRM0UPsfn83M81o52YyFAB2pPWdMQi9CqTbCKDArBXIT5bCzRYM1yVPzfyxuyW3Tw8524g"

# def start_dolphin_profile(profile_id):
#     url = "http://localhost:3001/v1.0/browser_profiles/{PROFILE_ID}/start?automation=1" 

#     headers = {
#         "Authorization": f"Bearer {DOLPHIN_API_KEY}",
#         "Content-Type": "application/json"
#     }
#     payload = {
#         "profile_id": profile_id
#     }

#     response = requests.post(url, json=payload, headers=headers)

#     print("Status code:", response.status_code)
#     print("Response:", response.text)

#     response.raise_for_status()  # will raise an error if 401, 403, etc.

#     data = response.json()
#     if not data.get("success"):
#         raise Exception("Profile start failed: " + str(data))
#     return data["automation"]["port"]
def start_dolphin_profile(profile_id):
    url = "http://localhost:3001/v1.0/browser_profiles/{}/start?automation=1".format(profile_id)

    request_data = {
        'token' : DOLPHIN_API_KEY,
    }

    headers = {
        "content-type": "application/json",
    }
    response = requests.get(url, json=request_data, headers=headers)
    if response.status_code != 200:
        print('Successful response:', response.json())
    else:
        print('Error response:', response.status_code, response.text)
        raise Exception(f"Failed to start profile {profile_id}: {response.text}")

def setup_driver(profile_id):
    port = start_dolphin_profile(profile_id)
    options = webdriver.ChromeOptions()
    driver = webdriver.Remote(
        command_executor=f"http://localhost:{port}",
        options=options
    )
    driver.implicitly_wait(10)
    return driver

# # === Setup Chrome ===
# def setup_driver():
#     chrome_options = Options()
#     chrome_options.add_argument("--start-maximized")
#     chrome_options.add_argument("--disable-notifications")
#     chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
#     chrome_options.add_experimental_option('useAutomationExtension', False)
#     driver = webdriver.Chrome(options=chrome_options)
#     driver.implicitly_wait(10)
#     return driver

# === Instagram Login ===
def login_instagram(driver, username, password):
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(random.uniform(5, 7))

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )

    driver.find_element(By.NAME, "username").send_keys(username)
    time.sleep(1)
    driver.find_element(By.NAME, "password").send_keys(password)
    time.sleep(2)
    driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)
    time.sleep(2)

    time.sleep(random.uniform(7, 12))  # Wait for login to complete

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
        time.sleep(random.uniform(5, 10))

        # Just type the message directly (textarea usually auto-focused)
        # actions = webdriver.ActionChains(driver)
        # for line in message.split("\n"):
        #     actions.send_keys(line).send_keys(Keys.SHIFT, Keys.ENTER)
        # actions.send_keys(Keys.RETURN)
        # actions.perform()

        # Build the message with line breaks after full stops
        sentences = [s.strip() for s in message.split('.') if s.strip()]
        formatted_message = "\n".join([s + '.' for s in sentences])

        actions = webdriver.ActionChains(driver)
        actions.send_keys(formatted_message)
        actions.send_keys(Keys.RETURN) # Final enter to send
        # sentences = [s.strip() for s in message.split('.') if s.strip()]
        # for sentence in sentences:
        #     actions.send_keys(sentence + '.')
        #     actions.send_keys(Keys.SHIFT + Keys.ENTER)
#         for line in message.split("\n"):
#             actions.send_keys(line).send_keys(Keys.SHIFT + Keys.ENTER)
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
    personalized_messages = load_personalized_messages("personalized_messages.txt")

    # For each account, use corresponding Dolphin profile
    profile_ids = ["612565928", "612566138", "612566190",]

    for acc_index, (username, password) in enumerate(accounts):
        profile_id = profile_ids[acc_index]  # Match to account
        print(f"\n[+] Using profile {profile_id} for @{username}")
        driver = setup_driver(profile_id)

        for acc_index, (username, password) in enumerate(accounts):
            print(f"\n[+] Logging in with @{username}")
            driver = setup_driver()
        try:
            login_instagram(driver, username, password)
            dms_sent = 0

            for target, message in personalized_messages.items():
                if dms_sent >= MAX_DMS_PER_ACCOUNT:
                    print(f"[i] Reached DM limit for @{username}")
                    break

                # message = personalized_messages.get(target, "Hi there! Just wanted to connect.")  # Fallback message
                success = send_message(driver, target, message)

                if success:
                    log_successful_dm(target)
                    dms_sent += 1
                    time.sleep(random.uniform(5, 20))
                else:
                    print(f"[!] Skipping {target}")

        except Exception as e:
            print(f"[!] Error with @{username}: {e}")
        finally:
            driver.quit()

if __name__ == "__main__":
    main()
