# Call Center Trends Analysis

![Project Cover](https://github.com/datawithdickson/call_center_trends/blob/main/pexels-kampus-8204317.jpg)

## Overview

**Dataset:** PwC Call Center Trends | **AI assistant:** Claude
An interactive dashboard built with Claude AI exploring call volume, customer satisfaction, resolution, abandoned calls, speed of answer and agent metrics. I defined the goal, Added data cleaning prompts, metrics and design requirements. The analysis code and dashboard were generated with AI assistance (Claude). This is a prototype for demonstration, not a validated business assessment.


## Tools & Technologies

- Claude
- Python
- HTML, CSS, JavaScript and SVG

## Dashboard preview

![PwC Call center Trends Dashboard](https://github.com/datawithdickson/call_center_trends/blob/main/Call_center_Trends_Dashboard.png)

## Key insights

| Metric | Result |
|---|---|
| Total calls | 5,000 |
| Unanswered calls | 946 (18.9%) |
| Resolution rate for answered calls | 89.9% |
| Resolution rate for all incoming calls | 72.9% |
| CSAT (ratings of 4 or 5) | 49.9% |
| Average rating | 3.40 out of 5 |
| Average speed of answer | 67.5 seconds |
| Average talk time | 224.9 seconds |

- Nearly one call in five was not answered.
- About half of rated calls scored 4 or 5.
- Full operating hours ranged from 499 calls (14:00) to 594 calls (13:00).
- Speed of answer showed no linear relationship with satisfaction.
- Differences between agents in unanswered rate, resolution, speed of answer and satisfaction were not statistically significant.

## DAX measures

### Call Volume
```dax
Total Calls = COUNTROWS ( calls )
```

### Answered Calls
```dax
Answered Calls =
CALCULATE ( [Total Calls], calls[answered] = TRUE () )
```

### Abandoned Calls
```dax
Abandoned Calls =
CALCULATE ( [Total Calls], calls[answered] = FALSE () )
```

### Calls Abandoned %
```dax
Abandoned % =
DIVIDE ( [Abandoned Calls], [Total Calls] )
```

### Resolved Calls
```dax
Resolved Calls =
CALCULATE ( [Total Calls], calls[resolved] = TRUE () )
```

### Resolution Rate for Answered Calls
```dax
Resolved % (Answered) =
DIVIDE ( [Resolved Calls], [Answered Calls] )
```

### Resolution Rate for All Calls
```dax
Resolved % (All Calls) =
DIVIDE ( [Resolved Calls], [Total Calls] )
```

### Rated Calls
```dax
Rated Calls = COUNT ( calls[satisfaction_rating] )
```

### Customer Satisfaction (CSAT)
```dax
-- Share of rated calls scoring 4 or 5
CSAT % =
DIVIDE (
    CALCULATE ( [Total Calls], calls[satisfaction_rating] >= 4 ),
    [Rated Calls]
)
```

### Average Satisfaction Rating
```dax
Average Rating = AVERAGE ( calls[satisfaction_rating] )
```

### Low Satisfaction Rate
```dax
-- Share of rated calls scoring 1 or 2; unrated calls are excluded
Low Rating % =
DIVIDE (
    CALCULATE (
        [Total Calls],
        FILTER (
            calls,
            NOT ISBLANK ( calls[satisfaction_rating] )
                && calls[satisfaction_rating] <= 2
        )
    ),
    [Rated Calls]
)
```

### Average Speed of Answer
```dax
Avg Speed of Answer (s) = AVERAGE ( calls[speed_of_answer_sec] )
```

### Median Speed of Answer
```dax
Median Speed of Answer (s) = MEDIAN ( calls[speed_of_answer_sec] )
```

### 90th Percentile Speed of Answer
```dax
P90 Speed of Answer (s) =
PERCENTILE.INC ( calls[speed_of_answer_sec], 0.9 )
```

### Calls Answered Within 20 Seconds
```dax
-- The answered filter stops blank values counting as 0 seconds
Answered Within 20s % =
DIVIDE (
    CALCULATE (
        [Total Calls],
        calls[answered] = TRUE (),
        calls[speed_of_answer_sec] <= 20
    ),
    [Answered Calls]
)
```

### Average Talk Time
```dax
Avg Talk Time (s) = AVERAGE ( calls[talk_duration_sec] )
```

### Average Call Handling Time
```dax
-- Talk time only, shown as minutes:seconds
Avg Handling Time (m:ss) =
VAR s = ROUND ( [Avg Talk Time (s)], 0 )
RETURN
    IF (
        NOT ISBLANK ( s ),
        INT ( s / 60 ) & ":" & FORMAT ( MOD ( s, 60 ), "00" )
    )
```

### Last Call Received
```dax
Last Call Received = MAX ( calls[call_received_at] )
```

### Call Hour
```dax
-- Calculated column
Call Hour = HOUR ( calls[call_received_at] )
```

### Month Name
```dax
-- Calculated column; sort by Month Number
Month Name = FORMAT ( calls[call_received_at], "MMMM" )
```

### Month Number
```dax
-- Calculated column
Month Number = MONTH ( calls[call_received_at] )
```

### Weekday Name
```dax
-- Calculated column; sort by Weekday Number
Weekday Name = FORMAT ( calls[call_received_at], "dddd" )
```

### Weekday Number
```dax
-- Calculated column; Monday = 1
Weekday Number = WEEKDAY ( calls[call_received_at], 2 )
```

## Project files
| File | Purpose |
|---|---|
| `README.md` | Project description |
| `profile_data.py` | Data quality profile |
| `clean_calls.py` | Data cleaning |
| `verify.py` | Recalculates reported figures from the original data |
| `eda_charts.py` | Exploratory charts |
| `dashboard_preview.png` | Screenshot of a project dashboard |
| `PROMPTS.txt` | Prompts used in this project |

## Conclusion
This project turned 5,000 call records into a clear view of call center activity. Two areas stand out for further investigation: 18.9% of calls went unanswered, and only 49.9% of rated calls scored 4 or 5. A resolution rate of 89.9% for answered calls does not, on its own, show that customers were satisfied. 

Important thing to note is that, this project shows that AI assistance can speed up analysis and dashboard design, but the results still need human checking. Metric definitions, assumptions and data quality should be confirmed before any business use. The important step is to rebuild the dashboard in Power BI and validate the DAX measures against these results.
