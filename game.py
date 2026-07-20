import itertools
import random

from band import Band
from band_archetypes import GENRES
from events import generate_weekly_event, InboxEntry
from generator import generate_musician, generate_lineup, ROLE_INSTRUMENTS
from scoring import score_band, format_score_breakdown
from talent_market import TalentMarket

# NOTE: `make_musician` from musician.py was imported here but never used.
# Removed -- re-add if you find a real call site for it elsewhere.


class Game:
    def __init__(self, genre="Indie Rock", ensemble_size="Trio", band_name="The Rising Tide"):
        self.week = 1
        self.genre = genre
        self.ensemble_size = ensemble_size
        self._next_musician_id = itertools.count(1).__next__

        musicians = generate_lineup(genre, ensemble_size)
        for musician in musicians:
            musician.id = self._next_musician_id()
        self.musicians = musicians

        # Seed band roles from the lineup template so roles exist from the
        # start and vacancies are visible when a musician is removed.
        genre_data = GENRES[genre]
        template = genre_data["lineup_templates"][ensemble_size]
        # Each template entry is a list of roles for one musician slot;
        # use the first role in each slot as the band role name.
        initial_roles = {}
        for member_roles, musician in zip(template, self.musicians):
            primary_role = member_roles[0]
            initial_roles[primary_role] = musician.id

        self.inbox = []
        self.bands = [
            Band(
                name=band_name,
                roles=initial_roles,
                genre=genre,
                archetype=genre_data,
            )
        ]
        # Same id generator as above, so market and roster musicians never
        # collide on id.
        self.talent_market = TalentMarket(id_generator=self._next_musician_id)
        self.market_refreshed_this_week = False

    def musicians_by_id(self):
        return {musician.id: musician for musician in self.musicians}

    def next_week(self):
        self.week += 1

        for musician in self.musicians:
            musician.ca = min(musician.pa, musician.ca + 1)
            musician.stage_presence = min(25, musician.stage_presence + 1)

        self.market_refreshed_this_week = False
        self.talent_market.update_market(self.week)

        musician = random.choice(self.musicians)
        event = generate_weekly_event(musician, self.week, roster=self.musicians)
        self.inbox.append(event)
        return event

    def show_help(self):
        return "\n".join(
            [
                "Commands:",
                "  help         - show this list",
                "  roster       - view your roster",
                "  bands        - list all bands",
                "  band <n>     - inspect a band in detail",
                "  market       - view the current talent market",
                "  refresh      - refresh the market once per week",
                "  inbox        - review weekly reports",
                "  next         - advance to the next week",
                "  musician <n> - inspect a musician in detail",
                "  recruit <n>  - recruit a musician from the talent market",
                "  fire <n>     - release a musician from the label",
                "  assign <musician_n> <role> - assign a musician to a band role",
                "  rename band <n> <name>     - rename a band",
                "  quit         - leave the game",
            ]
        )

    def show_bands(self):
        if not self.bands:
            return "No bands yet."
        lines = ["Bands", ""]
        by_id = self.musicians_by_id()
        for index, band in enumerate(self.bands, start=1):
            fit = score_band(band, by_id)
            lines.append(f"{index}. {band.describe(by_id)} | {fit['summary']}")
            if band.vacant_slots:
                lines.append(f"   Vacant: {', '.join(band.vacant_slots)}")
        return "\n".join(lines)

    def rename_band(self, number, new_name):
        try:
            band = self.bands[number - 1]
        except (TypeError, IndexError):
            return False, "Band not found."
        if not new_name.strip():
            return False, "Band name cannot be empty."
        old_name = band.name
        band.name = new_name.strip()
        return True, f'"{old_name}" renamed to "{band.name}".'

    def show_band(self, number):
        try:
            band = self.bands[number - 1]
        except (TypeError, IndexError):
            return "Band not found."
        by_id = self.musicians_by_id()
        fit = score_band(band, by_id)
        lines = [
            band.name,
            f"Genre: {band.genre} | Size: {band.ensemble_size_label} | Chemistry: {band.chemistry}",
            "",
            "Roles:",
            band.describe_roles(by_id),
            "",
            format_score_breakdown(fit),
        ]
        if band.vacant_slots:
            lines.append("")
            lines.append(f"Vacant: {', '.join(band.vacant_slots)}")
        lines.append("")
        lines.append(f"  assign <musician_n> <role>  |  rename band {number} <name>")
        return "\n".join(lines)

    def show_roster(self):
        by_id = self.musicians_by_id()
        # Build a reverse lookup: musician_id -> (band_name, role)
        assignments = {}
        for band in self.bands:
            for role, mid in band.roles.items():
                if mid is not None:
                    assignments[mid] = (band.name, role)

        lines = ["Roster", ""]
        for index, musician in enumerate(self.musicians, start=1):
            assignment = assignments.get(musician.id)
            role_str = f" [{assignment[1]} in {assignment[0]}]" if assignment else " [unassigned]"
            lines.append(
                f"{index}. {musician.name} | {musician.career_specialty} | "
                f"CA {musician.ca} | PA {musician.pa}{role_str}"
            )
        return "\n".join(lines)

    def show_inbox(self):
        if not self.inbox:
            return "Inbox is empty."
        lines = ["Inbox", ""]
        for entry in self.inbox:
            lines.append(f"- [{entry.week}] {entry.message}")
        return "\n".join(lines)

    def show_market(self):
        return self.talent_market.describe()

    def refresh_market(self):
        if self.market_refreshed_this_week:
            return "The market was already refreshed this week."
        self.market_refreshed_this_week = True
        self.talent_market.update_market(self.week)
        return self.talent_market.describe()

    def show_musician(self, number):
        try:
            musician = self.musicians[number - 1]
        except (TypeError, IndexError):
            return "Musician not found."
        return musician.inspect()

    def recruit_from_market(self, number):
        musician = self.talent_market.recruit(number)
        if musician is None:
            return None
        self.musicians.append(musician)
        return musician

    def fire_musician(self, number):
        try:
            musician = self.musicians[number - 1]
        except (TypeError, IndexError):
            return None

        self.musicians.remove(musician)

        # Vacate their role in any band, log each departure to inbox.
        for band in self.bands:
            if musician.id in band.members:
                role = band.role_of(musician.id)
                band.remove_member(musician.id)
                self.inbox.append(InboxEntry(
                    week=self.week,
                    message=f"{musician.name} has left {band.name} ({role} is now vacant).",
                    source="Label News",
                ))

        return musician

    def assign_role(self, musician_number, role):
        """Assign a roster musician to a named role in the first band.

        Accepts any role in the genre's core_roles + support_roles, creating
        the slot if it doesn't exist yet. Auto-vacates the musician's previous
        role. Soft-validates instrument fit: warns but doesn't block.
        Returns a (success, message) tuple.
        """
        try:
            musician = self.musicians[musician_number - 1]
        except (TypeError, IndexError):
            return False, "Musician not found."

        if not self.bands:
            return False, "No bands exist yet."

        # For now, assign into the first band. Multi-band support can extend this.
        band = self.bands[0]
        archetype = band.archetype or {}
        valid_roles = archetype.get("core_roles", []) + archetype.get("support_roles", [])

        previous_role = band.role_of(musician.id)

        try:
            band.assign(role, musician.id, valid_roles=valid_roles)
        except ValueError:
            valid_str = ", ".join(valid_roles) if valid_roles else "none defined"
            return False, f"'{role}' is not a valid role for {band.genre}. Valid roles: {valid_str}"

        # Soft instrument validation
        expected_instruments = ROLE_INSTRUMENTS.get(role, [])
        instrument_warning = ""
        if expected_instruments and musician.instrument not in expected_instruments:
            plays = musician.instrument if musician.instrument != "None" else "no instrument"
            instrument_warning = (
                f" (note: plays {plays}, "
                f"expected {', '.join(expected_instruments)})"
            )

        vacated_str = f", vacating {previous_role}" if previous_role and previous_role != role else ""
        return True, f"{musician.name} assigned to {role}{vacated_str}.{instrument_warning}"