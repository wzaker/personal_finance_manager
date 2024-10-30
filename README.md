# Personal Finance Manager 
**Python**

## Purpose
The Personal Finance Manager (PFM) is designed to help users keep track of their finances by:
- Tracking income and expenses
- Calculating net balances
- Generating detailed financial reports

## Project Goals
- **Track Transactions**: Log and categorize each financial entry (income and expenses).
- **Calculate Balance**: Compute the net balance by subtracting expenses from income.
- **Generate Reports**: Provide users with a summary of their financial activities and current balance.

## CLI Commands Overview

### Usage
To start using the PFM, run the main script:
```bash
python3 personal_finance_manager.py
```
### Add Transaction
To add a transaction, use the following command:
```bash
python3 personal_finance_manager.py add <name> <amount> <date> <description>
```
### Generate Report
To generate a report, use the following command:
```bash
python3 personal_finance_manager.py report <name>
```
### View Balance
To view the balance, use the following command:
```bash
python3 personal_finance_manager.py balance <name>
```
### Remove User
To remove a user, use the following command:
```bash
python3 personal_finance_manager.py remove_user <name>
```
 
## Testing
Testing for the personal finance manager was done using **pytest**


