import gspread
import re
from google.oauth2.service_account import Credentials
from tabulate import tabulate
from classes import Person,Premise,create_person,create_premise
from pick import pick #https://github.com/wong2/pick

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('applicationDB')

requests = SHEET.worksheet('requests')
actions = SHEET.worksheet('actions')
contact = SHEET.worksheet('contact')
location = SHEET.worksheet('location')

# Master menus
def main_menu():
    """
    To select which menu you would like to do on a request
    """
    menu = pick(['Search menu','Create menu'],'Welcome to python console Public Protection resource system\n\nPlease select one of the below','>>>')[1]

    if menu == 0:
        search_menu()
    else:
        create_menu()

def search_menu():
    """
    To select which search menu you would like select
    """
    menu_title = 'Please select one of the following options'
    selections = ['Search for requests','Search for contacts','Search for location','Main menu']

    selection = pick(selections,menu_title,'>>>')[1]

    if selection == 0:
        find_request_menu()
    elif selection == 1:
        find_contact_menu()
    elif selection == 2:
        find_location_menu()
    else:
        main_menu()

def create_menu():
    """
    To select which create menu you would like select
    """

    menu_title = 'Please select one of the following options'
    selections = ['Create a requests','Create a contacts','Create a location','Main menu']

    selection = pick(selections,menu_title,'>>>')[1]

    if selection == 0:
        create_request()
    elif selection == 1:
        create_record(contact)
    elif selection == 2:
        create_record(location)
    else:
        main_menu()

# Requests
def find_request_menu():
    """
    To select which search you would like to do on a request
    """

    menu_title = 'Please select one of the following options'
    selections = ['Request by ID','Requests by received data','Requests by completed date','Requests by type','Search menu']

    selection = pick(selections,menu_title,'>>>')[1]

    if selection == 0:
        find_by_id(1)
    elif selection == 1:
        find_for_report(1,'Please enter the received date you want to search in dd/mm/yyyy format',4)
    elif selection == 2:
        find_for_report(1,'Please enter the completed date you want to search in dd/mm/yyyy format',5)
    elif selection == 3:
        find_for_report(1,'Please enter either flytip or noise',7)
    else:
        search_menu()

def get_request_details(id,row):
    """
    Prints request details to console
    """
    date_received = requests.cell(row,4).value
    date_completed = requests.cell(row,5).value
    text = requests.cell(row,6).value
    type = requests.cell(row,7).value
    time_to_complete = requests.cell(row,8).value

    print(f'Request ID: {id}\nDate Received: {date_received}\nDate Completed: {date_completed}\nRequest Details: {text}\nType: {type}\nTime to complete: {time_to_complete} days')

    # Asking if user wants to view actions
    actions_view = input('Would you like to view the actions? (1 for yes 2 for no) ')

    if actions_view == '1':
        find_actions(id)
    else:
        search_menu()

def create_request():
    """
    Add new request 
    """
    record = []
    date_test = re.compile(r"^[0-9]{2}/[0-9]{2}/[0-9]{4}$")
    while True:
        #contact id
        contact_search = pick(['By ID','By first name','By last name'],'Please select which way you want to search for the contact','>>>')[1]
        if contact_search == 0:
            print('id')
        elif contact_search == 1:
            print('first name')
        else:
            print('last name')

        #location id
        location_search = pick(['By ID','By street','By postcode'],'Please select which way you want to search for the contact','>>>')[1]
        if location_search == 0:
            print('id')
        elif location_search == 1:
            print('street')
        else:
            print('postcode')

        date_rec = input("What's the date the request was received? (Enter in dd/mm/yyyy format)")
        if not date_test.match(date_rec):
            raise ValueError("The date was entered in the wrong format the format needs to be dd/mm/yyyy")
        date_comp = None
        text = input("What is the request about?")
        type_text = 'Please select the request type:'
        types = ['flytip','noise','abandoned vehicle']
        type = pick(types,type_text,indicator='>>>')[0]
        record.append(date_rec)
        record.append(date_comp)
        record.append(text)
        record.append(type)
        print(record)


# Actions
def find_actions(req_id):
    """
    Finds actions for requests
    """

    results = actions.findall(req_id,in_column=2)

    print_actions(req_id,results)

def print_actions(req_id,results):
    """
    Prints actions report to console
    """
    report = []
    header = ['ID','Details','Date']
    for result in results:
        line = result.row
        details = actions.row_values(line)
        del details [1]
        report.append(details)

    print(f"Actions for Request {req_id}\n{tabulate(report,headers=header,tablefmt='github')}")

    add_to_actions = input('Do you want to add an action? (1 for yes 2 for main menu) \n')
    if add_to_actions == '1':
        add_action(req_id)
    else:
        main_menu()

def add_action(req_id):
    """
    Adds actions to action
    """
    while True:
        record = []
        try:
            text = input('What are the details of the action?\n')
            date_input = input("what's the date of the action? (Enter in dd/mm/yyyy format)\n")
            date_test = re.compile(r"^[0-9]{2}/[0-9]{2}/[0-9]{4}$")
            if not date_test.match(date_input):
                raise ValueError("The date was entered in the wrong format the format needs to be dd/mm/yyyy")
            record.append(int(req_id))
            record.append(text)
            record.append(date_input)       
        except ValueError as e:
            print(e)
        else:
            add_new_record_to_worksheet(record,actions)
            break

