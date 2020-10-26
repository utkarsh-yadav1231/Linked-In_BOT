
#--------------------------------------------------------------------------------------------------
#                        Imports
#--------------------------------------------------------------------------------------------------
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.chrome.options import Options
import pandas as pd
import csv
import re
import sys


#--------------------------------------------------------------------------------------------------
#                       SETTINGS to Change
#--------------------------------------------------------------------------------------------------
 
MY_USERNAME = 'myname1234@gmail.com'
MY_PASSWORD = '1234password1234'

BOT1_filters = 'site:Linkedin.com "Accenture" AND "Bangalore" AND "@gmail.com"'

BOT2_names_to_connect = ['HR/Recruiter Name 1', 'HR/Recruiter Name 2', 'HR/Recruiter Name 3']
BOT2_message_to_connect = "Hi " + name.strip().split(' ')[0] + ",\n\n I Hope all is well! Please accept my connection request.  \nBest regards,\nROHIT SINGHANIA "

BOT3_names_to_message = ['Connection Name 1','Connection Name 2']
BOT3_message = 'Hello! My name is Rohit. \n I understand your time is valuabale. I\'ll only write three bullet points. \n\n Coding since 11th grade. \n\n Have most experience working on Java/Python/Web & Anroid Development/Machine Learning. \n\n Want to work for your company as a software engineer. \n\nBest regards,\n ROHIT SINGHANIA'

BOT4_linkedIn_post_URL = "https://www.linkedin.com/posts/activity-6722028677061783552-kVws/"

chrome_driver_path = 'C:/Users/ut/Desktop/drivers/chromedriver.exe'

#--------------------------------------------------------------------------------------------------
#              Open Chrome browser and then LinkedIn Login Page
#--------------------------------------------------------------------------------------------------

browser = webdriver.Chrome(chrome_driver_path)
browser.get('https://www.linkedin.com/login')

#--------------------------------------------------------------------------------------------------
#                Login into LinkedIn automatically
#--------------------------------------------------------------------------------------------------

browser.find_element_by_id('username').send_keys(MY_USERNAME)
sleep(1)
browser.find_element_by_id('password').send_keys(MY_PASSWORD)
sleep(2)
browser.find_element_by_xpath("//button[@type = 'submit']").click()
sleep(3)



#--------------------------------------------------------------------------------------------------
#                            LINKEDIN BOT 1
#
#      This bot function loops to search company employees, their emails and scrapes all the
#      employees profile details on LinkedIn and stores all the scraped information into
#      a separate csv format (MS excel) file.
#
#      User just have to input the Company Name and Location in the BOT1_filters .  
#--------------------------------------------------------------------------------------------------
        
