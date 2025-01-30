import os
import json
from typing import Dict
from pathlib import Path
from character import Character

class Item:
    def __init__(
        self,
        item_id: str,
        name: str,
        item_type: str,
        description: str,
        weight: float,
        value: int,
        stat_bonuses: Dict[str, int] = None,
        effect: Dict = None,
        special_abilities: list = None
    ):
        self.id = item_id
        self.name = name
        self.item_type = item_type
        self.description = description
        self.weight = weight
        self.value = value
        self.stat_bonuses = stat_bonuses or {}
        self.effect = effect
        self.special_abilities = special_abilities or []

class Ability:
    def __init__(
        self,
        name: str,
        ability_type: str,
        effect: str,
        activation_cost: Dict[str, int] = None,
        attack_speed_bonus: float = 1.0,
        num_hits: int = 1,
        duration: int = 1,
        cooldown: int = 0,
        **kwargs
    ):
        # ... (existing parameters)
        self.activation_cost = activation_cost or {}
        self.attack_speed_bonus = attack_speed_bonus
        self.num_hits = num_hits
        self.duration = duration
        self.current_cooldown = 0  # Tracks remaining cooldown turns
"""
    def trigger(self, user: 'Character', target: 'Character') -> bool:
         # Activate the ability if stamina/resources allow.
        if self.current_cooldown > 0:
            print(f"{self.name} is on cooldown ({self.current_cooldown} turns left).")
            return False

        # Check resource cost (e.g., stamina)
        for resource, cost in self.activation_cost.items():
            if getattr(user, resource, 0) < cost:
                print(f"Not enough {resource} to use {self.name}!")
                return False
            setattr(user, resource, getattr(user, resource) - cost)

        # Apply speed buff and multi-hit
        user.apply_status(
            status_id="hiten_speed_burst",
            duration=self.duration,
            attack_speed=self.attack_speed_bonus,
            num_hits=self.num_hits
        )
        self.current_cooldown = self.cooldown
        print(f"{user.name} activates {self.name} – a whirlwind of strikes begins!")
        return True
"""
def use_consumable(character: Character, item: Item):
    if item.item_type != "consumable":
        print(f"{item.name} isn’t a consumable!")
        return
"""
    effect = item.effect
    if effect["type"] == "restore_hp":
        character.hp = min(character.max_hp, character.hp + effect["potency"])
        print(f"{character.name} restored {effect['potency']} HP!")
    elif effect["type"] == "buff":
        character.apply_buff(effect["stat"], effect["value"], effect["duration"])
    # ... handle other effect types

    # Remove the item from inventory after use
    character.inventory.remove_item(item.id)
"""


def load_all_items() -> Dict[str, Item]:
    """Load all items from JSON files in the /data/items directory."""
    # Get the project root path (assuming items.py is in /src)
    project_root = Path(__file__).parent.parent  # Goes up from /src to project root
    items_dir = project_root / "data" / "items"
    items = {}

    for filename in os.listdir(items_dir):
        if filename.endswith(".json"):
            filepath = items_dir / filename
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    for item_id, item_data in data.items():
                        try:
                            # Extract item type from filename (e.g., "weapons.json" -> "weapon")
                            item_type = filename.replace(".json", "").rstrip('s').lower()

                            # Build the Item
                            items[item_id] = Item(
                                item_id=item_id,
                                name=item_data["name"],
                                item_type=item_type,
                                description=item_data.get("description", ""),
                                weight=item_data["weight"],
                                value=item_data["value"],
                                stat_bonuses=item_data.get("stat_bonuses", {}),
                                effect=item_data.get("effect", None),
                                special_abilities=item_data.get("special_abilities", [])
                            )
                        except KeyError as e:
                            print(f"ERROR in {filename}/{item_id}: Missing required field {e}!")
                            continue
            except json.JSONDecodeError:
                print(f"ERROR: {filename} is invalid JSON!")
                continue
            except FileNotFoundError:
                print(f"ERROR: {filename} not found in {items_dir}!")
                continue

    return items

# Load all items
all_items = load_all_items()

# Filter items by type (e.g., "weapon")
def get_items_by_type(item_type: str) -> list:
    return [item for item in all_items.values() if item.item_type == item_type]

weapons = get_items_by_type("weapon")
armor = get_items_by_type("armor")
"""
# Access a consumable's effect
health_potion = all_items["minor_healing_potion"]
print(f"Potion Effect: {health_potion.effect['type']}")  # "restore_hp"

# Access weapon abilities
for item_id, item in all_items.items():
    print(f"{item_id}: {item.name} ({item.item_type})")

# Access armor stats
chainmail = all_items["chainmail_tunic"]
print(f"Defense Bonus: {chainmail.stat_bonuses.get('endurance', 0)}")"""