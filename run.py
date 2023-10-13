import gspread
from google.oauth2.service_account import Credentials
from tabulate import tabulate

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

def main_menu():
    """
    To select which menu you would like to do on a request
    """
    menu=True

    while menu:
        print('1. For search menu\n2. For create menu')
        selection = input('Please enter the number of what you would like to search by \n')
        if selection == '1':
            search_menu()
            menu = False
        elif selection == '2':
            print('2')
            menu = False
        else:
            print(f'Invalid selection: You selected {selection} please try again')

def search_menu():
    """
    To select which menu you would like select
    """
    menu=True

    while menu:
        print('1. Search for requests\n2. Search for contacts\n3. Search for location')
        selection = input('Please enter the number of what you would like to search by \n')
        if selection == '1':
            find_request_menu()
            menu = False
        elif selection == '2':
            find_contact_menu()
            menu = False
        elif selection == '3':
            print('3')
            menu = False
        else:
            print(f'Invalid selection: You selected {selection} please try again')

# Requests
def find_request_menu():
    """
    To select which search you would like to do on a request
    """
    menu=True

    while menu:
        print('1. Search by request ID\n2. Search by received date\n3. Search by completed date\n4. Search by type')
        selection = input('Please enter the number of what you would like to search by \n')
        if selection == '1':
            find_by_id(1)
            menu = False
        elif selection == '2':
            find_for_report(1,'Please enter the received date you want to search in dd/mm/yyyy format',4)
            menu = False
        elif selection == '3':
            find_for_report(1,'Please enter the completed date you want to search in dd/mm/yyyy format',5)
            menu = False
        elif selection == '4':
            find_for_report(1,'Please enter either flytip or noise',7)
            menu = False
        else:
            print(f'Invalid selection: You selected {selection} please try again')

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
        find_request_menu()

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

# Contact
def find_contact_menu():
    """
    To select which search you would like to do on a request
    """
    menu=True

    while menu:
        print('1. Search by contact ID\n2. Search by first name\n3. Search by last name\n4. Search by phone number\n5. Display all contacts')
        selection = input('Please enter the number of what you would like to search by \n')
        if selection == '1':
            find_by_id(3)
            menu = False
        elif selection == '2':
            find_for_report(3,'Please enter first name of contact',2)
            menu = False
        elif selection == '3':
            find_for_report(3,'Please enter last name of contact',3)
            menu = False
        elif selection == '4':
            find_for_report(3,'Please enter phone number of contact',4)
            menu = False
        elif selection == '5':
            display_all(3)
        else:
            print(f'Invalid selection: You selected {selection} please try again')

def get_contact_details(id,row):
    """
    Prints contact details to console
    """
    first_name = contact.cell(row,2).value
    last_name = contact.cell(row,3).value
    phone = contact.cell(row,4).value
    email = contact.cell(row,5).value

    print(f'Contact ID: {id}\nFirst Name: {first_name}\nLast Name: {last_name}\nPhone: {phone}\nEmail: {email}')

# General search Functions
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

    id = input('What is the request id you would like to view? \n')
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
        selected_database=location

def find_for_report(database,search,col):
    """
    Finds for report
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

    search_criteria = input(f'{search}\n')

    results = selected_database.findall(search_criteria,in_column=col)

    if database == 1:
        print_report(database,results)
    elif database == 2:
        print_report(database,results)
    elif database == 3:
        print_report(database,results)
    else:
        print('location')

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


main_menu()