def bot1():
    # Here this Bot creates a list for all LinkedIn User/ Company employee professional information.
    # Like his/her Name, Profile Page link, Company Name Working in, Job position, YOE, Qualification etcetra.  
    counter = 0
    full_name = []
    first_name = []
    last_name = []
    profile_page = []
    working = []
    position = []
    years_of_experience = []
    years_of_experience_at_that_pos = []
    institute = []
    qualification = []
    time_of_qualification = []
    list_xp = [] # for storing xpaths
    
    
    # Open Google Search Page and search for filters already specified by user beforehand.
    
    google = browser.get("https://www.google.com/")
    #BOT1_filters = 'site:Linkedin.com "Adobe" AND "Bangalore" AND "@gmail.com"'
    browser.find_element_by_name('q').send_keys(BOT1_filters)
    sleep(2)
    browser.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[3]/center/input[1]').click() #clicks on search button
    sleep(4)
    page_no = int(input("\n\n\n Upto what pages you want to get the results,\n Enter page number here (Single Digit Expected): "))
    
    # Below Loop iterates all the pages that come within the range. 
    for page in range(page_no):
        if counter == 1:
            break
        url = browser.current_url
        search_mail = browser.find_elements_by_class_name('IsZvec') # will look for emails in the page description card. 
        google_page = browser.page_source
        source_page = BeautifulSoup(google_page,'lxml') #Selenium hands the google page source to Beautiful Soup for parsing
        google_links = source_page.find_all('div',{'class':'yuRUbf'}) #Finds all the 10 Blue Lines of unvisited links available on the cureent search page results.
        
        #Below loop iterates all the blue links to search for xpaths to append in list_xp( x paths list) later. 
        for links_to_iterate in google_links:
            p_l = links_to_iterate.find('a', href=True)
            p_l = str(p_l)
            p_l = p_l.split()
            list_xp.append(p_l[1].strip('href=').strip('""'))
        
        #Below loop searches for emails using findall ( text@text.text) and prints emails.
        for i in search_mail:
            mail = emails = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", i.text)
            print(mail)
        
        # Below loop runs a loop for finding xpath from the (list_xp) xpaths list stored earlier.
        # Looks for information of each employee by opening below 
        for x_path in list_xp:
            try:
                browser.get(x_path)
                sleep(2)
                browser.execute_script("window.scrollTo(0,800)","") # 0 to 800 slides the scroll bar to 800 pixels down
                sleep(7)
            except:
                    try:
                        sheet = pd.DataFrame([full_name,first_name,last_name,working,profile_page,position,years_of_experience,years_of_experience_at_that_pos,institute,qualification,time_of_qualification])
                        sheet.to_csv('FINAL Sheet2.csv')
                        quit()
                    except:
                        print("File is open please close the file")
                        #input("Done? ")
                        sheet = pd.DataFrame([full_name,first_name,last_name,working,profile_page,position,years_of_experience,years_of_experience_at_that_pos,institute,qualification,time_of_qualification])
                        sheet.to_csv('FINAL Sheet2.csv')
                        quit()
            try: 
                src = browser.page_source
                html_page = BeautifulSoup(src, "lxml") #Selenium hands the page source to Beautiful Soup for parsing 
                profile_link = browser.current_url
                profile_link = str(profile_link)
                profile_page.append(profile_link) # It appends the profile links of the employees into the Profile_page = [] list 
            except:
                profile_page.append("Could not extract profile link.")
            try:
                # extracts the first and last name of all the employees and appends into the list later.
                name_div = html_page.find('div', {'class':'flex-1 mr5'}) 
                name_loc = name_div.find_all('ul')
                name = name_loc[0].find('li').get_text().strip()
                full_name.append(name)
                name = name.split()
                first = name[0]
                last = name[-1]

                first_name.append(first) #appends name into the list.
                last_name.append(last)
            except:
                full_name.append("Full Name not found")
                first_name.append("Not found")
                last_name.append("Not found")
            try:
                # EXTRACTS Profile Title/Position. 
                profile_title = name_div.find('h2', {'class':'mt1 t-18 t-black t-normal break-words'}).get_text().strip()
                position.append(profile_title)
            except:
                position.append('No profile title/Job Position found')
            try:
                # EXTRACTS Years of Experience of the employee and appends later
                experience = html_page.find('h4',{'class':'t-14 t-black t-normal'})
                years_of_experience.append(experience.get_text().strip('Total Duration\n'))
            except:
                years_of_experience.append("No experience provided")
            try:
                # EXTRACTS Years of Experience at that position and appends later
                time_dur = browser.find_element_by_class_name('pv-entity__bullet-item-v2').text
                years_of_experience_at_that_pos.append(time_dur)
            except:
                years_of_experience_at_that_pos.append("YOE at that position Not provided")
            try:
                # EXTRACTS Institute from which the employee completed his education and appends it later.
                edu = browser.find_element_by_class_name('pv-entity__school-name').text
                institute.append(edu)
            except:
                institute.append("Institute Not provided")
            try:
                # EXTRACTS Qualification/Degree of the employee and appends later
                spec = browser.find_elements_by_class_name('pv-entity__comma-item')
                qualification.append(spec[0].text + " " + spec[1].text)
            except:
                qualification.append("Not provided")
            try:
                # EXTRACTS Time of Qualification of the employee and appends later
                time_of_edu = browser.find_elements_by_tag_name('time')
                time_of_qualification.append(time_of_edu[0].text + "-" + time_of_edu[1].text)
            except:
                time_of_qualification.append("Not provided")
            try:
                # EXTRACTS Work Experience of the employee and appends later
                work = browser.find_element_by_class_name('pv-top-card--experience-list-item').text
                working.append(work)
            except:
                working.append("Not provided")
            
            # If last employee in the x paths list occurs then it looks for the Next button to click it.
            if x_path == list_xp[len(list_xp) -1]:
                try:
                    browser.get(url)
                    sleep(5)
                    browser.find_element_by_link_text('Next').click()
                    list_xp.clear() #clears the x_path list
                except: #if next button is not found, then this exception code is executed.
                    try:
                        counter = counter + 1 #increments the counter, so that this BOT doesn't loops again as it reached on the last page.
                        # A Data frame is a two-dimensional data structure, i.e., data is aligned in a tabular fashion 
                        # in rows and columns.
                        sheet = pd.DataFrame([full_name,first_name,last_name,working,profile_page,position,years_of_experience,years_of_experience_at_that_pos,institute,qualification,time_of_qualification])
                        # Above line creates DataFrame using a list
                        sheet.to_csv('FINAL Sheet1.csv') # prepares the csv (comma separate value) format file from sheet  
                        print("\n\n\nExcel sheet is ready... 1")
                    except:
                        counter = counter + 1
                        print("\n\n\nFile is open please close the file 2") #To Close already opened file
                        input("Done? ")
                        sheet = pd.DataFrame([full_name,first_name,last_name,working,profile_page,position,years_of_experience,years_of_experience_at_that_pos,institute,qualification,time_of_qualification])
                        sheet.to_csv('FINAL Sheet1.csv')
                        print("\n\n\n Excel sheet is ready... 2")
    try:
        if counter == 0:
            sheet = pd.DataFrame([full_name,first_name,last_name,working,profile_page,position,years_of_experience,years_of_experience_at_that_pos,institute,qualification,time_of_qualification])
            sheet.to_csv('FINAL Sheet1.csv')
            print("\n\n\n Excel sheet is ready...3") # prepares the csv (comma separate value) format file from sheet 
    except:
        if counter == 0:
            print("\n\n\nFile is open please close the file") #To Close already opened file
            input("Done? ")
            sheet = pd.DataFrame([full_name,first_name,last_name,working,profile_page,position,years_of_experience,years_of_experience_at_that_pos,institute,qualification,time_of_qualification])
            sheet.to_csv('FINAL Sheet1.csv')
            print("\n\n\n Excel sheet is ready...4") # prepares the csv (comma separate value) format file from sheet 




