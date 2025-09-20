from py_cfg.cfg import Cfg
from py_cfg.cst import *


def test_cfg_get_string():
    text = """string = "string"
    """

    cfg = Cfg.from_text(text)

    assert cfg.get("string") == "string"


def test_cfg_get_int():
    text = """number = 1
    """

    cfg = Cfg.from_text(text)

    assert cfg.get("number") == 1


def test_cfg_get_float():
    text = """float = 1.0
    """

    cfg = Cfg.from_text(text)

    assert cfg.get("float") == 1.0


def test_cfg_get_boolean():
    text = """boolean = true
    """

    cfg = Cfg.from_text(text)

    assert cfg.get("boolean") == True


def test_cfg_get_array():
    text = """array = [1, 2, 3, 4, 5]
    """

    cfg = Cfg.from_text(text)

    assert cfg.get("array") == Array.from_iter([1, 2, 3, 4, 5])


def test_cfg_set():
    text = """string = "string"
    """

    cfg = Cfg.from_text(text)

    cfg.set("string", "string-1")

    assert cfg.get("string") == "string-1"


def test_cfg_set_array():
    text = """array = [1, 2, 3 , 4]
    """

    cfg = Cfg.from_text(text)

    cfg.set("array", Array.from_iter([1, 2, 3, 4, 5]))

    assert cfg.get("array") == Array.from_iter([1, 2, 3, 4, 5])


def test_cfg_remove():
    text = """string = "string"
    """

    cfg = Cfg.from_text(text)

    cfg.remove("string")

    assert cfg.get("string") is None


def test_cfg_clear():
    text = """string = "string"
    """

    cfg = Cfg.from_text(text)

    cfg.clear()

    assert cfg.get("string") is None
