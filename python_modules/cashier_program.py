#!/usr/bin/env python3
"""
Future Mall - Cashier Program
A console-based shop simulation with cart management, discounts, and receipt generation.
"""

import sys
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field

# Add shared constants to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'shared'))
from constants import CASHIER, BRAND, format_currency, print_header, print_section


def format_egp(amount: float) -> str:
    """Format an amount as Egyptian Pounds."""
    return f"{amount:,.2f} EGP"


@dataclass
class Product:
    """Represents a product in the catalog."""
    name: str
    price: float

    def __str__(self) -> str:
        return f"{self.name}: {format_egp(self.price)}"


@dataclass
class CartItem:
    """Represents an item in the shopping cart."""
    product: Product
    quantity: int = 1

    @property
    def line_total(self) -> float:
        return self.product.price * self.quantity

    def __str__(self) -> str:
        return f"{self.product.name} x{self.quantity} = {format_egp(self.line_total)}"


@dataclass
class Receipt:
    """Represents a complete purchase receipt."""
    store_name: str
    receipt_number: str
    date: datetime
    items: List[CartItem]
    subtotal: float
    discount: float
    tax: float
    grand_total: float

    def __str__(self) -> str:
        lines = []
        lines.append("=" * 50)
        lines.append(f"{self.store_name.center(50)}")
        lines.append(f"Receipt #{self.receipt_number}".center(50))
        lines.append(f"{self.date.strftime('%Y-%m-%d %H:%M:%S')}".center(50))
        lines.append("=" * 50)
        lines.append(f"{'Item':<20} {'Qty':>4} {'Price':>10} {'Total':>12}")
        lines.append("-" * 50)

        for item in self.items:
            lines.append(f"{item.product.name:<20} {item.quantity:>4} "
                         f"{format_egp(item.product.price):>10} "
                         f"{format_egp(item.line_total):>12}")

        lines.append("-" * 50)
        lines.append(f"{'Subtotal:':<36} {format_egp(self.subtotal):>12}")
        lines.append(f"{'Discount:':<36} -{format_egp(self.discount):>11}")
        lines.append(f"{'Tax (10%):':<36} {format_egp(self.tax):>12}")
        lines.append("=" * 50)
        lines.append(f"{'GRAND TOTAL:':<36} {format_egp(self.grand_total):>12}")
        lines.append("=" * 50)
        lines.append("")
        lines.append("Thank you for shopping at Future Mall!")
        lines.append("Shopping for Tomorrow")
        lines.append("=" * 50)

        return "\n".join(lines)


