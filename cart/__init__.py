import json
from typing import List, Optional
from cart import dao
from products import Product, get_product


class Cart:
    def __init__(self, id: int, username: str, contents: List[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data: dict) -> "Cart":
        return Cart(
            id=data['id'],
            username=data['username'],
            contents=data.get('contents', []),
            cost=data['cost']
        )


def get_cart(username: str) -> List[Product]:
    """Fetch the cart for a given username and return a list of Product objects."""
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []
    
    products_in_cart = []
    for cart_detail in cart_details:
        try:
            # Safely parse the contents JSON
            contents = json.loads(cart_detail.get('contents', '[]'))
            # Fetch products in a single comprehension
            products_in_cart.extend(
                get_product(product_id) for product_id in contents
            )
        except (json.JSONDecodeError, KeyError):
            # Log error or handle invalid JSON data gracefully
            continue

    return products_in_cart

def add_to_cart(username: str, product_id: int) -> None:
    """Add a product to the user's cart."""
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int) -> None:
    """Remove a product from the user's cart."""
    dao.remove_from_cart(username, product_id)


def delete_cart(username: str) -> None:
    """Delete the entire cart for a user."""
    dao.delete_cart(username)
