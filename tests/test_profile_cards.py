"""Verify contribution attribution and preservation on upstream failures."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('cards', Path(__file__).resolve().parents[1] / 'scripts/update-profile-cards.py')
cards = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cards)


class CardSyncTests(unittest.TestCase):
    def test_merge_closure_reopen_and_draft(self):
        for payload, expected in [
            ({'state': 'closed', 'merged': True}, 'Merged'),
            ({'state': 'closed', 'merged': False}, 'Closed · unmerged'),
            ({'state': 'open', 'merged': False}, 'Under review'),
            ({'state': 'open', 'draft': True}, 'Draft'),
        ]:
            with self.subTest(payload=payload):
                self.assertEqual(cards.pr_status(payload), expected)

    def test_only_exact_pr_label_changes(self):
        url = 'https://github.com/owner/repo/pull/12'
        projects = [{'evidence': [{'url': url, 'status': 'Merged', 'live_pr': True}]}]
        text = f'| **Under review** | **[Title]({url})**<br>My description. |\n'
        text += f'**Under review** · [#12]({url})<br>**Resolved report** · [#13](https://github.com/owner/repo/issues/13)\n'
        text += '**Under review** · [#120](https://github.com/owner/repo/pull/120)\n'
        after = cards.sync_status_text(text, projects)
        self.assertEqual(after, text.replace('**Under review**', '**Merged**', 2))

    def test_other_authors_are_rejected(self):
        project = {'repo': 'owner/repo', 'evidence': [{'url': 'https://github.com/owner/repo/pull/12'}]}
        with patch.object(cards, 'api', side_effect=[
            {'private': False, 'stargazers_count': 3},
            {'user': {'login': 'someone-else'}, 'state': 'closed', 'merged': True},
        ]):
            with self.assertRaisesRegex(ValueError, 'author'):
                cards.get_metadata(project)

    def test_api_failure_keeps_last_good_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            projects = root / 'contributions/projects'
            projects.mkdir(parents=True)
            record = '# Example\n[Upstream repository](https://github.com/owner/repo)\n| **Under review** | [Patch](https://github.com/owner/repo/pull/12) |\n'
            (projects / 'example.md').write_text(record)
            (root / 'profile-card-captions.json').write_text('{}')
            out = root / 'assets/profile/contributions'
            out.mkdir(parents=True)
            (out / 'example-light.svg').write_text('last good image')
            before = {p.relative_to(root): p.read_bytes() for p in root.rglob('*') if p.is_file()}
            with patch.object(cards, 'ROOT', root), patch.object(cards, 'OUT', out), patch.object(cards, 'api', side_effect=RuntimeError('upstream unavailable')):
                with self.assertRaises(RuntimeError):
                    cards.main()
            after = {p.relative_to(root): p.read_bytes() for p in root.rglob('*') if p.is_file()}
            self.assertEqual(before, after)


if __name__ == '__main__':
    unittest.main()
