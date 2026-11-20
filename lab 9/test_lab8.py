
"""Lab 8 tests: association, aggregation, composition, LSP and
polymorphism. Run with:  python test_lab8.py
"""

from inventory import Inventory
from order import Order
from product import Product, PhysicalProduct, DigitalProduct
from supplier import Supplier


def heading(title: str) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def test_association() -> None:
    heading("SECTION 2: ASSOCIATION (Supplier <-> Product)")

    supplier = Supplier("S001", "Acme Supplies", "sales@acme.com")
    guitar = PhysicalProduct("P001", "Guitar", 250.0, 2, supplier, 5.0)
    ebook = DigitalProduct("D001", "Guitar E-Book", 15.0, 100, supplier, 12.5)

    # Separate objects: products and supplier each have their own identity
    assert id(guitar) != id(supplier) and id(ebook) != id(supplier)
    # Both products refer to the SAME Supplier object
    assert guitar.get_supplier() is ebook.get_supplier() is supplier
    print(f"id(supplier)            = {id(supplier)}")
    print(f"id(guitar.supplier)     = {id(guitar.get_supplier())}")
    print(f"id(ebook.supplier)      = {id(ebook.get_supplier())}")

    # Predict first: what happens after `del supplier`?
    del supplier
    print("\nAfter `del supplier`, supplier info via each product:")
    print("--- Guitar's supplier ---")
    guitar.get_supplier().display_information()
    print("--- E-Book's supplier ---")
    ebook.get_supplier().display_information()
    print("\n`del` only removed the variable name; the Supplier object is "
          "still referenced by the products.")

    # A Supplier can also exist without any Product
    lonely = Supplier("S002", "No Products Ltd", "hello@noproducts.com")
    lonely.display_information()
    print("PASS: association")


def test_aggregation() -> None:
    heading("SECTION 3: AGGREGATION (Inventory <>-- Product)")

    supplier = Supplier("S001", "Acme Supplies", "sales@acme.com")
    # Product is created BEFORE any Inventory exists
    keyboard = PhysicalProduct("P002", "Keyboard", 80.0, 10, supplier, 1.2)

    inventory_a = Inventory()
    inventory_b = Inventory()

    inventory_a.add_product(keyboard)
    assert inventory_a.find_product("P002") is keyboard
    print("Added Keyboard to Inventory A.")

    # Predict first: does the Product still work after removal?
    removed = inventory_a.remove_product("P002")
    assert removed is keyboard
    assert inventory_a.find_product("P002") is None
    print("Removed Keyboard from Inventory A. It still works:")
    keyboard.display_information()
    keyboard.update_stock(7)
    assert keyboard.get_stock() == 7

    inventory_b.add_product(keyboard)
    assert inventory_b.find_product("P002") is keyboard
    print("\nSame object added to Inventory B "
          f"(same id: {id(inventory_b.find_product('P002')) == id(keyboard)})")

    # Transfer back and empty the inventory
    inventory_b.transfer_product("P002", inventory_a)
    assert inventory_a.find_product("P002") is keyboard
    inventory_a.remove_product("P002")
    print("Inventory A after emptying:")
    inventory_a.display_all_products()
    print(f"Keyboard still exists: {keyboard.get_name()}, "
          f"stock {keyboard.get_stock()}")
    print("PASS: aggregation")


def test_composition() -> None:
    heading("SECTION 4: COMPOSITION (Order <*>-- OrderLine)")

    supplier = Supplier("S001", "Acme Supplies", "sales@acme.com")
    guitar = PhysicalProduct("P001", "Guitar", 250.0, 2, supplier, 5.0)
    ebook = DigitalProduct("D001", "Guitar E-Book", 15.0, 100, supplier, 12.5)

    order_1 = Order("O001")
    order_1.add_order_line(guitar, 1)
    order_1.add_order_line(ebook, 2)
    order_1.display_order()
    assert order_1.calculate_total() == 250.0 + 2 * 15.0

    # Predict first: same Product in two Orders
    order_2 = Order("O002")
    order_2.add_order_line(guitar, 3)
    order_2.display_order()

    line_1 = order_1.get_order_lines()[0]
    line_2 = order_2.get_order_lines()[0]
    print(f"\nOrderLine in O001 id = {id(line_1)}")
    print(f"OrderLine in O002 id = {id(line_2)}")
    print(f"Same OrderLine object?  {line_1 is line_2}")
    print(f"Same Product object?    "
          f"{line_1.get_product() is line_2.get_product()}")
    assert line_1 is not line_2
    assert line_1.get_product() is line_2.get_product() is guitar

    # Remove a line through the Order
    assert order_1.remove_order_line("D001")
    print("\nAfter removing the E-Book line from O001:")
    order_1.display_order()
    assert order_1.calculate_total() == 250.0

    # Removing the Order removes its lines; the Product survives
    del order_1
    print(f"Order O001 deleted; Guitar still exists: {guitar.get_name()}")
    print("PASS: composition")


def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


def test_lsp() -> None:
    heading("SECTION 6: LISKOV SUBSTITUTION")

    supplier = Supplier("S001", "Acme Supplies", "sales@acme.com")
    products: list[Product] = [
        PhysicalProduct("P001", "Guitar", 250.0, 2, supplier, 5.0),
        DigitalProduct("D001", "Guitar E-Book", 15.0, 100, supplier, 12.5),
    ]

    inventory = Inventory()

    for product in products:
        show_product_details(product)
        print("-" * 30)
        inventory.add_product(product)

        # Expectation set by Product.update_stock(): any quantity >= 0
        # is accepted and becomes the new stock. Both subclasses keep it.
        product.update_stock(0)
        assert product.get_stock() == 0
        product.update_stock(42)
        assert product.get_stock() == 42

        # ...and both reject negative stock in the same way
        try:
            product.update_stock(-1)
            raise AssertionError("negative stock was accepted")
        except ValueError:
            pass

        # get_fulfilment_info() always returns a str
        assert isinstance(product.get_fulfilment_info(), str)

    assert inventory.find_product("D001") is products[1]
    print("Both product types passed the same Product checks.")
    print("PASS: LSP")


def test_polymorphism() -> None:
    heading("SECTION 7: POLYMORPHISM")

    supplier = Supplier("S001", "Acme Supplies", "sales@acme.com")
    inventory = Inventory()
    inventory.add_product(
        PhysicalProduct("P001", "Guitar", 250.0, 2, supplier, 5.0))
    inventory.add_product(
        DigitalProduct("D001", "Guitar E-Book", 15.0, 100, supplier, 12.5))

    # One loop over Product references, no isinstance() checks.
    # The SAME method calls run different code depending on the object.
    products: list[Product] = inventory.get_products()
    print("Collection type: list[Product]  (one loop, no isinstance)\n")

    for product in products:
        print(f"Reference type: Product -> actual object: "
              f"{type(product).__name__}")
        product.display_information()
        print(f"get_fulfilment_info(): {product.get_fulfilment_info()}")
        print("-" * 30)

    # The same function also works for both, without being changed
    print("show_product_details(product: Product) with each object:")
    for product in products:
        show_product_details(product)
        print("-" * 30)

    fulfilment = [p.get_fulfilment_info() for p in products]
    assert "physical shipping" in fulfilment[0]
    assert "$10.00" in fulfilment[0]
    assert "delivered digitally" in fulfilment[1]
    assert fulfilment[0] != fulfilment[1]
    print("Same call, different specialised results -> PASS: polymorphism")


if __name__ == "__main__":
    test_association()
    test_aggregation()
    test_composition()
    test_lsp()
    test_polymorphism()
    heading("ALL TESTS PASSED")
