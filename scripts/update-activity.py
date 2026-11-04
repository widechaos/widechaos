"""Render official annual contributions and calendar-derived activity metrics."""
from datetime import date, datetime, timedelta
from html import escape
from pathlib import Path
from zoneinfo import ZoneInfo
import argparse
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/profile/activity'
START, END = '<!-- GITHUB-ACTIVITY:START -->', '<!-- GITHUB-ACTIVITY:END -->'
MONO = 'SFMono-Regular,Consolas,Liberation Mono,monospace'
SANS = 'Avenir Next,Segoe UI,Arial,sans-serif'
LEVELS = ['NONE', 'FIRST_QUARTILE', 'SECOND_QUARTILE', 'THIRD_QUARTILE', 'FOURTH_QUARTILE']


def parse_snapshot(response, year, updated_on):
    if response.get('errors'):
        raise ValueError('GitHub returned GraphQL errors')
    collection = response['data']['user']['contributionsCollection']
    if collection['startedAt'][:10] != f'{year}-01-01' or collection['endedAt'][:10] != f'{year}-12-31':
        raise ValueError('Wrong annual contribution interval')
    calendar = collection['contributionCalendar']
    total = calendar['totalContributions']
    if type(total) is not int or total < 0:
        raise ValueError('Invalid annual contribution total')
    days = []
    for week in calendar['weeks']:
        for day in week['contributionDays']:
            d = date.fromisoformat(day['date'])
            if d.year == year:
                count = day['contributionCount']
                if type(count) is not int or count < 0:
                    raise ValueError('Invalid daily contribution count')
                level=day['contributionLevel']
                if level not in LEVELS or (count==0)!=(level=='NONE'):
                    raise ValueError('Invalid official contribution level')
                days.append({'date':d.isoformat(),'count':count,'level':LEVELS.index(level)})
    days.sort(key=lambda d: d['date'])
    expected = [str(date(year, 1, 1) + timedelta(days=i))
                for i in range((date(year + 1, 1, 1) - date(year, 1, 1)).days)]
    if [d['date'] for d in days] != expected or sum(d['count'] for d in days) != total:
        raise ValueError('Incomplete calendar or annual/daily count mismatch')
    return {'year':year,'total':total,'updated_on':updated_on,
            'source':'https://api.github.com/graphql','days':days}


def fetch_snapshot(year):
    query = '''query { user(login:"widechaos") { contributionsCollection(
      from:"%s-01-01T00:00:00Z", to:"%s-12-31T23:59:59Z") {
      startedAt endedAt
      contributionCalendar { totalContributions weeks { contributionDays { date contributionCount contributionLevel } } }
    } } }''' % (year, year)
    # Existing gh authentication locally; existing repository token in Actions.
    # Only aggregate counts are requested; no repository details or credentials are output.
    result = subprocess.run(['gh', 'api', 'graphql', '-f', 'query=' + query],
                            capture_output=True, text=True, check=True, timeout=45)
    return json.loads(result.stdout)


def activity_metrics(data):
    first=date(data['year'],1,1)
    as_of=min(max(date.fromisoformat(data['updated_on']),first),date(data['year'],12,31))
    start=max(first,as_of-timedelta(days=29))
    elapsed=(as_of-start).days+1
    run=longest=recent=recent_active=0
    for day in data['days']:
        d=date.fromisoformat(day['date'])
        if d>as_of:
            continue
        if day['count']>0:
            run+=1
            longest=max(longest,run)
        else:
            run=0
        if d>=start:
            recent+=day['count']
            recent_active+=int(day['count']>0)
    return {f'Last {elapsed} {"day" if elapsed==1 else "days"}':recent,
            'Active days':f'{recent_active}/{elapsed}','Longest streak':longest},str(start),str(as_of)


