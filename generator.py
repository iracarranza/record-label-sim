import random

from band_archetypes import GENRES, get_lineup_template
from musician import Musician, STAT_FIELDS


if not hasattr(Musician, "role"):
    @property
    def _role(self):
        return self.career_specialty

    @_role.setter
    def _role(self, value):
        self.career_specialty = value

    Musician.role = _role


PAIR_THRESHOLD = 24

NON_INSTRUMENTAL_SPECIALTIES = {"Songwriter", "Composer"}

INSTRUMENTS = [
    "Vocals",
    "Electric Guitar",
    "Acoustic Guitar",
    "Bass Guitar",
    "Piano",
    "Keyboard/Synth",
    "Drums",
    "Percussion",
    "Violin",
    "Cello",
    "Saxophone",
    "Trumpet",
    "Trombone",
    "Flute",
    "Clarinet",
    "Harmonica",
    "Turntables",
    "Sampler",
    "Studio Console",
]

ENSEMBLE_SIZES = ["Solo Act", "Duo", "Trio", "Quartet", "Band"]

NAME_POOLS = {
    "american": {
        "weight": 14,
        "first_names": [
            "Jacob", "Julian", "Mason", "Liam", "Noah", "Ethan", "Owen", "Lucas",
            "Pearl", "Mia", "Ava", "Sophia", "Emma", "Chloe", "Ella", "Grace", "Zoe", "Leo",
            "Henry", "Mila", "Lily", "Nora", "Harper", "Avery", "Riley", "Quinn",
            "Kai", "Dylan", "Elijah", "Gabe", "Iris", "Maya",
        ],
        "last_names": [
            "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
            "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
            "Wilson", "Anderson", "Taylor", "Thomas", "Moore", "Jackson", "Martin",
            "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark",
            "Ramirez", "Lewis", "Robinson",
        ],
    },
    "african_american": {
        "weight": 10,
        "first_names": [
            "Malik", "DeAndre", "Jaden", "Marcus", "Darius", "Trevon", "Isaiah",
            "Amir", "Brielle", "Tasha", "Imani", "Aaliyah", "Nia", "Kira", "Kenya",
            "Jayden", "Marquise", "Tyrell", "Jalen", "Kamari", "Shani", "Laila",
            "Jordan", "Nyla", "Tionne", "Zuri", "Amani", "Keisha", "Devon", "Darnell",
        ],
        "last_names": [
            "Washington", "Jefferson", "Carter", "Brooks", "Simmons", "Mitchell",
            "Parker", "Coleman", "Robinson", "Turner", "Foster", "Barnes", "Reed",
            "Hayes", "Gray", "Price", "Howard", "Long", "Watson", "Bailey", "Hughes",
            "Ward", "Sanders", "Russell", "Morris", "Stewart", "Fisher", "Hamilton",
            "Murphy", "Lawson",
        ],
    },
    "hispanic": {
        "weight": 8,
        "first_names": [
            "Mateo", "Sofia", "Diego", "Lucia", "Valentina", "Camila", "Alejandro",
            "Javier", "Elena", "Isabella", "Gabriel", "Emilia", "Adrian", "Natalia",
            "Daniel", "Carmen", "Luis", "Olivia", "Bruno", "Renata", "Miguel",
            "Clara", "Marco", "Sara", "Esteban", "Paula", "Andres", "Nina", "Rafael",
            "Diana",
        ],
        "last_names": [
            "Garcia", "Martinez", "Rodriguez", "Lopez", "Hernandez", "Gonzalez",
            "Perez", "Sanchez", "Ramirez", "Torres", "Flores", "Rivera", "Gomez",
            "Diaz", "Cruz", "Ruiz", "Moreno", "Alvarez", "Romero", "Jimenez", "Vargas",
            "Castro", "Ortiz", "Salazar", "Mendoza", "Navarro", "Rojas", "Vega",
            "Medina", "Aguirre",
        ],
    },
    "chinese": {
        "weight": 7,
        "first_names": [
            "Wei", "Jia", "Lin", "Ming", "Hao", "Rui", "Xinyi", "Yujie", "Qiang",
            "Tian", "Jun", "Yan", "Lei", "Xin", "Yu", "Han", "Bo", "Mei", "Chen",
            "Zhen", "Shan", "Qiao", "Huan", "Jiajun", "Pei", "Wen", "Kai", "Lian",
            "Ning",
        ],
        "last_names": [
            "Wang", "Li", "Zhang", "Liu", "Chen", "Yang", "Huang", "Zhao", "Zhou",
            "Wu", "Xu", "Sun", "Hu", "Lin", "He", "Gao", "Liang", "Guo", "Dong",
            "Peng", "Lu", "Xie", "Tang", "Han", "Feng", "Cai", "Yao", "Cheng",
            "Jiang", "Wei",
        ],
    },
    "japanese": {
        "weight": 6,
        "first_names": [
            "Haruto", "Yui", "Ren", "Sora", "Mai", "Kaito", "Hana", "Riku", "Aoi",
            "Yuto", "Mei", "Shiori", "Ryota", "Miki", "Daiki", "Nao", "Sota", "Yuna",
            "Kotaro", "Akari", "Rina", "Yuma", "Nozomi", "Keita", "Miu", "Takumi",
            "Ayaka", "Rei", "Shun", "Minato", "Mio",
        ],
        "last_names": [
            "Sato", "Suzuki", "Takahashi", "Tanaka", "Watanabe", "Ito", "Yamamoto",
            "Nakamura", "Kobayashi", "Kato", "Yoshida", "Yamada", "Sasaki", "Matsumoto",
            "Inoue", "Kimura", "Abe", "Shimizu", "Hayashi", "Mori", "Ikeda", "Arai",
            "Nakajima", "Fujita", "Ogawa", "Okada", "Hasegawa", "Maeda", "Fukuda",
            "Nakano",
        ],
    },
    "korean": {
        "weight": 6,
        "first_names": [
            "Minseo", "Jisoo", "Junho", "Hana", "Seojun", "Soojin", "Jiho", "Yuna",
            "Taeho", "Hyewon", "Minjun", "Nari", "Seungmin", "Jiwon", "Dasom",
            "Hyejin", "Kyung", "Chan", "Sunwoo", "Minsu", "Jaeho", "Eunji", "Suhyun",
            "Taeyang", "Yunseo", "Seohyun", "Joon", "Daeho", "Inha", "Hyun", "Mina",
        ],
        "last_names": [
            "Kim", "Park", "Lee", "Choi", "Jung", "Kang", "Cho", "Yoon", "Han",
            "Lim", "Shin", "Song", "Baek", "Jang", "Oh", "Seo", "Ryu", "Kwon", "Moon",
            "Ahn", "Bae", "Hwang", "Hong", "Do", "Nam", "Cha", "Yu", "Paik", "Jeong",
            "Kwon",
        ],
    },
    "vietnamese": {
        "weight": 5,
        "first_names": [
            "An", "Linh", "Minh", "Duy", "Hanh", "Hoa", "Khanh", "Quang", "Thao",
            "Vinh", "Lan", "Nam", "Tuan", "Nhi", "Phuong", "Nghia", "Khoa", "Trinh",
            "Bao", "Son", "Hieu", "Ly", "Anh", "Tam", "Dat", "Binh", "Chi", "Huy",
            "Diem", "Khang",
        ],
        "last_names": [
            "Nguyen", "Tran", "Le", "Pham", "Hoang", "Vu", "Dang", "Bui", "Do",
            "Ngo", "Dinh", "Huynh", "Vo", "Duong", "Truong", "Phan", "Quach", "Vũ",
            "Lê", "Trần", "Nguyễn", "Phạm", "Hoàng", "Đặng", "Bùi", "Võ", "Đỗ",
            "Ngô", "Trương", "Lý",
        ],
    },
    "filipino": {
        "weight": 5,
        "first_names": [
            "Mika", "Janelle", "Nico", "Bea", "Adrian", "Carla", "Miguel", "Grace",
            "Joaquin", "Sofia", "Rianne", "Paolo", "Kelsey", "Ezra", "Nicole",
            "Leandro", "Andrea", "Rafael", "Maris", "Alyssa", "CJ", "Talia", "Vince",
            "Mariel", "Carlos", "Angela", "Justin", "Denise", "Marco", "Bianca", "Ryan",
        ],
        "last_names": [
            "Santos", "Reyes", "Cruz", "Garcia", "Bautista", "Mendoza", "Flores",
            "Villanueva", "Ramos", "Navarro", "Agustin", "Lim", "Tan", "Sy", "De Leon",
            "Castillo", "Coronel", "Santiago", "Fernandez", "Aquino", "Marquez",
            "Domingo", "Arevalo", "Samson", "Salvador", "Valdez", "Enriquez", "Go",
            "Ocampo", "Delos Reyes",
        ],
    },
    "indian": {
        "weight": 5,
        "first_names": [
            "Aarav", "Anika", "Ishan", "Meera", "Rohan", "Priya", "Dev", "Nisha",
            "Kunal", "Kavya", "Neha", "Arjun", "Aditi", "Uma", "Saanvi", "Vihaan",
            "Asha", "Riya", "Karthik", "Diya", "Mohan", "Tara", "Sanjay", "Pooja",
            "Yash", "Naina", "Kabir", "Ishaan", "Veda", "Asha", "Ira",
        ],
        "last_names": [
            "Patel", "Shah", "Kumar", "Singh", "Gupta", "Mehta", "Rao", "Desai",
            "Verma", "Joshi", "Iyer", "Nair", "Menon", "Kapoor", "Malhotra", "Bhatia",
            "Sharma", "Chawla", "Reddy", "Pillai", "Dutta", "Banerjee", "Sethi",
            "Thakur", "Agarwal", "Kaur", "Anand", "Srivastava", "Khanna", "Goyal",
            "Bhatt",
        ],
    },
    "middle_eastern": {
        "weight": 4,
        "first_names": [
            "Omar", "Layla", "Khaled", "Noura", "Samir", "Yasmin", "Farid", "Leila",
            "Zain", "Mariam", "Tarek", "Noor", "Karim", "Rania", "Bilal", "Dana",
            "Hadi", "Salma", "Amir", "Hana", "Nadine", "Elias", "Sara", "Adam",
            "Reem", "Mustafa", "Maya", "Hassan", "Hiba", "Malik", "Lina",
        ],
        "last_names": [
            "Hassan", "Rahman", "Haddad", "Khalil", "Farah", "Al-Sayed", "Ibrahim",
            "El-Tayeb", "Zaydan", "Majid", "Abboud", "Barakat", "Nasser", "Salim",
            "Karimi", "Alami", "Ata", "Dajani", "Jaber", "Mouawad", "Maroun", "Sabri",
            "Harb", "Qureshi", "Farouk", "Sayegh", "Hmoud", "Hakim", "Taha", "Azar",
        ],
    },
    "irish": {
        "weight": 4,
        "first_names": [
            "Aiden", "Caoimhe", "Niamh", "Finn", "Conor", "Oisin", "Eoin", "Maeve",
            "Siobhan", "Ronan", "Cian", "Saoirse", "Aaron", "Erin", "Brendan",
            "Ciara", "Evan", "Aoife", "Kieran", "Roisin", "Cormac", "Orla", "Declan",
            "Fionn", "Eamon", "Niall", "Eimear", "Muiris", "Padraig", "Keira", "Tara",
        ],
        "last_names": [
            "Murphy", "Kelly", "O'Brien", "Walsh", "Byrne", "Ryan", "O'Connor",
            "Doyle", "Gallagher", "Moore", "Lynch", "McLaughlin", "Quinn", "Sullivan",
            "O'Neill", "Brennan", "Fitzpatrick", "Kavanagh", "Donovan", "O'Rourke",
            "Higgins", "Kennedy", "Collins", "Daly", "Boyle", "Flynn", "McCarthy",
            "Connolly", "Nolan",
        ],
    },
    "italian": {
        "weight": 4,
        "first_names": [
            "Luca", "Giulia", "Marco", "Sofia", "Matteo", "Chiara", "Davide", "Elena",
            "Gabriele", "Beatrice", "Andrea", "Aurora", "Fabio", "Marta", "Nicolo",
            "Giada", "Leonardo", "Noemi", "Alessio", "Sara", "Tommaso", "Clara",
            "Edoardo", "Francesca", "Lorenzo", "Caterina", "Paolo", "Vittoria", "Dario",
            "Viviana", "Pietro",
        ],
        "last_names": [
            "Rossi", "Russo", "Bianchi", "Romano", "Ferrari", "Esposito", "Bianchi",
            "Ricci", "Marino", "Greco", "Bruno", "Gallo", "Conti", "De Luca", "Mancini",
            "Costa", "Giordano", "Rizzo", "Lombardi", "Moretti", "Barbieri", "Fontana",
            "Santoro", "Caruso", "Mariani", "Rinaldi", "Parisi", "Villa", "Ferri",
            "Fabbri", "Bellini",
        ],
    },
    "french": {
        "weight": 4,
        "first_names": [
            "Louis", "Camille", "Gabriel", "Lina", "Jules", "Manon", "Enzo", "Chloe",
            "Luc", "Alice", "Nicolas", "Emma", "Theo", "Clara", "Arthur", "Ines",
            "Hugo", "Lea", "Mathis", "Eva", "Noa", "Juliette", "Bastien", "Maia",
            "Adrien", "Margot", "Axel", "Celeste", "Nathan", "Laura", "Robin",
        ],
        "last_names": [
            "Martin", "Bernard", "Dubois", "Thomas", "Robert", "Richard", "Petit",
            "Durand", "Leroy", "Moreau", "Simon", "Laurent", "Lefebvre", "Michel",
            "Garcia", "David", "Bertrand", "Roux", "Vincent", "Fournier", "Morel",
            "Girard", "Andre", "Mercier", "Dupont", "Lambert", "Fontaine", "Rousseau",
            "Chevalier", "Blanchard",
        ],
    },
    "german_scandinavian": {
        "weight": 4,
        "first_names": [
            "Lukas", "Maja", "Jonas", "Sophie", "Noah", "Lea", "Felix", "Emilia",
            "Milan", "Nora", "Finn", "Hanna", "Paul", "Mila", "Elias", "Lina",
            "Leon", "Ella", "Maximilian", "Amelia", "Theo", "Freja", "Oscar", "Alma",
            "David", "Ingrid", "Jakob", "Vera", "Samuel", "Selma", "Nils",
        ],
        "last_names": [
            "Muller", "Schmidt", "Schneider", "Fischer", "Weber", "Wagner", "Becker",
            "Hoffmann", "Schulz", "Koch", "Berg", "Richter", "Klein", "Wolf", "Neumann",
            "Schwarz", "Zimmermann", "Braun", "Kruger", "Hansen", "Larsen", "Johansen",
            "Nielsen", "Pedersen", "Olsen", "Svensson", "Andersen", "Henriksen",
            "Jakobsen", "Iversen", "Bergmann",
        ],
    },
    "eastern_european": {
        "weight": 3,
        "first_names": [
            "Marek", "Ania", "Kacper", "Zofia", "Luka", "Natalia", "Jakub", "Marta",
            "Tomasz", "Maja", "Pawel", "Karolina", "Filip", "Ewa", "Mateusz", "Olga",
            "Damian", "Klara", "Adrian", "Iga", "Bartosz", "Nadia", "Rafal", "Patrycja",
            "Milosz", "Daria", "Nikola", "Sonia", "Viktor", "Elena", "Aleksander",
        ],
        "last_names": [
            "Nowak", "Kowalska", "Wisniewski", "Wójcik", "Kowalczyk", "Kamiński",
            "Lewandowski", "Zielinski", "Szymanski", "Dabrowski", "Jankowski",
            "Mazur", "Wojciechowski", "Krawczyk", "Pawlowski", "Jasinski", "Gorski",
            "Baran", "Mikolajczyk", "Krol", "Grabowski", "Pietrzak", "Nowicki",
            "Mazurek", "Kucera", "Novak", "Horak", "Pavlov", "Sokolov", "Petrov",
            "Dmitriev",
        ],
    },
}