#--------------------------------------------------------------------------------------------------
#                            LINKEDIN BOT 2
#
#      This bot function loops to search for all the names on LinkedIn (specified by user)
#      and automatically sends connection request along with personalized message to them.  
#--------------------------------------------------------------------------------------------------

def bot2():
    # Lookup names, add a note, and send connection request    
    for name in BOT2_names_to_connect:
        # Lookup name
        browser.find_element_by_xpath("//input[@type = 'text']").send_keys(name)
        sleep(1.5)
        browser.find_element_by_xpath("//input[@type = 'text']").send_keys(Keys.ENTER)
        sleep(1.5)

        # 'Add a Note' to send along with connection request
        browser.find_element_by_xpath("//button[text() = 'Connect']").click()
        sleep(1.5)
        browser.find_element_by_xpath("//span[text()='Add a note']").click()
        sleep(1.5)

        #BOT2_message_to_connect = "Hi " + name.strip().split(' ')[0] + ",\n\n I Hope all is well! Please accept my connection request.  \nBest regards,\nROHIT "

        browser.find_element_by_xpath("//textarea").send_keys(BOT2_message_to_connect)
        sleep(1.5)

        browser.find_element_by_xpath("//span[text()='Send']").click()
        sleep(1.5)

        browser.find_element_by_xpath("//input[@type = 'text']").clear()
        sleep(15)
        
        browser.close()

        
#--------------------------------------------------------------------------------------------------
#                            LINKEDIN BOT 3
#
#      This bot function loops to search for present connections (specified by user)
#      and automatically sends personalized message to them.  
#--------------------------------------------------------------------------------------------------
        
def bot3():
    #Search for connections and send below Customized message
    #message = 'Hello! I Hope all is well at your home! \n\nBest regards,\nROHIT'
    ctr = 0
    #Lookup names and send messages
    #BOT3_names_to_message = ['LinkedIn User 1','LinkedIn User 2']
    
    for name in BOT3_names_to_message:

        browser.find_element_by_xpath("//input[@type = 'text']").send_keys(name)
        sleep(1.5)
        browser.find_element_by_xpath("//input[@type = 'text']").send_keys(Keys.ENTER)
        sleep(1.5)

        browser.find_element_by_xpath("//button[text() = 'Message']").click()
        sleep(1)
        
        # For sending message to first person, ctr is 0 and to open another message box
        # on the side of the first one, then ctr is incremented by 1 so that it opens another
        # box everytime,instead of pasting same message in the first box again and again. 
        
        if ctr == 0:
            browser.find_element_by_xpath("//div[@role = 'textbox']").send_keys(message)
        else:
            browser.find_elements_by_xpath("//div[@role = 'textbox']")[ctr].send_keys(message)
        sleep(1.5)

        if ctr == 0:
            browser.find_element_by_xpath("//button[@type = 'submit']").click()
        else:
            browser.find_elements_by_xpath("//button[@type = 'submit']")[ctr].click()

        ctr += 1
        sleep(1)
        browser.find_element_by_xpath("//input[@type = 'text']").clear()



#--------------------------------------------------------------------------------------------------
#                            LINKEDIN BOT 4
#
#      This bot function loops to search for all the emails on the LinkedIn post (specified by user)
#      and stores all the mails scraped into a separate csv format (MS excel) file.  
#--------------------------------------------------------------------------------------------------
        
