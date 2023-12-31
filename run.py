import re
import datetime
import pandas as pd
import numpy as np
import gspread
from google.oauth2.service_account import Credentials
from pick import pick  # https://github.com/wong2/pick
from tabulate import tabulate
from classes import create_person, create_premise

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
    menu = pick(['Search menu', 'Create menu'],
                ('Welcome to python console Public Protection resource system\n'
                 '\nPlease select one of the below'), '>>>')[1]

    if menu == 0:
        search_menu()
    else:
        create_menu()

def search_menu():
    """
    To select which search menu you would like select
    """
    menu_title = 'Please select one of the following options'
    selections = ['Search for requests',
                  'Search for contacts',
                  'Search for location',
                  'Print statistics report',
                  'Main menu']

    selection = pick(selections, menu_title, '>>>')[1]

    if selection == 0:
        find_request_menu()
    elif selection == 1:
        find_contact_menu()
    elif selection == 2:
        find_location_menu()
    elif selection == 3:
        print_stats()
    else:
        main_menu()

def create_menu():
    """
    To select which create menu you would like select
    """
    menu_title = 'Please select one of the following options'
    selections = ['Create a requests',
                  'Create a contacts',
                  'Create a location',
                  'Main menu']

    selection = pick(selections, menu_title, '>>>')[1]

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
    selections = ['Request by ID',
                  'Requests by received data',
                  'Requests by completed date',
                  'Requests by type',
                  'Search menu']

    selection = pick(selections, menu_title, '>>>')[1]

    if selection == 0:
        find_by_id(requests, None)
    elif selection == 1:
        find_for_report(
            requests, ('Please enter the received '
                       'date you want to search in dd/mm/yyyy format'), 4, 0)
    elif selection == 2:
        find_for_report(
            requests, ('Please enter the completed date you '
                       'want to search in dd/mm/yyyy format'), 5, 0)
    elif selection == 3:
        find_for_report(requests, 'Please enter request type', 7, 0)
    else:
        search_menu()


def get_request_details(rec_id, row):
    """
    Prints request details to console
    """

    contact_info = int(requests.cell(row, 2).value)+1
    location_info = int(requests.cell(row, 3).value)+1

    date_received = requests.cell(row, 4).value
    date_completed = requests.cell(row, 5).value
    text = requests.cell(row, 6).value
    rec_type = requests.cell(row, 7).value
    time_to_complete = requests.cell(row, 8).value
    contact_name = contact.cell(
        contact_info, 2).value + ' ' + contact.cell(contact_info, 3).value
    contact_number = contact.cell(contact_info, 4).value
    contact_email = contact.cell(contact_info, 5).value
    address1 = location.cell(location_info, 2).value
    address2 = location.cell(location_info, 3).value
    address3 = location.cell(location_info, 4).value
    postcode = location.cell(location_info, 5).value

    print((f'\nRequest ID: {rec_id}\n'
           'Contact Information\n'
           f'Contact Name: {contact_name}\n'
           f'Contact Number: {contact_number}\n'
           f'Contact Email: {contact_email}\n'
           'Location Information\n'
           f'House number/building number: {address1}\n'
           f'Street: {address2}\n'
           f'Area: {address3}\n'
           f'Postcode: {postcode}\n'
           f'Date Received: {date_received}\n'
           f'Date Completed: {date_completed}\n'
           f'Request Details: {text}\n'
           f'Type: {rec_type}\n'
           f'Time to complete: {time_to_complete} days'))

    input('Click enter to continue\n')
    menu_title = 'Please select one of the following options'
    selections = ['View actions', 'Add completed date',
                  'Search Menu', 'Main menu']

    selection = pick(selections, menu_title, '>>>')[1]
    if selection == 0:
        find_actions(rec_id)
    elif selection == 1:
        add_completed_date(rec_id, row, date_received)
    elif selection == 2:
        search_menu()
    else:
        main_menu()