STAGE_NAMES = [
    "Nova", "Echo", "Halo", "Riot", "Static", "Velvet", "Pearl", "Neon", "Pixel",
    "Lyric", "Cipher", "Aura", "Vanta", "Rebel", "Ember", "Solace", "Fable", "Zephyr",
    "Orbit", "Prism", "Sable", "Quill", "Riven", "Cinder", "Lumen", "Lark", "Veil",
    "Pulse", "Glint", "Haze", "Cipher", "Mosaic", "Spire", "Drift", "Tonic", "Onyx",
    "Sage", "Echoes", "Quartz", "Wilder", "Carve", "Vector", "Flicker", "Mirth",
    "Aria", "Violet", "Kite", "Fjord", "Rook", "Bloom", "Blaze", "Satin", "Cove",
    "Ritual", "Atlas", "Vesper", "Dusk", "Luxe", "Nexus", "Surge", "Lumen", "Coda",
    "Riven", "Sway", "Kairo", "Noir", "Marlow", "Skye", "Aspen", "Lace",
]

MIXED_HERITAGE_CHANCE = 0.10
HYPHENATED_SURNAME_CHANCE = 0.04
STAGE_NAME_CHANCE = 0.03
INITIALS_CHANCE = 0.04


def _select_culture() -> str:
    """Select a culture by weighted random choice."""
    cultures = list(NAME_POOLS.keys())
    weights = [NAME_POOLS[culture]["weight"] for culture in cultures]
    return random.choices(cultures, weights=weights, k=1)[0]


