"""Band archetype fit scoring.

Scores a band's current roster against its genre archetype across four
components, returning a 0-100 composite fit score plus a breakdown the
player can read. Kept as a standalone module so scoring logic stays
isolated from band state and is independently testable.

Score components and weights:
  Role coverage  40%  -- are core roles filled?
  Specialty fit  25%  -- do musicians' specialties match genre preferences?
  Attribute fit  25%  -- are the genre's key stats high on the right musicians?
  Personality    10%  -- do traits overlap with the genre's personality profile?
"""

from musician import Musician, STAT_FIELDS


ROLE_COVERAGE_WEIGHT = 0.40
SPECIALTY_WEIGHT = 0.25
ATTRIBUTE_WEIGHT = 0.25
PERSONALITY_WEIGHT = 0.10


def _role_coverage_score(band, archetype) -> tuple[float, str]:
    """0-100: what fraction of core roles are filled."""
    core_roles = archetype.get("core_roles", [])
    if not core_roles:
        return 100.0, "No core roles defined."

    filled = sum(1 for role in core_roles if role in band.roles and band.roles[role] is not None)
    score = (filled / len(core_roles)) * 100
    detail = f"{filled}/{len(core_roles)} core roles filled"
    if filled < len(core_roles):
        missing = [r for r in core_roles if r not in band.roles or band.roles[r] is None]
        detail += f" (missing: {', '.join(missing)})"
    return score, detail


def _specialty_score(musicians: list[Musician], archetype) -> tuple[float, str]:
    """0-100: fraction of musicians whose specialty is preferred by the genre."""
    if not musicians:
        return 0.0, "No musicians."
    preferred = set(archetype.get("preferred_specialties", []))
    if not preferred:
        return 100.0, "No specialty preferences defined."

    matches = sum(1 for m in musicians if m.career_specialty in preferred)
    score = (matches / len(musicians)) * 100
    detail = f"{matches}/{len(musicians)} musicians with preferred specialties"
    return score, detail


def _attribute_score(musicians: list[Musician], archetype) -> tuple[float, str]:
    """0-100: how well the roster's average on preferred attributes compares
    to the theoretical max (25) and min (5)."""
    preferred_attrs = archetype.get("preferred_attributes", [])
    if not preferred_attrs or not musicians:
        return 50.0, "No attribute preferences defined."

    # Average of preferred attribute values across all musicians
    total = sum(
        getattr(m, attr, 5)
        for m in musicians
        for attr in preferred_attrs
        if attr in STAT_FIELDS
    )
    count = len(musicians) * len(preferred_attrs)
    if count == 0:
        return 50.0, "No matching attributes."

    avg = total / count
    # Normalize: stat range is 5-25, map to 0-100
    score = max(0.0, min(100.0, (avg - 5) / 20 * 100))
    detail = f"Avg {', '.join(preferred_attrs)}: {avg:.1f}/25"
    return score, detail


def _personality_score(musicians: list[Musician], archetype) -> tuple[float, str]:
    """0-100: fraction of musicians who have at least one preferred trait."""
    if not musicians:
        return 0.0, "No musicians."
    preferred = set(archetype.get("preferred_personalities", []))
    if not preferred:
        return 100.0, "No personality preferences defined."

    matches = sum(
        1 for m in musicians
        if any(trait in preferred for trait in m.personality_traits)
    )
    score = (matches / len(musicians)) * 100
    detail = f"{matches}/{len(musicians)} musicians with preferred traits"
    return score, detail


def score_band(band, musicians_by_id: dict) -> dict:
    """Compute full fit score for a band against its archetype.

    Returns a dict with:
      total         -- 0-100 composite fit score (int)
      grade         -- letter grade (S/A/B/C/D)
      components    -- {name: (score, detail)} per component
      summary       -- one-line human-readable summary
    """
    archetype = band.archetype or {}
    musicians = [
        musicians_by_id[mid]
        for mid in band.members
        if mid in musicians_by_id
    ]

    role_score, role_detail = _role_coverage_score(band, archetype)
    spec_score, spec_detail = _specialty_score(musicians, archetype)
    attr_score, attr_detail = _attribute_score(musicians, archetype)
    pers_score, pers_detail = _personality_score(musicians, archetype)

    total = int(
        role_score * ROLE_COVERAGE_WEIGHT
        + spec_score * SPECIALTY_WEIGHT
        + attr_score * ATTRIBUTE_WEIGHT
        + pers_score * PERSONALITY_WEIGHT
    )

    if total >= 90:
        grade = "S"
    elif total >= 75:
        grade = "A"
    elif total >= 60:
        grade = "B"
    elif total >= 40:
        grade = "C"
    else:
        grade = "D"

    return {
        "total": total,
        "grade": grade,
        "components": {
            "Role Coverage":  (int(role_score), role_detail),
            "Specialty Fit":  (int(spec_score), spec_detail),
            "Attribute Fit":  (int(attr_score), attr_detail),
            "Personality":    (int(pers_score), pers_detail),
        },
        "summary": f"Fit: {total}/100 ({grade})",
    }


def format_score_breakdown(score_result: dict) -> str:
    """Human-readable multi-line breakdown for show_band()."""
    lines = [score_result["summary"], ""]
    for component, (component_score, detail) in score_result["components"].items():
        lines.append(f"  {component}: {component_score}/100 — {detail}")
    return "\n".join(lines)