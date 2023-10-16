import re
from pick import pick


class Person:
    """
    Person class
    """

    def __init__(self, first_name, last_name, phone, email):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email

    def list(self):
        """
        returns self in list format
        """
        return [self.first_name, self.last_name, int(self.phone), self.email]


class Premise:
    """
    Premise class
    """

    def __init__(self, address1, address2, address3, postcode):
        self.address1 = address1
        self.address2 = address2
        self.address3 = address3
        self.postcode = postcode

    def list(self):
        """
        returns self in list format
        """
        return [self.address1, self.address2, self.address3, self.postcode]

# Create objects


def create_person():
    """
    Create person with class
    """
    mandatory_pass = False
    while True:
        try:
            while not mandatory_pass:
                first_name = input("Enter first name: ").title()
                mandatory_pass = input_empty(first_name)
            mandatory_pass = False
            while not mandatory_pass:
                last_name = input("Enter last name: ").title()
                mandatory_pass = input_empty(last_name)
            phone = input("Enter phone number: ")
            email = input("Enter email address: ").lower()
            try:
                phone_test = int(phone)
            except TypeError:
                phone_test = ''
            if not isinstance(phone_test, int):
                raise ValueError("Phone number must be an integer")
            # https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
            email_regex = re.compile(
                r"^[a-zA-Z0-9.!#$%&'*+-/=?^_`{|}~]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$")
            if not email_regex.match(email):
                raise ValueError("Invalid email address format")

            return Person(first_name, last_name, phone, email)
        except ValueError as e:
            print(f'{e}\nPlease try again')


def create_premise():
    """
    Create premise with class
    """
    mandatory_pass = False
    while True:
        try:
            while not mandatory_pass:
                address1 = input("Enter house number or name: ").title()
                mandatory_pass = input_empty(address1)
            mandatory_pass = False
            while not mandatory_pass:
                address2 = input("Enter street name: ").title()
                mandatory_pass = input_empty(address2)
            mandatory_pass = False
            while not mandatory_pass:
                address3 = input("Enter area: ").title()
                mandatory_pass = input_empty(address3)
            postcode = input("Enter postcode: ").upper()
            postcode_test = re.compile(
                r"^[A-Z]{2}[0-9]{1,2}\s[0-9]{1}[A-Z]{2}$")
            if not postcode_test.match(postcode):
                raise ValueError(
                    "The postcode format needs to be #### ### or ### ### eg, sa12 2aa")
            return Premise(address1, address2, address3, postcode)
        except ValueError as e:
            print(f'{e}\nPlease try again')


def input_empty(entry):
    """
    Check if string id empty
    """
    if len(entry) == 0:
        print('Field is mandatory please try again\n')
        return False
    else:
        return True
