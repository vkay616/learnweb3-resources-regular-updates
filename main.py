import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

URLS = ["https://learnweb3.io/minis/", "https://learnweb3.io/lessons/", "https://learnweb3.io/degrees/"]
LEADERBOARD_URL = 'https://learnweb3.io/leaderboard/'
PREFIX_URL = "https://learnweb3.io"

minis_count = 0
minis_url = list()
minis_title = list()

lessons_count = 0
lessons_url = list()
lessons_title = list()

degrees_count = 0
degrees_url = list()
degrees_title = list()


def get_html(url):
    return requests.get(url, timeout=None).text

def get_resources(url, course_type):
    urls = list()
    titles = list()
    date_added = list()

    try:
        source_code = get_html(url)
        soup = BeautifulSoup(source_code, 'html.parser')
        whole_section = soup.find_all('section')
        courses = BeautifulSoup(str(whole_section), 'html.parser').find_all('a')
        for course in courses:
            if course_type in course['href']:
                urls.append(course['href'])

        count = len(urls)

        if course_type == 'degrees':
            course_titles = soup.select("h3.flex")
        else:
            course_titles = soup.select("h3.flex.justify-between.text-xl.font-medium")
        for course_title in course_titles:
            titles.append(course_title.get_text())

        dates = soup.select('span.text-xs.text-gray-700')
        for d in dates:
            date_added.append(d.get_text())

        return count, titles, urls, date_added

    except Exception as e:
        print("Error:", e)

# For getting the top 5 people in the leaderboard

chrome_options = Options()

chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-notifications")

driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
driver.get(LEADERBOARD_URL)

usernames = list()
github_links = list()

for i in range(1,6):
    username = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, f'//*[@id="__next"]/div/div[1]/div[1]/div/main/div/div/ul/li[{i}]/a/div/div[1]/div[3]/div/p'))
    )

    usernames.append(username.text)

profile_links = [f'https://learnweb3.io/u/{username}' for username in usernames]

# print(profile_links)

for link in profile_links:
    driver.get(link)

    github = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div[1]/div[1]/div/div[4]/div/div[1]/div[2]/div/a[1]'))
    )

    github_links.append(github.get_attribute('href'))

driver.close()

top_5_leaderboard = list()

for i in range(5):
    top_5_leaderboard.append(f"**{i+1}. [{usernames[i]}]({github_links[i]})**\n\n")


# For all the different resources like minis, lessons and degrees
  
minis_count, minis_titles, minis_urls, minis_dates = get_resources(URLS[0], "minis")
lessons_count, lessons_titles, lessons_urls, lessons_dates = get_resources(URLS[1], "lessons")
degrees_count, degrees_titles, degrees_urls, degrees_dates = get_resources(URLS[2], "degrees")

minis_urls = [PREFIX_URL + url for url in minis_urls]
lessons_urls = [PREFIX_URL + url for url in lessons_urls]
degrees_urls = [PREFIX_URL + url for url in degrees_urls]

total_count = minis_count + lessons_count + degrees_count

heading = "# LearnWeb3 Platform Resource Updates \n"

description = f"This repository scraps all the resources (Minis, Lessons and Degrees) available on [LearnWeb3]({PREFIX_URL}) platform every hour and updates the README file with the total number of resources, the first 5 resources available from each category. \n"

total_resources_heading = f"#### **Total Number of Resources on LearnWeb3: {total_count}** \n"

# for minis content

recent_minis_titles = minis_titles[:5]
recent_minis_urls = minis_urls[:5]
recent_minis_dates = minis_dates[:5]

recent_minis = list()

for i in range(5):
    recent_minis.append(f"**{i+1}. [{recent_minis_titles[i]}]({recent_minis_urls[i]})** | Date Added: {recent_minis_dates[i]} \n\n")


minis_heading = "## Minis on LearnWeb3 \n"
minis_description = f"Total Number of Minis available: {minis_count} \n #### First 5 Minis \n"

# for lessons content

recent_lessons_titles = lessons_titles[:5]
recent_lessons_urls = lessons_urls[:5]
recent_lessons_dates = lessons_dates[:5]

recent_lessons = list()

for i in range(5):
    recent_lessons.append(f"**{i+1}. [{recent_lessons_titles[i]}]({recent_lessons_urls[i]})** | Date Added: {recent_lessons_dates[i]} \n\n")


lessons_heading = "## Lessons on LearnWeb3 \n"
lessons_description = f"Total Number of Lessons available: {lessons_count} \n #### First 5 Lessons \n"

# for degrees content
recent_degrees = list()

if degrees_count > 5:
    recent_degrees_titles = degrees_titles[:5]
    recent_degrees_urls = degrees_urls[:5]
    recent_degrees_dates = degrees_dates[:5]


    for i in range(5):
        recent_degrees.append(f"**{i+1}. [{recent_degrees_titles[i]}]({recent_degrees_urls[i]})** | Date Added: {recent_degrees_dates[i]} \n\n")

else:
    for i in range(degrees_count):
        recent_degrees.append(f"**{i+1}. [{degrees_titles[i]}]({degrees_urls[i]})** | Date Added: {degrees_dates[i]} \n\n")



degrees_heading = "## Degrees on LearnWeb3 \n"
if degrees_count > 5:
    degrees_description = f"Total Number of Degrees available: {degrees_count} \n #### First 5 Degrees \n"
else:
    degrees_description = f"Total Number of Degrees available: {degrees_count} \n #### All Degrees \n"

leaderboard_heading = "## Leaderboard (Top 5) \n"

# full README content

README_CONTENT = heading + description + total_resources_heading + minis_heading + minis_description + "".join(recent_minis) + lessons_heading + lessons_description + "".join(recent_lessons) + degrees_heading + degrees_description + "".join(recent_degrees) + leaderboard_heading + "".join(top_5_leaderboard)

with open('README.md', 'w') as readme:
    readme.write(README_CONTENT)
