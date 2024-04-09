
def load_tickets(file_path, num_elements):
    tickets = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                items = line.strip().split(',')
                if len(items) == num_elements:
                    tickets.append(items)
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
    return tickets


def update_and_save_dining(file_path, dinings, dining_type, group_size):
    for item in dinings:
        if item[0] == dining_type:
            item[1] = str(int(item[1]) + group_size)
            break

    with open(file_path, 'w') as file:
        for item in dinings:
            file.write(','.join(item) + '\n')



def save_tickets(file_path, tickets):
    with open(file_path, 'w') as file:
        for ticket in tickets:
            line = ','.join(ticket) + '\n'
            file.write(line)


def show_tickets(tickets):
    for ticket in tickets:
        ticket_type, price, max_tickets, sold_tickets = ticket
        available = int(max_tickets) - int(sold_tickets)
        print(f"{ticket_type} - Price: \u20AC{price}, Available: {available}")


def show_dining(dinings):
    for dining in dinings:
        dining_type, sold_dinings = dining
        print(f"{dining_type} - Sold: {sold_dinings}")


def create_sale_file(name, ticket_type, phone_number, group_size, total, is_dining):
    file_name = f"music_festival_docs/customer_details/{name.replace(' ', '_')}_sale.txt"
    with open(file_name, 'w') as file:
        file.write(f"Ticket Type: {ticket_type}\n")
        file.write(f"Phone Number: {phone_number}\n")
        file.write(f"Group Size: {group_size}\n")
        file.write(f"Total Cost: €{total}\n")
        file.write("Fine Dining Included: Yes" if is_dining else "Fine Dining Included: No")


def sell_ticket(file_path, tickets, ticket_type, quantity, total, name, phone_number, is_dining=False):
    for ticket in tickets:
        if ticket[0] == ticket_type:
            available = int(ticket[2]) - int(ticket[3])
            if quantity > available:
                print("Cannot sell tickets. Exceeds the maximum available.")
            else:
                ticket[3] = str(int(ticket[3]) + quantity)
                save_tickets(file_path, tickets)
            create_sale_file(name, ticket_type, phone_number, quantity, total, is_dining)
            break
    else:
        print("Invalid ticket type.")
