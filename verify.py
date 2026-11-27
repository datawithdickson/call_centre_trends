"""Independent check of reported figures, computed from the ORIGINAL CSV only."""
import pandas as pd
from scipy import stats

d = pd.read_csv('01_Call-Center-Dataset.csv')
d.columns = ['id','agent','date','time','topic','answered','resolved','speed','talk','rating']
d['ts'] = pd.to_datetime(d.date + ' ' + d.time, format='%m/%d/%Y %H:%M:%S')
a = d[d.answered == 'Y']                                   # answered calls

def check(name, got, reported, places=1):
    ok = round(float(got), places) == reported
    print(f"{'OK  ' if ok else 'FAIL'} {name:34} computed={got:.4f}  reported={reported}")

check('Total calls', len(d), 5000, 0)
check('Unanswered calls', (d.answered == 'N').sum(), 946, 0)
check('Unanswered %', (d.answered == 'N').mean()*100, 18.9)
check('Resolved calls', (d.resolved == 'Y').sum(), 3646, 0)
check('Resolved % of answered', (a.resolved == 'Y').mean()*100, 89.9)
check('Resolved % of all calls', (d.resolved == 'Y').mean()*100, 72.9)
check('CSAT % (rating 4 or 5)', (a.rating >= 4).mean()*100, 49.9)
check('Average rating', a.rating.mean(), 3.40, 2)
check('Low ratings % (1 or 2)', (a.rating <= 2).mean()*100, 20.1)
check('Rating 3 %', (a.rating == 3).mean()*100, 30.0)
check('Speed of answer, mean (s)', a.speed.mean(), 67.5)
check('Speed of answer, median (s)', a.speed.median(), 68, 0)
check('Speed of answer, 90th pct (s)', a.speed.quantile(.9), 114, 0)
check('Answered within 20 s %', (a.speed <= 20).mean()*100, 9.2)
check('Average talk time (s)', a.talk.mean(), 224.9)
check('Correlation speed vs rating', a.speed.corr(a.rating), 0.00, 2)
check('Rating, resolved calls', a[a.resolved == 'Y'].rating.mean(), 3.40, 2)
check('Rating, unresolved calls', a[a.resolved == 'N'].rating.mean(), 3.43, 2)

print('\nAgent differences (p-values; above 0.05 = not significant)')
print(' unanswered', stats.chi2_contingency(pd.crosstab(d.agent, d.answered))[1])
print(' resolved  ', stats.chi2_contingency(pd.crosstab(a.agent, a.resolved))[1])
print(' CSAT 4-5  ', stats.chi2_contingency(pd.crosstab(a.agent, a.rating >= 4))[1])
for col in ['speed', 'rating']:
    print(f' {col:10}', stats.kruskal(*[g[col] for _, g in a.groupby('agent')]).pvalue)

print('\nAgent table')
print(pd.DataFrame({
    'total': d.groupby('agent').size(),
    'unanswered': d[d.answered == 'N'].groupby('agent').size(),
    'speed_s': a.groupby('agent').speed.mean(),
    'resolved_pct': a.groupby('agent').resolved.apply(lambda s: (s == 'Y').mean()*100),
    'csat_pct': a.groupby('agent').rating.apply(lambda s: (s >= 4).mean()*100),
    'avg_rating': a.groupby('agent').rating.mean()}).round(2).to_string())

print('\nCalls by hour\n', d.ts.dt.hour.value_counts().sort_index().to_string())
days = d.groupby(d.ts.dt.day_name()).agg(calls=('id','size'), dates=('date','nunique'))
days['per_day'] = days.calls / days.dates
print('\nCalls by weekday\n', days.round(1).to_string())
print('\nLast call received:', d.ts.max())
