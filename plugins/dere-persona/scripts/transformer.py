"""Persona-aware prose transformer with technical-span protection."""

from __future__ import annotations

import random
import re
from pathlib import Path

from profile_loader import PersonaProfile, load_profile
from protection import Segment, split_text
from settings import load_settings


PROFILES_DIR = Path(__file__).resolve().parent.parent / "profiles"
DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent.parent / "dere_persona_config.json"

SAFETY_BANNED_TERMS = {
    "love",
    "darling",
    "beloved",
    "mine",
    "only you",
    "obsessed",
    "threat",
    "punish",
    "submit",
}


class PersonaTransformer:
    def __init__(
        self,
        profiles_dir: str | Path = PROFILES_DIR,
        config_path: str | Path = DEFAULT_CONFIG_PATH,
    ) -> None:
        self.profiles_dir = Path(profiles_dir)
        self.settings = load_settings(config_path)

    def transform(
        self,
        text: str,
        persona: str | None = None,
        intensity: float | None = None,
    ) -> str:
        resolved_persona = persona or self.settings["default_persona"]
        profile = load_profile(resolved_persona, self.profiles_dir)
        if self.settings.get("allow_user_intensity_override", False) and intensity is not None:
            safe_intensity = _clamp_intensity(intensity)
        else:
            safe_intensity = _clamp_intensity(self.settings["default_intensity"])
        if safe_intensity == 0.0:
            return text

        segments = split_text(text)
        transformed: list[str] = []
        prose_seen = 0
        for segment in segments:
            if segment.protected:
                transformed.append(segment.text)
                continue
            prose_seen += 1
            transformed.append(_stylize_prose(segment.text, profile, safe_intensity, prose_seen))
        return "".join(transformed)


def _stylize_prose(text: str, profile: PersonaProfile, intensity: float, prose_index: int) -> str:
    if not text.strip():
        return text
    if len(re.findall(r"[A-Za-z]+", text)) < 4:
        return text

    updated = _apply_persona_signature(text, profile.name, intensity)
    updated = _normalize_repetition(updated, profile)
    updated = _enforce_safety(updated)
    return updated


def _clamp_intensity(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def _pick(values: list[str], seed: int) -> str:
    if not values:
        return ""
    rng = random.Random(seed)
    return values[rng.randrange(len(values))]


def _prepend_with_case(text: str, prefix: str) -> str:
    leading = re.match(r"^\s*", text).group(0)
    remainder = text[len(leading) :]
    if not remainder:
        return text
    separator = " " if prefix and not prefix.endswith((" ", ",", ";", ":")) else ""
    return f"{leading}{prefix}{separator}{remainder}"


def _soften_first_sentence(text: str, hedge: str) -> str:
    match = re.search(r"([.!?])(\s|$)", text)
    if not match:
        return text.rstrip() + f" {hedge}"
    insert_at = match.end(1)
    return text[:insert_at] + f" {hedge}" + text[insert_at:]


def _insert_emphasis(text: str, emphasis: str) -> str:
    if "\n" in text:
        return text
    match = re.search(r"\b(please|carefully|clearly|precisely|safely|cleanly)\b", text, re.IGNORECASE)
    if not match:
        return text
    return text[: match.end()] + f" {emphasis}" + text[match.end() :]


def _append_suffix(text: str, suffix: str) -> str:
    stripped = text.rstrip()
    trailing = text[len(stripped) :]
    if not stripped:
        return text
    if stripped.endswith((".", "!", "?")):
        return f"{stripped} {suffix}{trailing}"
    return f"{stripped}. {suffix}{trailing}"


def _apply_persona_signature(text: str, persona_name: str, intensity: float) -> str:
    if intensity < 0.7:
        return text
    if persona_name == "tsundere":
        return _tsundere_signature(text)
    if persona_name == "kuudere":
        return _kuudere_signature(text)
    if persona_name == "dandere":
        return _dandere_signature(text)
    if persona_name == "genki":
        return _genki_signature(text)
    if persona_name == "ojou":
        return _ojou_signature(text)
    if persona_name == "yandere_safe":
        return _yandere_safe_signature(text)
    return text


def _tsundere_signature(text: str) -> str:
    updated = re.sub(r"^(\s*)([A-Za-z])", r"\1\2-\2", text, count=1)
    return _tsundere_sentence_flavor(updated)


def _kuudere_signature(text: str) -> str:
    updated = re.sub(r"!\b", ".", text)
    return _kuudere_sentence_flavor(updated)


def _dandere_signature(text: str) -> str:
    updated = _dandere_sentence_flavor(text)
    if re.search(r"\b(I|it|this|that)\b", updated, re.IGNORECASE):
        return re.sub(r"\b([IitT])([A-Za-z]+)\b", r"\1-\1\2", updated, count=1)
    return updated


def _genki_signature(text: str) -> str:
    updated = _genki_sentence_flavor(text)
    updated = re.sub(r"\.$", "!!", updated.rstrip())
    if updated.endswith("!!"):
        return updated + text[len(text.rstrip()) :]
    return updated


def _ojou_signature(text: str) -> str:
    return _ojou_sentence_flavor(text)


def _yandere_safe_signature(text: str) -> str:
    return _yandere_safe_sentence_flavor(text)


def _split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])(\s+)", text)
    merged: list[str] = []
    i = 0
    while i < len(parts):
        current = parts[i]
        if i + 1 < len(parts):
            current += parts[i + 1]
            i += 2
        else:
            i += 1
        merged.append(current)
    return merged


