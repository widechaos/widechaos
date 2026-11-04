import importlib.util
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

spec=importlib.util.spec_from_file_location('activity',Path(__file__).parents[1]/'scripts/update-activity.py')
activity=importlib.util.module_from_spec(spec);spec.loader.exec_module(activity)


def snapshot(year=2026):
    first=activity.date(year,1,1)
    days=(activity.date(year+1,1,1)-first).days
    calendar=[{'date':str(first+activity.timedelta(days=i)),
               'contributionCount':10 if i==0 else 0,
               'contributionLevel':'FIRST_QUARTILE' if i==0 else 'NONE'} for i in range(days)]
    return {'data':{'user':{'contributionsCollection':{
        'startedAt':f'{year}-01-01T00:00:00Z','endedAt':f'{year}-12-31T23:59:59Z',
        'contributionCalendar':{'totalContributions':10,'weeks':[{'contributionDays':calendar}]}
    }}}}


class ActivityTests(unittest.TestCase):
    def test_retired_card_does_not_fetch_or_rewrite_the_profile(self):
        import tempfile
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            readme=root/'README.md'
            readme.write_text('# Selected work\n')
            with patch.object(activity, 'ROOT', root), patch.object(activity, 'fetch_snapshot') as fetch, patch('sys.argv', ['update-activity.py']):
                activity.main()
            fetch.assert_not_called()
            self.assertEqual(readme.read_text(), '# Selected work\n')
            self.assertFalse((root/'assets').exists())

    def test_snapshot_preserves_leap_days_and_official_color_levels(self):
        data=activity.parse_snapshot(snapshot(2028),2028,'2028-12-31')
        self.assertEqual(len(data['days']),366)
        self.assertEqual(data['days'][0]['level'],1)
        self.assertEqual(data['days'][1]['level'],0)
        metrics,start,end=activity.activity_metrics(data)
        self.assertEqual(metrics,{'Last 30 days':0,'Active days':'0/30','Longest streak':1})
        self.assertEqual((start,end),('2028-12-02','2028-12-31'))

    def test_rejects_inconsistent_partial_or_wrong_year_data(self):
        bad=[]
        r=snapshot();r['errors']=[{'message':'partial failure'}];bad.append(r)
        r=snapshot();r['data']['user']['contributionsCollection']['contributionCalendar']['totalContributions']=9;bad.append(r)
        r=snapshot();r['data']['user']['contributionsCollection']['contributionCalendar']['weeks'][0]['contributionDays'].pop();bad.append(r)
        r=snapshot();r['data']['user']['contributionsCollection']['contributionCalendar']['weeks'][0]['contributionDays'][1]['date']='2026-01-01';bad.append(r)
        r=snapshot();r['data']['user']['contributionsCollection']['contributionCalendar']['weeks'][0]['contributionDays'][0]['contributionLevel']='NONE';bad.append(r)
        r=snapshot();r['data']['user']['contributionsCollection']['contributionCalendar']['weeks'][0]['contributionDays'][1]['contributionCount']=-1;bad.append(r)
        bad.append(snapshot(2025))
        for response in bad:
            with self.subTest(response=str(response)[:100]),self.assertRaises(ValueError):
                activity.parse_snapshot(response,2026,'2026-11-03')

    def test_recent_window_is_inclusive_and_early_year_is_labeled_honestly(self):
        days=[{'date':str(activity.date(2026,1,1)+activity.timedelta(days=i)),
               'count':100 if i==0 else 5 if i==1 else 7 if i==30 else 0} for i in range(31)]
        data={'year':2026,'updated_on':'2026-01-31','days':days,'total':112}
        metrics,start,end=activity.activity_metrics(data)
        self.assertEqual(metrics,{'Last 30 days':12,'Active days':'2/30','Longest streak':2})
        self.assertEqual((start,end),('2026-01-02','2026-01-31'))
        data['updated_on']='2026-01-01'
        metrics,start,end=activity.activity_metrics(data)
        self.assertEqual(metrics,{'Last 1 day':100,'Active days':'1/1','Longest streak':1})
        data={'year':2026,'updated_on':'2026-01-01','days':[{'date':'2026-01-01','count':0}]}
        metrics,_,_=activity.activity_metrics(data)
        self.assertEqual(metrics['Active days'],'0/1')
        self.assertEqual(metrics['Longest streak'],0)

    def test_desktop_and_mobile_name_metrics_and_render_full_calendar(self):
        data=activity.parse_snapshot(snapshot(),2026,'2026-11-03')
        for dark in (True,False):
            for mobile in (True,False):
                svg=activity.render(data,dark,mobile)
                root=ET.fromstring(svg)
                self.assertEqual(root.attrib['width'],'320' if mobile else '640')
                self.assertIn('Total contributions',svg)
                self.assertIn('Active days',svg)
                self.assertIn('Longest streak',svg)
                self.assertIn('Last 30 days',svg)
                self.assertNotIn('Per active day',svg)
                self.assertNotIn('Peak day',svg)
                self.assertIn('not a commit total',svg)
                self.assertNotIn('https://',svg)
                self.assertEqual(len(root.findall('.//{http://www.w3.org/2000/svg}rect')),370)


if __name__=='__main__': unittest.main()
