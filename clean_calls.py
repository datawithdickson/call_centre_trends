import pandas as pd, numpy as np

src = pd.read_csv('01_Call-Center-Dataset.csv')
d = src.rename(columns={
    'call id': 'call_id', 'date': 'call_date', 'time': 'call_time',
    'answered (Y/N)': 'answered', 'speed of answer in seconds': 'speed_of_answer_sec',
    'avgtalkduration': 'talk_duration_sec', 'satisfaction rating': 'satisfaction_rating'})

# Types: call_time is when the call was received
received = pd.to_datetime(d.call_date + ' ' + d.call_time, format='%m/%d/%Y %H:%M:%S')
d['call_date'], d['call_time'] = received.dt.date, received.dt.time
for c in ['answered', 'resolved']:
    assert set(d[c]) == {'Y', 'N'}
    d[c] = d[c].map({'Y': True, 'N': False}).astype('boolean')
for c in ['speed_of_answer_sec', 'talk_duration_sec', 'satisfaction_rating']:
    d[c] = d[c].astype('Int64')                      # blanks stay null
d.loc[~d.answered, 'talk_duration_sec'] = pd.NA      # unanswered: no talk time
d['call_received_at'] = received

# Flag 1 and 2: shared timestamps (all calls / same agent)
d['flag_shared_timestamp'] = received.duplicated(keep=False)
d['flag_agent_shared_timestamp'] = d.duplicated(['agent', 'call_received_at'], keep=False)

# Flag 3: handling interval = [received + answer delay, + talk), answered calls only
a = d[d.answered]
start = a.call_received_at + pd.to_timedelta(a.speed_of_answer_sec.astype(int), unit='s')
iv = pd.DataFrame({'agent': a.agent, 's': start,
                   'e': start + pd.to_timedelta(a.talk_duration_sec.astype(int), unit='s')})
d['flag_overlap'] = False
for _, g in iv.sort_values(['agent', 's', 'e']).groupby('agent'):
    prev_end = g.e.cummax().shift()                  # latest end among earlier calls
    next_start = g.s.shift(-1)
    hit = (g.s < prev_end) | (next_start < g.e)      # mark both sides of an overlap
    d.loc[g.index, 'flag_overlap'] = hit

d.to_csv('out/call_center_clean.csv', index=False,
         date_format='%Y-%m-%d %H:%M:%S')
d.to_parquet('out/call_center_clean.parquet', index=False)

# ---- verification ----
p = pd.read_parquet('out/call_center_clean.parquet')
assert len(p) == len(src) == 5000 and p.call_id.is_unique
assert (p.agent == src.agent).all() and (p.topic == src.topic).all()
assert p.answered.sum() == 4054 and p.resolved.sum() == 3646
for c in ['speed_of_answer_sec', 'talk_duration_sec', 'satisfaction_rating']:
    assert p[c].isna().sum() == 946
assert p.talk_duration_sec.sum() == src.avgtalkduration.sum()
assert p.speed_of_answer_sec.sum() == src['speed of answer in seconds'].sum()
assert p.satisfaction_rating.sum() == src['satisfaction rating'].sum()
for c in ['flag_shared_timestamp', 'flag_agent_shared_timestamp', 'flag_overlap']:
    print(c, int(p[c].sum()))
import pyarrow.parquet as pq
print(pq.read_schema('out/call_center_clean.parquet').to_string(show_schema_metadata=False))
print(open('out/call_center_clean.csv').read(600))
