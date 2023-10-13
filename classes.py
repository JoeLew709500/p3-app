import re

class Person:
    def __init__(self,first_name,last_name,phone,email):
        self.first_name =first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email

    def comma_sep_person(self):
        return [self.first_name,self.last_name,int(self.phone),self.email]

class Premise:
    def __init__(self,address1,address2,address3,postcode):
        self.address1 = address1
        self.address2 = address2
        self.address3 = address3
        self.postcode = postcode

# Create objects
def create_person():
    """
    Create person with class
    """
    while True:
        try:
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            phone = input("Enter phone number: ")
            email = input("Enter email address: ")
            try:
                phone_test = int(phone)
            except:
                phone_test=''
            if not isinstance(phone_test, int):
                raise ValueError("Phone number must be an integer")
            #https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
            email_regex = re.compile(r"^[a-zA-Z0-9.!#$%&'*+-/=?^_`{|}~]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$")
            if not email_regex.match(email):
                raise ValueError("Invalid email address format")

            return Person(first_name, last_name, phone, email)    
        except ValueError as e:
            print(f'{e}\nPlease try again')
