import json
import os
import re

def store_details_to_json(details, filepath):
    # Read the content of the file
    with open(filepath, 'r+') as f:
        content = f.read()
        
        # Move file pointer to the correct position for appending
        if content == '[]':  # Check if the file contains an empty array
            f.seek(1)  # Move to just after the opening bracket
        elif content.strip() == '':  # Check if the file is empty
            f.write('[')  # Start the JSON array
            f.seek(1)  # Move to just after the opening bracket
        else:
            f.seek(0, os.SEEK_END)  # Move to the end of the file
            position = f.tell()  # Get the current position (should be the end)
            f.seek(position - 1)  # Move back one position to the closing bracket
            f.truncate()  # Truncate the last character (the closing bracket)
            f.write(',\n')  # Add a comma and newline to separate entries

        # Append the new details
        json.dump(details, f)
        #print(details.to_json())
        f.write(']')  # Close the JSON array

# Defining custum classes for exception handling       
class NoMatchingNameError(Exception):
    pass

class NoMatchingIdError(Exception):
    pass

def authentication():
    with open("teachers.json", 'r') as f:
        content = f.read()
        
        # Move file pointer to the correct position for appending
        if content == '[]':  # Check if the file contains an empty array
            raise ValueError("Empty record")
    print("You need to verify yourself as a teacher to add new entry.")
    name = input("Enter your name: ")
    id = input("Enter your Id number: ")

    try:
        with open("teachers.json", "r") as f:
            data = json.load(f)
            matching_entries = [entry for entry in data if entry["name"] == name]

            if not matching_entries:
                raise NoMatchingNameError("No matching Teacher name found in the database.")

            for entry in matching_entries:
                if entry.get('id') == id:
                    # Returning True to indicate successful authentication
                    return True
            else:
                # If no matching ID found in the loop, raise NoMatchingIdError
                raise NoMatchingIdError("Teacher's Id does not match.")

    except NoMatchingNameError as e:
        print(f"Error: {e}")
    except NoMatchingIdError as e:
        print(f"Error: {e}")


class AuthenticationError(Exception):
    pass

def check_record(filepath, value):
    with open(filepath, 'r') as f:
        data = json.load(f)
    # Create a new list containing only the 'roll_number' from each dictionary
    if filepath == 'teachers.json':
        data_list = [item["id"] for item in data]
    else:
        data_list = [item["roll_number"] for item in data]
    if value in data_list:
        if filepath == 'teachers.json':
            raise AuthenticationError("id already taken.")
        else:
            raise AuthenticationError("Roll number already taken.")


# Create class "Teacher"
class Teacher:
    def __init__(self, id , name : str, subject, address, email, phone_number : int):
        self.id = id
        self.name = name
        self.subject = subject
        self.address = address
        
        # Define the regex pattern for a valid email address
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        # Check if the email matches the pattern
        if not isinstance(email, str) or not re.match(email_pattern, email):
            raise ValueError("Email address must be a valid format.")
        
        self.email = email

        # Validate phone number length
        if not isinstance(phone_number, int) or not (len(str(phone_number)) == 10):
            raise ValueError("Phone number must be an integer of exactly 10 digits.")
        
        self.phone_number = phone_number

    # method to convert the input data to json format
    def base_json(self):
        return {
            "name": self.name,
            "address": self.address,
            "email": self.email,
            "phone_number": self.phone_number
        }
    def to_json(self):
        data = self.base_json()
        data["id"] = self.id
        data["subject"] = self.subject
        return data

    # function to create and append new teachers
    @classmethod
    def accept(cls):
        # Check if file exists; if not, create an empty JSON file and grant authority for new entry
        filepath = f"{cls.__name__.lower()}s.json"
        new_entry = False
        if not os.path.exists(filepath):
            with open(filepath, 'w') as f:
                f.write('[]')  # Create an empty JSON array
            # grant permission to teachers only
            if cls.__name__ == __class__.__name__:
                new_entry = True # garnt authority

        if not new_entry:
            new_entry = authentication()

        # In case of not authenticated error is handeled using exception handelling in authentication()
        if new_entry:
            print(f"Enter the detail of new {cls.__name__}.")
            name = input(f"Enter {cls.__name__} name: ")
            address = input(f"Enter {cls.__name__} address: ")
            email = input(f"Enter {cls.__name__} email: ")
            phone_number = int(input(f"Enter {cls.__name__} phone number: "))
            # store data to json file if calling class is teacher class else retrun values which is used by student class 
            # checking if calling call is teacher class itself in order to add id
            if cls.__name__  == __class__.__name__:
                id = input(f"Enter {cls.__name__} id number: ")
                check_record(filepath, id)
                subject = input(f"Enter {cls.__name__} subject: ")
                # storing to json file
                new_teacher = cls(id, name, subject, address, email, phone_number)
                details = new_teacher.to_json()
                store_details_to_json(details, filepath)
            else:
                return name, address, email, phone_number
        else:
            # if nothing is returned typeerror occurs as we are tying to assign single none value to three variable in student class
            return None, None, None, None
        
        return None, None, None, None
        


    @classmethod
    def display_all(cls):
        # using calling class name to handle both teacher and student class
        filepath = f"{cls.__name__}s.json"
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                if not data:
                    raise FileNotFoundError
                else:
                    for item in data:
                        print("Name : ", item["name"])
                        print("Address : ", item["address"])
                        print("Email Address : ", item["email"])
                        print("Phone number : ", item["phone_number"])
                        print("Subject: ", item["subject"])
                        print("\n")
        except FileNotFoundError:
            print(f"The file {cls.__name__}s.json does not exist.")

    
    # method to search detail of single information
    @staticmethod
    def search(name):
        filepath = 'teachers.json'
        teacher_found = False  # Flag to track if any teacher with the name is found

        with open(filepath, 'r') as f:
            data = json.load(f)
            for item in data:
                if item.get("name") == name:
                    print("Name : ", item["name"])
                    print("Email Address : ", item["email"])
                    print("Phone number : ", item["phone_number"])
                    print("\n")
                    teacher_found = True

            if not teacher_found:
                print("No teacher found with the name", name)

