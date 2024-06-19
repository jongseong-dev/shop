from webapp.cart.forms import CartAddProductForm


def test_cart_add_product_form_valid_quantity():
    form = CartAddProductForm(data={"quantity": 5, "override": False})
    assert form.is_valid()


def test_cart_add_product_form_invalid_quantity():
    form = CartAddProductForm(data={"quantity": 25, "override": False})
    assert not form.is_valid()


def test_cart_add_product_form_valid_override():
    form = CartAddProductForm(data={"quantity": 5, "override": True})
    assert form.is_valid()
