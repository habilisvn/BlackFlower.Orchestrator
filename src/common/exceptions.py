class MissingParameterException(Exception):
    def __init__(self, *, valid_params: list[str], message: str | None = None):
        # Ensure valid_params is a list of expected parameters
        assert isinstance(valid_params, list), "valid_params must be a list"

        # Construct the default message if no custom message is provided
        if message is None:
            message = (
                f"Missing required parameter. Please provide at least one of "
                f"the following: {', '.join(valid_params)}"
            )

        super().__init__(message)


class IsExistentException(Exception):
    pass
