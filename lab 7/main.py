
from inventory import Inventory
from product import PhysicalProduct, DigitalProduct


def main():
    inventory = Inventory()

    inventory.load_inventory()

    while True:
        print("\n===== INVENTORY MANAGEMENT SYSTEM =====")
        print("1. Display all products")
        print("2. Add a product")
        print("3. Update stock")
        print("4. Search for a product")
        print("5. Save inventory")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            inventory.display_all_products()

        elif choice == "2":
            print("\n1. Physical Product")
            print("2. Digital Product")

            product_type = input("Choose product type: ")

            product_id = input("Enter product ID: ")
            name = input("Enter product name: ")
            price = float(input("Enter product price: "))
            stock = int(input("Enter stock quantity: "))

            if product_type == "1":
                weight = float(input("Enter weight in kg: "))

                product = PhysicalProduct(
                    product_id, name, price, stock, weight
                )

            elif product_type == "2":
                download_size = float(
                    input("Enter download size in MB: ")
                )

                product = DigitalProduct(
                    product_id, name, price, stock, download_size
                )

            else:
                print("Invalid product type.")
                continue

            inventory.add_product(product)

        elif choice == "3":
            product_id = input("Enter product ID: ")
            quantity = int(input("Enter quantity to add/remove: "))

            inventory.update_stock(product_id, quantity)

        elif choice == "4":
            product_id = input("Enter product ID: ")
            inventory.search_product(product_id)

        elif choice == "5":
            inventory.save_inventory()

        elif choice == "6":
            inventory.save_inventory()
            print("Thank you for using the system!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
