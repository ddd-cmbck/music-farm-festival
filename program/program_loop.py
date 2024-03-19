def get_pos_int(prompt: str):
    while True:
        try:
            number = int(input(prompt))
            if number in range(1, 4):
                return number
            else:
                raise ValueError('int can not be negative(0 included)')

        except ValueError:
            print('please enter correct value')
        except TypeError:
            print('must be int')


def get_label(prog_name, sign='=', length=20):
    label = prog_name.upper() + '\n'
    label += sign * length
    return label


def get_menu():
    menu = '1. Make a Booking\n' + \
           '2. Review Bookings\n' + \
           '3. Exit\n'
    return menu


def show_menu():
    print(get_label('Music Farm Festival'))
    print(get_menu())


def execute_func(user_choice):
    pass


def run():
    show_menu()
    user_choice = get_pos_int('=>   ')
    execute_func(user_choice)
