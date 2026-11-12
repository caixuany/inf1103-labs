
from abc import ABC, abstractmethod

from supplier import Supplier


# Abstract parent class
class Product(ABC):
    """Common abstraction for every product type.

    Expectations every subclass must preserve (Liskov Substitution):
    - update_stock(quantity) accepts any quantity >= 0 and sets the stock
      to that value; it only rejects negative quantities.
    - get_fulfilment_info() always returns a str describing delivery.
    - display_information() prints the product's details and returns None.
    """

    def __init__(self, product_id: str, name: str, price: float,
                 stock_quantity: int, supplier: Supplier):
        if price < 0 or stock_quantity < 0:
            raise ValueError("Price and stock cannot be negative.")

        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = float(price)
        self.__stock_quantity: int = int(stock_quantity)
        # Association: the Product refers to its Supplier but does not own it
        self.__supplier: Supplier = supplier

    def update_stock(self, quantity: int) -> None:
        if quantity < 0:
            raise ValueError("Stock cannot be negative.")

        self.__stock_quantity = int(quantity)

    def display_information(self) -> None:
        print(f"Product ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock_quantity}")
        print(f"Supplier: {self.__supplier.get_name()}")

    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock_quantity

    def get_supplier(self) -> Supplier:
        return self.__supplier

    def to_dict(self) -> dict:
        return {
            "product_id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock_quantity": self.__stock_quantity,
            "supplier": self.__supplier.to_dict()
        }

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass


# Interface-style abstract class
class CanBeShipped(ABC):

    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        pass


# Physical product inherits Product and CanBeShipped
class PhysicalProduct(Product, CanBeShipped):

    def __init__(self, product_id: str, name: str, price: float,
                 stock_quantity: int, supplier: Supplier, weight: float):
        super().__init__(product_id, name, price, stock_quantity, supplier)

        if weight < 0:
            raise ValueError("Weight cannot be negative.")

        self.__weight: float = float(weight)

    def display_information(self) -> None:
        super().display_information()
        print(f"Weight: {self.__weight} kg")

    def get_fulfilment_info(self) -> str:
        shipping_cost = self.calculate_shipping_cost()
        return (
            "This product requires physical shipping "
            f"(shipping cost: ${shipping_cost:.2f})."
        )

    def calculate_shipping_cost(self) -> float:
        return self.__weight * 2

    def get_weight(self) -> float:
        return self.__weight

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data


# Digital product inherits Product
class DigitalProduct(Product):

    def __init__(self, product_id: str, name: str, price: float,
                 stock_quantity: int, supplier: Supplier,
                 download_size: float):
        super().__init__(product_id, name, price, stock_quantity, supplier)

        if download_size < 0:
            raise ValueError("Download size cannot be negative.")

        self.__download_size: float = float(download_size)

    def display_information(self) -> None:
        super().display_information()
        print(f"Download Size: {self.__download_size} MB")

    def get_fulfilment_info(self) -> str:
        return "This product is delivered digitally."

    def get_download_size(self) -> float:
        return self.__download_size

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data
