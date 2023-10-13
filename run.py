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

def find_request_menu():
    """
    To select which search you would like to do on a request
    """
    menu=True

    while menu:
        print('1. Search by request ID\n2. Search by received date\n3. Search by completed date\n4. Search by type')
        selection = input('Please enter the number of what you would like to search by \n')
        if selection == '1':
            find_request_by_id()
            menu = False
        elif selection == '2':
            find_request_for_report('Please enter the received date you want to search in dd/mm/yyyy format',4)
            menu = False
        elif selection == '3':
            find_request_for_report('Please enter the completed date you want to search in dd/mm/yyyy format',5)
            menu = False
        elif selection == '4':
            find_request_for_report('Please enter either flytip or noise',7)
            menu = False
        else:
            print(f'Invalid selection: You selected {selection} please try again')

def find_request_for_report(search,col):
    """
    Finds requests for report
    """

    date_comp = input(f'{search}\n')

    results = requests.findall(date_comp,in_column=col)

    print_requests_report(results)

def print_requests_report(results):
    """
    Prints requests report to console
    """
    report = []
    header = ['ID','Received Date','Completed Date','Request Details','Type','Time to complete in days']
    for result in results:
        line = result.row
        request_details = requests.row_values(line)
        del request_details[1:3]
        report.append(request_details)
    
    print(tabulate(report,headers=header,tablefmt='github'))
    
def find_request_by_id():
    """
    Get request details from id number
    """

    id = input('What is the request id you would like to view? \n')
    # Finds the id and stores what cell that id is in
    cell = requests.find(id,in_column=1)

    line = cell.row

    get_request_details(id,line)

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

find_request_menu()