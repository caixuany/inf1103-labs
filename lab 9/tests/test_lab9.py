"""Lab 9 tests: Strategy, Factory, validation and exception handling.

Run from the lab 9 folder with:
    python -m unittest discover -s tests -v
"""

import inspect
import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

# make the project files importable when running from the tests folder
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from discount import (DiscountStrategy, NoDiscount, PercentageDiscount,  # noqa: E402
                      BulkDiscount, StudentDiscount)
from inventory import Inventory, load_products  # noqa: E402
from main import get_positive_float  # noqa: E402
from order import Order, OrderLine  # noqa: E402
from product import Product, PhysicalProduct, DigitalProduct  # noqa: E402
from product_factory import ProductFactory  # noqa: E402
from supplier import Supplier  # noqa: E402

PRODUCTS_CSV = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "products.csv"
)


def make_supplier() -> Supplier:
    return Supplier("S001", "Acme Supplies", "sales@acme.com")


def make_order_of_250() -> Order:
    # 2 x 100 + 1 x 50 = 250
    supplier = make_supplier()
    chair = ProductFactory.create("physical", "P001", "Chair", 100, 5,
                                  supplier, weight=3)
    software = ProductFactory.create("digital", "D001", "Software", 50, 10,
                                     supplier, download_size=200)
    order = Order("O001")
    order.add_order_line(chair, 2)
    order.add_order_line(software, 1)
    return order


class TestDiscountStrategy(unittest.TestCase):

    def test_default_is_no_discount(self):
        order = make_order_of_250()
        self.assertIsInstance(order.get_discount(), NoDiscount)
        self.assertAlmostEqual(order.calculate_total(), 250)

    def test_bulk_discount(self):
        order = Order("O002", BulkDiscount(200, 20))
        supplier = make_supplier()
        order.add_order_line(
            ProductFactory.create("physical", "P1", "Desk", 250, 1, supplier), 1)
        self.assertAlmostEqual(order.calculate_total(), 230)

    def test_bulk_discount_below_threshold(self):
        self.assertAlmostEqual(BulkDiscount(200, 20).apply(150), 150)

    def test_percentage_discount(self):
        self.assertAlmostEqual(PercentageDiscount(10).apply(250), 225)

    def test_set_discount_changes_existing_order(self):
        order = make_order_of_250()
        order.set_discount(BulkDiscount(200, 20))
        self.assertAlmostEqual(order.calculate_total(), 230)
        order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225)

    def test_student_discount_works_without_changing_order(self):
        order = make_order_of_250()
        order.set_discount(StudentDiscount())
        self.assertAlmostEqual(order.calculate_total(), 237.5)

    def test_brand_new_strategy_works_with_order(self):
        # a strategy defined only inside this test - Order was never edited
        class HalfPrice(DiscountStrategy):
            def apply(self, total: float) -> float:
                return total / 2

            def describe(self) -> str:
                return "Half price"

        order = make_order_of_250()
        order.set_discount(HalfPrice())
        self.assertAlmostEqual(order.calculate_total(), 125)

    def test_order_has_no_discount_if_elif(self):
        source = inspect.getsource(Order.calculate_total)
        self.assertNotIn("elif", source)
        self.assertNotIn("Percentage", source)
        self.assertNotIn("Bulk", source)

    def test_two_orders_can_share_one_strategy(self):
        shared = PercentageDiscount(10)
        order_1 = Order("O1", shared)
        order_2 = Order("O2", shared)
        self.assertIs(order_1.get_discount(), order_2.get_discount())

    def test_invalid_percentage_rejected(self):
        with self.assertRaises(ValueError):
            PercentageDiscount(150)

    def test_cannot_create_abstract_strategy(self):
        with self.assertRaises(TypeError):
            DiscountStrategy()


