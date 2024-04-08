# global variables
DAY1_PRICE = 850
DAY2_PRICE = 850
WEEKEND_CAMP_PRICE = 2000
DAY1_NUMBER_OF_TICKETS = 50
DAY2_NUMBER_OF_TICKETS = 50
WEEKEND_CAMP_NUMBER_OF_TICKETS = 10
FILE_PATH_TO_SUMMARY = 'music_festival_docs/booking_data/'
FILE_PATH_TO_CUSTOMER_DETAILS = 'music_festival_docs/customer_details/'


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
    label = prog_name.upper() + '\n'
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


def print_summary(*args):
    print(get_label('Booking Details', '-'))
    print(f'{"Day1:":<20}' + f'{args[0]:<10}')
    print(f'{"Day2:":<20}' + f'{args[1]:<10}')
    print(f'{"Weekend-Camp:":<20}' + f'{args[2]:<10}')
    print(f'{"Fine Dining Day 1:":<20}' + f'{args[3]:<10}')
    print(f'{"Fine Dining Day 2:":<20}' + f'{args[4]:<10}')


def calc_total(price, dining, group_size):
    total = price * group_size
    if dining and price <= 2000:
        total += (group_size * 20)

    return total


def get_ticket_type(user_choice):
    ticket_type = None
    price = None
    if user_choice == 1:
        ticket_type = 'Day 1'
        price = 850
    elif user_choice == 2:
        ticket_type = 'Day 2'
        price = 850
    elif user_choice == 3:
        ticket_type = 'Weekend-Camp'
        price = 2000
    else:
        print('Incorrect value being used')
    return ticket_type, price


def make_booking():
    print(get_label(prog_name='MUSIC FARM FESTIVAL (BOOKING)'))
    name = get_proper_str(prompt='Enter your full name: >> ', end=15)
    phone_num = get_proper_str(prompt='Enter your phone number: >> ', end=10)
    print(get_menu(prompt='Choose the ticket type:', menu_items_list=['Day 1', 'Day 2', 'Weekend-Camp']))
    user_choice = get_pos_int(prompt='=>   ', end=3)
    ticket_type, price = get_ticket_type(user_choice)
    group_size = get_pos_int(prompt='How many people in your group? >> ', end=4)
    dining = get_answ(prompt='Do you require fine dining pass (Y/N)? >> ')
    total = calc_total(price, dining, group_size)
    print_receipt(name, ticket_type, group_size, dining, total)


def review_booking():
    print(get_label(prog_name='MUSIC FARM FESTIVAL - SUMMARY'))
    print_summary()


def execute_func(user_choice):
    if user_choice == 1:
        make_booking()
    elif user_choice == 2:
        review_booking()
    elif user_choice == 3:
        return False
    else:
        print('Incorrect value being used')


def run():
    show_menu()
    user_choice = get_pos_int('=>   ')
    execute_func(user_choice)
