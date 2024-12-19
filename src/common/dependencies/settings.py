from typing import Annotated
from fastapi import Depends

from config.settings import Settings, get_settings


SettingsDpd = Annotated[Settings, Depends(get_settings)]