def create_request():
    """
    Add new request 
    """
    selected_contact = ''
    selected_location = ''
    record = []
    while True:
        try:
            # contact id
            while selected_contact == '':
                contact_search = pick(['By ID',
                                        'By first name',
                                        'By last name'],
                                        ('Please select which way you want to'
                                        ' search for the contact'), '>>>')[1]
                if contact_search == 0:
                    while True:
                        try:
                            selected_contact = int(input('What is the id you would like to select? \n'))
                        except ValueError:
                            print('Entries must be an integer')
                        else:
                            break
                elif contact_search == 1:
                    selected_contact = find_for_report(
                        contact, 'Please enter first name of contact', 2, 1)
                else:
                    selected_contact = find_for_report(
                        contact, 'Please enter last name of contact', 3, 1)


            # location id
            while selected_location == '':
                location_search = pick(['By ID',
                                        'By street',
                                        'By area',
                                        'By postcode'],
                                        ('Please select which way you want to '
                                        'search for the locations'), '>>>')[1]
                if location_search == 0:
                    while True:
                        try:
                            selected_location = int(input('What is the id you would like to select? \n'))
                        except ValueError:
                            print('Entries must be an integer')
                        else:
                            break
                elif location_search == 1:
                    selected_location = find_for_report(
                        location, 'Please enter street name', 3, 1)
                elif location_search == 2:
                    selected_location = find_for_report(
                        location, 'Please enter area eg, Port Talbot', 4, 1)
                else:
                    selected_location = find_for_report(
                        location, 'Please enter postcode eg, sa12 1aa', 5, 1)


            date_rec = date_validator()
            date_comp = None
            text = input("What is the request about?\n")
            rec_type = request_type_selector()
            record.append(selected_contact)
            record.append(selected_location)
            record.append(date_rec)
            record.append(date_comp)
            record.append(text)
            record.append(rec_type)
        except ValueError as e:
            print(e)
        else:
            input('Click enter to continue\n')
            menu_title = 'Please select one of the following options'
            selections = ['Create record',
                        'Create Menu',
                        'Main menu']
            selection = pick(selections, menu_title, '>>>')[1]
            if selection == 0:
                add_new_record_to_worksheet(record, requests)
            elif selection == 1:
                create_menu()
            else:
                main_menu()       
                            

def add_completed_date(rec_id, row, date_rec):
    """
    Adds completed date to request and calculates time to complete
    """

    date_comp = date_validator()
    days_to_comp = calculate_days_between_dates(date_rec, date_comp)
    requests.update_cell(row, 5, date_comp)
    requests.update_cell(row, 8, days_to_comp)
    print('Completed date added')
    get_request_details(rec_id, row)

# Actions


def find_actions(req_id):
    """
    Finds actions for requests
    """

    results = actions.findall(req_id, in_column=2)

    print_actions(req_id, results)


def print_actions(req_id, results):
    """
    Prints actions report to console
    """
    report = []
    header = ['ID', 'Details', 'Date']
    for result in results:
        line = result.row
        details = actions.row_values(line)
        del details[1]
        report.append(details)

    print(f'Actions for Request {req_id}')
    print(tabulate(report,headers=header,tablefmt='github'))

    input('Click enter to continue\n')
    menu_title = 'Please select one of the following options'
    selections = ['Add an action',
                  'Back to request',
                  'Search Menu',
                  'Main menu']

    selection = pick(selections, menu_title, '>>>')[1]
    if selection == 0:
        add_action(req_id)
    elif selection == 1:
        find_by_id(requests, req_id)
    elif selection == 2:
        search_menu()
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
            date_input = date_validator()
            record.append(int(req_id))
            record.append(text)
            record.append(date_input)
        except ValueError as e:
            print(e)
        else:
            input('Click enter to continue\n')
            menu_title = 'Please select one of the following options'
            selections = ['Create action',
                        'Back to request',
                        'Main menu']
            selection = pick(selections, menu_title, '>>>')[1]
            if selection == 0:
                add_new_record_to_worksheet(record, actions)
            elif selection == 1:
                find_by_id(requests,req_id)
            else:
                main_menu()           

# Contact


def find_contact_menu():
    """
    To select which search you would like to do on a request
    """

    menu_title = 'Please select one of the following options'
    selections = ['Contact by ID',
                  'Contact by first name',
                  'Contact by last name',
                  'Contact by phone number',
                  'All contacts',
                  'Search menu']

    selection = pick(selections, menu_title, '>>>')[1]

    if selection == 0:
        find_by_id(contact, None)
    elif selection == 1:
        find_for_report(contact, 'Please enter first name of contact', 2, 0)
    elif selection == 2:
        find_for_report(contact, 'Please enter last name of contact', 3, 0)
    elif selection == 3:
        find_for_report(contact, 'Please enter phone number of contact', 4, 0)
    elif selection == 4:
        display_all(contact)
    else:
        search_menu()


