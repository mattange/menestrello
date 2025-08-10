from treelib.tree import Tree
from treelib.node import Node
from typing import Self
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

from .response import Response
from .interaction import Interaction

local_folder = Path(__file__).parent
default_developer_prompt_file = local_folder / "default_developer_prompt.txt"
with default_developer_prompt_file.open("r") as f:
    developer_prompt = f.read()

class StoryTree():
    def __init__(self, root_location: str | Path):
        self._story_tree: Tree = Tree()
        self._story_root_location: Path = Path(root_location)
        self._current_step_identifier = None
        self._current_subtree: Tree = self._story_tree
        self._current_step_root_location: Path = self._story_root_location
        self._chatbot_conversation = self.chatbot_setup()
    
    def __len__(self) -> int:
        return len(self._story_tree)

    def add_interaction(self, interaction: Interaction) -> Self:
        tag = interaction.title.replace(" ", "_").lower()
        parent_node_identifier = self._current_step_identifier
        node = Node(tag=tag, data=interaction, identifier=str(interaction.identifier))
        if parent_node_identifier is None:
            self.title = interaction.title
        self._story_tree.add_node(node=node, parent=parent_node_identifier)
        self._current_step_identifier = node.identifier
        self._current_subtree = self._story_tree.subtree(node.identifier)
        interaction.storage_folder = self._current_step_root_location / interaction.short_identifier
        interaction.store_as_json()
        self._current_step_root_location = interaction.storage_folder
        logger.debug(f"Added interaction w/ tag '{tag}' under parent node '{parent_node_identifier}'")
        return self
    
    def rewind_up(self) -> Self:
        if self._current_step_identifier is None:
            return self
        parent_node = self._story_tree.parent(self._current_step_identifier)
        if parent_node is None:
            return self
        intrcn: Interaction = parent_node.data
        self._current_step_identifier = parent_node.identifier  # type: ignore
        self._current_subtree = self._story_tree.subtree(self._current_step_identifier)
        self._current_step_root_location = intrcn.storage_folder
        logger.debug(f"Rewound to parent node '{self._current_step_identifier}'")
        return self
    
    @property
    def current_story_interaction(self) -> Interaction | None:
        n = self._story_tree.get_node(self._current_step_identifier)
        return n.data if n else None
    
    def show(self) -> None:
        self._story_tree.show()

    @property
    def chatbot_conversation(self) -> list[dict[str, str]]:
        return self._chatbot_conversation
    
    def _chatbot_conversation_append_to(self, role: str, content: str) -> Self:
        self._chatbot_conversation.append({"role": role, "content": content})
        return self
    
    def chatbot_conversation__append_user_input(self, content: str) -> Self:
        return self._chatbot_conversation_append_to(role="user", content=content)
    
    def chatbot_conversation__append_chatbot_response(self, content: str) -> Self:
        user_input = self._chatbot_conversation[-1]["content"]
        story_interaction = Interaction.from_primitives(user_input, content)
        self.add_interaction(story_interaction)
        return self._chatbot_conversation_append_to(role="assistant", content=content)

    @staticmethod
    def chatbot_response_format():
        return {
            "type": "json_schema",
            "json_schema": {
                "name": "Response",
                "schema": Response.model_json_schema(),
            }
        }
    
    @staticmethod
    def chatbot_setup() -> list[dict[str, str]]:
        return [
            {
                "role": "system",
                "content": developer_prompt,
            },
        ]
    