def render(data,dark,mobile=False):
    year,total=data['year'],data['total']
    metrics,start,as_of=activity_metrics(data)
    width,height=(320,310) if mobile else (640,282)
    ink,muted,border=('#e6edf3','#aab5c4','#424a62') if dark else ('#1f2328','#566174','#d7dbe8')
    accent='#b69aff' if dark else '#7541c8'
    palette=['#252d3c','#17484b','#17696d','#20979b','#50d4ca'] if dark else ['#edf0f5','#c8efeb','#83d7d0','#3cb3ae','#087e8b']
    pad=18 if mobile else 28
    grid_x,grid_y,step=(28,204,4.95) if mobile else (32,162,10.8)
    first=date(year,1,1)
    origin=first-timedelta(days=(first.weekday()+1)%7)
    desc=f'{total:,} total GitHub contributions in {year}; not a commit total. '+ '; '.join(f'{k}: {v:,}' if isinstance(v,int) else f'{k}: {v}' for k,v in metrics.items())+f'. Longest streak is measured in consecutive days. Recent contributions and active-day fraction cover {start} through {as_of}, inclusive. Metrics derive from the same official calendar; colors use GitHub contribution levels.'
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
         f'<title id="title">{escape(desc)}</title><desc id="desc">Official GitHub snapshot, {data["updated_on"]}.</desc>',
         f'<path d="M10 .5H{width-10.5}L{width-.5} 10V{height-11}L{width-11} {height-.5}H.5V10Z" fill="none" stroke="{border}"/>',
         f'<path d="M{pad} 22h20" stroke="{accent}" stroke-width="2"/>']
    def text(x,y,value,size=12,color=muted,font=SANS,weight=400):
        return f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(str(value))}</text>'
    svg+=[text(pad+28,26,f'{year} / GITHUB ACTIVITY',10 if mobile else 12,accent,MONO),
          text(pad,78 if mobile else 88,f'{total:,}',40 if mobile else 44,ink,MONO,700),
          text(pad,101 if mobile else 111,'Total contributions',12)]
    for i,(label,value) in enumerate(metrics.items()):
        x=pad+i*(width-2*pad)/3 if mobile else 234+i*128
        y=138 if mobile else 86
        number=f'{value:,}' if isinstance(value,int) else value
        color=('#50d4ca' if dark else '#087e8b') if label.startswith('Last ') else ink
        svg.append(text(round(x,2),y,number,23 if mobile else 26,color,MONO,600))
        if label=='Longest streak':
            unit_x=x+len(str(value))*(13.8 if mobile else 15.6)+5
            svg.append(text(round(unit_x,2),y,'days',9 if mobile else 10))
        caption=f'Active days · {(date.fromisoformat(as_of)-date.fromisoformat(start)).days+1}d' if label=='Active days' else label
        svg.append(text(round(x,2),159 if mobile else 111,caption,10.5 if mobile else 11))
    svg.append(f'<path d="M{pad} {176 if mobile else 130}H{width-pad}" stroke="{border}"/>')
    for month in range(1,13):
        if mobile and month%2==0:
            continue
        day=date(year,month,1)
        x=grid_x+((day-origin).days//7)*step
        svg.append(text(round(x,2),193 if mobile else 151,day.strftime('%b'),8.5 if mobile else 10))
    for day in data['days']:
        d=date.fromisoformat(day['date']);offset=(d-origin).days
        opacity=' opacity=".35"' if day['date']>as_of else ''
        svg.append(f'<rect x="{grid_x+offset//7*step:.2f}" y="{grid_y+offset%7*step:.2f}" width="{step-(1 if mobile else 2):.2f}" height="{step-(1 if mobile else 2):.2f}" rx="1" fill="{palette[day["level"]]}"{opacity}><title>{day["date"]}: {day["count"]} contributions</title></rect>')
    legend_x=166 if mobile else 480
    legend_y=260 if mobile else 261
    svg.append(text(legend_x,legend_y,'Less',9))
    for i,color in enumerate(palette):
        svg.append(f'<rect x="{legend_x+26+i*10}" y="{legend_y-7}" width="7" height="7" rx="1" fill="{color}"/>')
    svg.append(text(legend_x+80,legend_y,'More',9))
    svg.append(text(pad,291 if mobile else 263,f'Updated {data["updated_on"]}',9.5,muted,MONO))
    svg.append('</svg>')
    return '\n'.join(svg)+'\n'


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--snapshot', type=Path, help='Render a saved official response for review')
    args=parser.parse_args()
    readme=(ROOT/'README.md').read_text()
    if START not in readme and END not in readme:
        print('Custom activity card retired; the native GitHub calendar is retained.')
        return
    now=datetime.now(ZoneInfo('Asia/Muscat'))
    response=json.loads(args.snapshot.read_text()) if args.snapshot else fetch_snapshot(now.year)
    data=parse_snapshot(response,now.year,now.date().isoformat())
    readme=(ROOT/'README.md').read_text()
    if readme.count(START)!=1 or readme.count(END)!=1 or readme.index(START)>readme.index(END):
        raise ValueError('Invalid activity boundaries')
    assets, names={},{}
    for mobile in (False,True):
        for theme in ('light','dark'):
            svg=render(data,theme=='dark',mobile)
            name=f'calendar-{theme}{"-mobile" if mobile else ""}-{hashlib.sha256(svg.encode()).hexdigest()[:12]}.svg'
            assets[name]=svg;names[(theme,mobile)]=name
    prefix='assets/profile/activity/'
    link=f'https://github.com/widechaos?tab=overview&amp;from={now.year}-01-01&amp;to={now.year}-12-31'
    block=f'\n<p><a href="{link}"><picture>'
    for theme,mobile,media in [('dark',True,'(prefers-color-scheme: dark) and (max-width:520px)'),('light',True,'(max-width:520px)'),('dark',False,'(prefers-color-scheme: dark)')]:
        block+=f'<source media="{media}" srcset="{prefix+names[(theme,mobile)]}">'
    metrics,start,as_of=activity_metrics(data)
    alt=f'{now.year}: {data["total"]:,} total GitHub contributions; '+', '.join(f'{k} {v:,}' if isinstance(v,int) else f'{k} {v}' for k,v in metrics.items())+f'. Calendar-derived metrics; longest streak in days, recent interval {start} through {as_of}.'

    block+=f'<img src="{prefix+names[("light",False)]}" width="640" alt="{escape(alt)}"></picture></a></p>\n'
    updated=readme[:readme.index(START)+len(START)]+block+readme[readme.index(END):]
    # All remote data and boundaries are validated before touching current output.
    OUT.mkdir(parents=True,exist_ok=True)
    for name,svg in assets.items(): (OUT/name).write_text(svg)
    (OUT/'calendar.json').write_text(json.dumps(data,indent=2)+'\n')
    (ROOT/'README.md').write_text(updated)
    for old in OUT.glob('calendar-*.svg'):
        if old.name not in assets: old.unlink()
    print(f'{now.year}: {data["total"]:,} contributions; {metrics}; recent interval {start} to {as_of}.')


if __name__=='__main__': main()