def get_contact_details(rec_id, row):
    """
    Prints contact details to console
    """
    first_name = contact.cell(row, 2).value
    last_name = contact.cell(row, 3).value
    phone = contact.cell(row, 4).value
    email = contact.cell(row, 5).value

    print('Contact ID: ',rec_id,
          '\nFirst Name: ',first_name,
          '\nLast Name: ',last_name,
          '\nPhone: ',phone,
          '\nEmail: ',email)

    input('Click enter to continue\n')
    menu_title = 'Please select one of the following options'
    selections = ['View linked requests', 'Search Menu', 'Main menu']

    selection = pick(selections, menu_title, '>>>')[1]
    if selection == 0:
        report_results(requests, rec_id, 2, 0)
    elif selection == 1:
        search_menu()
    else:
        main_menu()

# location


def find_location_menu():
    """
    To select which search you would like to do on a request
    """

    menu_title = 'Please select one of the following options'
    selections = ['Location by ID',
                  'Location by house name/number',
                  'Location by street name',
                  'Location by area',
                  'Location by postcode',
                  'All locations',
                  'Search menu']

    selection = pick(selections, menu_title, '>>>')[1]

    if selection == 0:
        find_by_id(location, None)
    elif selection == 1:
        find_for_report(location, 'Please enter house number of contact', 2, 0)
    elif selection == 2:
        find_for_report(location, 'Please enter street name', 3, 0)
    elif selection == 3:
        find_for_report(location, 'Please enter area eg, Port Talbot', 4, 0)
    elif selection == 4:
        find_for_report(location, 'Please enter postcode eg, sa12 1aa', 5, 0)
    elif selection == 5:
        display_all(location)
    else:
        search_menu()


def get_location_details(rec_id, row):
    """
    Prints location details to console
    """
    address1 = location.cell(row, 2).value
    address2 = location.cell(row, 3).value
    address3 = location.cell(row, 4).value
    postcode = location.cell(row, 5).value

    print('Location ID: ',rec_id,
          '\nHouse Number: ',address1,
          '\nStreet: ',address2,
          '\nArea: ',address3,
          '\nPostcode: ',postcode)

    input('Click enter to continue\n')
    menu_title = 'Please select one of the following options'
    selections = ['View linked requests', 'Search Menu', 'Main menu']

    selection = pick(selections, menu_title, '>>>')[1]
    if selection == 0:
        report_results(requests, rec_id, 3, 0)
    elif selection == 1:
        search_menu()
    else:
        main_menu()

# General Functions


def find_by_id(database, rec_id):
    """
    Get details from id number
    """

    if rec_id is None:
        while True:
            try:
                rec_id = int(input('What is the id you would like to view? \n'))
            except ValueError:
                print('Entries must be an integer')
            else:
                break
    # Finds the id and stores what cell that id is in
    try:    
        cell = database.find(str(rec_id), in_column=1)
        line = cell.row
    except AttributeError:
        print('Record',rec_id,"doesn't exist in",database.title,'\n')
        input('Click enter to continue to the search menu\n')
        search_menu()

    if database == requests:
        get_request_details(str(rec_id), line)
    elif database == contact:
        get_contact_details(str(rec_id), line)
    else:
        get_location_details(str(rec_id), line)


def find_for_report(database, search, col, from_create):
    """
    Obtains search criteria
    """
    if database == requests and col == 7:
        search_criteria = request_type_selector()
    elif database == requests and col == 4 or database == requests and col == 5:
        search_criteria = date_validator()
    elif database == location and col == 5:
        search_criteria = input(f'{search}\n').upper()
    else:
        search_criteria = input(f'{search}\n').title()

    return report_results(database, search_criteria, col, from_create)


def report_results(database, search_criteria, col, from_create):
    """
    Gets results for report
    """

    results = database.findall(search_criteria, in_column=col)

    return print_report(database, results, from_create)


