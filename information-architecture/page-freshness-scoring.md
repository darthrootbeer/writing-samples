---
title: Scoring Documentation Pages for Freshness
type: Internal tooling documentation
original_format: PDF (internal wiki page)
---

> **Why this is here.** A wiki with a few thousand pages has no useful signal for
> what to fix first. This scores every page on how recently it was updated and how
> often it gets read, so maintenance goes where it matters instead of where someone
> happens to look. Written for the people who had to run it, not for an audience.

# Using Google Sheets to Calculate Content Freshness

## Overview

Using Confluence data from a custom API script, we can calculate how "fresh" pages are (and why), and recommend action on the page, such as archive or update. Freshness is a magical calculation of article view counts, update recency, and content age.

## Freshness Calculation

The provided Google Sheets formula identifies fresh content by age, number of views, and when the content was last updated. It incorporates these specific metrics into the output messages within the cell for a clear understanding of why content is flagged in a certain way.

This formula provides a nuanced approach to content evaluation, offering specific insights into why content might need updating or further review. By including actual view counts and comparing them to the lifetime average, content managers can make more informed decisions about prioritizing updates or reevaluations based on concrete engagement metrics and update history.

> **TL;DR:** We use cool maths to calculate how fresh pages are.
>
> We do some calculations and output a plain English response with numerical codes. We can use these codes to apply conditional formatting to the Google Sheet for easy visual identification. (Red, yellow, etc.)
>
> Here's how the numbers break down, from highest priority (001) to lowest (005):

| Code | Meaning |
|---|---|
| 001 | Page popularity has gone way down, and it hasn't been updated in a long time. |
| 002 | Page popularity has gone way down. |
| 003 | Page hasn't been updated in a long time, but it's relatively popular. |
| 004 | Page is probably old, but it's popular and being updated. |
| 005 | Too new to consider. |

See Examples below for detailed scenarios.

### Required variables (columns)

This single cell formula requires the following values (columns) to exist in the Google Sheet:

- **ViewCountLastYear**: The number of views the content received in the last year.
- **ViewsPerYear**: The calculated average number of views per year since the content was created. This is derived from `ViewCountAllTime / (DaysSinceCreation / 365)`.
- **DaysSinceCreation**: The total number of days since the content was created.
- **DaysSinceEdited**: The number of days since the content was last updated.

### Formula

Here's the formula in a code block for easy copy-paste:

```
=IF(DaysSinceCreation > 730, IF(AND((ViewCountLastYear / (ViewCountAllTime / (DaysSinceCreation / 365))) < 0.2, DaysSinceEdited > 730), "[001] Last year's views (" & ViewCountLastYear & ") have had a large decline from the lifetime average (" & ViewsPerYear & " per year), and it hasn't been updated in over 2 years.", IF((ViewCountLastYear / (ViewCountAllTime / (DaysSinceCreation / 365))) < 0.2, "[002] Last year's views (" & ViewCountLastYear & ") have had a large decline from the lifetime average (" & ViewsPerYear & " per year).", IF(DaysSinceEdited > 730, "[003] This content hasn't been updated in over 2 years.", "[004] This content does not require urgent updates."))), "[005] Content is less than 2 years old (" & DaysSinceCreation & " days).")
```

How to use this formula:

1. Create a new column in your spreadsheet and name the column "Freshness" (or similar).
2. Copy and paste the formula into the topmost cell.
3. Make the following changes to the formula:
   a. Replace each instance of `ViewCountLastYear` with the same row's cell number in the ViewCountLastYear column.
   b. Replace each instance of `ViewsPerYear` with the same row's cell number in the ViewsPerYear column.
   c. Replace each instance of `DaysSinceCreation` with the same row's cell number in the DaysSinceCreation column.
   d. Replace each instance of `DaysSinceEdited` with the same row's cell number in the DaysSinceEdited column.
4. Save the formula (press Enter/Return).
5. Copy the formula to the whole column.

### Formula breakdown

Here's a breakdown of the formula and its components.

```
=IF(DaysSinceCreation > 730,
  IF(AND((ViewCountLastYear / (ViewCountAllTime / (DaysSinceCreation / 365))) < 0.2, DaysSinceEdited > 730),
    "[001] Last year's views (" & ViewCountLastYear & ") have had a large decline from the lifetime average (" & ViewsPerYear & " per year), and it hasn't been updated in over 2 years.",
    IF((ViewCountLastYear / (ViewCountAllTime / (DaysSinceCreation / 365))) < 0.2,
      "[002] Last year's views (" & ViewCountLastYear & ") have had a large decline from the lifetime average (" & ViewsPerYear & " per year).",
      IF(DaysSinceEdited > 730,
        "[003] This content hasn't been updated in over 2 years.",
        "[004] This content does not require urgent updates."
      )
    )
  ),
  "Content is less than 2 years old (" & DaysSinceCreation & " days)."
)
```

