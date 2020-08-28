from bs4 import BeautifulSoup
import requests
import urllib.parse
import smtplib

# Setting up entry variables for search parameter and building url string for scraping.
daysAgo = 30
job = "dermatolog"
loc = "Sweden"
URL = "https://se.indeed.com/jobs?q=" + urllib.parse.quote(job) + "&l=" + urllib.parse.quote(loc) + "&fromage=" + str(
    daysAgo)


# Doing some scraping.
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
result = soup.find(id='resultsCol')
print(result.find(attrs={'aria-label': 'Nästa'}))
job_elements = result.find_all('div', class_="jobsearch-SerpJobCard")

#
gmail_user = ''
gmail_password = ''

sent_from = gmail_user
to = ''
subject = "Current joblistings"
body = ""

# Loop through all job containers to extract wanted information.
for element in job_elements:
    # Extracting information and storing in variables.
    title = element.find('a', class_="jobtitle")
    company = element.find('span', class_="company")
    summaryContainer = element.find(class_="summary")
    flavorTexts = summaryContainer.find_all('li')
    location = element.find(class_="location")

    # Getting link for further scraping and getting more information about job.
    jobCode = element['data-jk']
    link = "https://se.indeed.com/viewjob?jk=" + jobCode

    # Write information to file.
    body += ("Role: " + title.text.strip() + "\n")
    body += ("Company: " + company.text.strip() + "\n")
    body += ("Location: " + location.text.strip() + "\n")
    body += ("Link: " + link + "\n")

    # loop through flavortext elements.
    for i, t in enumerate(flavorTexts):
        body += (t.text.strip() + "\n")
    body += "\n"

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, to, subject, body)

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, email_text.encode('utf-8'))
    server.close()

    print("Email Sent")
except Exception as ex:
    print(ex)
