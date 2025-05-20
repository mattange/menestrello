import logging
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class Option(BaseModel):
    number: int = Field(..., description="The option number.")
    description: str = Field(..., description="The description of the option.")
