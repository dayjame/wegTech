from typing import Dict, Optional


from src.items import Item, all_items
from src.inventory import Inventory
from src.item_registry import ItemRegistry

class Character:
    def __init__(
            self,
            name: str,
            level: int = 1,
            base_stats: Dict[str, int] = None,
    ):

        # Core Identity
        self.name = name
        self.level = level
        self.xp = 0

        # Ensure all base stats exist, even if not provided
        default_stats = {
            "strength": 10,
            "agility": 10,
            "intelligence": 10,
            "endurance": 10,
            "wisdom": 10
        }
        if base_stats:
            default_stats.update(base_stats)  # Override defaults with provided stats
        self.base_stats = default_stats
        # Health/Mana
        self.hp = self.max_hp
        self.mp = self.max_mp

        # Inventory and Equipment
        self.inventory = Inventory(max_weight=50.0)
        self.equipment = {
            "weapon": None,  # Item ID (e.g., "frostbrand")
            "armor": None,
            "accessory": None
        }

        # Status Effects (e.g., "poison", "stunned")
        self.status_effects: Dict[str, Dict] = {}

    # === Derived Properties ===
    @property
    def max_hp(self) -> int:
        return 50 + (self.base_stats["endurance"] * 5)

    @property
    def max_mp(self) -> int:
        return 30 + (self.base_stats["wisdom"] * 3)

    @property
    def effective_stats(self) -> Dict[str, int]:
        """Calculate stats with equipment and status modifiers."""
        stats = self.base_stats.copy()

        # Apply equipment bonuses
        for item_id in self.equipment.values():
            if not item_id:  # Skip empty slots
                continue
            item = ItemRegistry.get_item(item_id)
            if item:
                for stat, bonus in item.stat_bonuses.items():
                    stats[stat] += bonus

        # Apply status effect penalties/bonuses
        for effect in self.status_effects.values():
            if "stat_modifiers" in effect:
                for stat, mod in effect["stat_modifiers"].items():
                    stats[stat] += mod

        return stats

    # === Core Methods ===
    def equip(self, item_id: str) -> bool:
        """Equip an item from the inventory."""
        if not self.inventory.has_item(item_id):
            print(f"Error: {self.name} doesn't have {item_id} in their inventory!")
            return False

        item = ItemRegistry.get_item(item_id)
        if  not item:
            print(f"Error: Item {item_id} not found in the registry!")
            return False

        # Check if the item is equippable (e.g., weapon/armor)
        if item.item_type not in ["weapon", "armor", "accessory"]:
            print(f"Error: {item.name} cannot be equipped!")
            return False

        slot = item.item_type  # e.g., "weapon"

        # Unequip existing item first
        if self.equipment[slot]:
            self.unequip(slot)

        self.equipment[slot] = item_id
        self.inventory.remove_item(item_id)
        return True

    def unequip(self, slot: str) -> Optional[str]:
        """Unequip an item and return it to the inventory."""
        item_id = self.equipment[slot]
        if not item_id:
            return None

        if self.inventory.add_item(item_id):
            self.equipment[slot] = None
            return item_id
        return None  # Inventory full

    def take_damage(self, damage: int) -> None:
        self.hp = max(0, self.hp - damage)

    def restore(self, hp: int = 0, mp: int = 0) -> None:
        self.hp = min(self.max_hp, self.hp + hp)
        self.mp = min(self.max_mp, self.mp + mp)

    def apply_status_effect(
            self,
            effect_id: str,
            duration: int,
            stat_modifiers: Dict[str, int] = None
    ) -> None:
        """Apply a status effect (e.g., poison, haste)."""
        self.status_effects[effect_id] = {
            "duration": duration,
            "stat_modifiers": stat_modifiers or {}
        }

    def update_statuses(self) -> None:
        """Decrement status effect durations (call this per turn)."""
        expired = []
        for effect_id, data in self.status_effects.items():
            data["duration"] -= 1
            if data["duration"] <= 0:
                expired.append(effect_id)
        for effect_id in expired:
            del self.status_effects[effect_id]

    # === Serialization ===
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "level": self.level,
            "xp": self.xp,
            "base_stats": self.base_stats,
            "hp": self.hp,
            "mp": self.mp,
            "inventory": self.inventory.to_dict(),
            "equipment": self.equipment,
            "status_effects": self.status_effects
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Character':
        char = cls(
            name=data["name"],
            level=data["level"],
            base_stats=data["base_stats"]
        )
        char.xp = data["xp"]
        char.hp = data["hp"]
        char.mp = data["mp"]
        char.inventory = Inventory.from_dict(data["inventory"])
        char.equipment = data["equipment"]
        char.status_effects = data["status_effects"]
        return char


