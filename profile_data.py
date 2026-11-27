"""Reproduces the data profile checks (read-only)."""
import pandas as pd
raw = pd.read_csv('01_Call-Center-Dataset.csv', dtype=str, keep_default_na=False)
d = pd.read_csv('01_Call-Center-Dataset.csv')
print('shape', raw.shape); print(d.dtypes)
words = {'n/a','na','none','null','nan','not specified','unknown','-','--','?','blank','missing','not available','nil','tbd','#n/a'}
for c in raw:
    s = raw[c]
    print(f"{c:28} empty={(s=='').sum()} placeholders={s.str.strip().str.lower().isin(words).sum()} padded={(s!=s.str.strip()).sum()}")
print('duplicate rows', raw.duplicated().sum(), '| duplicate ids', raw['call id'].duplicated().sum())
ts = pd.to_datetime(d.date + ' ' + d.time, format='%m/%d/%Y %H:%M:%S')
print('shared timestamp rows', ts.duplicated(keep=False).sum())
x = d.assign(t=ts, end=ts + pd.to_timedelta(d.avgtalkduration, unit='s'))
x = x[x['answered (Y/N)'] == 'Y'].sort_values(['agent', 't'])
# Profile method: time = call start, compared with the previous call only
print('overlaps, profile method', (x.t < x.groupby('agent').end.shift()).sum())
