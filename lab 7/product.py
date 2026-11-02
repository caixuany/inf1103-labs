
from abc import ABC, abstractmethod


# Parent abstract class
class Product(ABC):

    def __init__(self, product_id, name, price, stock_quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock_quantity = stock_quantity

    def update_stock(self, quantity):
        self.stock_quantity += quantity

    def display_information(self):
        print(f"Product ID: {self.product_id}")
        print(f"Name: {self.name}")
        print(f"Price: ${self.price:.2f}")
        print(f"Stock Quantity: {self.stock_quantity}")

    @abstractmethod
    def get_fulfilment_info(self):
        pass


# Interface-style abstract class
class CanBeShipped(ABC):

    @abstractmethod
    def calculate_shipping_cost(self):
        pass


# Physical product child class
class PhysicalProduct(Product, CanBeShipped):

    def __init__(self, product_id, name, price, stock_quantity, weight):
        super().__init__(product_id, name, price, stock_quantity)
        self.weight = weight

    def display_information(self):
        super().display_information()
        print(f"Weight: {self.weight} kg")

    def get_fulfilment_info(self):
        return "This product requires physical shipping."

    def calculate_shipping_cost(self):
        return self.weight * 2


# Digital product child class
class DigitalProduct(Product):

    def __init__(self, product_id, name, price, stock_quantity, download_size):
        super().__init__(product_id, name, price, stock_quantity)
        self.download_size = download_size

    def display_information(self):
        super().display_information()
        print(f"Download Size: {self.download_size} MB")

    def get_fulfilment_info(self):
        return "This product is delivered digitally."
