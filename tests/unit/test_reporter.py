from reporter import hello


def test_hello() -> None:
    assert hello("there") == "Hello, there"