The formula starts by checking if the content is older than 730 days (2 years). If the content is less than 2 years, it outputs a [005] message indicating the content's age and that it's being ignored for this specific evaluation. Otherwise, it continues to evaluate and produce a 001–004 code.

- **Code [001] - High Urgency**: If the content is older than 2 years, the formula then evaluates two conditions using the AND function:
  - The ratio of last year's views to the average annual views (calculated as total views divided by the number of years since creation) is less than 0.2, indicating a significant drop (80%) in engagement.
  - The content hasn't been updated in over 730 days (2 years).
  - If both conditions are met, it outputs a code [001] and a detailed message with the specific last year's views, the calculated lifetime average views per year, and notes the lack of updates in over 2 years.
- **Code [002] - Moderate Urgency Due to Views**: If only the engagement drop condition is met, it outputs a code [002] and a similar detailed message but focuses solely on the drop in views without mentioning the update frequency.
- **Code [003] - Moderate Urgency Due to Lack of Updates**: If the content hasn't been updated in over 2 years but doesn't meet the engagement drop condition, it outputs a code [003] and highlights the lack of recent updates.
- **Code [004] - Low Urgency**: If neither of the conditions for higher urgency is met, it outputs a code [004] and indicates that the content does not require urgent updates.
- **Code [005] - No Urgency**: If the page is not yet 2 years old, we ignore further checks.

## Examples

Below are examples of what each result code from the formula might look like, along with a simple explanation for each. These illustrate how the formula can be used to categorize content based on its age, engagement, and update history, helping content managers prioritize their efforts.

### [001] High urgency (least fresh)

This content is very old and has seen a significant drop in views in the last year, plus it hasn't been updated in a long time.

- DaysSinceCreation: 1000 (more than 2 years)
- ViewCountLastYear: 10
- ViewCountAllTime: 1000
- DaysSinceEdited: 800 (more than 2 years)
- Result: "[001] Last year's views (10) have had a large decline from the lifetime average (50), and it hasn't been updated in over 2 years."

### [002] Moderate urgency due to views

Although this content has been updated more recently, the views have dropped significantly, indicating it may need to be reviewed.

- DaysSinceCreation: 1000 (more than 2 years)
- ViewCountLastYear: 10
- ViewCountAllTime: 1000
- DaysSinceEdited: 300 (less than 2 years)
- Result: "Last year's views (10) have had a large decline from the lifetime average (50)."

### [003] Moderate urgency due to lack of updates

This content has not been updated for a long time, but the views have not dropped as significantly. It may still be relevant but could benefit from a refresh.

- DaysSinceCreation: 1000 (more than 2 years)
- ViewCountLastYear: 100
- ViewCountAllTime: 1000
- DaysSinceEdited: 800 (more than 2 years)
- Result: "[003] This content hasn't been updated in over 2 years."

### [004] Low urgency

The content is older but has been updated relatively recently and maintains a steady number of views. It's not a high priority for updates right now.

- DaysSinceCreation: 1000 (more than 2 years)
- ViewCountLastYear: 100
- ViewCountAllTime: 1000
- DaysSinceEdited: 300 (less than 2 years)
- Result: "[004] This content does not require urgent updates."

### [005] New content

This is "new" content, so we're not concerned with it. Once it hits 2 years (730 days) old, we can consider other actions on it.

- DaysSinceCreation: 100 (less than 2 years)
- ViewCountLastYear: 5
- ViewCountAllTime: 5
- DaysSinceEdited: 100 (since creation)
- Result: "Content is less than 2 years old (100 days)."

## Screenshot

<!-- Screenshot omitted: a real-world Google Sheet example showing two color groups — red (pink) rows for code 001 items and pale yellow rows for code 003 items, with alternating light gray/white rows used for visual navigation. -->

In this screenshot from a real-world Google Sheet example, we have two color groups worth noting: red (pink) and pale yellow.

Note that the metrics page (line 1020) has only had 8 views in the last year, a change from the 49 view per year average (in the 2 years since it was created). It hasn't been updated in 2+ years – likely since it was created, too. So this gets a code 001. We're using conditional formatting to color 001 items with red (pink) background.

The next three items (lines 1021–1023) are getting moderate views per year, but the content hasn't been updated in 2+ years. Code 003, formatting as light yellow. (We should keep an eye on these, or consider them for update.)

The other colors in this screenshot are insignificant. We're using alternating colors (light gray, white) for visual navigation.

---

*Internal documentation. Company and internal page names removed.*

Related: [How documentation work actually moves](documentation-lifecycle-model.md) — the process this scoring feeds.
