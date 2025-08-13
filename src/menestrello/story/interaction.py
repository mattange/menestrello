import logging
from pydantic import BaseModel, Field, PrivateAttr 
from pathlib import Path
from typing import Self, ClassVar
import uuid
import hashlib
from functools import cached_property

logger = logging.getLogger(__name__)

from .response import Response

class Interaction(BaseModel):
    user: str = Field(..., description="The user input.")
    chatbot: Response = Field(..., description="The message from the chatbot.")
    
    
    # This field is set to a new UUID by default and is not included in the constructor
    identifier: uuid.UUID = Field(default_factory=uuid.uuid4, init=False) 

    # This field is set to None by default and is not included in the constructor
    # It is used to store the path to the storage folder
    _storage_folder: Path | None = PrivateAttr(default=None, init=False)
    
    interaction_json_file: ClassVar[str] = "interaction.json"

    @classmethod
    def from_primitives(cls, user_input: str, chatbot_json_string: str) -> "Interaction":
        chatbot_response = Response.model_validate_json(chatbot_json_string)
        c = cls(user=user_input, chatbot=chatbot_response)
        logger.debug(f"Created Interaction from chatbot JSON response.")
        return c
    
    @cached_property
    def title(self) -> str:
        return self.chatbot.title
        
    @cached_property
    def short_identifier(self) -> str:
        return self.identifier.hex[-6:]
    
    @property
    def storage_folder(self) -> Path:
        if self._storage_folder is None:
            raise ValueError("Storage folder not initialized.")
        return self._storage_folder
    
    @storage_folder.setter
    def storage_folder(self, value: Path) -> None:
        value.mkdir(exist_ok=True, parents=True)
        self._storage_folder = value
        logger.debug(f"Interaction directory initialised: {self.storage_folder.as_posix()}.")
    
    def store_as_json(self) -> Self:
        """
        Store the fragment as a JSON file.
        """
        with (self.storage_folder / self.interaction_json_file).open("w") as f:
            f.write(self.model_dump_json(indent=4))
        logger.debug(f"Storing interaction as JSON: {self.storage_folder.as_posix()}.")
        return self
        