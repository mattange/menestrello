from treelib import Tree, Node
from pathlib import Path
from typing import Self
import logging

logger = logging.getLogger(__name__)

class StoryTree():
    """
    A class representing a tree structure for stories.
    """
    def __init__(self, *args, **kwargs):
        self.story_tree = Tree()
        self.current_story_step = 0             # Store current story step at root level

    def initalize_storage_folder(self, root_location: str | Path) -> Self:
        if len(self.story_tree.children()) == 0:
            raise ValueError("Story tree is empty. Please add nodes before initializing the storage folder.")
        self.storage_folder = Path(root_location) / self.title
        self.storage_folder.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Story directory initialised: {self.storage_folder.as_posix()}")
        return self
    
    @property
    def current_story_node(self) -> Node | None:
        """Return the current story node."""
        return self.story_tree.get_node(self.current_story_step)
    