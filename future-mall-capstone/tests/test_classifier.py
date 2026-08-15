import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'python_modules'))

from product_classifier import ProductClassifier, Product


class TestProductClassifier:
    def setup_method(self):
        self.classifier = ProductClassifier()

    def test_classify_price(self):
        assert self.classifier.classify_price(1500) == "Premium"
        assert self.classifier.classify_price(1000) == "Premium"
        assert self.classifier.classify_price(500) == "Standard"
        assert self.classifier.classify_price(300) == "Standard"
        assert self.classifier.classify_price(299) == "Budget"
        assert self.classifier.classify_price(100) == "Budget"

    def test_classify_weight(self):
        assert self.classifier.classify_weight(0.5) == "Light"
        assert self.classifier.classify_weight(1) == "Light"
        assert self.classifier.classify_weight(5) == "Medium"
        assert self.classifier.classify_weight(10) == "Medium"
        assert self.classifier.classify_weight(15) == "Heavy"

    def test_classify_stock(self):
        assert self.classifier.classify_stock(20) == "In Stock"
        assert self.classifier.classify_stock(10) == "Low Stock"
        assert self.classifier.classify_stock(1) == "Low Stock"
        assert self.classifier.classify_stock(0) == "Out of Stock"

    def test_classify_product(self):
        product = Product("Test Product", 500, 2, 10)
        product = self.classifier.classify_product(product)
        assert product.price_class == "Standard"
        assert product.weight_class == "Medium"
        assert product.stock_class == "Low Stock"

    def test_product_boundary_values(self):
        # Price boundaries
        assert self.classifier.classify_price(999.99) == "Standard"
        assert self.classifier.classify_price(1000) == "Premium"
        assert self.classifier.classify_price(299.99) == "Budget"
        assert self.classifier.classify_price(300) == "Standard"

        # Weight boundaries
        assert self.classifier.classify_weight(0.99) == "Light"
        assert self.classifier.classify_weight(1.0) == "Light"
        assert self.classifier.classify_weight(9.99) == "Medium"
        assert self.classifier.classify_weight(10.0) == "Medium"
        assert self.classifier.classify_weight(10.01) == "Heavy"

        # Stock boundaries
        assert self.classifier.classify_stock(11) == "In Stock"
        assert self.classifier.classify_stock(10) == "Low Stock"
        assert self.classifier.classify_stock(1) == "Low Stock"
        assert self.classifier.classify_stock(0) == "Out of Stock"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])