# Create class "Student"
class Student(Teacher):
    # keyword argument is taken to store marks 
    def __init__(self, id, name, subject, address, email, phone_number, roll_number, **kwargs):
        super().__init__(
        id, name, subject, address, email, phone_number
        )
        self.roll_number = roll_number
        self.marks = kwargs

    def to_json(self):
        json_data = self.base_json()  # Call the _base_json() method directly
        json_data["roll_number"] = self.roll_number
        json_data["marks"] = self.marks
        return json_data
    
    @classmethod
    def accept(cls):
        filepath = f"{cls.__name__.lower()}s.json"
        try:
            name, address, email, phone_number = super().accept()
            # None value will be returned by super().accept() if authentication fails as it return nothing
            if name is None:
                raise AuthenticationError("Authentication failed. Cannot add new entry.")
            
            roll_number = input(f"Enter {cls.__name__} roll number : ")
            check_record(filepath, roll_number)
            marks = {}

            next_subject = 'y'
            while next_subject == 'y' or next_subject == 'Y':
                subject, mark = input("Enter the key value pair of subject and mark 'subject:mark'.\n").split(':')
                marks[subject.strip()] = float(mark.strip())
                next_subject = input("Press 'y' or 'Y' to add another subject: ")
            new_student = cls(id, name, subject, address, email, phone_number, roll_number, **marks)
            details = new_student.to_json()
            store_details_to_json(details, filepath)
        except AuthenticationError as e:
            print(f"Error: {e}")


    @classmethod
    def display_all(cls):
        filepath = f"{cls.__name__}s.json"
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                if not data:
                    raise FileNotFoundError
                else:
                    for item in data:
                        print("Name : ", item["name"])
                        print("Address : ", item["address"])
                        print("Email Address : ", item["email"])
                        print("Phone number : ", item["phone_number"])
                        print("\n")
        except FileNotFoundError:
            print(f"The file {cls.__name__}s.json does not exist.")

    @staticmethod
    def average(marks):
        if not marks:
            return 0.0  # Return 0.0 if marks is empty or None

        # Calculate the average
        average_value = sum(marks.values()) / len(marks)
        return average_value
    
    @staticmethod
    def result(item):
        failed_status = False
        for subject, mark in item.items():
            if mark < 32:
                print(f"{subject}: Failed (Mark: {mark})")
                failed_status = True
            else:
                print(f"{subject}: Passed (Mark: {mark})")

        return failed_status

    @staticmethod
    # method to search detail of single information
    def search(name):
        filepath = 'students.json'
        with open(filepath, 'r') as f:
            data = json.load(f)
            for item in data:
                if item["name"] == name:
                    print("Name : ", item["name"])
                    print("Email Address : ", item["email"])
                    print("Phone number : ", item["phone_number"])
                    print("Roll number : ", item["roll_number"])
                    #print("Marks : ", item["marks"])
                    # displaying the failed results only
                    failed = Student.result(item["marks"])
                    if not failed:
                        # calling average method of student class
                        student_percentage = Student.average(item["marks"])
                        print(f"Percentage: {student_percentage}")
                    print("\n")
                    return
            print("No student found with the name", name)
        f.close()

    
next_cycle = 'y'
while next_cycle == 'y' or next_cycle == 'Y':
    print("Enter the consequitive integer value to perform specific task.")
    task = input(" 1. New Teacher Entry \n 2. New Student Entry \n 3. Check Teachers detail \n 4. Check Students detail \n 5. Check Specific Teacher detail \n 6. Check Specific Student detail \n 7. Quit \n")
	
    if task == '1':
        Teacher.accept()
    elif task == '2':
        Student.accept()
    elif task == '3':
        Teacher.display_all()
    elif task == '4':
        Student.display_all()
    elif task == '5':
        name = input("Enter the name of the Teacher: ")
        Teacher.search(name)
    elif task == '6':
        name = input("Enter the name of the Student: ")
        Student.search(name)
    elif task == '7':
        break
    else:
        pass
    next_cycle = input("Press 'y' or 'Y' if you wish to continue else to terminate press any key.\n")

