'''
/*******************************************************************************
Project:       Python
File:          NewAccount.py
Author:        Meghna Vyas(MV)

Description:
    Implementing a bank account.


Revision History:
    2020-Jun-10 (MV): Project Created.
        1. Added class Account
        2. Added constructor and destructor
        3. Added static field for account number
        4. Added static method to get next account number
        5. Added read-only properties for account fields
        6. Added deposit & withdraw methods
        7. Added method to print customer details
        8. Added dunders for increment and decrement (deposit & withdraw)
        9. Added dunders for relatinal operators to compare the two account objects
       10. Added dunders for len, getitem, and str methods
       11. Added dunders for iter, next, call, repr, reversed
       12. Added a context manager class TransactionWriter
       13. Added __enter__ & __exit__ to implement passbook functionality using a file
*******************************************************************************/
'''

import datetime


class Account:

    '''

    ACCOUNT CLASS
    -> This is the base class, which contains the basic properties and functionalities of a Bank Account
    -> Contains the following fields :
    (All members are declared protected)
        * holders_name
        * balance
        * account_number 
        * transactions_log : a list of tuples used to log every transaction for the corresponding account
    -> Contains the following methods :
        * deposit()
        * withdraw()
        * print_cust_details()
        * get_next_account_number()
    -> Also contains a few special methods/dunders

'''

    # Static variable holding the account number
    account_number = 328710100001

    @staticmethod
    def get_next_account_number():
        return Account.account_number + 1

    # Constructor
    def __init__(self, name, balance=500.00):
        self._holders_name = name
        self._balance = balance
        self._transactions_log = []
        self._acc_number = Account.account_number
        self.pos = 0
        self.max = len(self)

        # Increment the account number for the next customer
        Account.account_number += 1

    # Destructor
    def __del__(self):
        print("Deleted account no. ", self._acc_number)

    # Read-only properties for Account attributes
    @property
    def number(self):
        return self._acc_number

    @property
    def name(self):
        return self._holders_name

    @property
    def balance(self):
        return self._balance

    # Method to deposit given amount to the account
    def deposit(self, amount):

        # Check if valid amount is being added
        if amount <= 0:
            return False

        # Amount given is valid; deposit and make a log
        self._balance += amount
        self._transactions_log.append(("CREDIT", datetime.datetime.now().strftime(
            "%d %B %Y %I:%M:%S %p"), self._balance - amount, amount, self._balance))
        return True

    # Method to withdraw given amount from the account
    def withdraw(self, amount):

        # Check if valid amount is being withdrawn, and make a log
        if self._balance - amount >= 0:
            self._balance -= amount
            self._transactions_log.append(("DEBIT ", datetime.datetime.now().strftime(
                "%d %B %Y %I:%M:%S %p"), self._balance + amount, -amount, self._balance))
            return True
        return False

    # Method to print customer details
    def print_cust_details(self):
        print("Account Number:  ", self._acc_number)
        print("Holder's Name:   ", self._holders_name)
        print("Balance:          Rs.", self._balance)

    # Overloading += operator for deposit

    def __iadd__(self, amount):
        print("Depositing using dunder ...")
        self.deposit(amount)
        return self

    # Overloading -= operator for withdraw
    def __isub__(self, amount):
        print("Withdrawing using dunder ...")
        self.withdraw(amount)
        return self

    # Overloading less than operator
    def __lt__(self, other):
        if self._balance < other._balance:
            print(self._holders_name, "'s balance is lesser.")
        else:
            print(other._holders_name, "'s balance is lesser.")

    # Overloading grater than operator
    def __gt__(self, other):
        if self._balance > other._balance:
            print(self._holders_name, "'s balance is greater.")
        else:
            print(other._holders_name, "'s balance is greater.")

    # Overloading <=
    def __le__(self, other):
        if self._balance <= other._balance:
            return True
        return False

    # Overloading >=
    def __ge__(self, other):
        if self._balance >= other._balance:
            return True
        return False

    # Overloading ==
    def __eq__(self, other):
        if self._acc_number == other._acc_number:
            return True
        return False

    # Overloading !=
    def __ne__(self, other):
        if self._acc_number != other._acc_number:
            return True
        else:
            return False

    # Overloading str() to display Account attributes
    def __str__(self):
        return "Account No.: {} of {} has Rs. {}".format(self._acc_number, self._holders_name, self._balance)

    # Dunder for number of accounts
    def __len__(self):
        return len(self._transactions_log)

    # Dunder to get a particular transaction from the transactions log
    def __getitem__(self, pos):
        return self._transactions_log[pos]

    # Dunder to iterate over an object
    def __iter__(self):
        self.pos = 0
        self.max = len(self)
        return self

    def __next__(self):
        if self.pos >= self.max:
            raise StopIteration
        else:
            txn = self._transactions_log[self.pos]
            self.pos += 1
            return txn

    def __call__(self):
        self.print_cust_details()

    def __repr__(self):
        return "Account no. {}, owned by {} has a balance of Rs. {}".format(self._acc_number, self._holders_name, self._balance)

    def __reversed__(self):
        return list(reversed(self._transactions_log))


class TransactionWriter:
    '''
       TRANSACTION WRITER
        -> A class to implement the passbook functionality for a bank account
        -> Makes use of context manager to use a file resource to write into it 
            all the transaction logs
    '''

    # Constructor
    def __init__(self, name, mode):
        self.file = None
        self.file_name = name
        self.file_mode = mode

    # Called on entering the runtime context
    def __enter__(self):

        # Open a file with the user given attributes and return it
        self.file = open(self.file_name, self.file_mode)
        print("File open successful!")
        return self.file

    # Called on exiting the runtime context
    def __exit__(self, exc_type, exc_value, exc_tb):

        # Check for any exceptions, if not close the file
        if exc_type == None:
            self.file.close()
            print("File close successful!")
        else:
            print("Something went wrong! ", exc_type)


# Driver code
if __name__ == "__main__":

    # Objects of Account class
    accountA = Account("Guido", 10000.00)
    accountA += 500.00
    accountA -= 3000.00
    accountA += 1000.00
    accountA -= 2000.00
    accountA.print_cust_details()

    accountB = Account("Meghna", 5000.00)

    print("Comparing accounts using dunders ...")
    print(" A > B: ")
    accountA > accountB
    print(" A < B: ")
    accountA < accountB
    print(" A >= B: ", accountA >= accountB)
    print(" A <= B: ", accountA <= accountB)

    print("Calling the dunder method for str()")
    print(str(accountA))

    print("No. of transactions: ", len(accountA))

    print("Printing transactions calling __iter__ & __next__:")
    for txn in accountA:
        print(txn)

    print("Printing account details using __call__: ")
    accountB()

    print("Printing account details by repr(): ")
    print(repr(accountB))

    print("List of transactions in reverse order: ")
    print(reversed(accountA))

    # Now updating the accountA's passbook
    # Calling the runtime context using 'with'
    with TransactionWriter('passbookA.txt', 'w') as passbook:
        for txn in accountA:
            passbook.write(str(txn))
            passbook.write('\n')