# Contact
def find_contact_menu():
    """
    To select which search you would like to do on a request
    """

    
    menu_title = 'Please select one of the following options'
    selections = ['Contact by ID','Contact by first name','Contact by last name','Contact by phone number','All contacts','Search menu']

    selection = pick(selections,menu_title,'>>>')[1]

    if selection == 0:
        find_by_id(3)
    elif selection == 1:
        find_for_report(3,'Please enter first name of contact',2)
    elif selection == 2:
        find_for_report(3,'Please enter last name of contact',3)
    elif selection == 3:
        find_for_report(3,'Please enter phone number of contact',4)
    elif selection == 4:
        display_all(3)
    else:
        search_menu()

def get_contact_details(id,row):
    """
    Prints contact details to console
    """
    first_name = contact.cell(row,2).value
    last_name = contact.cell(row,3).value
    phone = contact.cell(row,4).value
    email = contact.cell(row,5).value

    print(f'Contact ID: {id}\nFirst Name: {first_name}\nLast Name: {last_name}\nPhone: {phone}\nEmail: {email}')

    view_requests = input('Do you want to view all requests from this contact? (1 for yes 2 for no)\n')
    if view_requests == '1':
        report_results(1,id,2)
    else:
        search_menu()

# location
def find_location_menu():
    """
    To select which search you would like to do on a request
    """

    menu_title = 'Please select one of the following options'
    selections = ['Location by ID','Location by house name/number','Location by street name','Location by area','Location by postcode','All locations','Search menu']

    selection = pick(selections,menu_title,'>>>')[1]

    if selection == 0:
        find_by_id(4)
    elif selection == 1:
        find_for_report(4,'Please enter house number of contact',2)
    elif selection == 2:
        find_for_report(4,'Please enter street name',3)
    elif selection == 3:
        find_for_report(4,'Please enter area eg, Port Talbot',4)
    elif selection == 4:
        find_for_report(4,'Please enter postcode eg, sa12 1aa',5)
    elif selection == 5:
        display_all(3)
    else:
        search_menu()

def get_location_details(id,row):
    """
    Prints location details to console
    """
    address1 = location.cell(row,2).value
    address2 = location.cell(row,3).value
    address3 = location.cell(row,4).value
    postcode = location.cell(row,5).value

    print(f'Location ID: {id}\nHouse Number: {address1}\nStreet: {address2}\nArea: {address3}\nPostcode: {postcode}')

    view_requests = input('Do you want to view all requests linked to this location? (1 for yes 2 for no)\n')
    if view_requests == '1':
        report_results(1,id,2)
    else:
        search_menu()

# General Functions
def find_by_id(database):
    """
    Get details from id number
    """

    # Selects what sheet we are searching
    if database == 1:
        selected_database=requests
    elif database == 2:
        selected_database=actions
    elif database == 3:
        selected_database=contact
    else:
        selected_database=location

    id = input('What is the id you would like to view? \n')
    # Finds the id and stores what cell that id is in
    cell = selected_database.find(id,in_column=1)

    line = cell.row

    if database == 1:
        get_request_details(id,line)
    elif database == 2:
        selected_database=actions
    elif database == 3:
        get_contact_details(id,line)
    else:
        get_location_details(id,line)

def find_for_report(database,search,col):
    """
    Obtains search criteria
    """
    search_criteria = input(f'{search}\n')
    report_results(database,search_criteria,col)

def report_results(database,search_criteria,col):
    """
    Gets results for report
    """

    # Selects what sheet we are searching
    if database == 1:
        selected_database=requests
    elif database == 2:
        selected_database=actions
    elif database == 3:
        selected_database=contact
    else:
        selected_database=location

    results = selected_database.findall(search_criteria,in_column=col)

    if database == 1:
        print_report(database,results)
    elif database == 2:
        print_report(database,results)
    elif database == 3:
        print_report(database,results)
    else:
        print_report(database,results)

def print_report(database,results):
    """
    Prints report to console
    """

    # Selects what sheet we are searching
    if database == 1:
        selected_database=requests
        header = ['ID','Received Date','Completed Date','Request Details','Type','Time to complete in days']
    elif database == 2:
        selected_database=actions
        header = ['ID','Details','Date']
    elif database == 3:
        selected_database=contact
        header = ['ID','First Name','Last Name','Phone','Email']
    else:
        selected_database=location
        header = ['ID','House Number','Street','Area','Postcode']

    report = []
    
    for result in results:
        line = result.row
        details = selected_database.row_values(line)
        if database == 1:
            del details[1:3]
        report.append(details)
    
    print(tabulate(report,headers=header,tablefmt='github'))

    search_menu()

def display_all(database):
    """
    Shows all of database in console
    """
    # Selects what sheet we are searching
    if database == 1:
        selected_database=requests
    elif database == 2:
        selected_database=actions
    elif database == 3:
        selected_database=contact
    else:
        selected_database=location

    report = selected_database.get_all_values()

    print(tabulate(report,headers='firstrow',tablefmt='github'))

def create_record(database):
    if database == contact:
        record = create_person()
    elif database == location:
        record = create_premise()

    correct = input('Would you like to create this record? (1 for yes 2 for no) ')
    if correct == '1':
        add_new_record_to_worksheet(record.list(),database)

    else:
        create_menu()

def add_new_record_to_worksheet(record,database):
    """
    Adds new data to worksheet
    """
    print(f'Updating......\n')

    # Get max number in id column for next ID
    all_ids = database.col_values(1)
    del all_ids[0]
    all_ids = [int(i) for i in all_ids]
    new_id = max(all_ids)+1

    record.insert(0,new_id)

    database.append_row(record)

    print(f'{database.title} has updated\n')

    main_menu()

main_menu()