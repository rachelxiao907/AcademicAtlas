from bs4 import BeautifulSoup
import requests
import csv

website = 'https://hs.sas.upenn.edu'
college = 'University of Pennsylvania'

# Fetch the HTML content
url = 'https://hs.sas.upenn.edu/academic-year-program/courses'
response = requests.get(url) #send an HTTP request to the web page
html = response.content #get the HTML content

# Create BeautifulSoup object
soup = BeautifulSoup(html, 'html.parser')

# Find courses
# rows = soup.find_all('td', class_='views-field-title')
tables = soup.find('div', class_='paragraph__column')
a_tags = tables.find_all('a') # all links to a course

data = []

# For each course
for a_tag in a_tags:
    course_url = website + a_tag['href']
    course_html = requests.get(course_url).content
    content = BeautifulSoup(course_html, 'html.parser')

    course = {}
    course['college'] = college
    
    info = content.find('div', class_="col-md-9").find_all('div', class_='field')
    program_name = info.pop(0).find('a').get_text()
    course['program_name'] = program_name
    course_title = a_tag.get_text()
    #print(course_title)
    course['course_title'] = course_title
    course['program_category'] = ""

    term = ""
    for row in info:
        key = row.find('div', class_='field--label').get_text()
        value = row.find('div', class_='field--item').get_text()
        if key == 'Course Description:':
            course['course_description'] = value
        elif key == 'Term':
            term = value
    
    # Application and admissions scraping
    admissions_html = requests.get(website + '/academic-year-program/admissions', 'html.parser').content
    admissions = BeautifulSoup(admissions_html, 'html.parser')

    course['city'] = "Philadelphia"
    course['state'] = "PA"
    course['zip_code'] = ""
    course['country'] = "United States"
    course['residential'] = "no"

    course['application'] = "yes"
    course['transcript'] = "yes"
    course['letter_of_recommendation'] = "yes" 
    course['counselor_report'] = "no"
    course['test_scores'] = "yes"
    course['toefl_or_english_exam'] = "yes"
    course['app_fee'] = 75
    application_deadlines = iter(admissions.find_all('td'))
    for x in application_deadlines:
        if x == term:
            course['app_date'] = next(application_deadlines)
            break

    course['enrollment_fee'] = 1,500
    course['credit_offerred'] = "college"
    course['tuition'] = 4,222
    course['start_date_term_1'] = "" #TERM?? they're in a pdf but it's outdated
    course['end_date_term_1'] = ""
    course['start_date_term_2'] = ""
    course['end_date_term_2'] = ""
    course['start_date_term_3'] = ""
    course['end_date_term_3'] = ""

    course['elligibility_requirements'] = "For juniors and seniors attending a local high school. Students can start applying the summer after grade 10. Not designed for students who have already graduated high school, nor for those admitted to Penn through the Early Decision option. Scores in the 85th percentile or greater in all sections of their standardized tests (SAT, PSAT, ACT). (Students who have not taken any standardized tests may submit an additional letter of recommendation.) A variety of extracurricular interests."
    course['grades'] = 11, 12
    
    course['link'] = course_url
    course['tags'] = ""
    course['images'] = ""
    course['blurbs'] = ""
    course['college_label'] = ""
    
    data.append(course)

with open('upenn_data.csv', 'w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
    writer.writeheader()
    
    for item in data:
        writer.writerow(item)
