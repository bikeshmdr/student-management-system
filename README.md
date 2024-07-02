# student-management-system

This is a simple student managament system program that records the detail of studen and teacher in json file

example of teacher data: 
    {"name": "hari", "address": "kathmandu", "email": "hari@gmail.com", "phone_number": 1236548754, "id": "1", "subject": "social"}

example of student data: 
    {"name": "gita", "address": "ktm", "email": "gita@gmail.com", "phone_number": 1425362514, "roll_number": "45", "marks": {"social": 98.0, "science": 35.0, "english": 65.0, "nepali": 68.0}}

only teacher can add new entry so need to authenticate using teacher name and id.

checking teachers details
    gives the entire data of teachers.json

checking students details
    gives the general data of students from students.json

check specific teacher detail 
    gives the specific teacher data from teachers.json

check specific student detail
    gives the specific student data along with some additional information from students.json