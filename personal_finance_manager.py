import argparse
import json
from datetime import datetime

class Transaction:
    """
    Represents a financial transaction.

    Attributes:
        amount (float): The amount of the transaction.
        date (str): The date of the transaction in YYYY-MM-DD format.
        description (str): A description of the transaction.
    """

    def __init__(self, amount, date, description):
        """
        Initializes a Transaction instance.

        Args:
            amount (float): The amount of the transaction.
            date (str): The date of the transaction.
            description (str): The description of the transaction.
        """
        self.amount = amount
        self.date = date
        self.description = description

    def __str__(self):
        """
        Returns a string representation of the transaction.

        Returns:
            str: A string describing the transaction.
        """
        return f"{self.date} - {self.description}: ${self.amount:.2f}"

class Income(Transaction):
    """
    Represents an income transaction.

    Inherits from:
        Transaction
    """

    def __init__(self, amount, date, description):
        """
        Initializes an Income instance.

        Args:
            amount (float): The amount of the income.
            date (str): The date of the income.
            description (str): The description of the income.
        """
        super().__init__(amount, date, description)

class Expense(Transaction):
    """
    Represents an expense transaction.

    Inherits from:
        Transaction
    """

    def __init__(self, amount, date, description):
        """
        Initializes an Expense instance.

        Args:
            amount (float): The amount of the expense.
            date (str): The date of the expense.
            description (str): The description of the expense.
        """
        super().__init__(amount, date, description)

class UserProfile:
    """
    Represents a user profile that manages financial transactions.

    Attributes:
        name (str): The name of the user.
        transactions (list): A list of Transaction instances associated with the user.
    """

    def __init__(self, name):
        """
        Initializes a UserProfile instance.

        Args:
            name (str): The name of the user.
        """
        self.name = name
        self.transactions = []

    def add_transaction(self, transaction):
        """
        Adds a transaction to the user's profile.

        Args:
            transaction (Transaction): The transaction to be added.

        Raises:
            TypeError: If the transaction is not an instance of Transaction.
        """
        if not isinstance(transaction, Transaction):
            raise TypeError("Only Transaction instances can be added.")
        self.transactions.append(transaction)

    def get_balance(self):
        """
        Calculates the current balance of the user.

        Returns:
            float: The difference between total income and total expenses.
        """
        income_total = sum(t.amount for t in self.transactions if isinstance(t, Income))
        expense_total = sum(t.amount for t in self.transactions if isinstance(t, Expense))
        return income_total - expense_total

    def generate_report(self):
        """
        Generates a report of all transactions sorted by date.

        Returns:
            str: A string containing the report with transaction details and the current balance.
        """
        # Sorting transactions by date
        self.transactions.sort(key=lambda t: datetime.strptime(t.date, "%Y-%m-%d"))
        
        report_lines = [f"Report for {self.name}:"]
        report_lines.append("Transactions:")
        for transaction in self.transactions:
            report_lines.append(str(transaction))
        report_lines.append(f"Current Balance: ${self.get_balance():.2f}")
        return "\n".join(report_lines)

class FinanceManager:
    """
    Manages multiple user profiles and overall app management.

    Attributes:
        profiles (dict): A dictionary of UserProfile objects keyed by user name.
    """

    def __init__(self):
        """
        Initializes a FinanceManager instance.
        """
        self.profiles = {}

    def add_user(self, user_profile):
        """
        Adds a user profile to the manager.

        Args:
            user_profile (UserProfile): The UserProfile to be added.

        Raises:
            TypeError: If the user_profile is not an instance of UserProfile.
        """
        if not isinstance(user_profile, UserProfile):
            raise TypeError("Only UserProfile instances can be added.")
        self.profiles[user_profile.name] = user_profile

    def remove_user(self, user_name):
        """
        Removes a user profile from the manager.

        Args:
            user_name (str): The name of the user profile to be removed.

        Raises:
            KeyError: If the user profile is not found.
        """
        if user_name in self.profiles:
            del self.profiles[user_name]
        else:
            raise KeyError("User profile not found.")

    def get_user_profile(self, user_name):
        """
        Retrieves a user profile from the manager.

        Args:
            user_name (str): The name of the user profile to retrieve.

        Returns:
            UserProfile: The requested UserProfile.

        Raises:
            KeyError: If the user profile is not found.
        """
        if user_name in self.profiles:
            return self.profiles[user_name]
        else:
            raise KeyError("User profile not found.")

    def save_profiles(self, filename='profiles.json'):
        """
        Saves all user profiles to a JSON file.

        Args:
            filename (str): The name of the file to save the profiles to.
        """
        with open(filename, 'w') as file:
            profiles_data = {}
            for name, profile in self.profiles.items():
                profiles_data[name] = {
                    'transactions': [
                        {'amount': t.amount, 'date': t.date, 'description': t.description, 'type': 'Income' if isinstance(t, Income) else 'Expense'}
                        for t in profile.transactions
                    ]
                }
            json.dump(profiles_data, file, indent=4)

    def load_profiles(self, filename='profiles.json'):
        """
        Loads user profiles from a JSON file.

        Args:
            filename (str): The name of the file to load the profiles from.
        """
        try:
            with open(filename, 'r') as file:
                profiles_data = json.load(file)
                for name, data in profiles_data.items():
                    profile = UserProfile(name)
                    for t_data in data['transactions']:
                        if t_data['type'] == 'Income':
                            transaction = Income(t_data['amount'], t_data['date'], t_data['description'])
                        else:
                            transaction = Expense(t_data['amount'], t_data['date'], t_data['description'])
                        profile.add_transaction(transaction)
                    self.add_user(profile)
        except FileNotFoundError:
            pass

# Command Line Interface

def parse_args():
    """
    Parses command-line arguments.

    Returns:
        argparse.Namespace: The parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Personal Finance Manager CLI")
    parser.add_argument("command", choices=["add", "report", "balance", "remove_user"], help="Command to execute")
    parser.add_argument("name", type=str, help="User profile name")
    parser.add_argument("amount", type=float, nargs="?", help="Transaction amount (required for 'add' command)")
    parser.add_argument("date", type=str, nargs="?", help="Transaction date (YYYY-MM-DD) (required for 'add' command)")
    parser.add_argument("description", type=str, nargs="?", help="Transaction description (required for 'add' command)")
    return parser.parse_args()

def main():
    """
    Main function to execute commands based on parsed arguments.
    """
    args = parse_args()
    fm = FinanceManager()
    fm.load_profiles()

    if args.command == "add":
        if not (args.amount and args.date and args.description):
            print("Error: amount, date, and description are required for 'add' command.")
            return

        profile = fm.get_user_profile(args.name) if args.name in fm.profiles else UserProfile(args.name)
        if args.amount > 0:
            transaction = Income(args.amount, args.date, args.description)
        else:
            transaction = Expense(-args.amount, args.date, args.description)
        profile.add_transaction(transaction)
        fm.add_user(profile)
        fm.save_profiles()
        print("Transaction added successfully.")

    elif args.command == "report":
        try:
            profile = fm.get_user_profile(args.name)
            print(profile.generate_report())
        except KeyError:
            print("Error: User profile not found.")

    elif args.command == "balance":
        try:
            profile = fm.get_user_profile(args.name)
            print(f"Current Balance for {args.name}: ${profile.get_balance():.2f}")
        except KeyError:
            print("Error: User profile not found.")
    
    elif args.command == "remove_user":
        try:
            fm.remove_user(args.name)
            fm.save_profiles()
            print(f"User profile '{args.name}' removed successfully.")
        except KeyError:
            print("Error: User profile not found.")

if __name__ == "__main__":
    main()
