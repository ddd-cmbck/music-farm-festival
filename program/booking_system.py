def load_tickets(file_path):
    tickets = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 4:
                    tickets.append(parts)
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
    return tickets


def save_tickets(file_path, tickets):
    with open(file_path, 'w') as file:
        for ticket in tickets:
            line = ','.join(ticket) + '\n'
            file.write(line)


def show_tickets(tickets):
    for ticket in tickets:
        ticket_type, price, max_tickets, sold_tickets = ticket
        available = int(max_tickets) - int(sold_tickets)
        print(f"{ticket_type} - Price: €{price}, Available: {available}")


def sell_ticket(file_path, tickets, ticket_type, quantity):
    for ticket in tickets:
        if ticket[0] == ticket_type:
            available = int(ticket[2]) - int(ticket[3])
            if quantity > available:
                print("Cannot sell tickets. Exceeds the maximum available.")
            else:
                ticket[3] = str(int(ticket[3]) + quantity)
                print(f"Sold {quantity} {ticket_type} ticket(s).")
                save_tickets(file_path, tickets)
            break
    else:
        print("Invalid ticket type.")
