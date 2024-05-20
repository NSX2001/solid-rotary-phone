import csv
from datetime import datetime
import unittest

# Singleton Design Pattern
class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

# Expense Classes
class Expense:
    def __init__(self, amount, description, user):
        self.amount = amount
        self.description = description
        self.user = user
        self.date = datetime.now()

    def __str__(self):
        return f"{self.date.strftime('%Y-%m-%d %H:%M:%S')} - {self.user}: {self.description}: ${self.amount:.2f}"

class FoodExpense(Expense):
    def __init__(self, amount, description="Food", user=""):
        super().__init__(amount, description, user)

class TransportExpense(Expense):
    def __init__(self, amount, description="Transport", user=""):
        super().__init__(amount, description, user)

# Finance Tracker Class
class FinanceTracker(metaclass=SingletonMeta):
    def __init__(self):
        self.expenses = []
        self.users = set()
        self.limits = {'daily': 0, 'weekly': 0, 'monthly': 0}

    def add_expense(self, expense):
        self.expenses.append(expense)

    def remove_expense(self, index):
        if 0 <= index < len(self.expenses):
            del self.expenses[index]

    def print_expense_history(self):
        for expense in self.expenses:
            print(expense)

    def save_to_file(self, filename):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'User', 'Description', 'Amount'])
            for expense in self.expenses:
                writer.writerow([expense.date.strftime('%Y-%m-%d %H:%M:%S'), expense.user, expense.description, expense.amount])

    def load_from_file(self, filename):
        self.expenses.clear()
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                date_str, user, description, amount = row
                date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                amount = float(amount)
                self.expenses.append(Expense(amount, description, user))

    def set_limits(self, daily, weekly, monthly):
        self.limits = {'daily': daily, 'weekly': weekly, 'monthly': monthly}

    def add_user(self, user):
        self.users.add(user)

    def remove_user(self, user):
        self.users.discard(user)

    def list_users(self):
        for user in self.users:
            print(user)

# Decorator Function
def track_operations(func):
    def wrapper(*args, **kwargs):
        print(f"Executing: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

# Unit Testing
class TestFinanceTracker(unittest.TestCase):
    def setUp(self):
        self.tracker = FinanceTracker()
        self.tracker.expenses = []
        self.tracker.users = set()

    def test_add_expense(self):
        self.tracker.add_expense(FoodExpense(10.0, user="Alice"))
        self.assertEqual(len(self.tracker.expenses), 1)

    def test_remove_expense(self):
        self.tracker.add_expense(FoodExpense(10.0, user="Alice"))
        self.tracker.remove_expense(0)
        self.assertEqual(len(self.tracker.expenses), 0)

    def test_set_limits(self):
        self.tracker.set_limits(50, 300, 1200)
        self.assertEqual(self.tracker.limits['daily'], 50)
        self.assertEqual(self.tracker.limits['weekly'], 300)
        self.assertEqual(self.tracker.limits['monthly'], 1200)

    def test_save_load_file(self):
        self.tracker.add_expense(FoodExpense(10.0, user="Alice"))
        self.tracker.save_to_file('expenses.csv')
        self.tracker.expenses = []
        self.tracker.load_from_file('expenses.csv')
        self.assertEqual(len(self.tracker.expenses), 1)
        self.assertEqual(self.tracker.expenses[0].amount, 10.0)

    def test_add_user(self):
        self.tracker.add_user("Alice")
        self.tracker.add_user("Bob")
        self.assertIn("Alice", self.tracker.users)
        self.assertIn("Bob", self.tracker.users)

    def test_remove_user(self):
        self.tracker.add_user("Alice")
        self.tracker.remove_user("Alice")
        self.assertNotIn("Alice", self.tracker.users)

# Main Program and CLI
def display_menu():
    print("\nFinance Tracker Menu")
    print("1. Add Expense")
    print("2. Remove Expense")
    print("3. View Expenses")
    print("4. Save Expenses to File")
    print("5. Load Expenses from File")
    print("6. Set Limits")
    print("7. Add User")
    print("8. Remove User")
    print("9. List Users")
    print("10. Exit")

def main():
    tracker = FinanceTracker()

    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            amount = float(input("Enter amount: "))
            description = input("Enter description: ")
            user = input("Enter user: ")
            category = input("Enter category (food/transport/other): ").lower()
            if category == "food":
                expense = FoodExpense(amount, description, user)
            elif category == "transport":
                expense = TransportExpense(amount, description, user)
            else:
                expense = Expense(amount, description, user)
            tracker.add_expense(expense)
            print("Expense added.")

        elif choice == '2':
            tracker.print_expense_history()
            index = int(input("Enter the index of the expense to remove: "))
            tracker.remove_expense(index)
            print("Expense removed.")

        elif choice == '3':
            tracker.print_expense_history()

        elif choice == '4':
            filename = input("Enter filename to save expenses: ")
            tracker.save_to_file(filename)
            print("Expenses saved to file.")

        elif choice == '5':
            filename = input("Enter filename to load expenses: ")
            tracker.load_from_file(filename)
            print("Expenses loaded from file.")

        elif choice == '6':
            daily = float(input("Enter daily limit: "))
            weekly = float(input("Enter weekly limit: "))
            monthly = float(input("Enter monthly limit: "))
            tracker.set_limits(daily, weekly, monthly)
            print("Limits set.")

        elif choice == '7':
            user = input("Enter user to add: ")
            tracker.add_user(user)
            print("User added.")

        elif choice == '8':
            user = input("Enter user to remove: ")
            tracker.remove_user(user)
            print("User removed.")

        elif choice == '9':
            tracker.list_users()

        elif choice == '10':
            print("Exiting Finance Tracker.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        unittest.main(argv=['first-arg-is-ignored'], exit=False)
    else:
        main()