class CashierSystem:
    """Main cashier system managing products, cart, and transactions."""

    def __init__(self):
        self.products: List[Product] = [
            Product(p["name"], p["price"]) for p in CASHIER["products"]
        ]
        self.cart: List[CartItem] = []
        self.receipt_counter = 0
        self.transaction_history: List[Receipt] = []

    def display_products(self) -> None:
        """Display all available products."""
        print_section("Available Products")
        print(f"{'#':<4} {'Product':<20} {'Price':>10}")
        print("-" * 36)
        for i, product in enumerate(self.products, 1):
            print(f"{i:<4} {product.name:<20} {format_egp(product.price):>10}")
        print("-" * 36)

    def display_cart(self) -> None:
        """Display current cart contents."""
        if not self.cart:
            print("\nYour cart is empty.")
            return

        print_section("Shopping Cart")
        print(f"{'#':<4} {'Product':<20} {'Qty':>4} {'Price':>10} {'Total':>12}")
        print("-" * 54)
        for i, item in enumerate(self.cart, 1):
            print(f"{i:<4} {item.product.name:<20} {item.quantity:>4} "
                  f"{format_egp(item.product.price):>10} "
                  f"{format_egp(item.line_total):>12}")
        print("-" * 54)
        subtotal = self.calculate_subtotal()
        print(f"{'Subtotal:':<38} {format_egp(subtotal):>12}")

    def calculate_subtotal(self) -> float:
        """Calculate cart subtotal."""
        return sum(item.line_total for item in self.cart)

    def calculate_discount(self, subtotal: float) -> Tuple[float, str]:
        """Calculate applicable discount: 10% when subtotal exceeds 500 EGP."""
        if subtotal > CASHIER["discount_threshold"]:
            rate = CASHIER["discount_rate"]
            return round(subtotal * rate, 2), f"{int(rate * 100)}%"
        return 0.0, "0%"

    def calculate_tax(self, amount: float) -> float:
        """Calculate tax on amount."""
        return round(amount * CASHIER["tax_rate"], 2)

    def get_user_choice(self, max_choice: int, prompt: str = "Enter your choice: ") -> Optional[int]:
        """Get and validate user menu choice."""
        while True:
            try:
                choice = input(prompt).strip()
                if choice.lower() in ('q', 'quit', 'exit'):
                    return None
                value = int(choice)
                if 1 <= value <= max_choice:
                    return value
                print(f"Please enter a number between 1 and {max_choice}.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def get_quantity(self, prompt: str = "Enter quantity: ") -> Optional[int]:
        """Get and validate quantity input."""
        while True:
            try:
                qty = input(prompt).strip()
                if qty.lower() in ('q', 'quit', 'cancel'):
                    return None
                value = int(qty)
                if value > 0:
                    return value
                print("Quantity must be positive.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def add_to_cart(self) -> None:
        """Add a product to the cart."""
        self.display_products()
        choice = self.get_user_choice(len(self.products), "Select product number (or 'q' to cancel): ")
        if choice is None:
            return

        product = self.products[choice - 1]
        qty = self.get_quantity(f"Enter quantity for {product.name}: ")
        if qty is None:
            return

        # Check if product already in cart
        for item in self.cart:
            if item.product.name == product.name:
                item.quantity += qty
                print(f"\nUpdated {product.name} quantity to {item.quantity}.")
                return

        self.cart.append(CartItem(product, qty))
        print(f"\nAdded {product.name} x{qty} to cart.")

    def add_to_cart_manual(self, product_index: int, qty: int) -> None:
        """Add a product to cart programmatically (for testing)."""
        if 0 <= product_index < len(self.products):
            product = self.products[product_index]
            for item in self.cart:
                if item.product.name == product.name:
                    item.quantity += qty
                    return
            self.cart.append(CartItem(product, qty))

    def remove_from_cart_by_index(self, index: int) -> None:
        """Remove item from cart by index (for testing)."""
        if 0 <= index < len(self.cart):
            self.cart.pop(index)

    def remove_from_cart(self) -> None:
        """Remove an item from the cart."""
        if not self.cart:
            print("\nCart is empty.")
            return

        self.display_cart()
        choice = self.get_user_choice(len(self.cart), "Select item number to remove (or 'q' to cancel): ")
        if choice is None:
            return

        removed = self.cart.pop(choice - 1)
        print(f"\nRemoved {removed.product.name} from cart.")

    def update_quantity(self) -> None:
        """Update quantity of an item in cart."""
        if not self.cart:
            print("\nCart is empty.")
            return

        self.display_cart()
        choice = self.get_user_choice(len(self.cart), "Select item number to update (or 'q' to cancel): ")
        if choice is None:
            return

        item = self.cart[choice - 1]
        new_qty = self.get_quantity(f"Enter new quantity for {item.product.name} (current: {item.quantity}): ")
        if new_qty is None:
            return

        if new_qty == 0:
            self.cart.pop(choice - 1)
            print(f"\nRemoved {item.product.name} from cart.")
        else:
            item.quantity = new_qty
            print(f"\nUpdated {item.product.name} quantity to {new_qty}.")

    def clear_cart(self, confirm: bool = True) -> None:
        """Clear all items from cart."""
        if not self.cart:
            print("\nCart is already empty.")
            return

        if confirm:
            response = input("Are you sure you want to clear the cart? (y/N): ").strip().lower()
        else:
            response = 'y'
        if response == 'y':
            self.cart.clear()
            print("\nCart cleared.")

    def cancel_purchase(self, confirm: bool = True) -> None:
        """Cancel current purchase and clear cart."""
        if not self.cart:
            print("\nNo active purchase to cancel.")
            return

        if confirm:
            response = input("Cancel current purchase? (y/N): ").strip().lower()
        else:
            response = 'y'
        if response == 'y':
            self.cart.clear()
            print("\nPurchase cancelled. Cart cleared.")

    def checkout(self, confirm: bool = True) -> Optional[Receipt]:
        """Process checkout and generate receipt."""
        if not self.cart:
            print("\nCart is empty. Add items before checkout.")
            return None

        self.display_cart()
        subtotal = self.calculate_subtotal()
        discount_amount, discount_pct = self.calculate_discount(subtotal)
        taxable = subtotal - discount_amount
        tax = self.calculate_tax(taxable)
        grand_total = round(taxable + tax, 2)

        print(f"\n{'Subtotal:':<38} {format_egp(subtotal):>12}")
        print(f"{'Discount (' + discount_pct + '):':<38} -{format_egp(discount_amount):>11}")
        print(f"{'Tax (10%):':<38} {format_egp(tax):>12}")
        print("=" * 54)
        print(f"{'GRAND TOTAL:':<38} {format_egp(grand_total):>12}")

        if confirm:
            response = input("\nConfirm purchase? (y/N): ").strip().lower()
        else:
            response = 'y'
        if response != 'y':
            print("\nPurchase cancelled.")
            return None

        # Generate receipt
        self.receipt_counter += 1
        receipt = Receipt(
            store_name=CASHIER["store_name"],
            receipt_number=f"FM-{datetime.now().strftime('%Y%m%d')}-{self.receipt_counter:04d}",
            date=datetime.now(),
            items=self.cart.copy(),
            subtotal=subtotal,
            discount=discount_amount,
            tax=tax,
            grand_total=grand_total
        )

        # Save to history
        self.transaction_history.append(receipt)

        # Clear cart
        self.cart.clear()

        return receipt

    def save_receipt_to_file(self, receipt: Receipt) -> str:
        """Save receipt to a text file."""
        filename = f"receipt_{receipt.receipt_number}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(str(receipt))
        return filename

    def view_history(self) -> None:
        """Display transaction history."""
        if not self.transaction_history:
            print("\nNo transactions yet.")
            return

        print_section("Transaction History")
        for receipt in self.transaction_history:
            print(f"\nReceipt: {receipt.receipt_number}")
            print(f"Date: {receipt.date.strftime('%Y-%m-%d %H:%M')}")
            print(f"Items: {len(receipt.items)} | Total: {format_egp(receipt.grand_total)}")
            print("-" * 40)

    def display_main_menu(self) -> None:
        """Display the main menu options."""
        print_header("FUTURE MALL - CASHIER SYSTEM")
        print(f"\n{'1.':<4} View Products")
        print(f"{'2.':<4} Add to Cart")
        print(f"{'3.':<4} View Cart")
        print(f"{'4.':<4} Update Quantity")
        print(f"{'5.':<4} Remove Item")
        print(f"{'6.':<4} Clear Cart")
        print(f"{'7.':<4} Checkout")
        print(f"{'8.':<4} Cancel Purchase")
        print(f"{'9.':<4} View History")
        print(f"{'0.':<4} Exit")
        print("-" * 30)

    def run(self) -> None:
        """Main application loop."""
        print_header("WELCOME TO FUTURE MALL CASHIER")
        print(f"\n{CASHIER['store_name']} - {BRAND['slogan']}")

        while True:
            self.display_main_menu()
            choice = self.get_user_choice(9, "Enter your choice (0-9): ")

            if choice is None or choice == 0:
                print("\nThank you for using Future Mall Cashier System!")
                print("Shopping for Tomorrow")
                break

            actions = {
                1: self.display_products,
                2: self.add_to_cart,
                3: self.display_cart,
                4: self.update_quantity,
                5: self.remove_from_cart,
                6: self.clear_cart,
                7: lambda: self.process_checkout(),
                8: self.cancel_purchase,
                9: self.view_history,
            }

            action = actions.get(choice)
            if action:
                action()
            else:
                print("Invalid choice.")

            input("\nPress Enter to continue...")

    def process_checkout(self) -> None:
        """Process checkout and display receipt."""
        receipt = self.checkout()
        if receipt:
            print("\n" + "=" * 50)
            print("RECEIPT GENERATED")
            print("=" * 50)
            print(receipt)

            # Save to file
            filename = self.save_receipt_to_file(receipt)
            print(f"\nReceipt saved to: {filename}")


def main():
    """Entry point for the cashier program."""
    system = CashierSystem()
    system.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)
