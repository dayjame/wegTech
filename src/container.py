import random
from typing import Dict, List, Optional, Callable
from src.items import Item
from src.inventory import Inventory


class Container(Inventory):
    def __init__(
            self,
            name: str = "Chest",
            max_weight: float = 50.0,
            max_slots: int = 10,
            locked: bool = False,
            location: str = "unknown"
    ):
        super().__init__(max_weight, max_slots)
        self.name = name  # e.g., "Rusty Chest", "Scholar's Bookshelf"
        self.locked = locked
        self.location = location  # e.g., "tavern_cellar", "forest_ruins"

    def generate_contents(
            self,
            all_items: Dict[str, Item],
            item_types: Optional[List[str]] = None,
            max_attempts: int = 100,
            probability_curve: Callable[[Item], float] = None
    ):
        """
        Fill the container with random items that fit its constraints.

        Args:
            all_items: Dictionary of all loaded items (from load_all_items()).
            item_types: Optional filter (e.g., ["weapon", "consumable"]).
            max_attempts: Prevent infinite loops if items are too heavy.
            probability_curve: Function to weight item selection (e.g., prefer rare items).
        """
        candidates = [
            item for item in all_items.values()
            if (not item_types or item.item_type in item_types)
        ]

        if not candidates:
            return

        # Default probability: equal chance for all items
        if not probability_curve:
            probability_curve = lambda item: 1.0

        weights = [probability_curve(item) for item in candidates]

        attempts = 0
        while attempts < max_attempts:
            attempts += 1
            item = random.choices(candidates, weights=weights, k=1)[0]

            # Check if the item can fit
            if (self.current_weight(all_items) + item.weight > self.max_weight or
                    (self.max_slots and len(self.items) >= self.max_slots)):
                continue

            # Add 1-3 copies (if stackable)
            quantity = random.randint(1, 3) if item.item_type == "consumable" else 1
            self.add_item(item.id, all_items, quantity=quantity)

    def to_dict(self) -> Dict:
        """Serialize for saving."""
        data = super().to_dict()
        data.update({
            "name": self.name,
            "locked": self.locked,
            "location": self.location
        })
        return data

    @classmethod
    def from_dict(
            cls,
            data: Dict,
            all_items: Dict[str, Item]
    ) -> 'Container':
        """Deserialize from a dictionary."""
        container = cls(
            name=data.get("name", "Chest"),
            max_weight=data["max_weight"],
            max_slots=data["max_slots"],
            locked=data.get("locked", False),
            location=data.get("location", "unknown")
        )
        container.items = data["items"]
        return container

# Load all items
from src.items import load_all_items
ALL_ITEMS = load_all_items()

# Create a chest that holds weapons/armor (max 30kg)
chest = Container(
    name="Bandit's Stash",
    max_weight=30.0,
    max_slots=8,
    location="forest_cave"
)

# Generate loot (only weapons/armor, prefer rare items)
chest.generate_contents(
    all_items=ALL_ITEMS,
    item_types=["weapon", "armor"],
    probability_curve=lambda item: item.value / 250  # Higher value = rarer
)

print(chest.display(ALL_ITEMS))