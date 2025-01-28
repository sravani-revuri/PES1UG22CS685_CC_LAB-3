from typing import List, Dict
from products import dao


class Product:
    def __init__(self, id: int, name: str, description: str, cost: float, qty: int = 0):
        self.id = id
        self.name = name
        self.description = description
        self.cost = cost
        self.qty = qty

    @staticmethod
    def load(data: dict) -> "Product":
        """Safely load a Product instance from a dictionary."""
        return Product(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            cost=data['cost'],
            qty=data.get('qty', 0)  # Default to 0 if 'qty' is missing
        )


def list_products() -> List[Product]:
    """Retrieve and return a list of all products."""
    products = dao.list_products()
    return [Product.load(product) for product in products]  # List comprehension


def get_product(product_id: int) -> Product:
    """Retrieve a specific product by ID."""
    product_data = dao.get_product(product_id)
    if not product_data:
        raise ValueError(f"Product with ID {product_id} not found.")
    return Product.load(product_data)

def add_product(product: Dict):
    """Add a new product to the database with basic validation."""
    required_keys = {"id", "name", "description", "cost"}
    if not required_keys.issubset(product.keys()):
        raise ValueError(f"Product data must include keys: {required_keys}")
    if product.get("cost", 0) < 0:
        raise ValueError("Product cost cannot be negative.")
    dao.add_product(product)


def update_qty(product_id: int, qty: int):
    """Update the quantity of a specific product."""
    if qty < 0:
        raise ValueError("Quantity cannot be negative.")
    dao.update_qty(product_id, qty)
