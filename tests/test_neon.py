import importlib.util
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

spec = importlib.util.spec_from_file_location('neon_cards', Path(__file__).resolve().parents[1] / 'scripts/update-profile-cards.py')
cards = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cards)
from profile_neon import apply_neon


class NeonTests(unittest.TestCase):
    def test_light_surface_is_idempotent_and_keeps_content(self):
        source='<svg xmlns="http://www.w3.org/2000/svg" width="205" height="48" viewBox="0 0 205 48"><title>Contact</title><path d="M1 1H204V47H1Z"/><text x="12" y="30">Blog</text></svg>'
        once=apply_neon(source, 'light')
        self.assertEqual(once, apply_neon(once, 'light'))
        self.assertIn('<title>Contact</title>', once)
        self.assertIn('viewBox="-3 -3 212 55"', once)
        section=apply_neon(source, 'dark', 'section')
        self.assertNotIn('<g filter=', section)
        self.assertIn('<path filter=', section)
        ET.fromstring(section)

    def test_extra_records_are_not_total_or_merged_count(self):
        for count in (1, 2, 6, 101):
            statuses=['Merged #1'] + ['Under review #'+str(i) for i in range(2,count+1)]
            for theme in ('light','dark'):
                svg=cards.render(dict(slug='sample',name='Sample',stars=123,caption='Public contribution records',statuses=statuses),theme)
                ET.fromstring(svg)
                if count>1:
                    self.assertIn(f'{count-1} additional contribution records',svg)
                    self.assertIn('>'+str('+'+str(count-1))+'</text>',svg)
                    self.assertIn('prefers-reduced-motion:reduce',svg)
                    self.assertNotIn('repeatCount="indefinite"',svg)
                else:
                    self.assertNotIn('class="combo-hit"',svg)
                self.assertIn('; '.join(statuses),svg)
                self.assertIn('Details ↗',svg)
