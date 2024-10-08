import pytest
import os
import json
from personal_finance_manager import Transaction, Income, Expense, UserProfile, FinanceManager

# Path for saving and loading profiles
TEST_PROFILE_FILE = 'test_profiles.json'

def test_transaction():
    t = Transaction(100.0, "2024-08-16", "Salary")
    assert t.amount == 100.0
    assert t.date == "2024-08-16"
    assert t.description == "Salary"
    assert str(t) == "2024-08-16 - Salary: $100.00"

def test_income():
    i = Income(150.0, "2024-08-15", "Freelance Work")
    assert isinstance(i, Income)
    assert str(i) == "2024-08-15 - Freelance Work: $150.00"

def test_expense():
    e = Expense(50.0, "2024-08-14", "Groceries")
    assert isinstance(e, Expense)
    assert str(e) == "2024-08-14 - Groceries: $50.00"

def test_user_profile():
    profile = UserProfile("John Doe")
    income = Income(1000.0, "2024-08-01", "Salary")
    expense = Expense(200.0, "2024-08-05", "Utilities")
    profile.add_transaction(income)
    profile.add_transaction(expense)
    assert profile.get_balance() == 800.0
    expected_report = (
        "Report for John Doe:\n"
        "Transactions:\n"
        "2024-08-01 - Salary: $1000.00\n"
        "2024-08-05 - Utilities: $200.00\n"
        "Current Balance: $800.00"
    )
    assert profile.generate_report() == expected_report

def test_finance_manager():
    fm = FinanceManager()
    profile = UserProfile("Jane Smith")
    fm.add_user(profile)
    assert "Jane Smith" in fm.profiles
    fm.remove_user("Jane Smith")
    assert "Jane Smith" not in fm.profiles
    with pytest.raises(KeyError):
        fm.get_user_profile("Jane Smith")

    profile = UserProfile("Alex Brown")
    fm.add_user(profile)
    assert fm.get_user_profile("Alex Brown") == profile

def test_remove_user_success():
    fm = FinanceManager()
    profile = UserProfile("Remove Success")
    fm.add_user(profile)
    assert "Remove Success" in fm.profiles

    fm.remove_user("Remove Success")
    assert "Remove Success" not in fm.profiles

def test_remove_nonexistent_user():
    fm = FinanceManager()
    fm.add_user(UserProfile("Existing User"))

    with pytest.raises(KeyError, match="User profile not found."):
        fm.remove_user("Nonexistent User")

def test_add_invalid_transaction():
    profile = UserProfile("Invalid User")
    with pytest.raises(TypeError):
        profile.add_transaction("Not a Transaction")

def test_handle_nonexistent_profile():
    fm = FinanceManager()
    with pytest.raises(KeyError):
        fm.get_user_profile("Nonexistent User")

def test_save_and_load_profiles():
    fm = FinanceManager()
    profile = UserProfile("Save Load Test")
    income = Income(500.0, "2024-08-10", "Testing Save")
    profile.add_transaction(income)
    fm.add_user(profile)
    fm.save_profiles(TEST_PROFILE_FILE)

    # Create a new FinanceManager and load profiles
    fm_loaded = FinanceManager()
    fm_loaded.load_profiles(TEST_PROFILE_FILE)

    loaded_profile = fm_loaded.get_user_profile("Save Load Test")
    assert loaded_profile.get_balance() == 500.0
    assert str(loaded_profile.transactions[0]) == "2024-08-10 - Testing Save: $500.00"

    # Clean up
    os.remove(TEST_PROFILE_FILE)
