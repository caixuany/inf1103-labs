
import json
import os

from product import Product
from inventory import Inventory


DATA_FILE = "inventory.json"


def load_inventory(inventory):
    if not os.path.exists(DATA_FILE):
        print("No saved inventory found. Starting with empty inventory.")
        return

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("Inventory JSON must contain a list.")

        for item in data:
            product = Product(
                item["id"],
                item["name"],
                item["price"],
                item["stock"]
            )
            inventory.add_product(product)

        print("Inventory loaded successfully.")

    except (json.JSONDecodeError, KeyError, TypeError,
            ValueError) as error:
        print(f"Could not load inventory: {error}")


def save_inventory(inventory):
    data = [
        product.to_dict()
        for product in inventory.get_products()
    ]

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print("Inventory saved successfully.")


def add_product(inventory):
    try:
        product_id = input("Enter product ID: ").strip()
        name = input("Enter product name: ").strip()

        if not product_id or not name:
            print("Product ID and name cannot be empty.")
            return

        price = float(input("Enter product price: "))
        stock = int(input("Enter stock quantity: "))

        if price < 0 or stock < 0:
            print("Price and stock cannot be negative.")
            return

        product = Product(product_id, name, price, stock)
        inventory.add_product(product)

        print("Product added successfully.")

    except ValueError as error:
        print(f"Invalid input: {error}")


def update_product_stock(inventory):
    product_id = input("Enter product ID: ").strip()
    product = inventory.search_product(product_id)

    if product is None:
        print("Product not found.")
        return

    try:
        quantity = int(input("Enter new stock quantity: "))

        if quantity < 0:
            print("Stock cannot be negative.")
            return

        product.update_stock(quantity)
        print("Stock updated successfully.")

    except ValueError:
        print("Please enter a valid whole number.")


def search_product(inventory):
    product_id = input("Enter product ID to search: ").strip()
    product = inventory.search_product(product_id)

    if product is None:
        print("Product not found.")
    else:
        product.display_information()


def display_menu():
    print("\n===== INVENTORY MANAGEMENT SYSTEM =====")
    print("1. Display all products")
    print("2. Add a product")
    print("3. Update stock")
    print("4. Search for a product")
    print("5. Save inventory")
    print("6. Exit")


def main():
    inventory = Inventory()
    load_inventory(inventory)

    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            inventory.display_all()

        elif choice == "2":
            add_product(inventory)

        elif choice == "3":
            update_product_stock(inventory)

        elif choice == "4":
            search_product(inventory)

        elif choice == "5":
            try:
                save_inventory(inventory)
            except OSError as error:
                print(f"Could not save inventory: {error}")

        elif choice == "6":
            print("Exiting Inventory Management System.")
            break

        else:
            print("Invalid choice. Please enter 1 to 6.")


if __name__ == "__main__":
    main()