class TestProductFactory(unittest.TestCase):

    def test_creates_physical_product(self):
        product = ProductFactory.create("physical", "P1", "Lamp", 25, 10,
                                        make_supplier(), weight=2)
        self.assertIsInstance(product, PhysicalProduct)
        self.assertIsInstance(product, Product)

    def test_creates_digital_product(self):
        product = ProductFactory.create("digital", "D1", "Editor", 49.9, 100,
                                        make_supplier(), download_size=500)
        self.assertIsInstance(product, DigitalProduct)

    def test_unknown_type_raises_value_error(self):
        with self.assertRaises(ValueError) as context:
            ProductFactory.create("service", "S1", "Installation", 30, 5,
                                  make_supplier())
        self.assertEqual(str(context.exception),
                         "Unknown product type: service")

    def test_main_and_inventory_use_factory(self):
        # main.py and inventory.py should not build products directly
        import inventory
        import main
        for module in (main, inventory):
            source = inspect.getsource(module)
            self.assertNotIn("PhysicalProduct(", source)
            self.assertNotIn("DigitalProduct(", source)
            self.assertIn("ProductFactory.create(", source)


class TestValidation(unittest.TestCase):

    def test_zero_price_rejected(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P1", "Lamp", 0, 1,
                                  make_supplier())

    def test_negative_price_rejected(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("digital", "D1", "App", -5, 1,
                                  make_supplier())

    def test_negative_stock_rejected(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P1", "Lamp", 10, -1,
                                  make_supplier())

    def test_digital_product_keeps_stock_rule(self):
        # LSP: the child must not loosen the parent's rule
        product = ProductFactory.create("digital", "D1", "App", 10, 5,
                                        make_supplier())
        with self.assertRaises(ValueError):
            product.update_stock(-3)

    def test_zero_order_quantity_rejected(self):
        product = ProductFactory.create("physical", "P1", "Lamp", 10, 5,
                                        make_supplier())
        with self.assertRaises(ValueError):
            OrderLine(product, 0)
        with self.assertRaises(ValueError):
            Order("O1").add_order_line(product, -2)


class TestUserInput(unittest.TestCase):

    def test_get_positive_float_keeps_asking(self):
        output = io.StringIO()
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]):
            with redirect_stdout(output):
                value = get_positive_float("Enter price: ")

        self.assertEqual(value, 12.5)
        self.assertEqual(output.getvalue().splitlines(), [
            "Please enter a valid number, e.g. 12.50",
            "Please enter a number greater than zero.",
        ])


class TestLoadProducts(unittest.TestCase):

    def test_loads_good_rows_and_skips_bad_ones(self):
        inventory = Inventory()
        output = io.StringIO()
        with redirect_stdout(output):
            load_products(PRODUCTS_CSV, inventory, make_supplier())

        ids = [p.get_product_id() for p in inventory.get_products()]
        self.assertEqual(ids, ["P001", "D001", "P003"])

        text = output.getvalue()
        self.assertIn("Unknown product type: service", text)
        self.assertIn("could not convert string to float: 'abc'", text)
        self.assertIn("3 products loaded.", text)
        self.assertTrue(text.strip().endswith("Load attempt finished."))

    def test_missing_file_does_not_crash(self):
        inventory = Inventory()
        output = io.StringIO()
        with redirect_stdout(output):
            load_products("does_not_exist.csv", inventory, make_supplier())

        self.assertEqual(output.getvalue().splitlines(), [
            "Products file not found: does_not_exist.csv",
            "Load attempt finished.",
        ])
        self.assertEqual(inventory.get_products(), [])

    def test_negative_stock_row_is_skipped(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "bad.csv")
            with open(path, "w", encoding="utf-8") as file:
                file.write("product_type,product_id,name,price,stock_quantity\n")
                file.write("physical,P9,Broken,10.00,-4\n")
                file.write("digital,D9,Fine,5.00,1\n")

            inventory = Inventory()
            with redirect_stdout(io.StringIO()):
                load_products(path, inventory, make_supplier())

        ids = [p.get_product_id() for p in inventory.get_products()]
        self.assertEqual(ids, ["D9"])


if __name__ == "__main__":
    unittest.main()
