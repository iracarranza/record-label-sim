GENRES = {
    "Pop Punk": {
        "core_roles": ["Lead Vocal", "Guitar", "Bass", "Drums"],
        "support_roles": ["Back Vocal", "Keyboard"],
        "preferred_specialties": ["Performer", "Songwriter", "Multi-Instrumentalist"],
        "preferred_personalities": ["Driven", "Charismatic", "Intense"],
        "preferred_attributes": ["excitement", "stage_presence", "dexterity"],
        "lineup_templates": {
            "Solo Act": [["Lead Vocal", "Guitar"]],
            "Duo": [["Lead Vocal", "Guitar"], ["Bass", "Back Vocal"]],
            "Trio": [["Lead Vocal", "Guitar"], ["Bass"], ["Drums"]],
            "Quartet": [["Lead Vocal", "Guitar"], ["Bass"], ["Drums"], ["Keyboard"]],
            "Band": [["Lead Vocal", "Guitar"], ["Bass"], ["Drums"], ["Guitar"], ["Keyboard"]],
        },
    },
    "Funk": {
        "core_roles": ["Lead Vocal", "Bass", "Drums", "Guitar"],
        "support_roles": ["Keyboard", "Saxophone", "Trumpet"],
        "preferred_specialties": ["Performer", "Session Musician", "Producer"],
        "preferred_personalities": ["Collaborative", "Professional", "Charismatic"],
        "preferred_attributes": ["technique", "consistency", "excitement"],
        "lineup_templates": {
            "Solo Act": [["Lead Vocal", "Guitar"]],
            "Duo": [["Lead Vocal", "Guitar"], ["Bass", "Back Vocal"]],
            "Trio": [["Lead Vocal", "Guitar"], ["Bass"], ["Drums"]],
            "Quartet": [["Lead Vocal", "Guitar"], ["Bass"], ["Drums"], ["Keyboard"]],
            "Band": [["Lead Vocal", "Guitar"], ["Bass"], ["Drums"], ["Keyboard"], ["Saxophone"]],
        },
    },
    "Jazz Quartet": {
        "core_roles": ["Lead Vocal", "Piano", "Bass", "Drums"],
        "support_roles": ["Saxophone", "Trumpet", "Clarinet"],
        "preferred_specialties": ["Composer", "Session Musician", "Performer"],
        "preferred_personalities": ["Professional", "Eccentric", "Collaborative"],
        "preferred_attributes": ["music_theory", "technique", "improvisation"],
        "lineup_templates": {
            "Solo Act": [["Lead Vocal", "Piano"]],
            "Duo": [["Lead Vocal", "Piano"], ["Bass"]],
            "Trio": [["Lead Vocal", "Piano"], ["Bass"], ["Drums"]],
            "Quartet": [["Lead Vocal", "Piano"], ["Bass"], ["Drums"], ["Saxophone"]],
            "Band": [["Lead Vocal", "Piano"], ["Bass"], ["Drums"], ["Saxophone"], ["Trumpet"]],
        },
    },
    "Metal": {
        "core_roles": ["Lead Vocal", "Guitar", "Bass", "Drums"],
        "support_roles": ["Keyboard"],
        "preferred_specialties": ["Performer", "Composer", "Multi-Instrumentalist"],
        "preferred_personalities": ["Intense", "Driven", "Eccentric"],
        "preferred_attributes": ["technique", "dexterity", "stage_presence"],
        "lineup_templates": {
            "Solo Act": [["Lead Vocal", "Guitar"]],
            "Duo": [["Lead Vocal", "Guitar"], ["Bass"]],
            "Trio": [["Lead Vocal", "Guitar"], ["Bass"], ["Drums"]],
            "Quartet": [["Lead Vocal", "Guitar"], ["Bass"], ["Drums"], ["Keyboard"]],
            "Band": [["Lead Vocal", "Guitar"], ["Bass"], ["Drums"], ["Guitar"], ["Keyboard"]],
        },
    },
    "Indie Rock": {
        "core_roles": ["Lead Vocal", "Guitar", "Bass", "Drums"],
        "support_roles": ["Keyboard", "Back Vocal"],
        "preferred_specialties": ["Songwriter", "Performer", "Producer"],
        "preferred_personalities": ["Mysterious", "Driven", "Collaborative"],
        "preferred_attributes": ["creativity", "composition", "stage_presence"],
        "lineup_templates": {
            "Solo Act": [["Lead Vocal", "Guitar"]],
            "Duo": [["Lead Vocal", "Guitar"], ["Bass", "Back Vocal"]],
            "Trio": [["Lead Vocal", "Guitar"], ["Bass"], ["Drums"]],
            "Quartet": [["Lead Vocal", "Guitar"], ["Bass"], ["Drums"], ["Keyboard"]],
            "Band": [["Lead Vocal", "Guitar"], ["Bass"], ["Drums"], ["Guitar"], ["Keyboard"]],
        },
    },
    "Hip-Hop": {
        "core_roles": ["Lead Vocal", "Turntables", "Bass", "Drums"],
        "support_roles": ["Sampler", "Keyboard"],
        "preferred_specialties": ["Performer", "Producer", "Songwriter"],
        "preferred_personalities": ["Driven", "Charismatic", "Ambitious"],
        "preferred_attributes": ["excitement", "creativity", "consistency"],
        "lineup_templates": {
            "Solo Act": [["Lead Vocal", "Turntables"]],
            "Duo": [["Lead Vocal", "Turntables"], ["Bass"]],
            "Trio": [["Lead Vocal", "Turntables"], ["Bass"], ["Drums"]],
            "Quartet": [["Lead Vocal", "Turntables"], ["Bass"], ["Drums"], ["Sampler"]],
            "Band": [["Lead Vocal", "Turntables"], ["Bass"], ["Drums"], ["Sampler"], ["Keyboard"]],
        },
    },
    "Electronic": {
        "core_roles": ["Lead Vocal", "Keyboard", "Sampler", "Drums"],
        "support_roles": ["Turntables", "Studio Console"],
        "preferred_specialties": ["Producer", "Composer", "Multi-Instrumentalist"],
        "preferred_personalities": ["Experimental", "Eccentric", "Professional"],
        "preferred_attributes": ["experimentation", "music_theory", "creativity"],
        "lineup_templates": {
            "Solo Act": [["Lead Vocal", "Keyboard"]],
            "Duo": [["Lead Vocal", "Keyboard"], ["Sampler"]],
            "Trio": [["Lead Vocal", "Keyboard"], ["Sampler"], ["Drums"]],
            "Quartet": [["Lead Vocal", "Keyboard"], ["Sampler"], ["Drums"], ["Turntables"]],
            "Band": [["Lead Vocal", "Keyboard"], ["Sampler"], ["Drums"], ["Turntables"], ["Studio Console"]],
        },
    },
    "Singer-Songwriter": {
        "core_roles": ["Lead Vocal", "Guitar", "Piano"],
        "support_roles": ["Harmonica", "Violin"],
        "preferred_specialties": ["Songwriter", "Composer", "Performer"],
        "preferred_personalities": ["Mysterious", "Professional", "Collaborative"],
        "preferred_attributes": ["composition", "creativity", "stage_presence"],
        "lineup_templates": {
            "Solo Act": [["Lead Vocal", "Guitar"]],
            "Duo": [["Lead Vocal", "Guitar"], ["Piano"]],
            "Trio": [["Lead Vocal", "Guitar"], ["Piano"], ["Violin"]],
            "Quartet": [["Lead Vocal", "Guitar"], ["Piano"], ["Bass"], ["Drums"]],
            "Band": [["Lead Vocal", "Guitar"], ["Piano"], ["Bass"], ["Drums"], ["Harmonica"]],
        },
    },
    "Orchestra": {
        "core_roles": ["Lead Vocal", "Violin", "Cello", "Piano"],
        "support_roles": ["Flute", "Clarinet", "Trumpet", "Trombone", "Percussion"],
        "preferred_specialties": ["Composer", "Session Musician", "Performer"],
        "preferred_personalities": ["Professional", "Collaborative", "Eccentric"],
        "preferred_attributes": ["music_theory", "technique", "consistency"],
        "lineup_templates": {
            "Solo Act": [["Lead Vocal", "Piano"]],
            "Duo": [["Lead Vocal", "Violin"], ["Cello"]],
            "Trio": [["Lead Vocal", "Violin"], ["Cello"], ["Piano"]],
            "Quartet": [["Lead Vocal", "Violin"], ["Cello"], ["Piano"], ["Flute"]],
            "Band": [["Lead Vocal", "Violin"], ["Cello"], ["Piano"], ["Flute"], ["Percussion"]],
        },
    },
}

ENSEMBLE_SIZES = {
    "Solo Act": 1,
    "Duo": 2,
    "Trio": 3,
    "Quartet": 4,
    "Band": 5,
}


def get_lineup_template(genre_name, ensemble_size):
    genre_data = GENRES[genre_name]
    return genre_data["lineup_templates"][ensemble_size]


BAND_ARCHETYPES = GENRES
