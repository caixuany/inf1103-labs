
from discount import (DiscountStrategy, NoDiscount, PercentageDiscount,
                      BulkDiscount, StudentDiscount)
from inventory import Inventory, load_products
from order import Order
from product_factory import ProductFactory
from supplier import Supplier


def get_positive_float(prompt: str) -> float:
    """Keep asking until the user types a number greater than zero."""
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


def get_non_negative_int(prompt: str) -> int:
    """Keep asking until the user types a whole number that is 0 or more."""
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Please enter 0 or a positive whole number.")
                continue
            return value
        except ValueError:
            print("Please enter a whole number, e.g. 10")


def save_inventory(inventory: Inventory) -> None:
    try:
        inventory.save_inventory()
    except OSError as error:
        print(f"Could not save inventory: {error}")


def get_supplier(inventory: Inventory) -> Supplier | None:
    """Reuse an existing Supplier object or create a new one."""
    supplier_id = input("Enter supplier ID: ").strip()

    if not supplier_id:
        print("Supplier ID cannot be empty.")
        return None

    # Several products can be associated with the same Supplier object
    for product in inventory.get_products():
        if product.get_supplier().get_supplier_id() == supplier_id:
            supplier = product.get_supplier()
            print(f"Using existing supplier: {supplier.get_name()}")
            return supplier

    name = input("Enter supplier name: ").strip()
    contact_email = input("Enter supplier contact email: ").strip()

    if not name or "@" not in contact_email:
        print("Supplier name and a valid email are required.")
        return None

    return Supplier(supplier_id, name, contact_email)


def add_product(inventory: Inventory) -> None:
    print("\n===== ADD PRODUCT =====")
    print("1. Physical Product")
    print("2. Digital Product")

    choice = input("Choose product type: ").strip()
    product_types = {"1": "physical", "2": "digital"}

    if choice not in product_types:
        print("Invalid product type.")
        return

    product_id = input("Enter product ID: ").strip()
    name = input("Enter product name: ").strip()

    if not product_id or not name:
        print("Product ID and name cannot be empty.")
        return

    if inventory.find_product(product_id) is not None:
        print("A product with this ID already exists.")
        return

    # These helpers keep asking until the value is valid
    price = get_positive_float("Enter product price: ")
    stock = get_non_negative_int("Enter stock quantity: ")

    supplier = get_supplier(inventory)

    if supplier is None:
        return

    weight = 0.0
    download_size = 0.0

    if product_types[choice] == "physical":
        weight = get_positive_float("Enter weight in kg: ")
    else:
        download_size = get_positive_float("Enter download size in MB: ")

    try:
        product = ProductFactory.create(
            product_types[choice], product_id, name, price, stock,
            supplier, weight=weight, download_size=download_size
        )
        inventory.add_product(product)
        print("Product added successfully.")
    except ValueError as error:
        print(f"Could not add product: {error}")


def update_product_stock(inventory: Inventory) -> None:
    product_id = input("Enter product ID: ").strip()
    product = inventory.find_product(product_id)

    if product is None:
        print("Product not found.")
        return

    quantity = get_non_negative_int("Enter new stock quantity: ")
    product.update_stock(quantity)
    print("Stock updated successfully.")


def search_product(inventory: Inventory) -> None:
    product_id = input("Enter product ID to search: ").strip()
    product = inventory.find_product(product_id)

    if product is None:
        print("Product not found.")
    else:
        product.display_information()
        print(product.get_fulfilment_info())


def remove_product(inventory: Inventory) -> None:
    product_id = input("Enter product ID to remove: ").strip()
    product = inventory.remove_product(product_id)

    if product is None:
        print("Product not found.")
    else:
        print(f"{product.get_name()} removed from the inventory.")


def choose_discount() -> DiscountStrategy:
    # main.py picks which strategy to use, Order never has to know
    discounts: dict[str, DiscountStrategy] = {
        "1": NoDiscount(),
        "2": PercentageDiscount(10),
        "3": BulkDiscount(200, 20),
        "4": StudentDiscount(),
    }

    print("Discount options:")
    for key, discount in discounts.items():
        print(f"{key}. {discount.describe()}")

    choice = input("Choose a discount (default 1): ").strip()

    if choice not in discounts:
        print("No valid choice, using no discount.")
        return NoDiscount()

    return discounts[choice]


def create_order(inventory: Inventory) -> None:
    order_id = input("Enter order ID: ").strip()

    if not order_id:
        print("Order ID cannot be empty.")
        return

    order = Order(order_id)

    while True:
        product_id = input(
            "Enter product ID to order (blank to finish): "
        ).strip()

        if not product_id:
            break

        product = inventory.find_product(product_id)

        if product is None:
            print("Product not found.")
            continue

        try:
            quantity = int(input("Enter quantity: "))
            # The Order creates its own OrderLine internally
            order.add_order_line(product, quantity)
        except ValueError as error:
            print(f"Invalid input: {error}")

    order.set_discount(choose_discount())
    print()
    order.display_order()


def load_products_from_csv(inventory: Inventory) -> None:
    path = input("Enter CSV file path (default products.csv): ").strip()
    supplier = Supplier("S100", "CSV Import Supplier", "import@example.com")
    load_products(path or "products.csv", inventory, supplier)


def display_menu() -> None:
    print("\n===== INVENTORY MANAGEMENT SYSTEM =====")
    print("1. Display all products")
    print("2. Add a product")
    print("3. Update product stock")
    print("4. Search for a product")
    print("5. Remove a product")
    print("6. Create an order")
    print("7. Load products from CSV")
    print("8. Save inventory")
    print("9. Exit")


def main() -> None:
    inventory = Inventory()
    inventory.load_inventory()

    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            inventory.display_all_products()
        elif choice == "2":
            add_product(inventory)
        elif choice == "3":
            update_product_stock(inventory)
        elif choice == "4":
            search_product(inventory)
        elif choice == "5":
            remove_product(inventory)
        elif choice == "6":
            create_order(inventory)
        elif choice == "7":
            load_products_from_csv(inventory)
        elif choice == "8":
            save_inventory(inventory)
        elif choice == "9":
            save_inventory(inventory)
            print("Exiting Inventory Management System.")
            break
        else:
            print("Invalid choice. Please enter 1 to 9.")


if __name__ == "__main__":
    main()
