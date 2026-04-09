from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from profile_loader import load_profile
from protection import split_text
from transformer import transform_text


class ProtectionTests(unittest.TestCase):
    def test_fenced_code_block_is_unchanged(self) -> None:
        text = "Explain the fix.\n\n```python\nprint('hello')\n```\n\nThen rerun it."
        output = transform_text(text, persona="kuudere", profiles_dir=ROOT / "profiles", config_path=ROOT / "dere_persona_config.json")
        self.assertIn("```python\nprint('hello')\n```", output)

    def test_shell_command_is_unchanged(self) -> None:
        text = "Run this next:\n\nnpm test -- --runInBand\n"
        output = transform_text(text, persona="tsundere", profiles_dir=ROOT / "profiles", config_path=ROOT / "dere_persona_config.json")
        self.assertIn("npm test -- --runInBand", output)

    def test_inline_code_url_and_path_are_unchanged(self) -> None:
        text = "Open `src/app.py` and compare it with /tmp/build.log at https://example.com/docs."
        output = transform_text(text, persona="genki", profiles_dir=ROOT / "profiles", config_path=ROOT / "dere_persona_config.json")
        self.assertIn("`src/app.py`", output)
        self.assertIn("/tmp/build.log", output)
        self.assertIn("https://example.com/docs", output)

    def test_structured_blocks_are_unchanged(self) -> None:
        json_block = '{\n  "name": "dere-persona"\n}'
        yaml_block = "name: dere-persona\nmodes:\n  - tsundere\n  - kuudere\n"
        xml_block = "<root><mode>genki</mode></root>"
        text = f"{json_block}\n\n{yaml_block}\n\n{xml_block}"
        output = transform_text(text, persona="ojou", profiles_dir=ROOT / "profiles", config_path=ROOT / "dere_persona_config.json")
        self.assertIn(json_block, output)
        self.assertIn(yaml_block, output)
        self.assertIn(xml_block, output)

    def test_exact_quoted_error_text_is_unchanged(self) -> None:
        error = '"ModuleNotFoundError: No module named foo"'
        text = f"Handle {error} before retrying."
        output = transform_text(text, persona="dandere", profiles_dir=ROOT / "profiles", config_path=ROOT / "dere_persona_config.json")
        self.assertIn(error, output)

    def test_stack_trace_and_diff_are_unchanged(self) -> None:
        text = (
            "Traceback (most recent call last):\n"
            '  File "main.py", line 1, in <module>\n'
            "ValueError: bad value\n\n"
            "diff --git a/a.py b/a.py\n"
            "--- a/a.py\n"
            "+++ b/a.py\n"
            "@@ -1 +1 @@\n"
            '-print("a")\n'
            '+print("b")\n'
        )
        output = transform_text(text, persona="yandere_safe", profiles_dir=ROOT / "profiles", config_path=ROOT / "dere_persona_config.json")
        self.assertIn('  File "main.py", line 1, in <module>', output)
        self.assertIn('@@ -1 +1 @@', output)
        self.assertIn('+print("b")', output)

    def test_intensity_zero_returns_original_text(self) -> None:
        text = "Apply the patch and rerun the test."
        output = transform_text(text, persona="kuudere", profiles_dir=ROOT / "profiles", config_path=ROOT / "tests" / "fixtures" / "zero_intensity_config.json")
        self.assertEqual(text, output)

    def test_split_text_marks_fenced_blocks_as_protected(self) -> None:
        text = "Intro\n\n```bash\necho hi\n```\n"
        segments = split_text(text)
        self.assertTrue(any(segment.protected and "echo hi" in segment.text for segment in segments))