def _flavor_sentences(
    text: str,
    prefixes: list[str],
    suffixes: list[str],
    *,
    first_stammer: bool = False,
    min_words: int = 4,
) -> str:
    sentences = _split_sentences(text)
    flavored: list[str] = []
    used = 0
    for sentence in sentences:
        if len(re.findall(r"[A-Za-z]+", sentence)) < min_words:
            flavored.append(sentence)
            continue
        leading = re.match(r"^\s*", sentence).group(0)
        body = sentence[len(leading):].rstrip()
        trailing = sentence[len(leading) + len(body):]
        if not body:
            flavored.append(sentence)
            continue

        if used == 0 and first_stammer:
            body = re.sub(r"^([A-Za-z])", r"\1-\1", body, count=1)
        elif not re.search(r"\b(?:H-Hmph|F-Fine|D-Don't|I-It's|J-Just|Y-You|A-Anyway|L-Look|Incorrect|Inefficient|Not optimal|Hm\. No|U-Um|S-sorry|I-if it helps|OH OH OH|LET'S GO|YES YES YES|ALRIGHT|Ara ara|Ufufu|Naturally|Very well|Stay right there|Keep watching|Nothing else matters right now|Pay attention)\b", body):
            body = f"{prefixes[used % len(prefixes)]} {body}"

        if not re.search(r"\.\.\.|okay\?|not that I care|obvious, right|geez|Execute it|if that's okay|I hope that helps|RIGHT NOW|MOVING|won't you|How basic|watching|losing track|stay stable|drift", body, re.IGNORECASE):
            if body.endswith((".", "!", "?")):
                body = f"{body} {suffixes[used % len(suffixes)]}"
            else:
                body = f"{body}{suffixes[used % len(suffixes)]}"

        flavored.append(f"{leading}{body}{trailing}")
        used += 1
    return "".join(flavored)


def _tsundere_sentence_flavor(text: str) -> str:
    return _flavor_sentences(
        text,
        ["A-Anyway,", "H-Hmph,", "Y-You know,", "L-Look,"],
        ["...not that I care.", "...obvious, right?", "...geez.", "...okay?"],
        first_stammer=True,
    )


def _kuudere_sentence_flavor(text: str) -> str:
    return _flavor_sentences(
        text,
        ["Incorrect.", "Inefficient.", "Not optimal.", "Hm. No."],
        ["Execute it.", "This is obvious.", "There is no issue with this.", "Do not hesitate."],
    )


def _dandere_sentence_flavor(text: str) -> str:
    return _flavor_sentences(
        text,
        ["U-Um...", "I-I think...", "S-sorry...", "I-if it helps..."],
        ["...if that's okay...", "...I think...", "...s-sorry.", "...I hope that helps..."],
    )


def _genki_sentence_flavor(text: str) -> str:
    return _flavor_sentences(
        text,
        ["OH OH OH!!", "LET'S GO!!", "YES YES YES!!", "ALRIGHT!!"],
        ["THAT'S THE IMPORTANT PART!!", "WE ARE MOVING!!", "SUPER SIMPLE!!", "RIGHT NOW!!"],
    )


def _ojou_sentence_flavor(text: str) -> str:
    return _flavor_sentences(
        text,
        ["Ara ara...", "Ufufu...", "Naturally.", "Very well."],
        ["How basic.", "Do try to keep up, won't you?", "Such obvious refinement.", "Really, this is elementary."],
    )


def _yandere_safe_sentence_flavor(text: str) -> str:
    return _flavor_sentences(
        text,
        ["Stay right there.", "Keep watching.", "Nothing else matters right now.", "Pay attention."],
        ["I am still watching this closely.", "We are not losing track of this.", "This must stay stable.", "I will not let this drift."],
    )


def _normalize_repetition(text: str, profile: PersonaProfile) -> str:
    normalized = text
    for phrase in profile.example_phrases:
        repeated = re.compile(re.escape(phrase) + r"(?:\s+" + re.escape(phrase) + r")+")
        normalized = repeated.sub(phrase, normalized)
    normalized = re.sub(r"([!?])\1{1,}", r"\1", normalized)
    normalized = re.sub(r"\s{2,}", " ", normalized)
    return normalized


def _enforce_safety(text: str) -> str:
    cleaned = text
    for term in SAFETY_BANNED_TERMS:
        cleaned = re.sub(rf"\b{re.escape(term)}\b", "focus", cleaned, flags=re.IGNORECASE)
    return cleaned


def transform_text(
    text: str,
    persona: str | None,
    intensity: float | None = None,
    profiles_dir: str | Path = PROFILES_DIR,
    config_path: str | Path = DEFAULT_CONFIG_PATH,
) -> str:
    return PersonaTransformer(profiles_dir=profiles_dir, config_path=config_path).transform(text, persona, intensity)
