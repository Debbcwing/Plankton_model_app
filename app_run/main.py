from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import os

# Streamlit app URL from environment variable (or default)
STREAMLIT_URL = os.environ.get("STREAMLIT_APP_URL", "https://lake-plankton.streamlit.app/")

def main():
    print(f"Starting wake script for: {STREAMLIT_URL}")

    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')

    # For GitHub Actions - don't fail if button doesn't disappear quickly
    options.add_argument('--disable-blink-features=AutomationControlled')

    # Use system chromium if available (for GitHub Actions), otherwise use ChromeDriverManager
    try:
        if os.path.exists('/usr/bin/chromium-browser'):
            print("Using system Chromium browser")
            options.binary_location = '/usr/bin/chromium-browser'
            service = Service('/usr/bin/chromedriver')
        else:
            print("Using ChromeDriverManager")
            service = Service(ChromeDriverManager().install())

        driver = webdriver.Chrome(service=service, options=options)
        print("Chrome driver initialized successfully")
    except Exception as e:
        print(f"Failed to initialize Chrome driver: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

    try:
        print(f"Navigating to {STREAMLIT_URL}...")
        driver.get(STREAMLIT_URL)
        print(f"Successfully opened {STREAMLIT_URL}")

        wait = WebDriverWait(driver, 20)
        try:
            # Look for the wake-up button
            print("Looking for wake-up button...")
            button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Yes, get this app back up')]"))
            )
            print("Wake-up button found! Clicking...")
            button.click()

            # After clicking, wait a bit - don't fail if button doesn't disappear
            try:
                wait.until(EC.invisibility_of_element_located((By.XPATH, "//button[contains(text(),'Yes, get this app back up')]")))
                print("Button clicked and disappeared ✅ (app is waking up)")
            except TimeoutException:
                print("Button was clicked but still visible ⚠️ (app might be waking up anyway)")
                # Don't exit with error - button click might have worked

        except TimeoutException:
            # No button at all → app is assumed to be awake
            print("No wake-up button found. App is already awake ✅")

        print("Wake script completed successfully!")

    except Exception as e:
        print(f"Unexpected error during execution: {e}")
        import traceback
        traceback.print_exc()
        # Take a screenshot for debugging if possible
        try:
            screenshot_path = "/tmp/error_screenshot.png"
            driver.save_screenshot(screenshot_path)
            print(f"Screenshot saved to {screenshot_path}")
        except:
            pass
        exit(1)
    finally:
        try:
            driver.quit()
            print("Browser closed successfully")
        except:
            pass

if __name__ == "__main__":
    main()