from typing import Dict, Optional


from src.items import Item, all_items
from src.inventory import Inventory


class Character:
    def __init__(
            self,
            name: str,
            level: int = 1,
            base_stats: Dict[str, int] = None
    ):
        # Core Identity
        self.name = name
        self.level = level
        self.xp = 0

        # Base Stats (unmodified by equipment/statuses)
        self.base_stats = base_stats or {
            "strength": 10,
            "agility": 10,
            "intelligence": 10,
            "endurance": 10,
            "wisdom": 10
        }

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
            if item_id:
                item = Item.get_item(item_id)  # Assume a global Item registry
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
            return False

        item = Item.get_item(item_id)
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

    # Load items
    from src.items import load_all_items
    ALL_ITEMS = load_all_items()

    # Create a character
kenshin = Character(name="Kenshin", base_stats={"agility": 15, "strength": 12})

    # Add items to inventory
kenshin.inventory.add_item("stormcaller_katana", all_items)
kenshin.inventory.add_item("blessed_bandage", all_items, quantity=2)

    # Equip the katana
kenshin.equip("stormcaller_katana")

    # Check effective stats
print(kenshin.effective_stats["agility"])  # 15 (base) + 12 (katana) = 27

    # Apply poison status (agility penalty)
kenshin.apply_status_effect(
    effect_id="poison",
    duration=3,
    stat_modifiers={"agility": -5}
    )
print(kenshin.effective_stats["agility"])  # 27 - 5 = 22