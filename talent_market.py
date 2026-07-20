import itertools
import random
from dataclasses import dataclass

from generator import generate_musician
from musician import Musician


@dataclass
class MarketListing:
    """Pairs a Musician with market-only data.

    Market fields (interest, salary, weeks remaining) belong to the
    listing, not the musician -- a musician shouldn't carry stale market
    attributes once recruited onto the roster.
    """

    musician: Musician
    available_weeks: int
    asking_salary: int
    signing_bonus: int
    current_interest: int

    @property
    def name(self):
        return self.musician.name

    @property
    def instrument(self):
        return self.musician.instrument

    @property
    def career_specialty(self):
        return self.musician.career_specialty

    @property
    def pa(self):
        return self.musician.pa

    @property
    def ca(self):
        return self.musician.ca


class TalentMarket:
    def __init__(self, target_size=12, id_generator=None):
        # id_generator: callable returning the next musician id. Pass the
        # same generator Game uses so market and roster musicians never
        # collide on id. Defaults to a local counter for standalone use
        # (e.g. tests) where no shared generator is available.
        self._next_id = id_generator or itertools.count(1).__next__
        self.target_size = target_size
        self.available = []
        self.last_refreshed_week = 0
        self.new_arrivals = 0
        self.departures = 0
        self._seed_market()

    def _seed_market(self):
        while len(self.available) < self.target_size:
            self.available.append(self._create_listing())

    def _create_listing(self):
        musician = generate_musician()
        musician.id = self._next_id()
        return MarketListing(
            musician=musician,
            available_weeks=random.randint(3, 8),
            asking_salary=random.randint(30000, 250000),
            signing_bonus=random.randint(5000, 120000),
            current_interest=random.randint(20, 95),
        )

    def update_market(self, week):
        expired = []
        for listing in list(self.available):
            listing.available_weeks -= 1
            listing.current_interest = max(0, listing.current_interest - random.randint(2, 8))
            if listing.available_weeks <= 0:
                expired.append(listing)

        for listing in expired:
            self.available.remove(listing)

        self.departures = len(expired)
        self.new_arrivals = 0

        while len(self.available) < self.target_size:
            self.available.append(self._create_listing())
            self.new_arrivals += 1

        while len(self.available) > self.target_size + 3:
            self.available.pop(0)

        self.last_refreshed_week = week
        return self.available

    def recruit(self, index):
        try:
            listing = self.available.pop(index - 1)
        except (TypeError, IndexError):
            return None
        return listing.musician

    def describe(self):
        if not self.available:
            return "Talent market is empty."

        lines = ["Talent Market", ""]
        lines.append(f"Last refreshed: Week {self.last_refreshed_week}")
        lines.append(f"New arrivals this refresh: {self.new_arrivals}")
        lines.append(f"Departures this refresh: {self.departures}")
        lines.append("")
        for index, listing in enumerate(self.available, start=1):
            musician = listing.musician
            lines.append(
                f"{index}. {musician.name} | {musician.instrument} | {musician.career_specialty} | "
                f"PA {musician.pa} | CA {musician.ca} | Interest {listing.current_interest} | "
                f"Weeks {listing.available_weeks}"
            )
        return "\n".join(lines)