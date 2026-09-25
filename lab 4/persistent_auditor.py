def load_inventory():
    try:
        with open("inventory.txt", "r") as file:
            lines = file.readlines()

            inventory = int(lines[0].strip())

            history = []

            if len(lines) > 1:
                history_text = lines[1].strip()

                if history_text:
                    history = [int(value) for value in history_text.split(",")]

            return inventory, history

    except FileNotFoundError:
        return 0, []
    
def get_valid_input():
    stock = input("Enter stock quantity (or type 'quit' to stop): ")

    if stock.lower() == "quit":
        return "quit"

    if not stock.isdigit():
        print("Error: Please enter a valid integer.")
        return None

    stock = int(stock)

    if stock < 0:
        print("Error: Negative numbers are not allowed.")
        return None

    return stock


def process_delivery(current_total, new_value):
    new_total = current_total + new_value
    return new_total


def calculate_tax(amount):
    tax = amount * 0.10
    return tax


def generate_report(total_units, failed_attempts):
    print("Total Units Processed:", total_units)
    print("Number of Failed/Rejected Entries:", failed_attempts)


inventory, transaction_history = load_inventory()
failed_entries = 0
delivery_count = 0

def save_inventory(inventory, history):
    with open("inventory.txt", "w") as file:
        file.write(str(inventory) + "\n")
        file.write(",".join(str(value) for value in history))

    print("Inventory saved successfully.")
    
while True:
    stock = get_valid_input()

    if stock == "quit":
        save_inventory(inventory, transaction_history)
        break

    if stock is None:
        failed_entries += 1
        continue

    inventory = process_delivery(inventory, stock)
    transaction_history.append(stock)

    tax = calculate_tax(stock)

    delivery_count += stock

    print("Current inventory:", inventory)
    print("Tax for this delivery:", tax)

    if inventory > 500:
        print("ALERT: Inventory has exceeded 500 units!")
        break


print("Total Deliveries Processed:", delivery_count)
print("Transaction History:", transaction_history)
generate_report(inventory, failed_entries)