def _pick_name(culture: str, name_type: str) -> str:
    """Pick a first or last name from a cultural pool."""
    return random.choice(NAME_POOLS[culture][name_type])


def _same_origin(culture_a: str, culture_b: str) -> bool:
    """Return True when two cultures belong to the same non-hyphenation group."""
    eastern_asian = {"chinese", "japanese", "korean", "vietnamese"}
    return culture_a in eastern_asian and culture_b in eastern_asian


def _pick_other_culture(culture: str, *, disallow_same_origin: bool = False) -> str:
    """Choose another culture, optionally avoiding the same-origin group."""
    candidates = [candidate for candidate in NAME_POOLS if candidate != culture]
    if disallow_same_origin:
        candidates = [candidate for candidate in candidates if not _same_origin(culture, candidate)]
    return random.choice(candidates)


def _build_surname(culture: str, *, mixed_heritage: bool, hyphenate: bool) -> tuple[str, str | None]:
    """Build a legal surname, optionally with a hyphenated second surname."""
    if mixed_heritage:
        surname_culture = _pick_other_culture(culture)
        surname = _pick_name(surname_culture, "last_names")
    else:
        surname_culture = culture
        surname = _pick_name(culture, "last_names")

    if not hyphenate:
        return surname, None

    secondary_culture = _pick_other_culture(surname_culture, disallow_same_origin=True)
    secondary_surname = _pick_name(secondary_culture, "last_names")
    if secondary_surname == surname:
        secondary_surname = _pick_name(secondary_culture, "last_names")
    return f"{surname}-{secondary_surname}", secondary_culture