def bot4():
    # Any url of linkedIn post from where the emails are to be fetched
    browser.get(BOT4_linkedIn_post_URL)
    
    # Alternate posts links shared below for testing purpose of this BOT4. 
    # browser.get("https://www.linkedin.com/posts/activity-6722028677061783552-kVws/")
    # browser.get("https://www.linkedin.com/posts/matchai_covid19-hiring-tech-activity-6652411320551464960-Gh_1")
    # browser.get("https://www.linkedin.com/posts/sarvothama-thonse-kini-60908478_ibm-is-hiring-a-couple-of-finance-related-activity-6721496956994121728-Xzwi/")
    # button=browser.find_element_by_xpath("//*[@class='artdeco-button__text']")
    # button.click()

    sleep(4)
    hasLoadMore = True
    while hasLoadMore:
        print("\n Loading all comments in this post, Please wait.")
        sleep(3)
        try:
            print("...")
            if browser.find_element_by_xpath("//button[@class='comments-comments-list__load-more-comments-button artdeco-button artdeco-button--muted artdeco-button--1 artdeco-button--tertiary ember-view']"):
                browser.find_element_by_xpath("//button[@class='comments-comments-list__load-more-comments-button artdeco-button artdeco-button--muted artdeco-button--1 artdeco-button--tertiary ember-view']").click()
            
        except:
            print("\n All comments loaded successfully. ")
            hasLoadMore = False
    
    # search for all emails present in the post comments section 
    
    emails = browser.find_elements_by_css_selector("p a")
    #names = browser.find_elements_by_css_selector("h3 span")
    
    
    # Open BOT_4 Email csv file in write mode.
    
    with open('BOT_4_Emails List.csv', 'w', newline='') as f:
        fieldnames = ['Emails']
        thewriter = csv.DictWriter(f, fieldnames=fieldnames)
        thewriter.writeheader() #write Emails in header of excel column
        # Run a loop and search for all emails present in the comment section, 
        # by looking for '@' in all the comments.
        # and then write the whole email text in the row below email column.
        for ele in emails:      
            if (ele.text.find('@') != -1):
                thewriter.writerow({'Emails': ele.text})

        
#----------------------------------------------------------------------------------------------------------------------
#                       Call BOT function here, you want to execute.
#             All the BOT functions are specified above the function signature.  
#
#            Remove the 'hash'(#) and execute the particular bot you want to execute according to your preference.
#----------------------------------------------------------------------------------------------------------------------

#bot1()
#bot2()
#bot3()
#bot4()
print('\n\n\n Kudos User !! Your BOT Program executed successfully. ')



#--------------------------------------------------------------------------------------------------
#                       THIS WHOLE PROGRAM ENDS HERE
#                           WRITTEN BY UTKARSH  
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
"""                        WORKING OF ABOVE SCRIPT Explained below 

Important Steps to Run above script :

Step 1) Download Chrome Webdriver from the link below. Download Link : " https://chromedriver.chromium.org/downloads "

Step 2) Store the Driver at your desired location and paste the driver path into Line 30 ( Settings to change )
Step 3) Write your email and password in (Settings to change)
Step 4) Run the bot function according to your requirement from line number(370-373)
        Enjoy !!

-------------------------------------------------------------------------------------------------------------------
                                Other Useful Information 
-------------------------------------------------------------------------------------------------------------------

1) Use of BeautifulSoup :
        Beautiful Soup parses HTML into an easy machine readable tree format to 
        extract DOM Elements quickly. 
        Beautiful Soup is a Python library for pulling data out of HTML and XML files.
        It allows extraction of a certain paragraph and table elements with certain HTML ID/Class/XPATH.       
        Whenever we need a quick and dirty way approach to extract information online we can use BS.

2) Importing re : 
        (Regular Expression-re ) is a sequence of characters that forms a search pattern.
        RegEx can be used to check if a string contains the specified search pattern.


3) Use of Selenium :
        Selenium is a tool designed to automate Web Browser.
        It is commonly used by Quality Assurance (QA) engineers to automate their testings 
        using Selenium Browser application.
        Additionally, it is very useful to web scrape because of these automation capabilities:
            a) Clicking specific form buttons
            b) Inputting information in text fields
            c) Extracting the DOM elements for browser HTML code
          
4) How Selenium works :
        
        1) find_element by ID to return the relevant category listing.
        category_element = driver.find_element(By.ID,'Level_1_Category_No1').text;
        
        

5)  import sys :
    The sys module is a set of functions which provide crucial information 
    about how your Python script is interacting with the host system




"""
#                        
#--------------------------------------------------------------------------------------------------