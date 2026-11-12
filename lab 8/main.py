
from inventory import Inventory
from order import Order
from product import Product, PhysicalProduct, DigitalProduct
from supplier import Supplier


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
    try:
        print("\n===== ADD PRODUCT =====")
        print("1. Physical Product")
        print("2. Digital Product")

        product_type = input("Choose product type: ").strip()

        if product_type not in ("1", "2"):
            print("Invalid product type.")
            return

        product_id = input("Enter product ID: ").strip()
        name = input("Enter product name: ").strip()

        if not product_id or not name:
            print("Product ID and name cannot be empty.")
            return

        price = float(input("Enter product price: "))
        stock = int(input("Enter stock quantity: "))

        supplier = get_supplier(inventory)

        if supplier is None:
            return

        product: Product

        if product_type == "1":
            weight = float(input("Enter weight in kg: "))
            product = PhysicalProduct(
                product_id, name, price, stock, supplier, weight
            )
        else:
            download_size = float(input("Enter download size in MB: "))
            product = DigitalProduct(
                product_id, name, price, stock, supplier, download_size
            )

        inventory.add_product(product)
        print("Product added successfully.")

    except ValueError as error:
        print(f"Invalid input: {error}")


def update_product_stock(inventory: Inventory) -> None:
    product_id = input("Enter product ID: ").strip()
    product = inventory.find_product(product_id)

    if product is None:
        print("Product not found.")
        return

    try:
        quantity = int(input("Enter new stock quantity: "))
        product.update_stock(quantity)
        print("Stock updated successfully.")

    except ValueError as error:
        print(f"Invalid input: {error}")


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

    print()
    order.display_order()


def display_menu() -> None:
    print("\n===== INVENTORY MANAGEMENT SYSTEM =====")
    print("1. Display all products")
    print("2. Add a product")
    print("3. Update product stock")
    print("4. Search for a product")
    print("5. Remove a product")
    print("6. Create an order")
    print("7. Save inventory")
    print("8. Exit")


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
            save_inventory(inventory)
        elif choice == "8":
            save_inventory(inventory)
            print("Exiting Inventory Management System.")
            break
        else:
            print("Invalid choice. Please enter 1 to 8.")


if __name__ == "__main__":
    main()