def generate_name() -> dict[str, object]:
    """Generate a full legal name, display name, and stage-name metadata."""
    culture = _select_culture()
    first_name = _pick_name(culture, "first_names")
    mixed_heritage = random.random() < MIXED_HERITAGE_CHANCE
    hyphenate = random.random() < HYPHENATED_SURNAME_CHANCE
    surname, _ = _build_surname(culture, mixed_heritage=mixed_heritage, hyphenate=hyphenate)

    legal_name = f"{first_name} {surname}"
    uses_stage_name = random.random() < STAGE_NAME_CHANCE
    uses_initials = False if uses_stage_name else random.random() < INITIALS_CHANCE

    if uses_stage_name:
        display_name = random.choice(STAGE_NAMES)
    elif uses_initials:
        initial_letter = first_name[0]
        primary_surname = surname.split("-")[0]
        display_name = f"{initial_letter}{primary_surname[0]}"
    else:
        display_name = legal_name

    return {
        "legal_name": legal_name,
        "display_name": display_name,
        "first_name": first_name,
        "last_name": surname,
        "culture": culture,
        "stage_name": display_name if uses_stage_name else None,
        "uses_stage_name": uses_stage_name,
        "uses_initials": uses_initials,
    }


def _generate_pa():
    roll = random.random()
    if roll < 0.08:
        return random.randint(260, 300)
    if roll < 0.25:
        return random.randint(220, 260)
    if roll < 0.65:
        return random.randint(170, 220)
    return random.randint(120, 170)


