# imports
from program import booking_system as bs
import time

# global variables
FILE_PATH_TO_BOOKINGS = 'music_festival_docs/booking_data/booking_2024.txt'
FILE_PATH_TO_DININGS = 'music_festival_docs/booking_data/extras.txt'
FILE_PATH_TO_CUSTOMER_DETAILS = 'music_festival_docs/customer_details/'
TICKETS = bs.load_tickets(file_path=FILE_PATH_TO_BOOKINGS, num_elements=4)
DININGS = bs.load_tickets(file_path=FILE_PATH_TO_DININGS, num_elements=2)


def get_answ(prompt: str):
    while True:
        try:
            uansw: str = input(prompt)
            if uansw.lower() in ['y', 'yes', 'yeah', 'yep']:
                return True
            elif uansw.lower() in ['n', 'no', 'nope']:
                return False
            else:
                print('please, enter yes or no ')
        except ValueError:
            print('Provide input with correct input')


def get_proper_str(prompt: str, end=10000):
    while True:
        name = input(prompt)
        if len(name) in range(0, end + 1):
            return name
        else:
            print(f'can not be empty str or you reached a max capacity: {end}')


def get_pos_int(prompt: str, end=1000000000000):
    while True:
        try:
            number = int(input(prompt))
            if number in range(1, end + 1):
                return number
            else:
                print(f'Enter number between 0 and {end}')
        except ValueError:
            print('please enter correct value')
        except TypeError:
            print('must be int')


def get_label(prog_name, sign='='):
    label = '\n' + prog_name.upper() + '\n'
    label += sign * (len(prog_name) + 2)
    return label


def get_menu(prompt, menu_items_list: list):
    counter = 1
    menu = prompt + '\n'
    for item in menu_items_list:
        menu: str = menu + f'{counter}. {item} \n'
        counter += 1
    return menu


def show_menu():
    print(get_label('Music Farm Festival'))
    print(get_menu(prompt='', menu_items_list=['Make a Booking', 'Review Bookings', 'Exit']))


def print_receipt(name, ticket_type, group_size, dining, total):
    print(get_label('Booking Details', '-'))
    print(f'{"Name:":<15}' + f'{name.capitalize():<10}')
    print(f'{"Ticket Type:":<15}' + f'{ticket_type:<10}')
    print(f'{"No of People:":<15}' + f'{group_size:<10}')
    print(f'{"Fine Dining:":<15}' + f'{"Yes" if dining else "No":<10}')
    print(f'{"Total cost:":<15}' + f'{total:<10}')


def calc_total(price, dining, group_size):
    total = price * group_size
    if dining and price < 2000:
        total += (group_size * 20)

    return total


def get_ticket_type(user_choice):
    ticket_type = None
    price = None
    if user_choice == 1:
        ticket_type = 'Day1'
        price = 850
    elif user_choice == 2:
        ticket_type = 'Day2'
        price = 850
    elif user_choice == 3:
        ticket_type = 'Weekend-Camp'
        price = 2000
    else:
        print('Incorrect value being used')
    return ticket_type, price


def make_booking():
    # Display booking header
    print(get_label(prog_name='MUSIC FARM FESTIVAL (BOOKING)'))

    # Collect booking details from the user
    name = get_proper_str(prompt='Enter your full name: >> ', end=15)
    phone_num = get_proper_str(prompt='Enter your phone number: >> ', end=10)
    print(get_menu(prompt='Choose the ticket type:', menu_items_list=['Day1', 'Day2', 'Weekend-Camp']))
    user_choice = get_pos_int(prompt='=>   ', end=3)
    ticket_type, price = get_ticket_type(user_choice)
    group_size = get_pos_int(prompt='How many people in your group? >> ', end=4)

    # Automatically include dining for 'weekend-camp' ticket types, prompt for others
    dining = get_answ(
        prompt='Do you require fine dining pass (Y/N)? >> ') if ticket_type.lower() != 'weekend-camp' else True

    # Calculate total cost and process booking
    total = calc_total(price, dining, group_size)
    bs.sell_ticket(FILE_PATH_TO_BOOKINGS, TICKETS, ticket_type, group_size, total, name, phone_num, dining)

    # Update dining bookings if applicable
    if dining and ticket_type.lower() != 'weekend-camp':
        dining_type = f'FineDining{ticket_type}'
        bs.update_and_save_dining(FILE_PATH_TO_DININGS, DININGS, dining_type, group_size)

    # Print the booking receipt
    print_receipt(name, ticket_type, group_size, dining, total)


def review_booking():
    # Print summary header
    print(get_label(prog_name='MUSIC FARM FESTIVAL - SUMMARY'))

    # Show current tickets and dining bookings
    bs.show_tickets(TICKETS)
    bs.show_dining(DININGS)


def execute_func(user_choice):
    if user_choice == 1:
        make_booking()
        return True
    elif user_choice == 2:
        review_booking()
        return True
    elif user_choice == 3:
        return False
    else:
        print('Incorrect value being used')


def run():
    try:
        loop = True
        while loop:
            show_menu()
            user_choice = get_pos_int('=>   ')  # Get the user's menu choice
            loop = execute_func(user_choice)  # Execute the chosen function
            time.sleep(2)  # Pause for a better user interface experience
    except KeyboardInterrupt:
        print('\nProgram finished\n')