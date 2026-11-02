
import json
from product import PhysicalProduct, DigitalProduct


class Inventory:

    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)
        print("Product added successfully!")

    def display_all_products(self):
        if not self.products:
            print("No products found.")
            return

        for product in self.products:
            print("\n--------------------")
            product.display_information()
            print(product.get_fulfilment_info())

            if isinstance(product, PhysicalProduct):
                print(
                    "Shipping Cost: $",
                    product.calculate_shipping_cost()
                )

    def search_product(self, product_id):
        for product in self.products:
            if product.product_id == product_id:
                product.display_information()
                return product

        print("Product not found.")
        return None

    def update_stock(self, product_id, quantity):
        product = self.search_product(product_id)

        if product:
            if product.stock_quantity + quantity < 0:
                print("Insufficient stock.")
                return

            product.update_stock(quantity)
            print("Stock updated successfully!")

    def save_inventory(self, filename="inventory.json"):
        data = []

        for product in self.products:
            if isinstance(product, PhysicalProduct):
                item = {
                    "type": "physical",
                    "product_id": product.product_id,
                    "name": product.name,
                    "price": product.price,
                    "stock_quantity": product.stock_quantity,
                    "weight": product.weight
                }

            elif isinstance(product, DigitalProduct):
                item = {
                    "type": "digital",
                    "product_id": product.product_id,
                    "name": product.name,
                    "price": product.price,
                    "stock_quantity": product.stock_quantity,
                    "download_size": product.download_size
                }

            data.append(item)

        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

        print("Inventory saved successfully!")

    def load_inventory(self, filename="inventory.json"):
        try:
            with open(filename, "r") as file:
                data = json.load(file)

            self.products = []

            for item in data:
                if item["type"] == "physical":
                    product = PhysicalProduct(
                        item["product_id"],
                        item["name"],
                        item["price"],
                        item["stock_quantity"],
                        item["weight"]
                    )

                elif item["type"] == "digital":
                    product = DigitalProduct(
                        item["product_id"],
                        item["name"],
                        item["price"],
                        item["stock_quantity"],
                        item["download_size"]
                    )

                else:
                    print("Unknown product type. Skipping.")
                    continue

                self.products.append(product)

            print("Inventory loaded successfully!")

        except FileNotFoundError:
            print("No saved inventory found.")

        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
            print("Unable to load inventory:", error)
