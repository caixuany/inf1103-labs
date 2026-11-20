
import csv
import json
from typing import Any

from product import Product
from product_factory import ProductFactory
from supplier import Supplier

# One product record read from the JSON file. Its values are only known
# after loading (str, float, int or a nested dict), so Any is used here
# for raw, not-yet-validated file data.
ProductData = dict[str, Any]


class Inventory:
    """A collection of Product objects (AGGREGATION).

    The Inventory holds references to products that were created elsewhere.
    Removing a product only removes the reference; the Product itself keeps
    existing and can be added to another Inventory.

    The collection is typed with the base class Product, so any current or
    future subclass can be stored without changing this class (LSP).
    """

    def __init__(self) -> None:
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> None:
        if self.find_product(product.get_product_id()) is not None:
            raise ValueError("A product with this ID already exists.")

        self.__products.append(product)

    def remove_product(self, product_id: str) -> Product | None:
        """Remove the reference and hand the still-existing Product back."""
        product = self.find_product(product_id)

        if product is not None:
            self.__products.remove(product)

        return product

    def find_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product

        return None

    def transfer_product(self, product_id: str,
                         destination: "Inventory") -> bool:
        product = self.remove_product(product_id)

        if product is None:
            return False

        destination.add_product(product)
        return True

    def display_all_products(self) -> None:
        if not self.__products:
            print("Inventory is empty.")
            return

        # Polymorphism: each object runs its own implementation.
        # No isinstance() checks are needed.
        for product in self.__products:
            product.display_information()
            print(product.get_fulfilment_info())
            print("-" * 30)

    def get_products(self) -> list[Product]:
        return list(self.__products)

    def save_inventory(self, filename: str = "inventory.json") -> None:
        data = [product.to_dict() for product in self.__products]

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        print("Inventory saved successfully.")

    def load_inventory(self, filename: str = "inventory.json") -> None:
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, list):
                raise ValueError("Inventory JSON must contain a list.")

            loaded_products: list[Product] = []
            # Products with the same supplier ID share one Supplier object
            suppliers: dict[str, Supplier] = {}

            for item in data:
                supplier = self.__build_supplier(item, suppliers)
                product = self.__build_product(item, supplier)

                if product is None:
                    continue

                if any(existing.get_product_id() == product.get_product_id()
                       for existing in loaded_products):
                    raise ValueError(
                        f"Duplicate product ID: {product.get_product_id()}"
                    )

                loaded_products.append(product)

            self.__products = loaded_products
            print("Inventory loaded successfully.")

        except FileNotFoundError:
            print("No saved inventory found. Starting with empty inventory.")

        except (json.JSONDecodeError, KeyError, TypeError,
                ValueError) as error:
            print(f"Could not load inventory: {error}")

    @staticmethod
    def __build_supplier(item: ProductData,
                         suppliers: dict[str, Supplier]) -> Supplier:
        # Older save files have no supplier, so fall back to a placeholder
        supplier_data = item.get("supplier", {
            "supplier_id": "S000",
            "name": "Unknown Supplier",
            "contact_email": "unknown@example.com"
        })
        supplier_id = supplier_data["supplier_id"]

        if supplier_id not in suppliers:
            suppliers[supplier_id] = Supplier(
                supplier_id,
                supplier_data["name"],
                supplier_data["contact_email"]
            )

        return suppliers[supplier_id]

    @staticmethod
    def __build_product(item: ProductData, supplier: Supplier) -> Product | None:
        # Support both the original and updated JSON stock keys
        stock = item.get("stock_quantity", item.get("stock"))

        if stock is None:
            raise ValueError("Missing stock information.")

        # The factory decides which class to build, Inventory doesn't need
        # to know about PhysicalProduct or DigitalProduct any more
        try:
            return ProductFactory.create(
                item["type"], item["product_id"], item["name"],
                item["price"], stock, supplier,
                weight=item.get("weight", 0.0),
                download_size=item.get("download_size", 0.0)
            )
        except ValueError as error:
            print(f"{error}. Skipping product {item.get('product_id')}.")
            return None


def load_products(path: str, inventory: Inventory,
                  supplier: Supplier) -> None:
    """Load products from a CSV file into the inventory.

    Bad rows are reported and skipped so the good rows still load.
    """
    try:
        file = open(path, newline="", encoding="utf-8")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        loaded = 0

        with file:
            reader = csv.reader(file)
            next(reader, None)  # skip the header row

            # start=2 because line 1 of the file is the header
            for line_number, row in enumerate(reader, start=2):
                if not row:
                    continue

                try:
                    if len(row) != 5:
                        raise ValueError("expected 5 values")

                    product_type, product_id, name, price, stock = row
                    product = ProductFactory.create(
                        product_type, product_id, name,
                        float(price), int(stock), supplier
                    )
                    inventory.add_product(product)
                    loaded += 1
                except ValueError as error:
                    print(f"Skipping row {line_number} {row}: {error}")

        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")