def _generate_ca(pa):
    roll = random.random()
    if roll < 0.2:
        ratio = random.uniform(0.3, 0.45)
    elif roll < 0.6:
        ratio = random.uniform(0.45, 0.65)
    else:
        ratio = random.uniform(0.65, 0.85)
    return max(1, min(pa, int(round(pa * ratio))))


def _assign_stats(pa):
    base = {name: 5 for name in STAT_FIELDS}
    remaining = max(0, pa - (len(STAT_FIELDS) * 5))

    while remaining > 0:
        stat_name = random.choice(STAT_FIELDS)
        max_allowed = 25 if pa >= 240 and random.random() < 0.2 else 20
        if base[stat_name] >= max_allowed:
            continue
        base[stat_name] += 1
        remaining -= 1

    if pa >= 240 and random.random() < 0.25:
        legendary = random.choice(STAT_FIELDS)
        if base[legendary] < 25:
            base[legendary] = min(25, base[legendary] + 3)

    return {name: max(5, value) for name, value in base.items()}


# Football-Manager-style role fit: each specialty has "key" stats (weighted
# heavily), a unique "signature" stat (weighted heaviest -- no other specialty
# shares it, acts as a tie-breaker), and "preferred" stats (weighted lightly).
# Every specialty is scored independently, then chosen via weighted random
# selection -- strong fits are likely but not guaranteed.
#
# Songwriter/Producer/Composer share key stats (composition, creativity,
# music_theory) which is conceptually correct but creates correlation; the
# signature stats (eccentricity / technique / consistency) break the tie
# without removing the intentional overlap.
SPECIALTY_PROFILES = {
    "Performer": {
        "key": ["stage_presence", "excitement"],
        "signature": ["ego"],
        "preferred": ["consistency"],
    },
    "Songwriter": {
        "key": ["composition", "creativity"],
        "signature": ["eccentricity"],
        "preferred": ["music_theory"],
    },
    "Producer": {
        "key": ["music_theory", "creativity"],
        "signature": ["technique"],
        "preferred": ["experimentation"],
    },
    "Composer": {
        "key": ["composition", "music_theory"],
        "signature": ["consistency"],
        "preferred": ["creativity"],
    },
    "Session Musician": {
        "key": ["consistency", "professionalism"],
        "signature": ["collaboration"],
        "preferred": ["technique"],
    },
    "Multi-Instrumentalist": {
        "key": ["experimentation", "improvisation"],
        "signature": ["dexterity"],
        "preferred": ["collaboration"],
    },
}

