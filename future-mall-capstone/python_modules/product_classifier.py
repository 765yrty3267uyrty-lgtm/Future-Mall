#!/usr/bin/env python3
"""
Future Mall - Product Classifier Program
Automatically classifies products based on price, weight, and stock levels.
"""

import sys
import os
import json
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict

# Add shared constants to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'shared'))
from constants import CLASSIFIER, BRAND, format_currency, print_header, print_section


@dataclass
class Product:
    """Represents a product with classification results."""
    name: str
    price: float
    weight: float  # in kg
    stock: int
    category: str = ""

    # Classification results (populated after classification)
    price_class: str = ""
    weight_class: str = ""
    stock_class: str = ""

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'Product':
        """Create Product from dictionary."""
        return cls(**data)


class ProductClassifier:
    """Classifies products based on price, weight, and stock rules."""

    def __init__(self):
        self.products: List[Product] = []
        self.price_tiers = CLASSIFIER["price_tiers"]
        self.weight_tiers = CLASSIFIER["weight_tiers"]
        self.stock_tiers = CLASSIFIER["stock_tiers"]

    def validate_price(self, value: str) -> Optional[float]:
        """Validate price input."""
        try:
            price = float(value.strip())
            if price < 0:
                print("Price cannot be negative.")
                return None
            return price
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            return None

    def validate_weight(self, value: str) -> Optional[float]:
        """Validate weight input (in kg)."""
        try:
            weight = float(value.strip())
            if weight < 0:
                print("Weight cannot be negative.")
                return None
            return weight
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            return None

    def validate_stock(self, value: str) -> Optional[int]:
        """Validate stock quantity input."""
        try:
            stock = int(value.strip())
            if stock < 0:
                print("Stock cannot be negative.")
                return None
            return stock
        except ValueError:
            print("Invalid input. Please enter a whole number.")
            return None

    def get_non_empty_string(self, prompt: str) -> Optional[str]:
        """Get non-empty string input."""
        while True:
            value = input(prompt).strip()
            if value.lower() in ('q', 'quit', 'exit', 'cancel'):
                return None
            if value:
                return value
            print("This field cannot be empty.")

    def classify_price(self, price: float) -> str:
        """Classify product by price."""
        for tier_name, (min_val, max_val) in self.price_tiers.items():
            if min_val <= price <= max_val:
                return tier_name
        return "Unknown"

    def classify_weight(self, weight: float) -> str:
        """Classify product by weight."""
        for tier_name, (min_val, max_val) in self.weight_tiers.items():
            if min_val <= weight <= max_val:
                return tier_name
        return "Unknown"

    def classify_stock(self, stock: int) -> str:
        """Classify product by stock level."""
        for tier_name, (min_val, max_val) in self.stock_tiers.items():
            if min_val <= stock <= max_val:
                return tier_name
        return "Unknown"

    def classify_product(self, product: Product) -> Product:
        """Classify a product and update its classification fields."""
        product.price_class = self.classify_price(product.price)
        product.weight_class = self.classify_weight(product.weight)
        product.stock_class = self.classify_stock(product.stock)
        return product

    def add_product(self) -> Optional[Product]:
        """Add a new product through interactive input."""
        print_section("Add New Product")

        name = self.get_non_empty_string("Product Name: ")
        if name is None:
            return None

        price = None
        while price is None:
            price_input = input("Price: ").strip()
            if price_input.lower() in ('q', 'quit', 'exit', 'cancel'):
                return None
            price = self.validate_price(price_input)

        weight = None
        while weight is None:
            weight_input = input("Weight (kg): ").strip()
            if weight_input.lower() in ('q', 'quit', 'exit', 'cancel'):
                return None
            weight = self.validate_weight(weight_input)

        stock = None
        while stock is None:
            stock_input = input("Stock Quantity: ").strip()
            if stock_input.lower() in ('q', 'quit', 'exit', 'cancel'):
                return None
            stock = self.validate_stock(stock_input)

        category = input("Category (optional): ").strip()

        product = Product(
            name=name,
            price=price,
            weight=weight,
            stock=stock,
            category=category
        )

        product = self.classify_product(product)
        self.products.append(product)

        print(f"\nProduct '{name}' added and classified successfully!")
        return product

    def display_classification(self, product: Product) -> None:
        """Display product classification results."""
        print_section(f"Classification: {product.name}")

        print(f"{'Attribute':<20} {'Value':<15} {'Classification':<15}")
        print("-" * 55)
        print(f"{'Price':<20} {format_currency(product.price):<15} {product.price_class:<15}")
        print(f"{'Weight':<20} {f'{product.weight} kg':<15} {product.weight_class:<15}")
        print(f"{'Stock':<20} {f'{product.stock} units':<15} {product.stock_class:<15}")
        if product.category:
            print(f"{'Category':<20} {product.category:<15}")

        # Price tier info
        print("\nPrice Tiers:")
        for tier, (min_v, max_v) in self.price_tiers.items():
            marker = " ← YOUR PRODUCT" if tier == product.price_class else ""
            max_str = f"{max_v:.0f}" if max_v != float('inf') else "∞"
            print(f"  {tier}: {min_v:.0f} - {max_str} {marker}")

        # Weight tier info
        print("\nWeight Tiers:")
        for tier, (min_v, max_v) in self.weight_tiers.items():
            marker = " ← YOUR PRODUCT" if tier == product.weight_class else ""
            max_str = f"{max_v:.0f}" if max_v != float('inf') else "∞"
            print(f"  {tier}: {min_v:.1f} - {max_str} kg {marker}")

        # Stock tier info
        print("\nStock Tiers:")
        for tier, (min_v, max_v) in self.stock_tiers.items():
            marker = " ← YOUR PRODUCT" if tier == product.stock_class else ""
            max_str = f"{max_v:.0f}" if max_v != float('inf') else "∞"
            print(f"  {tier}: {min_v:.0f} - {max_str} units {marker}")

    def display_all_products(self) -> None:
        """Display all products in a summary table."""
        if not self.products:
            print("\nNo products added yet.")
            return

        print_section("All Products Summary")
        print(f"{'#':<4} {'Name':<20} {'Price':>10} {'Weight':>8} {'Stock':>6} {'Price Class':<12} {'Weight Class':<12} {'Stock Class':<12}")
        print("-" * 100)

        for i, p in enumerate(self.products, 1):
            print(f"{i:<4} {p.name:<20} {format_currency(p.price):>10} "
                  f"{f'{p.weight}kg':>8} {p.stock:>6} {p.price_class:<12} "
                  f"{p.weight_class:<12} {p.stock_class:<12}")

        # Summary statistics
        print("-" * 100)
        price_classes = {}
        weight_classes = {}
        stock_classes = {}

        for p in self.products:
            price_classes[p.price_class] = price_classes.get(p.price_class, 0) + 1
            weight_classes[p.weight_class] = weight_classes.get(p.weight_class, 0) + 1
            stock_classes[p.stock_class] = stock_classes.get(p.stock_class, 0) + 1

        print("\nClassification Summary:")
        print(f"  Price: {dict(price_classes)}")
        print(f"  Weight: {dict(weight_classes)}")
        print(f"  Stock: {dict(stock_classes)}")

    def save_to_json(self, filename: Optional[str] = None) -> str:
        """Save all products to JSON file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"products_{timestamp}.json"

        data = {
            "generated": datetime.now().isoformat(),
            "products": [p.to_dict() for p in self.products],
            "classification_rules": {
                "price_tiers": {k: list(v) for k, v in self.price_tiers.items()},
                "weight_tiers": {k: list(v) for k, v in self.weight_tiers.items()},
                "stock_tiers": {k: list(v) for k, v in self.stock_tiers.items()},
            }
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return filename

    def load_from_json(self, filename: str) -> bool:
        """Load products from JSON file."""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.products = [Product.from_dict(p) for p in data.get("products", [])]
            print(f"\nLoaded {len(self.products)} products from {filename}")
            return True
        except FileNotFoundError:
            print(f"File not found: {filename}")
            return False
        except json.JSONDecodeError:
            print(f"Invalid JSON file: {filename}")
            return False
        except Exception as e:
            print(f"Error loading file: {e}")
            return False

    def search_products(self, query: str) -> List[Product]:
        """Search products by name or category."""
        query = query.lower()
        return [p for p in self.products
                if query in p.name.lower() or query in p.category.lower()]

    def sort_products(self, key: str = "name", reverse: bool = False) -> None:
        """Sort products by specified key."""
        key_map = {
            "name": lambda p: p.name,
            "price": lambda p: p.price,
            "weight": lambda p: p.weight,
            "stock": lambda p: p.stock,
            "price_class": lambda p: p.price_class,
            "weight_class": lambda p: p.weight_class,
            "stock_class": lambda p: p.stock_class,
        }

        if key in key_map:
            self.products.sort(key=key_map[key], reverse=reverse)
            print(f"Products sorted by {key}.")
        else:
            print(f"Invalid sort key: {key}")

    def run(self) -> None:
        """Main application loop."""
        print_header("FUTURE MALL - PRODUCT CLASSIFIER")
        print(f"\n{BRAND['name']} - {BRAND['slogan']}")
        print("\nClassification Rules:")
        print("  Price:  Premium (>1000) | Standard (300-1000) | Budget (<300)")
        print("  Weight: Light (<1kg) | Medium (1-10kg) | Heavy (>10kg)")
        print("  Stock:  In Stock (>10) | Low Stock (1-10) | Out of Stock (0)")

        while True:
            print_section("Main Menu")
            print("1. Add New Product")
            print("2. View All Products")
            print("3. View Product Details")
            print("4. Search Products")
            print("5. Sort Products")
            print("6. Save to JSON")
            print("7. Load from JSON")
            print("8. Classification Rules Reference")
            print("0. Exit")

            choice = input("\nEnter choice (0-8): ").strip()

            if choice == '0':
                print("\nThank you for using Future Mall Product Classifier!")
                print("Shopping for Tomorrow")
                break

            elif choice == '1':
                self.add_product()

            elif choice == '2':
                self.display_all_products()

            elif choice == '3':
                if not self.products:
                    print("\nNo products added yet.")
                    continue
                self.display_all_products()
                try:
                    idx = int(input("\nEnter product number to view details: ")) - 1
                    if 0 <= idx < len(self.products):
                        self.display_classification(self.products[idx])
                    else:
                        print("Invalid product number.")
                except ValueError:
                    print("Invalid input.")

            elif choice == '4':
                if not self.products:
                    print("\nNo products to search.")
                    continue
                query = input("Enter search term: ").strip()
                if query:
                    results = self.search_products(query)
                    if results:
                        print(f"\nFound {len(results)} product(s):")
                        for p in results:
                            print(f"  - {p.name} ({p.price_class}, {p.weight_class}, {p.stock_class})")
                    else:
                        print("No products found.")

            elif choice == '5':
                if not self.products:
                    print("\nNo products to sort.")
                    continue
                print("\nSort by: name, price, weight, stock, price_class, weight_class, stock_class")
                key = input("Sort key: ").strip()
                if key:
                    order = input("Ascending (a) or Descending (d)? [a]: ").strip().lower()
                    self.sort_products(key, reverse=(order == 'd'))

            elif choice == '6':
                if not self.products:
                    print("\nNo products to save.")
                    continue
                filename = self.save_to_json()
                print(f"\nSaved to: {filename}")

            elif choice == '7':
                filename = input("Enter JSON filename to load: ").strip()
                if filename:
                    self.load_from_json(filename)

            elif choice == '8':
                print_section("Classification Rules Reference")
                print("\nPRICE CLASSIFICATION:")
                for tier, (min_v, max_v) in self.price_tiers.items():
                    max_str = f"{max_v:.0f}" if max_v != float('inf') else "∞"
                    print(f"  {tier}: {min_v:.0f} - {max_str}")

                print("\nWEIGHT CLASSIFICATION (kg):")
                for tier, (min_v, max_v) in self.weight_tiers.items():
                    max_str = f"{max_v:.0f}" if max_v != float('inf') else "∞"
                    print(f"  {tier}: {min_v:.1f} - {max_str}")

                print("\nSTOCK CLASSIFICATION:")
                for tier, (min_v, max_v) in self.stock_tiers.items():
                    max_str = f"{max_v:.0f}" if max_v != float('inf') else "∞"
                    print(f"  {tier}: {min_v:.0f} - {max_str}")

            else:
                print("Invalid choice. Please enter 0-8.")

            input("\nPress Enter to continue...")


def main():
    """Entry point for the product classifier program."""
    classifier = ProductClassifier()
    classifier.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)