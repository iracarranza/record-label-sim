import random
from dataclasses import dataclass


@dataclass
class InboxEntry:
    week: int
    message: str
    source: str = "Weekly Report"


def generate_weekly_event(musician, week, roster=None):
    if roster:
        # Compare by id, not name -- names can collide across musicians,
        # ids can't (see band.py for the same fix applied to band membership).
        roster_names = [member.name for member in roster if member.id != musician.id]
        collaborator = random.choice(roster_names) if roster_names else None
    else:
        collaborator = None

    collaborator_text = collaborator if collaborator is not None else "the band"

    templates = [
        f"spent some time shedding with {collaborator_text}.",
        f"collaborated with {collaborator_text} on a new idea.",
        f"impressed local scene scouts at rehearsal with {collaborator_text}.",
        f"struggled with nerves before a workshop, but leaned on {collaborator_text}.",
        f"started working on a new style with {collaborator_text}.",
        f"shared a new demo with {collaborator_text}.",
    ]

    event = random.choice(templates)
    message = f"Week {week}: {musician.name} {event}"
    return InboxEntry(week=week, message=message, source="Weekly Report")