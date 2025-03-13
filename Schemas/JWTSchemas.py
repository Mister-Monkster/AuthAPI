import datetime
from typing import Optional, Any
from typing_extensions import Self
import re

from pydantic import BaseModel, field_validator, ConfigDict


class JWTRefresh(BaseModel):
    id: int