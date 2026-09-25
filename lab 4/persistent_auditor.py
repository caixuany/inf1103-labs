def get_valid_input():
    stock = input("Enter stock quantity (or type 'quit' to stop): ")

    if stock.lower() == "quit":
        return "quit"

    try:
        stock = int(stock)
    except ValueError:
        print("Error: Please enter a valid integer.")
        return None

    if stock < 0:
        print("Error: Negative numbers are not allowed.")
        return None

    return stock


def process_delivery(current_total, new_value):
    return current_total + new_value


def calculate_tax(amount):
    return amount * 0.10


def generate_report(total_units, failed_attempts):
    print("\n----- Final Report -----")
    print("Total Units Processed:", total_units)
    print("Number of Failed/Rejected Entries:", failed_attempts)


def load_inventory():
    try:
        with open("inventory.txt", "r") as file:
            lines = file.readlines()

            # If file is empty
            if len(lines) == 0:
                return 0, []

            inventory = int(lines[0].strip())

            history = []

            if len(lines) > 1:
                history_text = lines[1].strip()

                if history_text:
                    history = [
                        int(value)
                        for value in history_text.split(",")
                    ]

            return inventory, history

    except FileNotFoundError:
        # If inventory.txt does not exist yet
        return 0, []

    except ValueError:
        # If file contains invalid data
        return 0, []


def save_inventory(inventory, history):
    with open("inventory.txt", "w") as file:
        file.write(str(inventory) + "\n")

        history_text = ",".join(str(value) for value in history)
        file.write(history_text)

    print("Inventory successfully saved to inventory.txt")


# Load previous inventory when program starts
inventory, transaction_history = load_inventory()

failed_entries = 0
delivery_count = 0

print("Starting inventory:", inventory)
print("Previous transaction history:", transaction_history)


while True:
    stock = get_valid_input()

    if stock == "quit":
        save_inventory(inventory, transaction_history)
        break

    if stock is None:
        failed_entries += 1
        continue

    # Update inventory
    inventory = process_delivery(inventory, stock)

    # Store every valid transaction
    transaction_history.append(stock)

    tax = calculate_tax(stock)

    delivery_count += 1

    print("\nCurrent inventory:", inventory)
    print("Tax for this delivery:", tax)
    print("Transaction history:", transaction_history)

    if inventory > 500:
        print("ALERT: Inventory has exceeded 500 units!")


print("\nTotal Deliveries Processed:", delivery_count)
generate_report(inventory, failed_entries)