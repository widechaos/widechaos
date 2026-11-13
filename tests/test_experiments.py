"""The front shelf stays bounded while every stable work and evidence remains available."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('experiments', Path(__file__).resolve().parents[1] / 'scripts/update-experiments.py')
experiments = importlib.util.module_from_spec(spec)
spec.loader.exec_module(experiments)


class ExperimentTests(unittest.TestCase):
    def test_duplicate_work_or_target_is_rejected(self):
        items = json.loads((experiments.ROOT / 'experiments.json').read_text())['items']
        with self.assertRaises(ValueError):
            experiments.validate(items + [dict(items[-1])])
        with self.assertRaises(ValueError):
            experiments.validate(items + [dict(items[-1], id='new-version')])

    def test_invalid_front_shelf_is_rejected(self):
        data = json.loads((experiments.ROOT / 'experiments.json').read_text())
        for keys in [[], ['missing'], ['router'] * 2, [i['id'] for i in data['items'][:4]]]:
            with self.assertRaises(ValueError):
                experiments.featured_items(dict(data, showcase={'featured': keys}), data['items'])

    def test_new_work_and_revision_do_not_grow_front_shelf_or_lose_evidence(self):
        data = json.loads((experiments.ROOT / 'experiments.json').read_text())
        original = data['items']
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'assets/experiments').mkdir(parents=True)
            legacy = root / 'assets/experiments/preserved-source.svg'
            legacy.write_text('untouched source')
            (root / 'README.md').write_text('before\n' + experiments.START + '\nold\n' + experiments.END + '\nafter')
            catalog = root / 'experiments.json'
            catalog.write_text(json.dumps(data))
            with patch.object(experiments, 'ROOT', root):
                experiments.main()
                first = (root / 'README.md').read_text()
                experiments.main()
                self.assertEqual(first, (root / 'README.md').read_text())
                added = dict(original[-1], id='new-public-work', name='New public work', href='https://example.org/work', details='Retained new evidence.')
                data['items'].append(added)
                data['items'][-2]['details'] += ' Same-work revision.'
                catalog.write_text(json.dumps(data))
                experiments.main()
                updated = (root / 'README.md').read_text()
            self.assertEqual(updated.count('<picture>'), 3)
            front = updated.split('<details>')[0]
            self.assertNotIn(added['href'], front)
            self.assertIn('[New public work](https://example.org/work)', updated)
            self.assertIn('Retained new evidence.', updated)
            self.assertIn('Same-work revision.', updated)
            self.assertTrue(updated.startswith('before\n'))
            self.assertTrue(updated.endswith('\nafter'))
            for item in original:
                self.assertIn(item['details'], updated)
            self.assertEqual(legacy.read_text(), 'untouched source')
            self.assertEqual(len(list((root / 'assets/experiments').glob('shelf-*.svg'))), 12)


if __name__ == '__main__':
    unittest.main()
