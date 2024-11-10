from copy import deepcopy
from typing import Callable

from common.exceptions import IsExistentException


async def iterate_validate(*, func: Callable, input: dict) -> None:
    # validate user email exists
    params = {"email": None, "username": None}
    unique_keys = ["email", "username"]
    for key in unique_keys:
        tmp_params = deepcopy(params)
        tmp_params[key] = input[key]
        _user = await func(**tmp_params)
        if _user:
            raise IsExistentException(f"{key} already exists")
