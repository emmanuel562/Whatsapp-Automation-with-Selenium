# Import modules after pip installing Selenium and Pyperclip
import os
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pyperclip
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import platform

x = dir(platform)
print(x)
# === CONFIGURATION ===
CHROMEDRIVER_PATH = "chromedriver.exe"
IMAGE_PATH = "WhatsApp Image 2025-07-19 at 5.49.26 PM.jpeg"
CONTACT_FILE = "THU Contacts.txt "
MESSAGE_TEMPLATES = ["""
🚀 Get September-Ready — Today!

“Success is where preparation and opportunity meet.” – Bobby Unser
Don’t wait until school resumes. Give your child a flying start with our Back-to-School Booster Classes.
✏️ Confidence. Competence. Comeback.
"""]
BATCH_SIZE = 10  # Number of contact per batch
MESSAGE_DELAY = 10  # seconds between each message
BATCH_DELAY = 1800   # 30 minutes between batches

# === FUNCTIONS ===


def load_contacts(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def send_message(driver, number, message, image_path):
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException

    try:
        clean_number = number.replace(" ", "").strip()
        print(f"📨 Opening chat with {clean_number}")
        driver.get(
            f"https://web.whatsapp.com/send?phone={clean_number}&text&app_absent=0")

        time.sleep(5)

        try:
            continue_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//a[contains(text(), "Continue to Chat")]'))
            )
            continue_btn.click()
            time.sleep(5)
        except:
            pass

        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
            )
        except TimeoutException:
            print(f"⚠️ Chat input not ready for {clean_number}. Skipping.")
            driver.save_screenshot(f"error_{clean_number}.png")
            return

        try:
            time.sleep(5)
            attach_btn = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div/div[1]/button'))
            )
            driver.execute_script("arguments[0].click();", attach_btn)
        except TimeoutException:
            print(
                f"⚠️ Still couldn’t find or click attach icon for {clean_number}.")
            driver.save_screenshot(f"error_{clean_number}_attach_missing.png")
            return

        # Upload image
        img_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]'))
        )
        img_input.send_keys(os.path.abspath(image_path))
        time.sleep(3)

        # Add caption
        try:
            pyperclip.copy(message)

            caption_box = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@contenteditable="true" and @aria-label="Add a caption"]'))
            )

            driver.execute_script(
                "arguments[0].scrollIntoView(true);", caption_box)
            time.sleep(1)

            caption_box.click()
            actions = ActionChains(driver)
            actions.key_down(Keys.CONTROL).send_keys(
                'v').key_up(Keys.CONTROL).perform()

            print(f"✏️ Caption pasted successfully.")

        except Exception as e:
            print(f"❌ Failed to write caption: {repr(e)}")
            driver.save_screenshot(f"error_{clean_number}_caption_fail.png")
            return

        send_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="app"]/div/div[3]/div/div[2]/div[2]/span/div/div/div/div[2]/div/div[2]/div[2]/div/div/span'))
        )

        send_btn.click()
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    '//span[contains(@data-icon, "msg-time") or contains(@data-icon, "msg-check") or contains(@data-icon, "msg-dblcheck")]'
                ))
            )
            print(f"✅ WhatsApp confirms sent to {clean_number}")
        except TimeoutException:
            print(
                f"⚠️ Message may not have fully sent to {clean_number} — retry or check manually")

        time.sleep(3)

    except Exception as e:
        print(f"❌ Failed to send to {clean_number}: {repr(e)}")
        driver.save_screenshot(f"error_{clean_number}.png")


def run_batches():
    contacts = load_contacts(CONTACT_FILE)
    batches = [contacts[i:i+BATCH_SIZE]
               for i in range(0, len(contacts), BATCH_SIZE)]

    service = ChromeService(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service)

    driver.get("https://web.whatsapp.com")
    input("📷 Scan QR code in Chrome, then press Enter to continue...")

    for i, batch in enumerate(batches):
        print(f"\n🚀 Starting batch {i+1}/{len(batches)}")
        for number in batch:
            msg = random.choice(MESSAGE_TEMPLATES)
            send_message(driver, number, msg, IMAGE_PATH)

        if i < len(batches) - 1:
            print(
                f"\n⏳ Waiting {BATCH_DELAY//60} minutes before next batch...")
            time.sleep(BATCH_DELAY)

    print("\n🎉 All messages sent!")
    input("💬 Press Enter to close browser...")


# === RUN ===
if __name__ == "__main__":
    run_batches()
