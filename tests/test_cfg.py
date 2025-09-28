from aloe.document import AloeDocument
from aloe.ast import Array, Null


def test_cfg_get_string():
    text = """string = "string"
    """

    doc = AloeDocument.from_text(text)

    assert doc.get("string") == "string"


def test_cfg_get_int():
    text = """number = 1
    """

    doc = AloeDocument.from_text(text)

    assert doc.get("number") == 1


def test_cfg_get_float():
    text = """float = 1.0
    """

    doc = AloeDocument.from_text(text)

    assert doc.get("float") == 1.0


def test_cfg_get_boolean():
    text = """boolean = true
    """

    doc = AloeDocument.from_text(text)

    assert doc.get("boolean")


def test_cfg_get_array():
    text = """array = [1, 2, 3, 4, 5]
    """

    doc = AloeDocument.from_text(text)

    assert doc.get("array") == Array.from_iter([1, 2, 3, 4, 5])


def test_cfg_set():
    text = """string = "string"
    """

    doc = AloeDocument.from_text(text)

    doc.set("string", "string-1")

    assert doc.get("string") == "string-1"


def test_cfg_set_array():
    text = """array = [1, 2, 3 , 4]
    """

    doc = AloeDocument.from_text(text)

    doc.set("array", Array.from_iter([1, 2, 3, 4, 5]))

    assert doc.get("array") == Array.from_iter([1, 2, 3, 4, 5])


def test_cfg_set_nested_array():
    text = """array = [1, 2, 3 , 4]
    """

    doc = AloeDocument.from_text(text)

    doc.set("array", Array.from_iter([1, 2, 3, 4, 5, Array.from_iter([1, 2, 3, 4, 5])]))

    assert doc.get("array") == Array.from_iter(
        [1, 2, 3, 4, 5, Array.from_iter([1, 2, 3, 4, 5])]
    )


def test_cfg_remove():
    text = """string = "string"
    """

    doc = AloeDocument.from_text(text)

    doc.remove("string")

    assert doc.get("string") is None


def test_cfg_clear():
    text = """string = "string"
    """

    doc = AloeDocument.from_text(text)

    doc.clear()

    assert doc.get("string") is None


def test_cfg_clear_key():
    text = """string = "string"
    """

    doc = AloeDocument.from_text(text)

    doc.clear("string")

    assert doc.get("string") is Null
