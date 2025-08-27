from typing import Optional


def must_have_value(option: str, msg: str) -> Optional[str]:
    if not option:
        raise ValueError(msg)
    return option