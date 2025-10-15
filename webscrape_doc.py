from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import datetime
import time

def get_web_data(url):

    # --------------------------
    # Chrome setup
    # --------------------------
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # run in background
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(driver, 20)

    # --------------------------
    # Open doctor page
    # --------------------------
    #url = "https://medicasapp.com/in/doctors-in-bangalore/general-practitioner/dr-b-l-avinash/"
    driver.get(url)
    time.sleep(3)  # wait for calendar to load

    ul_element = driver.find_element(By.CSS_SELECTOR, "ul.time-slots2")  # selects <ul class="time-slots2 ...">

    doctor_id = ul_element.get_attribute("data-doctor-id")
    doctor_name = driver.find_element(By.CSS_SELECTOR, "h2.font-size18").text.strip()
    specialization = driver.find_elements(By.CSS_SELECTOR, "p.margin-0px-bottom.font-size14")[0].text.strip()
    qualification = driver.find_elements(By.CSS_SELECTOR, "p.margin-0px-bottom.font-size14")[1].text.strip()
    #experience = driver.find_elements(By.CSS_SELECTOR, "p.margin-0px-bottom.font-size14")[-1].text.strip()
    experience = driver.find_elements(By.CSS_SELECTOR, "p.margin-0px-bottom.font-size14")[0].text.strip()
    consultation_fee = driver.find_element(By.CSS_SELECTOR, "span.bg-theme.text-white.padding-5px-tb.padding-15px-lr.border-radius-5.font-weight-500.sm-padding-5px-lr").text.strip()

    location_element = driver.find_element(By.XPATH, "//img[@alt='map']/parent::p")
    full_text = location_element.text.strip()
    location = full_text.split("experience")[-1].strip()  # everything after 'experience'

    print("Doctor ID:", doctor_id)
    print("Doctor Name:", doctor_name)
    print("Specialization:", specialization)
    print("Qualification:", qualification)
    print("Experience:", experience)
    print("Consultation Fee:", consultation_fee)
    print("Location:", location)

    doctor_dict = {
        "doctor_id": doctor_id,
        "name": doctor_name,
        "specialization": specialization,
        "qualification": qualification,
        "experience": experience,
        "consultation_fee": consultation_fee,
        "location": location
    }

    available_dates_dict = {}

    # --------------------------
    # Step 1: Collect available dates (ignore cloned)
    # --------------------------
    today = datetime.date.today()
    dates = driver.find_elements(By.CSS_SELECTOR, "li.item.link-available")

    available_dates = []
    for date_li in dates:
        classes = date_li.get_attribute("class")
        if "cloned" in classes:
            continue  # skip cloned elements

        data_date = date_li.get_attribute("data-date")
        available_span = date_li.find_elements(By.CSS_SELECTOR, "span.available")
        if available_span:
            available_dates.append((data_date, date_li))

    # --------------------------
    # Step 2: Remove duplicates by date
    # --------------------------
    unique_dates = {}
    for data_date, li_element in available_dates:
        if data_date not in unique_dates:
            unique_dates[data_date] = li_element

    # --------------------------
    # Step 3: Sort dates chronologically
    # --------------------------
    available_dates_sorted = sorted(
        unique_dates.items(),
        key=lambda x: datetime.datetime.strptime(x[0], "%Y-%m-%d").date()
    )

    # --------------------------
    # Step 4: Loop through all future dates
    # --------------------------
    for data_date, li_element in available_dates_sorted:
        date_obj = datetime.datetime.strptime(data_date, "%Y-%m-%d").date()
        if date_obj < today:
            continue  # skip past dates

        # Click the date
        driver.execute_script("arguments[0].click();", li_element)
        time.sleep(1.5)  # wait for slots to load

        # Wait for tabs to appear
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.nav.nav-pills li.nav-item a.nav-link")))
        tabs = driver.find_elements(By.CSS_SELECTOR, "ul.nav.nav-pills li.nav-item a.nav-link")

        # Collect all slots for this date
        merged_slots = []
        for tab in tabs:
            # Click tab
            driver.execute_script("arguments[0].click();", tab)
            time.sleep(0.5)  # wait for content to load

            tab_id = tab.get_attribute("href").split("#")[-1]
            tab_content = driver.find_element(By.ID, tab_id)

            no_slots = tab_content.find_elements(By.XPATH, ".//p[contains(text(), 'No')]")
            if not no_slots:
                slots = tab_content.find_elements(By.CSS_SELECTOR, "a.timing-available")
                merged_slots.extend([slot.text.strip() for slot in slots if slot.text.strip()])

        # Print results for this date
        if merged_slots:
            print(f"{data_date} slots available:", merged_slots)
        else:
            print(f"No slots available for {data_date}")

        available_dates_dict[data_date] = merged_slots

    driver.quit()

    return doctor_dict, available_dates_dict