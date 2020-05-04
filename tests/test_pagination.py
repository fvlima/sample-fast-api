from app.pagination import Pagination


def test_string_conversion():
    pagination = Pagination()

    assert str(pagination) == f"q: {pagination.q}, limit: {pagination.limit}, offset: {pagination.offset}"


def test_pagination_with_default_values():
    pagination = Pagination()

    assert pagination.q is None
    assert pagination.limit == 10
    assert pagination.offset == 0


def test_pagination_with_custom_values():
    pagination = Pagination(q="value", limit=100, offset=1)

    assert pagination.q == "value"
    assert pagination.limit == 100
    assert pagination.offset == 1
