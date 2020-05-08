import random
import os
import re
from datetime import datetime

"""
This function generate a unique 10 digits number. The first two numbers are constant and the last eight are 
automatically generated by the random module. This will generate the account number.
"""


def acc_number():
    length = 8
    gen_number = '22'
    auto_number = ''.join(map(str, random.sample(range(0, 9), length)))
    number = gen_number + auto_number
    return number

"""
This function will append customer information to the Customer database. I do this by calling the below created
function append_new_line() multiple times why the file is opened only once and append all the lines to it. 
I do this by:
Opening the file in append & read mode (‘a+’). Both read & write cursor points to the end of the file.
Move read cursor to the start of the file.
Read some text from the file and check if the file is empty or not.
If the file is not empty, then set appendEOL as True else False
Now for each element in the list
If its first element in List and appendEOL is False
Don’t append ‘\n’ at the end of the file using write() function.
Else
Append ‘\n’ at the end of the file using write() function.
Append the element  to the file using write() function.
Close the file
Basically we don’t need to write first ‘\n’ if the file is empty.
"""


def append_multiple_lines(lines_to_append):
    with open('customer', "a+") as append_file:
        append_eol = False
        append_file.seek(0)
        data = append_file.read(100)
        if len(data) > 0:
            append_eol = True
        for line in lines_to_append:
            if append_eol:
                append_file.write("\n")
            else:
                append_eol = True
            append_file.write(line)
    return


def append_lines(filename, lines_to_append):
    with open(filename, "a+") as append_file:
        append_eol = False
        append_file.seek(0)
        data = append_file.read(100)
        if len(data) > 0:
            append_eol = True
        for line in lines_to_append:
            if append_eol:
                append_file.write("\n")
            else:
                append_eol = True
            append_file.write(line)
    return


"""
This the function that enables the user to login. The user is asked to input their username and password. 
The database will be opened in read only format. 
A counter is set to 0. Each line of the file is read. 
Each line is split into two.
indexes, demarcated by :. The files before : is 0 and The files after : is 1. 
If the length of the demarcation is greater that 1. 
Index 0 will be compare with Username in the database and Index 1 will be compared with the user inputted username. 
If they both correlate, the counter will increase by 1. The same thing will occur for the Password and the counter 
will increment by 1 again. 
If the value of the counter compares to 2. 
The now method in the datetime class is called and kept with a variable.
The username and time were letter stored in a variable and written into a file. 
If the user login credential is wrong, an error message will be thrown.
"""


def login():
    while True:
        username = input("Please Enter your username: ")
        password = input('Enter password: ')

        with open('staff') as staff_file:
            is_logged_in = 0
            for lines in staff_file.readlines():
                staff_split = lines.split(':')
                if len(staff_split) > 1:
                    if staff_split[0] == 'Username' and staff_split[1].strip() == username:
                        is_logged_in += 1

                    elif staff_split[0] == 'Password' and staff_split[1].strip() == password:
                        is_logged_in += 1

            if is_logged_in == 2:
                time = datetime.now()
                session_items = [f'username: {username}', f'time: {time}']
                append_lines('session.txt', session_items)

                print(f'\n{username} logged in...')
                print(f"\nWelcome {username}.")
                break

            else:
                print('\nERROR! Wrong login details')

    return


regex = "^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"


while True:
    user_option = int(input(f"""
Please select 1 or 2 to proceed.
1 ===> Staff login
2 ===> Close App

Select an Option:
"""))

    if user_option == 1:
        login()

        while True:
            logged_in_option = int(input(f"""
Please select 1 or 2 or 3 to proceed.
1 ===> Create A New Bank Account
2 ===> Check Account Details
3 ===> Logout

Select an Option:
"""))

            if logged_in_option == 1:
                account_name = input('\nEnter the Account Name: ')
                opening_balance = input('Enter the Opening Balance: N')
                account_type = input('Enter the Account Type (Current or Savings): ')

                while True:
                    account_email = input('Enter the Account Email: ')
                    if re.search(regex, account_email):
                        pass
                        break
                    else:
                        print("\nInvalid Email. \nEnter your email again\n")

                while True:
                    account_number = acc_number()
                    is_acc_num = 0
                    customer_file = open('customer', 'r')
                    for file in customer_file.readlines():
                        x = file.split(':')
                        if len(x) > 1:
                            if x[0] == 'Account Number' and x[1].strip() == account_number:
                                is_acc_num += 1
                    if is_acc_num == 1:
                        pass

                    else:
                        pass
                        break

                list_items = [f'Account Number: {account_number}', f'Account Name: {account_name}',
                              f'Opening Balance: N{opening_balance}', f'Account Type: {account_type}',
                              f'Account Email: {account_email}\n---']
                append_multiple_lines(list_items)

                print(f'\n{account_name} Account Number is: {account_number}\n')

            elif logged_in_option == 2:
                while True:
                    customer_acc_number = input('Enter Account Number: ')
                    customer_file = open('customer', 'r').read()
                    if customer_acc_number in customer_file:
                        if len(customer_acc_number) == 10:
                            first_line = customer_file.find('Account Number: ' + customer_acc_number)
                            customer_line = customer_file[first_line:]
                            last_line = customer_line.find('---')
                            customer_line = customer_line[:last_line]
                            print(customer_line)
                            break

                        else:
                            print('ERROR! Account number not up to 10.\n')

                    else:
                        print('Customer not found!\n')

            elif logged_in_option == 3 and os.path.exists('session.txt'):

                print(f'\nSee you next time.')
                os.remove('session.txt')
                print('\nLogging out...')
                break

    elif user_option == 2:
        print('\nClosing App...')
        print('\nApp Closed. See you next time!')
        break

