"""Protect artwork provenance and catalog-driven additions during refreshes."""

import base64
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

spec = importlib.util.spec_from_file_location(
    "collection", Path(__file__).resolve().parents[1] / "scripts/update-collection.py"
)
collection = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collection)
card_spec = importlib.util.spec_from_file_location(
    "cards_grid",
    Path(__file__).resolve().parents[1] / "scripts/update-profile-cards.py",
)
cards = importlib.util.module_from_spec(card_spec)
card_spec.loader.exec_module(cards)


class CollectionTests(unittest.TestCase):
    def test_original_artwork_and_reduced_motion_survive_every_frame(self):
        payload = (
            b'<svg xmlns="http://www.w3.org/2000/svg"><text>Original 40</text></svg>'
        )
        uri = "data:image/svg+xml;base64," + base64.b64encode(payload).decode()
        for kind in range(3):
            for theme in ("light", "dark"):
                with self.subTest(kind=kind, theme=theme):
                    svg = collection.render(
                        "verified-source", "Owner credential", kind, uri, theme
                    )
                    root = ET.fromstring(svg)
                    embedded = root.find("{http://www.w3.org/2000/svg}image").get(
                        "href"
                    )
                    self.assertEqual(base64.b64decode(embedded.split(",")[1]), payload)
                    self.assertIn("prefers-reduced-motion", svg)

    def test_catalog_addition_inherits_frames_and_original_links(self):
        uri = "data:image/svg+xml;base64," + base64.b64encode(b"<svg/>").decode()
        item = dict(
            src="new-official-image",
            alt="New verified badge",
            link="https://example.com/owner/credential",
            kind=1,
        )
        with patch.object(collection, "artwork", return_value=uri):
            assets, block = collection.generate([[], [item], [], []])
        self.assertEqual(len(assets), 2)
        self.assertIn(item["link"], block)
        self.assertIn("prefers-color-scheme: dark", block)
        self.assertTrue(all("soft-reflection" in svg for svg in assets.values()))

    def test_fetch_failure_does_not_replace_readme(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            before = (
                "before\n" + collection.START + "\nold\n" + collection.END + "\nafter"
            )
            (root / "README.md").write_text(before)
            with (
                patch.object(collection, "ROOT", root),
                patch.object(collection, "collect", return_value=[]),
                patch.object(collection, "generate", side_effect=OSError("offline")),
            ):
                with self.assertRaises(OSError):
                    collection.main()
            self.assertEqual((root / "README.md").read_text(), before)

    def test_new_projects_flow_without_fixed_row_breaks(self):
        start = "<!-- OPEN-SOURCE-CONTRIBUTIONS:START -->"
        end = "<!-- OPEN-SOURCE-CONTRIBUTIONS:END -->"
        before = (
            "preserved-before"
            + start
            + '<a href="contributions/projects/old.md"></a><br>'
            + end
            + "preserved-after"
        )
        projects = [
            dict(slug=s, name=s.title(), caption="Verified work", evidence=[dict(status="Merged", sort_date="2026-10-14T00:00:00Z" if s == "new" else "2026-10-13T00:00:00Z", url="https://github.com/o/r/pull/1")])
            for s in ("new", "old")
        ]
        after = cards.sync_grid(before, projects)
        self.assertTrue(after.startswith("preserved-before"))
        self.assertTrue(after.endswith("preserved-after"))
        self.assertLess(after.index("projects/new.md"), after.index("projects/old.md"))
        self.assertNotIn("<br>", after)
        self.assertIn('width="300"', after)


if __name__ == "__main__":
    unittest.main()
