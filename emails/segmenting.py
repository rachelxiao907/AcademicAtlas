import csv

### READ THE CSV FILE AND ORGANIZE ALL THE DATA ###

# map the department to a list of emails
emails_by_department = {}

# COPY DATA OF THE WHOLE ROW

class Email:
    #name,position,department,phone,email,school_name,city,state,zip,staff_url,webpage
    def __init__(self, name, position, department, phone, email, school_name, city, state, zip, staff_url, webpage, values):
        self.name = name
        self.position = position
        self.department = department
        self.phone = phone
        self.email = email
        self.school_name = school_name
        self.city = city
        self.state = state
        self.zip = zip
        self.staff_url = staff_url
        self.webpage = webpage
        self.values = values

    def change_email(self, email):
        self.email = email

    def get_values(self):
        return self.values

    def get_department(self):
        return self.department

    def get_position(self):
        return self.position

with open('master_sheet.csv') as csv_file:
    # each row is a dictionary where the headers are keys and the row's values are the values
    reader = csv.DictReader(csv_file)

    # iterate through all the rows
    for row in reader:
        email = Email(row['name'], row['position'], row['department'], row['phone'], row['email'], row['school_name'], row['city'], row['state'], row['zip'], row['staff_url'], row['webpage'], row.values())
        department = row['department']

        # # if there is no department provided
        # if department == '':
        #     department = 'Other'

        # iterate through all the values to make sure we get the email if the email isn't in the right column
        if '@' not in row['email']:
            for e in row.values():
                if '@' in e:
                    email.change_email(e)
        
        # if the department does not exist in the dictionary
        if department not in emails_by_department:
            emails_by_department[department] = [] #create a list associated to it
        emails_by_department[department].append(email)
#print(emails_by_department.keys())



### FINDING THE DEPARTMENTS WITH THE MOST VALUE BY USING COUNTS ###

# i made this because some of the csv department values are a long blurb
# of why they are a teachers. the columns aren't all correctly populated.
# the department may not be in the correct column, so we need some sort of
# basis of departments to cross check it and look for those keywords in the
# whole dictionary for the row data and then determine the department 

# minimum specifies the desired substance needed by a department
def create_file_of_departments(minimum):
    filename = 'departments_over_' + str(minimum) + '_emails.txt'

    department_count = {} #number of emails per department

    with open(filename, 'w') as file:
        for department in emails_by_department:
            count = len(emails_by_department[department])
            if count > minimum:
                department_count[department] = count
                file.write(department + '\n')
    #print(department_count)
#create_file_of_departments(20)



### GROUPING DEPARTMENTS BY CATEGORIES ###

# what should i group by? key words that stood out to you with high substance?
# save the emails that don't fit into the categories

# TODO: Segment by these categories and synonyms --> go through the positions too
# Science, Admins, Athletics, Language, Math, Counselors, History, Arts, English
# APIs for synonyms

# SHARE SERGEY'S SEGMENTING CODE ON DOCS
# GROUP BY SCIENCE AND MATH

# each email is an object with its information
def group_by_category(department):
    department = department.lower()
    
    filename = str(department) + '_emails.csv'

    emails = ['name,position,department,phone,email,school_name,city,state,zip,staff_url,webpage'.split(",")]

    for key in emails_by_department:
        if department in key.lower(): #look for key word in all departments
            emails.extend(emails_by_department[key])
        else:
            department_emails = emails_by_department[key]
            for email in department_emails:
                # data = email.get_values()
                # for value in data:
                #     if department in value.lower():
                #         # ERROR IF THE DEPARTMENT ISN'T IN THE DEPARTMENT COLUMN OF THE CSV
                #         #emails.extend(emails_by_department[value])
                #         emails.extend(emails_by_department[key])
                if department in email.get_department() or department in email.get_position():
                    emails.append(email)

    with open(filename, 'w') as file:
        writer = csv.writer(file)

        writer.writerow(emails.pop(0))

        for email in emails:
            writer.writerow(email.get_values())
group_by_category('math')