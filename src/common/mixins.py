from typing import Any

from config.settings import get_settings


class SettingsMixin:
    """Mixin class that automatically injects settings values into class
    attributes.

    Usage:
        class MyClass(SettingsMixin):
            my_setting: str = "setting_attribute_name"

        # The attribute will be automatically populated from settings
        instance = MyClass()

        # Value from settings.setting_attribute_name
        print(instance.my_setting)
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._settings = get_settings()

        # Get all class attributes that should be populated from settings
        for attr_name, settings_key in self.__class__.__annotations__.items():
            if isinstance(getattr(self.__class__, attr_name, None), str):
                # Get the value from settings using the specified key
                settings_value = getattr(
                    self._settings, getattr(self.__class__, attr_name)
                )
                # Set the actual value on the instance
                setattr(self, attr_name, settings_value)

        super().__init__(*args, **kwargs)
