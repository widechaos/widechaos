import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('activity', Path(__file__).parents[1] / 'scripts/update-activity.py')
activity = importlib.util.module_from_spec(spec)
spec.loader.exec_module(activity)


def calendar(total=3, missing=False, duplicate=False, year=2026):
    first = activity.date(year, 1, 1)
    days = (activity.date(year + 1, 1, 1) - first).days
    cells, tips = [], []
    for i in range(days):
        day = first + activity.timedelta(days=i)
        cells.append(f'<td data-date="{day}" id="day-{i}"></td>')
        count = '3' if i == 0 else 'No'
        if not (missing and i == 1):
            tips.append(f'<tool-tip for="day-{i}">{count} contributions on January 1st.</tool-tip>')
    if duplicate:
        cells.append(cells[0])
    return f'<h2 id="js-contribution-activity-description">{total} contributions in {year}</h2>' + ''.join(cells + tips)


class ActivityTests(unittest.TestCase):
    def test_native_calendar_preserves_zero_days_and_checks_leap_year(self):
        total, days = activity.parse_calendar(calendar(year=2028), 2028)
        self.assertEqual((total, len(days), days[1]['count']), (3, 366, 0))

    def test_partial_or_inconsistent_response_is_rejected(self):
        for html in (calendar(total=4), calendar(missing=True), calendar(duplicate=True), calendar(year=2025)):
            with self.subTest(html=html[:80]), self.assertRaises(ValueError):
                activity.parse_calendar(html, 2026)

    def test_render_names_the_metric_and_escapes_no_remote_content(self):
        total, days = activity.parse_calendar(calendar(), 2026)
        svg = activity.render({'year': 2026, 'total': total, 'days': days, 'updated_on': '2026-11-03'}, False)
        self.assertIn('not a commit total', svg)
        self.assertEqual(svg.count('<rect '), 365)
        self.assertNotIn('https://', svg)

if __name__ == '__main__':
    unittest.main()
