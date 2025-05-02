from treelib import Tree, Node
from pathlib import Path
from typing import Self
import logging

logger = logging.getLogger(__name__)

class StoryTree():
    """
    A class representing a tree structure for stories.
    """
    def __init__(self, title: str, *args, **kwargs):
        self.title = title
        self.story_tree = Tree()
        self.story_tree.create_node(title, 0)   # Create root node with the story title
        self.current_story_step = 0             # Store current story step at root level

    def initalize_storage_folder(self, root_location: str | Path) -> Self:
        self.storage_folder = Path(root_location) / self.title
        self.storage_folder.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Story directory initialised: {self.storage_folder.as_posix()}")
        return self
    
    @property
    def current_story_node(self) -> Node:
        """Return the current story node."""
        return self.story_tree.get_node(self.current_story_step)
    