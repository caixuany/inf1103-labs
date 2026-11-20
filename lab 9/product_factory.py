
from product import Product, PhysicalProduct, DigitalProduct
from supplier import Supplier


class ProductFactory:
    """The only place in the program that decides which Product class
    to create. Everything else just asks the factory and gets a Product.

    Adding a new product type (e.g. BundleProduct) means changing this
    class, so the factory itself is not fully closed for modification.
    I'm ok with that here since it's a small app and the change is in one
    place instead of being spread around main.py and inventory.py.
    """

    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock_quantity: int, supplier: Supplier,
               weight: float = 0.0, download_size: float = 0.0) -> Product:
        product_type = product_type.strip().lower()

        if product_type == "physical":
            return PhysicalProduct(product_id, name, price, stock_quantity,
                                   supplier, weight)
        elif product_type == "digital":
            return DigitalProduct(product_id, name, price, stock_quantity,
                                  supplier, download_size)
        else:
            raise ValueError(f"Unknown product type: {product_type}")
