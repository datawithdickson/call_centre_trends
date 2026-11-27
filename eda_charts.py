import pandas as pd, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
d=pd.read_parquet('out/call_center_clean.parquet')
BLUE='#2a78d6'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.edgecolor':'#c3c2b7',
 'text.color':'#0b0b0b','xtick.color':'#52514e','ytick.color':'#52514e','axes.labelcolor':'#52514e'})
def finish(fig,ax,title,xl,yl,name,note=None):
    ax.set_title(title,loc='left',fontsize=13.5,fontweight='bold',pad=14)
    ax.set_xlabel(xl,labelpad=8); ax.set_ylabel(yl,labelpad=8)
    ax.spines[['top','right','left']].set_visible(False); ax.tick_params(length=0)
    ax.grid(axis='y',color='#e1e0d9',lw=.8); ax.set_axisbelow(True)
    fig.tight_layout(rect=(0,.05 if note else 0,1,1))
    if note: fig.text(.015,.02,note,fontsize=9,color='#52514e')
    fig.savefig('eda/'+name,dpi=180); plt.close(fig)

s=d.satisfaction_rating.dropna().astype(int).value_counts().sort_index()
fig,ax=plt.subplots(figsize=(9,5))
ax.bar(['1\nVery low','2','3','4','5\nVery high'],s.values,color=BLUE,width=.6)
finish(fig,ax,'3 is the most common rating; half of rated calls score 4 or 5','Satisfaction rating','Rated calls',
 '1_satisfaction_levels.png','4,054 answered calls, Jan-Mar 2021. Scale-end labels assume 5 is best.')

h=d.call_received_at.dt.hour.value_counts().sort_index()
fig,ax=plt.subplots(figsize=(9,5))
ax.plot([f'{i:02d}:00' for i in h.index],h.values,color=BLUE,lw=2,marker='o',ms=8)
ax.set_ylim(0,700)
finish(fig,ax,'Call volume is broadly steady from 09:00 to 17:59','Hour call was received','Total calls',
 '2_volume_by_hour.png','Jan-Mar 2021. The 18:00 point holds only calls stamped exactly 18:00:00, not a full hour.')

order=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
w=d.call_received_at.dt.day_name().value_counts().reindex(order)
fig,ax=plt.subplots(figsize=(9,5))
ax.plot([x[:3] for x in order],w.values,color=BLUE,lw=2,marker='o',ms=8)
ax.set_ylim(0,900)
finish(fig,ax,'Monday and Saturday record the most calls','Day of week','Total calls',
 '3_volume_by_day.png','Jan-Mar 2021. Thursday occurs 12 times, other days 13; its daily average (59) matches Monday and Saturday.')
assert s.sum()==4054 and h.sum()==5000 and w.sum()==5000
