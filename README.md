# Personal Expense Tracker

## Project Synopsis

The Personal Expense Tracker is a command-line application designed to help individuals manage their daily expenses effectively. In today's fast-paced world, keeping track of personal finances is crucial for financial well-being. This application allows users to log their daily expenses, categorize them, and monitor their spending against a monthly budget.

### Key Features

- **Expense Logging**: Record daily expenses with date, category, amount, and description
- **Expense Categorization**: Organize expenses into categories (e.g., Food, Transportation, Entertainment)
- **Budget Management**: Set monthly budgets and track spending against them
- **Data Persistence**: Save and load expense data from CSV files for future reference
- **User-Friendly Interface**: Navigate through an intuitive menu-driven interface

## High-Level Architecture

### Component Diagram

```
+---------------------+     +---------------------+     +---------------------+
|                     |     |                     |     |                     |
|  User Interface     |     |  Expense Manager    |     |  Data Storage       |
|  (CLI Menu)         |<--->|  (Core Logic)       |<--->|  (CSV File)         |
|                     |     |                     |     |                     |
+---------------------+     +---------------------+     +---------------------+
```

### Components

1. **User Interface (UI) Layer**
   - Handles user input and output through a command-line interface
   - Displays the menu and prompts for user actions
   - Formats and presents expense data and budget information

2. **Expense Manager (Business Logic Layer)**
   - Manages expense data (add, view, categorize)
   - Handles budget setting and tracking
   - Performs calculations and validations

3. **Data Storage Layer**
   - Manages reading from and writing to CSV files
   - Ensures data persistence between application sessions

### Data Flow

1. User interacts with the CLI menu
2. User input is processed by the Expense Manager
3. Expense Manager performs necessary operations on the data
4. Data is saved to or loaded from CSV files as needed
5. Results are displayed back to the user through the UI

### Data Model

```
Expense:
{
    'date': 'YYYY-MM-DD',
    'category': 'Category Name',
    'amount': float,
    'description': 'Description text'
}

Budget:
{
    'amount': float
}
```

## Implementation Details

The application is implemented in Python, utilizing built-in libraries for file handling and data manipulation. The code structure follows a modular approach for better maintainability and extensibility.

### File Structure

```
PersonalExpenseTracker/
│
├── expense_tracker.py    # Main application file
├── expenses.csv          # Data storage file (created when expenses are saved)
└── README.md             # Project documentation
```

### Dependencies

- Python 3.x
- Standard libraries: csv, datetime, os

## Usage

1. Run the application: `python expense_tracker.py`
2. Follow the on-screen menu to:
   - Add new expenses
   - View existing expenses
   - Set and track your budget
   - Save expenses to file
   - Exit the application

## Future Enhancements

- Data visualization for expense trends
- Multiple budget categories
- Export to different file formats
- Web or GUI interface
