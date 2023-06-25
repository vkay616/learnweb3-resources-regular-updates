import requests
from bs4 import BeautifulSoup

URLS = ["https://learnweb3.io/minis/", "https://learnweb3.io/lessons/", "https://learnweb3.io/degrees/"]
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
    return requests.get(url).text

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

# full README content

README_CONTENT = heading + description + total_resources_heading + minis_heading + minis_description + "".join(recent_minis) + lessons_heading + lessons_description + "".join(recent_lessons) + degrees_heading + degrees_description + "".join(recent_degrees)

with open('README.md', 'w') as readme:
    readme.write(README_CONTENT)