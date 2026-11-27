# PwC Call Centre Trends Dashboard with Claude

![Project Cover](https://github.com/datawithdickson/call_centre_trends/blob/main/pexels-kampus-8204317.jpg)

## Overview
An interactive one-page dashboard built using claude AI exploring call volume, customer satisfaction, resolution, abandoned calls, speed of answer and agent metrics. I defined the goal, data cleaning prompts, metrics and design requirements. The analysis code and dashboard were generated with AI assistance (Claude). This is a prototype for demonstration, not a validated business assessment.

## Dataset source
- **Source:** [add dataset name, provider and link]
- **Size:** 5,000 call records, 10 original columns
- **Period:** January to March 2021
- **Fields:** call ID, agent, date, time, topic, answered, resolved, speed of answer, talk duration, satisfaction rating
- **Note:** the data file is not included in this repository.

## Tools & Technologies
- **Python:** pandas (cleaning and metrics), SciPy (significance tests), Matplotlib (charts)
- **HTML, CSS, JavaScript and SVG:** interactive dashboard
- **Claude:** AI assistant used to generate the code

## Dashboard preview
**Link:** [add dashboard preview link]

![Dashboard preview](dashboard_preview.png)

## Key insights
| Metric | Result |
|---|---|
| Total calls | 5,000 |
| Unanswered calls | 946 (18.9%) |
| Resolved, of answered calls | 89.9% |
| Resolved, of all calls | 72.9% |
| CSAT (ratings of 4 or 5) | 49.9% |
| Average rating | 3.40 out of 5 |
| Average speed of answer | 67.5 seconds |
| Average talk time | 224.9 seconds |

- Nearly one call in five was not answered.
- About half of rated calls scored 4 or 5.
- Full operating hours ranged from 499 calls (14:00) to 594 calls (13:00).
- Speed of answer showed no linear relationship with satisfaction (r = 0.00).
- Differences between agents in unanswered rate, resolution, speed of answer and satisfaction were not statistically significant. This does not prove that agents perform equally.

### Assumptions and limits
- A rating of 5 is assumed to be the best.
- Unanswered calls are treated as abandoned; the reason is not recorded.
- "Resolved" is a recorded status. It is not customer-confirmed, and its measurement method is unknown.
- Handling time covers talk time only.
- Many records share timestamps and some agent calls overlap; the cause is unknown.
- Results were not analysed by topic.
- The findings do not show cause.

## DAX measures
The prototype calculates its metrics in JavaScript and Python. The DAX below is an equivalent for rebuilding it in Power BI. **It has not been tested in Power BI.**

It assumes `call_center_clean.csv` (produced by `clean_calls.py`) is loaded as a table named `calls`, with true/false, number and date/time column types.

### KPI measures
```dax
-- Volume
Total Calls = COUNTROWS ( calls )

Answered Calls =
CALCULATE ( [Total Calls], calls[answered] = TRUE () )

Abandoned Calls =
CALCULATE ( [Total Calls], calls[answered] = FALSE () )

Abandoned % = DIVIDE ( [Abandoned Calls], [Total Calls] )

-- Resolution: recorded status
Resolved Calls =
CALCULATE ( [Total Calls], calls[resolved] = TRUE () )

-- Denominator: answered calls
Resolved % (Answered) = DIVIDE ( [Resolved Calls], [Answered Calls] )

-- Denominator: all calls
Resolved % (All Calls) = DIVIDE ( [Resolved Calls], [Total Calls] )

-- Satisfaction
Rated Calls = COUNT ( calls[satisfaction_rating] )

-- CSAT: share of rated calls scoring 4 or 5
CSAT % =
DIVIDE (
    CALCULATE ( [Total Calls], calls[satisfaction_rating] >= 4 ),
    [Rated Calls]
)

Average Rating = AVERAGE ( calls[satisfaction_rating] )

-- Speed and handling (blank values are ignored)
Avg Speed of Answer (s) = AVERAGE ( calls[speed_of_answer_sec] )

Avg Talk Time (s) = AVERAGE ( calls[talk_duration_sec] )

Avg Handling Time (m:ss) =
VAR s = ROUND ( [Avg Talk Time (s)], 0 )
RETURN
    IF (
        NOT ISBLANK ( s ),
        INT ( s / 60 ) & ":" & FORMAT ( MOD ( s, 60 ), "00" )
    )

Last Call Received = MAX ( calls[call_received_at] )
```

### Other calculations
```dax
-- Filter to answered calls: DAX treats a blank as 0 in this comparison
Answered Within 20s % =
DIVIDE (
    CALCULATE (
        [Total Calls],
        calls[answered] = TRUE (),
        calls[speed_of_answer_sec] <= 20
    ),
    [Answered Calls]
)

Median Speed of Answer (s) = MEDIAN ( calls[speed_of_answer_sec] )

P90 Speed of Answer (s) = PERCENTILE.INC ( calls[speed_of_answer_sec], 0.9 )

-- Exclude blanks so unrated calls are not counted as low ratings
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

### Calculated columns for charts and slicers
```dax
Call Hour = HOUR ( calls[call_received_at] )

Month Name = FORMAT ( calls[call_received_at], "MMMM" )

Month Number = MONTH ( calls[call_received_at] )      -- sort Month Name by this

Weekday Name = FORMAT ( calls[call_received_at], "dddd" )

Weekday Number = WEEKDAY ( calls[call_received_at], 2 )  -- Monday = 1
```

## Project files
| File | Purpose |
|---|---|
| `README.md` | Project description |
| `profile_data.py` | Data quality profile |
| `clean_calls.py` | Data cleaning and flags |
| `verify.py` | Recalculates reported figures from the original data |
| `eda_charts.py` | Exploratory charts |
| `dashboard_preview.png` | Screenshot with neutral branding and anonymized agents |

To run: install `pandas pyarrow scipy matplotlib`, place `01_Call-Center-Dataset.csv` in the project folder, create `out` and `eda` folders, then run the scripts in the order listed.

## Conclusion
This prototype shows how AI assistance can turn defined requirements into an interactive call centre dashboard. It points to unanswered calls and satisfaction ratings as areas to investigate. Before any business use, the metric definitions, data quality and results need independent validation. The next step is to rebuild and test the measures in Power BI.
