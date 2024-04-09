# imports
from program import booking_system as bs
import time

# global variables
FILE_PATH_TO_BOOKINGS = 'music_festival_docs/booking_data/booking_2024.txt'
FILE_PATH_TO_DININGS = 'music_festival_docs/booking_data/extras.txt'
FILE_PATH_TO_GROUPS = 'music_festival_docs/booking_data/groups.txt'
FILE_PATH_TO_SUMMARY = 'music_festival_docs/booking_data/summary.txt'
FILE_PATH_TO_CUSTOMER_DETAILS = 'music_festival_docs/customer_details/'
TICKETS = bs.load_items(file_path=FILE_PATH_TO_BOOKINGS, num_elements=4)
DININGS = bs.load_items(file_path=FILE_PATH_TO_DININGS, num_elements=2)


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
    print(
        get_menu(prompt='', menu_items_list=['Make a Booking', 'Review Bookings', 'Groups', 'Stats', 'Income', 'Exit']))


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
    group_size = get_pos_int(prompt='How many people in your group? >> ')

    # Automatically include dining for 'weekend-camp' ticket types, prompt for others
    dining = get_answ(
        prompt='Do you require fine dining pass (Y/N)? >> ') if ticket_type.lower() != 'weekend-camp' else True

    # Calculate total cost and process booking
    total = calc_total(price, dining, group_size)
    TICKET_TOTALS.append(total)
    bs.sell_ticket(FILE_PATH_TO_BOOKINGS, TICKETS, ticket_type, group_size, total, name, phone_num, dining)
    bs.update_group_file(FILE_PATH_TO_GROUPS, name, group_size)

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


def review_groups():
    print(get_label(prog_name='MUSIC FARM FESTIVAL - GROUPS'))
    group_list = bs.load_items(file_path=FILE_PATH_TO_GROUPS, num_elements=2)
    if len(group_list) > 0:
        bs.show_groups(group_list)
    else:
        print('No bookings yet')


def show_names_and_sizes(group_list):
    name_list = []
    size_list = []
    for group in group_list:
        name_list.append(group[0])
        size_list.append(group[1])
    return name_list, size_list


def find_largest(sizes, names):
    name = 'default'
    biggest_num = 0
    largest_group = [name, biggest_num]
    for i in range(0, len(sizes) - 1):
        num = sizes[i]
        if num > biggest_num:
            biggest_num = num
            name = names[i]
    largest_group[0] = name
    largest_group[1] = biggest_num
    return largest_group


def find_average(sizes):
    total = 0
    for s in sizes:
        total += s
    average = total / len(sizes)
    return average


def show_stats():
    group_list = bs.load_items(file_path=FILE_PATH_TO_GROUPS, num_elements=2)
    names, sizes = show_names_and_sizes(group_list)
    largest_group = find_largest(sizes, names)
    average = find_average(sizes)
    print(f'The largest booking is by {largest_group[0]} and is for {largest_group[1]} people.')
    print(f'The average size is {average}')


def find_income_for_item(tickets_list, dinings_list):
    totals = []
    for item in tickets_list:
        totals.append(item[3])
    for item in dinings_list:
        totals.append(item[1])
    return totals


def review_income():
    totals = find_income_for_item(TICKETS, DININGS)
    day1 = int(totals[0]) * 850
    day2 = int(totals[1]) * 850
    weekend = int(totals[2]) * 2000
    dining = int(totals[3]) * 20
    dining += int(totals[3]) * 20
    total_income = int(day1 + day2 + weekend + dining)
    print(f'TOTAL: {total_income}')
    user_answ = get_answ('Would you like to see a breakdown Y/N: ')
    if user_answ:
        print(f'DAY1: {day1}\n'
              f'DAY2: {day2}\n'
              f'WEEKEND: {weekend}\n'
              f'FINE DINING: {dining}\n'
              f'TOTAL: {total_income}\n')


def execute_func(user_choice):
    if user_choice == 1:
        make_booking()
    elif user_choice == 2:
        review_booking()
    elif user_choice == 3:
        review_groups()
    elif user_choice == 4:
        show_stats()
    elif user_choice == 5:
        review_income()
    elif user_choice == 6:
        print('Program finished')
        return False
    else:
        print('Incorrect value being used')
    return True


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