SIGNATURE_STAT_WEIGHT = 3
KEY_STAT_WEIGHT = 2
PREFERRED_STAT_WEIGHT = 1

_TIER_WEIGHTS = {
    "signature": SIGNATURE_STAT_WEIGHT,
    "key": KEY_STAT_WEIGHT,
    "preferred": PREFERRED_STAT_WEIGHT,
}

# Independent-roll trait pool. Each trait fires on its own probability.
# A musician can end up with any combination (or none, falling back to
# "Quiet"). Kept as a single dict so band_archetypes.py's
# preferred_personalities always has a real pool to match against --
# if you add a trait there, add it here too.
TRAIT_POOL = {
    "Driven": 0.35,
    "Intense": 0.35,
    "Mysterious": 0.25,
    "Charismatic": 0.25,
    "Collaborative": 0.25,
    "Professional": 0.25,
    "Eccentric": 0.25,
    "Ambitious": 0.2,
    "Experimental": 0.2,
}

# Genre/archetype preferred personalities boost the weight of matching traits
# rather than injecting them from outside the pool -- keeps all traits
# genuinely random while making genre-appropriate traits more likely.
PREFERRED_PERSONALITY_BOOST = 0.2


ROLE_INSTRUMENTS = {
    "Lead Vocal": ["Vocals"],
    "Back Vocal": ["Vocals"],
    "Guitar": ["Electric Guitar", "Acoustic Guitar"],
    "Bass": ["Bass Guitar"],
    "Drums": ["Drums"],
    "Keyboard": ["Keyboard/Synth", "Piano"],
    "Piano": ["Piano"],
    "Turntables": ["Turntables"],
    "Sampler": ["Sampler"],
    "Studio Console": ["Studio Console"],
    "Saxophone": ["Saxophone"],
    "Trumpet": ["Trumpet"],
    "Violin": ["Violin"],
    "Cello": ["Cello"],
    "Flute": ["Flute"],
    "Clarinet": ["Clarinet"],
    "Harmonica": ["Harmonica"],
    "Percussion": ["Percussion"],
}

ROLE_STAT_BONUSES = {
    "Lead Vocal": ["stage_presence", "excitement"],
    "Back Vocal": ["stage_presence", "consistency"],
    "Guitar": ["dexterity", "technique"],
    "Bass": ["consistency", "technique"],
    "Drums": ["excitement", "consistency"],
    "Keyboard": ["music_theory", "creativity"],
    "Piano": ["composition", "music_theory"],
    "Turntables": ["experimentation", "improvisation"],
    "Sampler": ["experimentation", "creativity"],
    "Studio Console": ["music_theory", "creativity"],
    "Saxophone": ["technique", "improvisation"],
    "Trumpet": ["stage_presence", "excitement"],
    "Violin": ["technique", "music_theory"],
    "Cello": ["consistency", "technique"],
    "Flute": ["consistency", "music_theory"],
    "Clarinet": ["technique", "music_theory"],
    "Harmonica": ["stage_presence", "creativity"],
    "Percussion": ["excitement", "consistency"],
}

