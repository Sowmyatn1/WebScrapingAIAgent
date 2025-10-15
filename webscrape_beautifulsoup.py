import requests
from bs4 import BeautifulSoup
import sqlite3


#url = "https://medicasapp.com/in/doctors-in-bangalore/general-practitioner/dr-b-l-avinash/"
url ="https://www.practo.com/bangalore/doctor/dr-ravishankar-reddy-c-r-diabetologist?practice_id=659126&specialization=General%20Physician&referrer=doctor_listing&page_uid=6acdbe2e-1a45-4791-9646-d563ea872e30"
# 2️⃣ Parse with BeautifulSoup
soup = BeautifulSoup(r.text, 'html.parser')

# 3️⃣ Save to local HTML file
with open("doctor_page.html", "w", encoding="utf-8") as f:
    f.write(soup.prettify())  # prettify formats the HTML nicely

print("HTML saved as doctor_page.html")

# Extract doctor info
name = soup.find('h2', {'class': 'font-size18'}).text.strip()
print(name)
specialization1 = soup.find('p', {'class': 'margin-0px-bottom font-size14 sm-font-size13 font-weight-500 margin-0px-bottom'}).text.strip()
print(specialization1)

# Extract location
img_tag = soup.find('img', {'src': 'https://medicasapp.com/wp-content/themes/divi-child/img/map.svg'})
if img_tag:
    # The location is the text node right after the <img> tag
    location = img_tag.next_sibling.strip()
    print(location)
#extracted location END

# extracted fee
fee_tag = soup.find('span', class_=lambda c: c and 'bg-theme' in c)

if fee_tag:
    fee = fee_tag.get_text(strip=True)
    print(fee)
# extracted fee END



# extract date
# Select only the main tab-content that contains real slots
tab_content = soup.find("div", class_="tab-content margin-30px-left sm-margin-0px-left")

'''
# Find all <a> tags with class 'timing-available' inside this container
for a_tag in tab_content.find_all("a", class_="timing-available"):
    href = a_tag.get("href")
    
    # Skip empty or placeholder hrefs
    if href == "#" or not href:
        continue
    
    # The last part of URL is the date, the two parts before are start and end times
    parts = href.split('/')
    start_time = parts[-3]
    end_time = parts[-2]
    date = parts[-1]
    
    print(f"Date: {date}, Start: {start_time}, End: {end_time}")

'''



html = """
<div class="time-slots-container padding-20px-top clearfix sm-padding-0px-top">
    <ul class="owl-carousel owl-theme time-slots2">
        <li class="item link-available" data-date="2025-10-14" data-timezone="Asia/Kolkata">
            <span>14 Oct</span> 
            <span>Tue</span>
            <span class="available">Available</span>
        </li>
        <li class="item link-available" data-date="2025-10-15" data-timezone="Asia/Kolkata">
            <span>15 Oct</span> 
            <span>Wed</span>
            <span class="available">Available</span>
        </li>
        <li class="item link-available" data-date="2025-10-16" data-timezone="Asia/Kolkata">
            <span>16 Oct</span> 
            <span>Thu</span>
            <span class="available">Available</span>
        </li>
    </ul>
</div>
"""



# Assume html_content contains the full HTML of the page
#soup = BeautifulSoup(html_content, "html.parser")

# Dynamically find the outer container that has class containing "time-slots-container"
container = soup.find("div", class_="time-slots-container")

if container:
    # Find all <li> elements with class "item link-available" inside this container
    li_elements = container.find_all("li", class_="item link-available")
    
    dates = set()  # Using a set to avoid duplicates
    for li in li_elements:
        date = li.get("data-date")
        if date:
            dates.add(date)
    
    # Convert set to sorted list
    dates = sorted(dates)
    print(dates)
else:
    print("Time slots container not found!")





# Connect to DB
conn = sqlite3.connect('doctors.db')
cursor = conn.cursor()

# Example slot extraction
for slot in soup.select('a.timing-available'):
    href = slot['href']
    time = slot.text.strip()
    # parse date, start/end times from URL
    # insert into DB
