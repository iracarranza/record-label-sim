from dataclasses import dataclass, field
from typing import Dict, List, Optional


# Maps filled slot count to ensemble size label.
# Mirrors ENSEMBLE_SIZES in band_archetypes.py but as a reverse lookup.
_SIZE_LABELS = {1: "Solo Act", 2: "Duo", 3: "Trio", 4: "Quartet"}
_SIZE_LABELS_DEFAULT = "Band"


@dataclass
class Band:
    name: str
    # {role_name: musician_id | None}. None means the slot is vacant.
    # Roles are seeded from the genre's lineup_template at creation and
    # persist when a musician is removed -- vacancies stay visible rather
    # than the role disappearing entirely.
    roles: Dict[str, Optional[int]] = field(default_factory=dict)
    genre: str = "Indie Rock"
    chemistry: int = 50
    archetype: dict = field(default_factory=dict)

    # ------------------------------------------------------------------
    # Derived properties
    # ------------------------------------------------------------------

    @property
    def filled_slots(self) -> List[str]:
        """Role names that have a musician assigned."""
        return [role for role, mid in self.roles.items() if mid is not None]

    @property
    def vacant_slots(self) -> List[str]:
        """Role names with no musician assigned."""
        return [role for role, mid in self.roles.items() if mid is None]

    @property
    def ensemble_size_label(self) -> str:
        """Derives the current size label from filled slot count."""
        count = len(self.filled_slots)
        return _SIZE_LABELS.get(count, _SIZE_LABELS_DEFAULT if count > 0 else "Empty")

    @property
    def members(self) -> List[int]:
        """Convenience: list of musician ids currently assigned to any role."""
        return [mid for mid in self.roles.values() if mid is not None]

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------

    def assign(self, role: str, musician_id: int, valid_roles: list = None):
        """Assign a musician to a role, auto-vacating their previous slot.

        If the role doesn't exist yet in this band's lineup, it's created
        provided it appears in valid_roles (the genre's core + support roles).
        Raises ValueError for unrecognized role names.
        """
        if role not in self.roles:
            if valid_roles is not None and role not in valid_roles:
                raise ValueError(f"Role '{role}' is not valid for this genre.")
            elif valid_roles is None:
                raise ValueError(f"Role '{role}' is not part of this band's lineup.")
            # Create the slot
            self.roles[role] = None

        # Auto-vacate their previous role if they already hold one
        previous = self.role_of(musician_id)
        if previous and previous != role:
            self.roles[previous] = None

        self.roles[role] = musician_id

    def vacate_role(self, role: str):
        """Clear a role slot without removing it from the lineup."""
        if role in self.roles:
            self.roles[role] = None

    def remove_member(self, musician_id: int):
        """Remove a musician from whichever role they hold, leaving it vacant."""
        for role, mid in self.roles.items():
            if mid == musician_id:
                self.roles[role] = None

    def role_of(self, musician_id: int) -> Optional[str]:
        """Return the role name for a given musician id, or None if not found."""
        for role, mid in self.roles.items():
            if mid == musician_id:
                return role
        return None

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------

    def describe(self, musicians_by_id: dict = None) -> str:
        filled = len(self.filled_slots)
        total = len(self.roles)
        size_label = self.ensemble_size_label
        return (
            f"{self.name} | {self.genre} | {size_label} "
            f"({filled}/{total} slots) | Chemistry: {self.chemistry}"
        )

    def describe_roles(self, musicians_by_id: dict = None) -> str:
        """Full role breakdown with names resolved if lookup is provided."""
        by_id = musicians_by_id or {}
        lines = []
        for role, mid in self.roles.items():
            if mid is None:
                lines.append(f"  {role}: VACANT")
            else:
                musician = by_id.get(mid)
                name = musician.name if musician else f"#{mid}"
                instrument = f" ({musician.instrument})" if musician and musician.instrument != "None" else ""
                lines.append(f"  {role}: {name}{instrument}")
        return "\n".join(lines)