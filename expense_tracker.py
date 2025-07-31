#!/usr/bin/env python3
"""
Personal Expense Tracker

A command-line application to track personal expenses, categorize them,
and monitor spending against a monthly budget.
"""

import csv
import os
import datetime
from typing import List, Dict, Union, Optional


class ExpenseTracker:
    """Main class for the Personal Expense Tracker application."""

    def __init__(self):
        """Initialize the expense tracker with empty expenses list and budget."""
        self.expenses: List[Dict[str, Union[str, float]]] = []
        self.budget: Optional[float] = None
        self.data_file = "expenses.csv"
        self.load_expenses()

    def add_expense(self) -> None:
        """Prompt user for expense details and add to the expenses list."""
        print("\n=== Add Expense ===")
        
        # Get date
        while True:
            date_str = input("Enter date (YYYY-MM-DD) or 'today' for today's date: ")
            if date_str.lower() == 'today':
                date_str = datetime.datetime.now().strftime('%Y-%m-%d')
                break
            try:
                # Validate date format
                datetime.datetime.strptime(date_str, '%Y-%m-%d')
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
        
        # Get category
        category = input("Enter category (e.g., Food, Transportation, Entertainment): ")
        
        # Get amount
        while True:
            amount_str = input("Enter amount spent: ")
            try:
                amount = float(amount_str)
                if amount <= 0:
                    print("Amount must be greater than zero.")
                    continue
                break
            except ValueError:
                print("Invalid amount. Please enter a number.")
        
        # Get description
        description = input("Enter a brief description: ")
        
        # Create and add expense
        expense = {
            'date': date_str,
            'category': category,
            'amount': amount,
            'description': description
        }
        
        self.expenses.append(expense)
        print("Expense added successfully!")

    def view_expenses(self) -> None:
        """Display all stored expenses."""
        if not self.expenses:
            print("\nNo expenses recorded yet.")
            return
        
        print("\n=== Expense Records ===")
        print(f"{'Date':<12} {'Category':<15} {'Amount':<10} {'Description':<30}")
        print("-" * 67)
        
        # Sort expenses by date (most recent first)
        sorted_expenses = sorted(self.expenses, key=lambda x: x['date'], reverse=True)
        
        for expense in sorted_expenses:
            # Validate expense data
            if all(key in expense for key in ['date', 'category', 'amount', 'description']):
                print(f"{expense['date']:<12} {expense['category']:<15} ${expense['amount']:<9.2f} {expense['description']:<30}")
            else:
                print("Found incomplete expense record (skipped)")
        
        # Display total
        total = sum(expense['amount'] for expense in self.expenses if 'amount' in expense)
        print("-" * 67)
        print(f"Total expenses: ${total:.2f}")

    def set_budget(self) -> None:
        """Set the monthly budget."""
        print("\n=== Set Monthly Budget ===")
        while True:
            budget_str = input("Enter your monthly budget: ")
            try:
                budget = float(budget_str)
                if budget <= 0:
                    print("Budget must be greater than zero.")
                    continue
                self.budget = budget
                print(f"Monthly budget set to ${self.budget:.2f}")
                break
            except ValueError:
                print("Invalid amount. Please enter a number.")

    def track_budget(self) -> None:
        """Track expenses against the monthly budget."""
        if self.budget is None:
            print("\nNo budget set. Please set a budget first.")
            self.set_budget()
            return
        
        # Ask user if they want to track current month or a specific month
        print("\n=== Budget Tracker ===")
        print("1. Track current month")
        print("2. Track specific month")
        choice = input("Enter your choice (1-2): ")
        
        if choice == '2':
            # Get specific month from user
            while True:
                month_year = input("Enter month and year (MM-YYYY): ")
                try:
                    month_date = datetime.datetime.strptime(month_year, '%m-%Y')
                    year = month_date.year
                    month = month_date.month
                    break
                except ValueError:
                    print("Invalid format. Please use MM-YYYY (e.g., 08-2025)")
        else:
            # Use current month
            current_date = datetime.datetime.now()
            year = current_date.year
            month = current_date.month
            month_year = f"{month:02d}-{year}"
        
        # Get month name for display
        month_name = datetime.date(year, month, 1).strftime('%B %Y')
        
        # Filter expenses for the selected month
        monthly_expenses = []
        for expense in self.expenses:
            if 'date' in expense and expense['date']:
                try:
                    expense_date = datetime.datetime.strptime(expense['date'], '%Y-%m-%d')
                    if expense_date.year == year and expense_date.month == month:
                        monthly_expenses.append(expense)
                except ValueError:
                    # Skip expenses with invalid date format
                    continue
        
        # Debug information
        print(f"\nTracking budget for: {month_name}")
        print(f"Found {len(monthly_expenses)} expenses for this month")
        
        total_spent = sum(expense['amount'] for expense in monthly_expenses if 'amount' in expense)
        remaining = self.budget - total_spent
        
        print(f"Monthly Budget: ${self.budget:.2f}")
        print(f"Total Spent: ${total_spent:.2f}")
        print(f"Remaining: ${remaining:.2f}")
        
        if remaining < 0:
            print("WARNING: You have exceeded your budget!")
        else:
            print(f"You have ${remaining:.2f} left for the month.")
        
        # Show spending by category
        print("\nSpending by Category:")
        categories = {}
        for expense in monthly_expenses:
            if 'category' in expense and 'amount' in expense:
                cat = expense['category']
                categories[cat] = categories.get(cat, 0) + expense['amount']
        
        if categories:
            for category, amount in sorted(categories.items(), key=lambda x: x[1], reverse=True):
                percentage = (amount / self.budget) * 100 if self.budget > 0 else 0
                print(f"{category}: ${amount:.2f} ({percentage:.1f}% of budget)")
        else:
            print("No expenses recorded for this month.")

    def save_expenses(self) -> None:
        """Save expenses to a CSV file."""
        try:
            with open(self.data_file, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['date', 'category', 'amount', 'description'])
                writer.writeheader()
                writer.writerows(self.expenses)
            print(f"\nExpenses saved to {self.data_file}")
        except Exception as e:
            print(f"Error saving expenses: {e}")

    def load_expenses(self) -> None:
        """Load expenses from a CSV file if it exists."""
        if not os.path.exists(self.data_file):
            return
        
        try:
            with open(self.data_file, 'r', newline='') as file:
                reader = csv.DictReader(file)
                self.expenses = []
                for row in reader:
                    # Convert amount from string to float
                    if 'amount' in row:
                        row['amount'] = float(row['amount'])
                    self.expenses.append(row)
            
            # Try to load budget from the last line if it exists
            try:
                with open('budget.txt', 'r') as f:
                    self.budget = float(f.read().strip())
            except (FileNotFoundError, ValueError):
                self.budget = None
                
            print(f"Loaded {len(self.expenses)} expenses from {self.data_file}")
        except Exception as e:
            print(f"Error loading expenses: {e}")

    def save_budget(self) -> None:
        """Save the budget to a file."""
        if self.budget is not None:
            try:
                with open('budget.txt', 'w') as f:
                    f.write(str(self.budget))
            except Exception as e:
                print(f"Error saving budget: {e}")

    def display_menu(self) -> None:
        """Display the main menu options."""
        print("\n=== Personal Expense Tracker ===")
        print("1. Add expense")
        print("2. View expenses")
        print("3. Set budget")
        print("4. Track budget")
        print("5. Save expenses")
        print("6. Exit")

    def run(self) -> None:
        """Run the expense tracker application."""
        print("Welcome to Personal Expense Tracker!")
        
        while True:
            self.display_menu()
            choice = input("\nEnter your choice (1-6): ")
            
            if choice == '1':
                self.add_expense()
            elif choice == '2':
                self.view_expenses()
            elif choice == '3':
                self.set_budget()
                self.save_budget()
            elif choice == '4':
                self.track_budget()
            elif choice == '5':
                self.save_expenses()
                self.save_budget()
                print("All data saved successfully!")
            elif choice == '6':
                self.save_expenses()
                self.save_budget()
                print("Thank you for using Personal Expense Tracker. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    tracker = ExpenseTracker()
    tracker.run()
