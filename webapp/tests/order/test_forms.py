import pytest

from orders.forms import OrderCreateForm

valid_form_data = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "address": "123 Main St",
    "postal_code": "12345",
    "city": "City",
}


invalid_form_data = {
    "first_name": "",
    "last_name": "",
    "email": "invalid",
    "address": "",
    "postal_code": "",
    "city": "",
}


@pytest.mark.parametrize(
    "form_data, is_valid",
    [(valid_form_data, True), (invalid_form_data, False)],
)
def test_order_create_form(form_data, is_valid):
    form = OrderCreateForm(data=form_data)
    assert form.is_valid() is is_valid