ROLE_SPECIALTY_HINTS = {
    "Lead Vocal": ["Performer"],
    "Guitar": ["Performer", "Songwriter", "Multi-Instrumentalist"],
    "Bass": ["Session Musician", "Performer"],
    "Drums": ["Performer", "Session Musician"],
    "Keyboard": ["Producer", "Composer", "Session Musician"],
    "Piano": ["Composer", "Songwriter"],
    "Turntables": ["Producer", "Performer"],
    "Sampler": ["Producer", "Multi-Instrumentalist"],
    "Studio Console": ["Producer", "Composer"],
    "Saxophone": ["Session Musician", "Performer"],
    "Trumpet": ["Performer", "Session Musician"],
    "Violin": ["Session Musician", "Composer"],
    "Cello": ["Session Musician", "Composer"],
    "Flute": ["Session Musician", "Composer"],
    "Clarinet": ["Session Musician", "Composer"],
    "Harmonica": ["Performer", "Songwriter"],
    "Percussion": ["Performer", "Session Musician"],
}

ROLE_PRIORITY = {
    "Lead Vocal": 0,
    "Guitar": 1,
    "Bass": 2,
    "Drums": 3,
    "Keyboard": 4,
    "Piano": 5,
    "Turntables": 6,
    "Sampler": 7,
    "Studio Console": 8,
    "Violin": 9,
    "Cello": 10,
    "Flute": 11,
    "Clarinet": 12,
    "Saxophone": 13,
    "Trumpet": 14,
    "Harmonica": 15,
    "Percussion": 16,
    "Back Vocal": 17,
}


def _specialty_scores(stats):
    scores = {}
    for specialty, profile in SPECIALTY_PROFILES.items():
        score = 0
        for tier_name, weight in _TIER_WEIGHTS.items():
            score += sum(stats[s] for s in profile.get(tier_name, [])) * weight
        scores[specialty] = score
    return scores


def _determine_specialty(stats, genre_name=None, roles=None):
    """Specialty from stats alone (no instrument dependency).

    Scores every specialty FM-style, then boosts scores for specialties
    preferred by the genre or hinted at by roles. Chosen via weighted
    random selection -- strong fits are likely but not guaranteed.
    """
    genre_data = GENRES.get(genre_name, {})
    preferred_specialties = genre_data.get("preferred_specialties", [])
    scores = _specialty_scores(stats)
    specialties = list(scores.keys())
    weights = [max(scores[s], 1) for s in specialties]

    if preferred_specialties:
        for specialty in preferred_specialties:
            if specialty in specialties:
                weights[specialties.index(specialty)] += 3

    if roles:
        for role in sorted(roles, key=lambda r: ROLE_PRIORITY.get(r, 99)):
            for specialty in ROLE_SPECIALTY_HINTS.get(role, []):
                if specialty in specialties:
                    weights[specialties.index(specialty)] += 2

    return random.choices(specialties, weights=weights, k=1)[0]


def _determine_instrument(stats, genre_name=None, roles=None, specialty=None):
    # Non-instrumental specialties short-circuit before role/stat logic.
    if specialty in NON_INSTRUMENTAL_SPECIALTIES:
        return "None"

    for role in sorted(roles or [], key=lambda r: ROLE_PRIORITY.get(r, 99)):
        candidates = ROLE_INSTRUMENTS.get(role, [])
        if candidates:
            return random.choice(candidates)

    if stats["stage_presence"] + stats["excitement"] >= PAIR_THRESHOLD:
        return "Vocals"
    if stats["dexterity"] + stats["technique"] >= PAIR_THRESHOLD:
        return "Electric Guitar"
    if stats["consistency"] + stats["professionalism"] >= PAIR_THRESHOLD:
        return "Bass Guitar"
    if stats["excitement"] + stats["consistency"] >= PAIR_THRESHOLD:
        return "Drums"
    if stats["music_theory"] + stats["creativity"] >= PAIR_THRESHOLD:
        return "Studio Console"
    if stats["composition"] + stats["creativity"] >= PAIR_THRESHOLD:
        return "Piano"
    if stats["experimentation"] + stats["improvisation"] >= PAIR_THRESHOLD:
        return "Turntables"
    return random.choice(INSTRUMENTS)


def _apply_role_and_genre_preferences(stats, genre_name=None, roles=None):
    """Nudge stats upward for genre-preferred attributes and role bonuses.

    Mutates stats in place -- callers do not need to reassign the return value.
    """
    genre_data = GENRES.get(genre_name, {})
    for attr in genre_data.get("preferred_attributes", []):
        if attr in stats and stats[attr] < 25:
            stats[attr] = min(25, stats[attr] + 2)

    for role in roles or []:
        for attr in ROLE_STAT_BONUSES.get(role, []):
            if attr in stats and stats[attr] < 25:
                stats[attr] = min(25, stats[attr] + 1)