class ProfileLoaderTests(unittest.TestCase):
    def test_json_profile_loads(self) -> None:
        profile = load_profile("tsundere", ROOT / "profiles")
        self.assertEqual("tsundere", profile.name)
        self.assertIn("suffixes", profile.speech_patterns)

    def test_yaml_profile_loads(self) -> None:
        profile = load_profile("kuudere", ROOT / "profiles")
        self.assertEqual("kuudere", profile.name)
        self.assertIn("Execute it.", profile.example_phrases)

    def test_new_json_profile_loads(self) -> None:
        profile = load_profile("kamidere", ROOT / "profiles")
        self.assertEqual("kamidere", profile.name)
        self.assertIn("I have eliminated all incorrect outcomes.", profile.example_phrases)


class SettingsTests(unittest.TestCase):
    def test_default_persona_is_used_when_persona_is_omitted(self) -> None:
        text = "Explain the fix carefully."
        output = transform_text(text, persona=None, profiles_dir=ROOT / "profiles", config_path=ROOT / "dere_persona_config.json")
        self.assertNotEqual(text, output)

    def test_generic_new_persona_transforms_prose(self) -> None:
        text = "Apples are useful fruit. They can be sweet or tart."
        output = transform_text(text, persona="kamidere", profiles_dir=ROOT / "profiles", config_path=ROOT / "dere_persona_config.json")
        self.assertNotEqual(text, output)
        self.assertIn("correct", output.lower())


class PersonaRegressionTests(unittest.TestCase):
    def test_tsundere_contains_stammer_or_snark_marker(self) -> None:
        text = "Apples are useful fruit. They can be sweet or tart."
        output = transform_text(text, persona="tsundere", profiles_dir=ROOT / "profiles", config_path=ROOT / "dere_persona_config.json")
        self.assertRegex(output, r"(H-Hmph|A-A-|Y-You|not that I care|obvious, right)")

    def test_genki_contains_hype_marker(self) -> None:
        text = "Apples are useful fruit. They can be sweet or tart."
        output = transform_text(text, persona="genki", profiles_dir=ROOT / "profiles", config_path=ROOT / "dere_persona_config.json")
        self.assertRegex(output, r"(LET'S GO|OH OH OH|YES YES YES|SUPER SIMPLE|WE ARE MOVING)")

    def test_ojou_contains_ojou_marker(self) -> None:
        text = "Apples are useful fruit. They can be sweet or tart."
        output = transform_text(text, persona="ojou", profiles_dir=ROOT / "profiles", config_path=ROOT / "dere_persona_config.json")
        self.assertRegex(output, r"(Ara ara|Ufufu|Naturally|refinement)")

    def test_kamidere_contains_absolute_marker(self) -> None:
        text = "Apples are useful fruit. They can be sweet or tart."
        output = transform_text(text, persona="kamidere", profiles_dir=ROOT / "profiles", config_path=ROOT / "dere_persona_config.json")
        self.assertRegex(output, r"(only correct|optimal|valid solution|debate is unnecessary)")

    def test_bakadere_contains_chaos_marker(self) -> None:
        text = "Apples are useful fruit. They can be sweet or tart."
        output = transform_text(text, persona="bakadere", profiles_dir=ROOT / "profiles", config_path=ROOT / "dere_persona_config.json")
        self.assertRegex(output, r"(WAIT WAIT|I THINK IT WORKS|SHOULD NOT HAVE WORKED|FIXED)")

    def test_himedere_contains_praise_marker(self) -> None:
        text = "Apples are useful fruit. They can be sweet or tart."
        output = transform_text(text, persona="himedere", profiles_dir=ROOT / "profiles", config_path=ROOT / "dere_persona_config.json")
        self.assertRegex(output, r"(grateful|standards|recognition|thank me)")

    def test_sadodere_contains_teasing_marker(self) -> None:
        text = "Apples are useful fruit. They can be sweet or tart."
        output = transform_text(text, persona="sadodere", profiles_dir=ROOT / "profiles", config_path=ROOT / "dere_persona_config.json")
        self.assertRegex(output, r"(Adorable|Try to keep up|ruin it|entertaining)")


if __name__ == "__main__":
    unittest.main()