def print_report(database, results, from_create):
    """
    Prints report to console
    """

    # Selects what sheet we are searching
    if database == requests:
        header = ['ID',
                  'Received Date',
                  'Completed Date',
                  'Request Details',
                  'Type',
                  'Time to complete in days']
    elif database == actions:
        header = ['ID',
                  'Details',
                  'Date']
    elif database == contact:
        header = ['ID',
                  'First Name',
                  'Last Name',
                  'Phone',
                  'Email']
    else:
        header = ['ID',
                  'House Number',
                  'Street',
                  'Area',
                  'Postcode']

    report = []

    for result in results:
        line = result.row
        details = database.row_values(line)
        if database == requests:
            del details[1:3]
        report.append(details)

    print(tabulate(report, headers=header, tablefmt='github'))

    if from_create == 0:
        input('Click enter to continue\n')
        menu_title = 'Please select one of the following options'
        selections = ['View by Id', 'Search Menu', 'Main menu']

        selection = pick(selections, menu_title, '>>>')[1]
        if selection == 0:
            find_by_id(database, None)
        elif selection == 1:
            search_menu()
        else:
            main_menu()
    else:
        if database == contact:
            selected_contact_id = input(
                ('Please enter the ID of the contact you want\n'
                'To search again click enter with no values entered\n'))
            return selected_contact_id
        else:
            selected_location_id = input(
                ('Please enter the ID of the location you want\n'
                'To search again click enter with no values entered\n'))
            return selected_location_id


def display_all(database):
    """
    Shows all of database in console
    """

    report = database.get_all_values()

    print(tabulate(report, headers='firstrow', tablefmt='github'))

    input('Click enter to continue back to the search menu\n')
    search_menu()


def create_record(database):
    """
    creates record in sheets for any class based data
    """
    if database == contact:
        record = create_person()
    elif database == location:
        record = create_premise()

    input('Click enter to continue\n')
    menu_title = 'Please select one of the following options'
    selections = ['Create record',
                  'Create Menu',
                  'Main menu']

    selection = pick(selections, menu_title, '>>>')[1]
    if selection == 0:
        add_new_record_to_worksheet(record.list(), database)
    elif selection == 1:
        create_menu()
    else:
        main_menu()


def add_new_record_to_worksheet(record, database):
    """
    Adds new data to worksheet
    """
    print('Updating......\n')

    # Get max number in id column for next ID
    all_ids = database.col_values(1)
    del all_ids[0]
    all_ids = [int(i) for i in all_ids]
    new_id = max(all_ids)+1

    record.insert(0, new_id)

    database.append_row(record)

    print(f'{database.title} has updated\n')

    input('Click enter to continue\n')

    menu_title = 'Please select one of the following options'
    selections = ['View created record',
                  'Search Menu',
                  'Main menu']

    selection = pick(selections, menu_title, '>>>')[1]
    if selection == 0:
        if database == actions:
            find_by_id(requests, record[1])
        else:
            find_by_id(database, new_id)
    elif selection == 1:
        search_menu()
    else:
        main_menu()


def calculate_days_between_dates(date1, date2):
    """
    calculates number of days between 2 date in
    string where the format is dd/mm/yyyy
    """
    date1 = datetime.datetime.strptime(date1, "%d/%m/%Y")
    date2 = datetime.datetime.strptime(date2, "%d/%m/%Y")
    calc_days = date2-date1
    return calc_days.days


def date_validator():
    """
    Validate and input a date
    """
    date_test = re.compile(r"^[0-9]{2}/[0-9]{2}/[0-9]{4}$")
    while True:
        try:
            date_input = input(
                "what's the date? (Enter in dd/mm/yyyy format)\n")
            if not date_test.match(date_input):
                raise ValueError(("The date was entered in the wrong format the format "
                                 f"needs to be dd/mm/yyyy you entered {date_input}"))
        except ValueError as e:
            print(e)
        else:
            return date_input


def request_type_selector():
    """
    Selector for request types
    """
    type_text = 'Please select the request type:'
    types = ['flytip', 'noise', 'abandoned vehicle']
    type_chosen = pick(types, type_text, indicator='>>>')[0]
    return type_chosen


def print_stats():
    """
    Calculates and prints report of the mean time to complete each request type
    """
    print('Average number of days to complete request by request type')
    df = pd.DataFrame(requests.get_all_records())
    df.replace('', np.nan, inplace=True)
    df = df.dropna()
    mean_df = df.groupby('type')['timetocomp'].mean()
    print(mean_df)
    input('Click enter to continue back to main menu\n')
    main_menu()


def continue_menu_try_again(selected):
    """
    Pick menu for try again or continue or cancel
    """
    type_text = f'You selected {selected}\n\nPlease select one of the below:'
    types = ['This is the correct selection', 'search again', 'main menu']
    rec_type = pick(types, type_text, indicator='>>>')[1]
    if rec_type == 2:
        main_menu()
    else:
        return rec_type


main_menu()
