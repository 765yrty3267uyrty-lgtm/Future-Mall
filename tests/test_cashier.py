import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'python_modules'))

from cashier_program import CashierSystem, Product, CartItem, Receipt


class TestCashierSystem:
    def setup_method(self):
        self.system = CashierSystem()

    def test_products_loaded(self):
        assert len(self.system.products) == 10
        product_names = [p.name for p in self.system.products]
        assert "Milk" in product_names
        assert "Bread" in product_names

    def test_add_to_cart(self):
        self.system.add_to_cart_manual(0, 2)  # Milk x2
        assert len(self.system.cart) == 1
        assert self.system.cart[0].quantity == 2
        assert self.system.cart[0].product.name == "Milk"

    def test_add_duplicate_product_increments_quantity(self):
        self.system.add_to_cart_manual(0, 1)
        self.system.add_to_cart_manual(0, 2)
        assert len(self.system.cart) == 1
        assert self.system.cart[0].quantity == 3

    def test_calculate_subtotal(self):
        self.system.cart = [CartItem(Product("Milk", 25.00), 2)]
        assert self.system.calculate_subtotal() == 50.00

    def test_calculate_discount_threshold(self):
        # No discount at or under 500 EGP
        discount, pct = self.system.calculate_discount(150)
        assert discount == 0.0
        assert pct == "0%"
        discount, pct = self.system.calculate_discount(500)
        assert discount == 0.0
        assert pct == "0%"

        # 10% discount over 500 EGP
        discount, pct = self.system.calculate_discount(600)
        assert discount == 60.0
        assert pct == "10%"

    def test_calculate_tax(self):
        assert self.system.calculate_tax(100) == 10.00
        assert self.system.calculate_tax(50.50) == 5.05

    def test_receipt_generation(self):
        self.system.cart = [CartItem(Product("Milk", 25.00), 2)]
        receipt = self.system.checkout(confirm=False)
        assert receipt is not None
        assert receipt.subtotal == 50.00
        assert "GRAND TOTAL" in str(receipt)
        assert receipt.receipt_number.startswith("FM-")

    def test_cart_operations(self):
        self.system.add_to_cart_manual(0, 1)  # Milk
        self.system.add_to_cart_manual(1, 2)  # Bread
        assert len(self.system.cart) == 2

        self.system.remove_from_cart_by_index(0)
        assert len(self.system.cart) == 1
        assert self.system.cart[0].product.name == "Bread"

        self.system.clear_cart(confirm=False)
        assert len(self.system.cart) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])