# Microservice-361
Microservice README for CS361 by Caleb Gheorghita
Hi, This is my budget microservice that helps track expenses and income. Here's how to use it:

# Request Data
How to Request Data From My Microservice:
It's pretty simple! You just need to use Python's requests library to make GET requests. Here's how:
First, make sure you have requests installed:
pip install requests.
Then you can make requests to any of these three endpoints:

Get expense trends:
This shows expenses over time
response = requests.get("http://localhost:5000/api/expenses/trend", params={"user_id": 1})

Get income trends:
This shows income over time
response = requests.get("http://localhost:5000/api/income/trend", params={"user_id": 1})

Get expense categories:
This shows expenses grouped by category
response = requests.get("http://localhost:5000/api/expenses/categories", params={"user_id": 1})

# Getting data
How to Get the Data Back:
After you make a request, getting the data is easy! Just use .json() to convert the response:

Example of getting expense data
response = requests.get("http://localhost:5000/api/expenses/trend", params={"user_id": 1})
data = response.json()

# Example code for output
Now you can print it out!
for item in data:
    print(f"Year: {item['year']}")
    print(f"Month: {item['month']}")
    print(f"Total Expense: ${item['total_expense']}")

# Example Data output
What The Data Looks Like:
Here's what you'll get back for each request:


Expense Trends:
[
    {
        "year": 2024,
        "month": 1,
        "total_expense": 1200.00
    }
    # You'll get one of these for each month
]

Income Trends:
[
    {
        "year": 2024,
        "month": 1,
        "total_income": 3000.00
    }
    # You'll get one of these for each month
]

Expense Categories:
[
    {
        "year": 2024,
        "category": "Food",
        "total_expense": 500.00
    }
    # You'll get one of these for each category
]

# UML diagram
How It All Works (UML Diagram):
Here's a diagram showing how the requests and responses work:

![UML diagram](https://github.com/user-attachments/assets/07b56ef4-f229-464f-b0bd-f35cd60d29da)

