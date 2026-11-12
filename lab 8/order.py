
from product import Product


class OrderLine:
    """One product and the quantity requested within an Order.

    An OrderLine is part of an Order (COMPOSITION). It only refers to a
    Product (association) and does not own it.
    OrderLine objects should only be created by Order.add_order_line().
    """

    def __init__(self, product: Product, quantity: int):
        if quantity <= 0:
            raise ValueError("Quantity must be at least 1.")

        self.__product: Product = product
        self.__quantity: int = int(quantity)

    def get_product(self) -> Product:
        return self.__product

    def get_quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        return self.__product.get_price() * self.__quantity

    def display_information(self) -> None:
        print(
            f"{self.__product.get_name()} x {self.__quantity} "
            f"@ ${self.__product.get_price():.2f} = "
            f"${self.calculate_subtotal():.2f}"
        )


class Order:
    """A customer order made up of OrderLine objects (COMPOSITION).

    The Order creates and manages its own OrderLine objects. They are never
    passed in from outside, never handed to another Order, and disappear
    together with the Order.
    """

    def __init__(self, order_id: str):
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []

    def get_order_id(self) -> str:
        return self.__order_id

    def add_order_line(self, product: Product, quantity: int) -> None:
        # The Order creates the part itself, so the part's lifecycle is
        # tied to this Order.
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        for order_line in self.__order_lines:
            if order_line.get_product().get_product_id() == product_id:
                self.__order_lines.remove(order_line)
                return True

        return False

    def get_order_lines(self) -> tuple[OrderLine, ...]:
        # Return a read-only tuple so outside code cannot add or move lines
        return tuple(self.__order_lines)

    def calculate_total(self) -> float:
        return sum(
            order_line.calculate_subtotal()
            for order_line in self.__order_lines
        )

    def display_order(self) -> None:
        print(f"Order ID: {self.__order_id}")

        if not self.__order_lines:
            print("  (no order lines)")

        for order_line in self.__order_lines:
            print("  ", end="")
            order_line.display_information()

        print(f"Order Total: ${self.calculate_total():.2f}")