def _generate_traits(preferred_personalities=None):
    """Roll traits from TRAIT_POOL.

    preferred_personalities (from genre/archetype data) boosts the roll
    probability for matching traits rather than injecting them from outside
    the pool -- so genre-appropriate traits are more likely but never
    guaranteed, and musicians without a genre context still have a full
    trait pool to draw from.
    """
    boosts = {t: PREFERRED_PERSONALITY_BOOST for t in (preferred_personalities or [])}
    traits = [
        trait
        for trait, base_prob in TRAIT_POOL.items()
        if random.random() < base_prob + boosts.get(trait, 0.0)
    ]
    return traits or ["Quiet"]


def _generate_preferred_ensemble_size(genre_name=None):
    """Pick a preferred ensemble size, biased toward sizes the genre commonly uses.

    Solo Act and Duo are universally less likely -- most musicians prefer to
    play with others. Genre context nudges toward that genre's typical size
    without locking it in.
    """
    # Base weights across all sizes; smaller ensembles weighted lower
    # since most musicians prefer a fuller band context.
    base_weights = {
        "Solo Act": 1,
        "Duo": 2,
        "Trio": 3,
        "Quartet": 4,
        "Band": 4,
    }

    # Genres that lean small or large nudge weights in that direction.
    GENRE_SIZE_BIAS = {
        "Singer-Songwriter": {"Solo Act": 3, "Duo": 3},
        "Jazz Quartet": {"Quartet": 3},
        "Orchestra": {"Band": 4},
        "Electronic": {"Solo Act": 2, "Duo": 2},
    }

    weights = dict(base_weights)
    for size, boost in GENRE_SIZE_BIAS.get(genre_name, {}).items():
        weights[size] = weights.get(size, 1) + boost

    sizes = list(weights.keys())
    size_weights = [weights[s] for s in sizes]
    return random.choices(sizes, weights=size_weights, k=1)[0]


def _generate_preferred_genre(genre_name=None):
    """Pick a preferred genre.

    If the musician was generated for a specific genre, they lean toward it
    but aren't locked in -- a small chance they prefer something adjacent.
    Musicians generated without a genre context pick freely.
    """
    all_genres = list(GENRES.keys())
    if genre_name and genre_name in all_genres:
        # 70% chance they prefer the genre they were generated in
        if random.random() < 0.7:
            return genre_name
    return random.choice(all_genres)


def generate_musician(name=None, instrument=None, specialty=None, pa=None, ca=None, genre_name=None, roles=None):
    musician_pa = pa if pa is not None else _generate_pa()
    stats = _assign_stats(musician_pa)
    _apply_role_and_genre_preferences(stats, genre_name=genre_name, roles=roles)

    musician_specialty = specialty or _determine_specialty(stats, genre_name=genre_name, roles=roles)

    if instrument is not None:
        musician_instrument = instrument
    elif musician_specialty in NON_INSTRUMENTAL_SPECIALTIES:
        musician_instrument = "None"
    else:
        musician_instrument = _determine_instrument(stats, genre_name=genre_name, roles=roles, specialty=musician_specialty)

    musician_ca = ca if ca is not None else _generate_ca(musician_pa)
    generated_name = generate_name() if name is None else None
    musician_name = name or (generated_name["legal_name"] if generated_name is not None else "Unknown")
    genre_data = GENRES.get(genre_name, {})

    musician = Musician(
        name=musician_name,
        instrument=musician_instrument,
        career_specialty=musician_specialty,
        age=random.randint(16, 34),
        genre_preferences=[_generate_preferred_genre(genre_name=genre_name)],
        ca=musician_ca,
        pa=musician_pa,
        personality_traits=_generate_traits(genre_data.get("preferred_personalities")),
        career_history=["Independent demos"],
        **stats,
    )

    if generated_name is not None:
        musician.legal_name = generated_name["legal_name"]
        musician.display_name = generated_name["display_name"]
        musician.first_name = generated_name["first_name"]
        musician.last_name = generated_name["last_name"]
        musician.culture = generated_name["culture"]
        musician.stage_name = generated_name["stage_name"]
        musician.uses_stage_name = generated_name["uses_stage_name"]
        musician.uses_initials = generated_name["uses_initials"]
        musician.preferred_genre = _generate_preferred_genre(genre_name=genre_name)
        musician.preferred_ensemble_size = _generate_preferred_ensemble_size(genre_name=genre_name)

    return musician


def generate_lineup(genre_name, ensemble_size):
    template = get_lineup_template(genre_name, ensemble_size)
    return [generate_musician(genre_name=genre_name, roles=member_roles) for member_roles in template]