"""Protect same-work updates and the approved legacy artwork during daily refreshes."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location(
    "experiments", Path(__file__).resolve().parents[1] / "scripts/update-experiments.py"
)
experiments = importlib.util.module_from_spec(spec)
spec.loader.exec_module(experiments)


class ExperimentTests(unittest.TestCase):
    def test_duplicate_work_or_target_is_rejected(self):
        items = json.loads((experiments.ROOT / "experiments.json").read_text())["items"]
        with self.assertRaises(ValueError):
            experiments.validate(items + [dict(items[-1])])
        duplicate = dict(items[-1], id="new-version")
        with self.assertRaises(ValueError):
            experiments.validate(items + [duplicate])

    def test_same_work_revision_preserves_legacy_and_other_sections(self):
        items = json.loads((experiments.ROOT / "experiments.json").read_text())["items"]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / "assets/experiments"
            folder.mkdir(parents=True)
            old = {}
            for item in items[:2]:
                for path in item["legacy_assets"].values():
                    old[path] = (experiments.ROOT / path).read_bytes()
                    (root / path).write_bytes(old[path])
            source = "other-section-before\n" + experiments.START + "\nold\n" + experiments.END + "\nother-section-after"
            (root / "README.md").write_text(source)
            catalog = root / "experiments.json"
            catalog.write_text(json.dumps({"items": items}))
            with patch.object(experiments, "ROOT", root):
                experiments.main()
                first = (root / "README.md").read_text()
                experiments.main()
                self.assertEqual(first, (root / "README.md").read_text())
                items[-1]["headline"] = "Updated same-work evidence."
                catalog.write_text(json.dumps({"items": items}))
                experiments.main()
                updated = (root / "README.md").read_text()
            self.assertEqual(updated.count('<a href="' + items[-1]["href"] + '"><picture>'), 1)
            self.assertTrue(updated.startswith("other-section-before\n"))
            self.assertTrue(updated.endswith("\nother-section-after"))
            for path, data in old.items():
                self.assertEqual((root / path).read_bytes(), data)
            self.assertEqual(len(list(folder.glob("tiny-hash-intent-*.svg"))), 4)


if __name__ == "__main__":
    unittest.main()
