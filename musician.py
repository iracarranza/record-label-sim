from dataclasses import dataclass, field
from typing import List


STAT_FIELDS = (
    "dexterity",
    "technique",
    "ear_training",
    "music_theory",
    "improvisation",
    "creativity",
    "composition",
    "experimentation",
    "stage_presence",
    "excitement",
    "consistency",
    "nerves",
    "eccentricity",
    "professionalism",
    "ambition",
    "collaboration",
    "ego",
)


@dataclass
class Musician:
    name: str
    instrument: str
    career_specialty: str
    age: int = 20
    genre_preferences: List[str] = field(default_factory=list)
    ca: int = 10
    pa: int = 10
    personality_traits: List[str] = field(default_factory=list)
    relationships: dict = field(default_factory=dict)
    career_history: List[str] = field(default_factory=list)
    secondary_instrument: str | None = None
    id: int | None = None
    preferred_genre: str | None = None
    preferred_ensemble_size: str | None = None

    dexterity: int = 10
    technique: int = 10
    ear_training: int = 10
    music_theory: int = 10
    improvisation: int = 10
    creativity: int = 10
    composition: int = 10
    experimentation: int = 10
    stage_presence: int = 10
    excitement: int = 10
    consistency: int = 10
    nerves: int = 10
    eccentricity: int = 10
    professionalism: int = 10
    ambition: int = 10
    collaboration: int = 10
    ego: int = 10

    def inspect(self):
        stats = [
            f"{stat_name.replace('_', ' ').title()}: {getattr(self, stat_name)}"
            for stat_name in STAT_FIELDS
        ]
        traits = ", ".join(self.personality_traits) if self.personality_traits else "None"
        history = ", ".join(self.career_history) if self.career_history else "No career history yet"
        secondary = f" | Secondary: {self.secondary_instrument}" if self.secondary_instrument else ""
        preferred = []
        if self.preferred_genre:
            preferred.append(self.preferred_genre)
        if self.preferred_ensemble_size:
            preferred.append(self.preferred_ensemble_size)
        preferred_str = " / ".join(preferred) if preferred else "None"
        return "\n".join(
            [
                self.name,
                f"Instrument: {self.instrument}",
                f"Specialty: {self.career_specialty}{secondary}",
                f"Age: {self.age}",
                f"CA: {self.ca} | PA: {self.pa}",
                f"Prefers: {preferred_str}",
                f"Traits: {traits}",
                f"Career: {history}",
                "Stats:",
                *stats,
            ]
        )


def make_musician(name, instrument, specialty="Performer", **kwargs):
    return Musician(name=name, instrument=instrument, career_specialty=specialty, **kwargs)