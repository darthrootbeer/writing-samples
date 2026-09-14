---
title: Documentation Tooling UX Research
type: UX research report
original_format: PDF (internal report)
---

> **Why this is here.** This is research on the documentation system itself rather
> than on a product. It surveys the people who had to use an internal wiki, finds
> where they gave up looking, and recommends structural changes. It also names a
> flaw in its own measurement scale, which is the part worth reading.
>
> What follows is the original report as delivered, not a rewrite — kept in its own
> voice so the analysis and the recommendations stand on their own record.

**Role:** I designed the survey and wrote this report.

# Confluence User Experience Report

Conducted by the documentation team | March 22, 2024

## Executive Summary

This report presents the findings from a survey conducted by the documentation team to assess how well Confluence meets the needs of both users and space administrators across all teams.

### Key Findings

- Users struggle to find information due to poor search and outdated/inaccurate content.
- Both users and admins report that collaborating across teams is difficult.
- Moving teams to their own spaces, managed by a dedicated space admin, is working well.

### Recommendations

1. Dedicate more resources to cleaning up existing information by removing outdated and incorrect content and improving cross-linking of current content.
2. Continue promoting team-dedicated spaces with their own space admins to improve content management and cut down on maintenance resources.
3. Promote the Documentation Slack channel as the central support location for documentation issues.

By implementing these recommendations, the studio can improve the findability, accuracy, and cross-team accessibility of information in Confluence for all teams.

## Introduction

This survey was designed to capture how Confluence meets user needs across all teams, for both everyday users, and Confluence space administrators.

The studio relies on Confluence to be the central information management and documentation tool for the game. Therefore, it is important to regularly get a sense of what is working and what needs improvement, directly from the users.

Based on the information learned in the survey, the Documentation team has included recommendations on how to improve Confluence for the game's teams.

See the Appendices section at the end of this report for snapshots of the survey, spreadsheets and simplified data sets, and Miro workboard.

## Methodology

The survey was designed to capture important information in the fewest number of questions. This method allowed us to strike a balance between making it easy to participate while allowing users to feel like they could answer truthfully.

The questions were created based on the 10 most important answers that users and administrators could provide firsthand, as interpreted by the Documentation Team.

### Participation

Participation was optional, and open to all members of any team at the studio working on the game.

The survey was conducted for 2 weeks, between February 26 and March 8, 2024. It was announced on February 26 via Slack in the documentation channel and the team updates channel, with a link to the survey, asking people to participate. An additional reminder was sent on March 7th, and a team lead made an announcement during the team meeting on 3/8. The survey was closed at EOD March 8th.

All information was collected via Google Forms using native SSO authentication, capturing user email addresses for question follow up, if needed.

### Response counts

Based on channel user counts, approximately 530 people were notified of the survey on Slack. 42 people responded (about 8%). 6 of these responses were from space administrators, who answered both sets of questions.

### Limitations or biases

Anyone not viewing messages in the aforementioned Slack channels may have missed the survey invitation or reminder message, including any employees who were out of office.

Considering the estimated time to complete the survey was 5–10 minutes, the open period of 10 business days was long enough for interested parties to participate.

The survey was not mandatory, so anyone who chose not to participate was allowed to do so.

### How calculations were performed

While reviewing the survey results, it became clear that the options for answering could have been better defined. We allowed for an integer selection between Strongly Disagree (1) and Strongly Agree (5), but only the "strong" options were labeled.

<!-- Screenshot omitted: Example survey question, showing the limitations of the selection method. -->

Users could have misinterpreted the options between the labeled answers, and the exact middle selection (3) could have been interpreted in any number of ways, such as:

- Neither Agree nor Disagree
- Does not apply to me
- Other (such as "skip")

This means we should only count the positive (4, 5) options and the negative (1, 2) options, as users likely understood that the options directly adjacent to "strongly agree" and "strongly disagree" meant "agree, but not strongly" and "disagree, but not strongly".

## Results from Users

This section of the report focuses solely on the User questions.

For all questions:

- 56% of the responses were positive (agree or strongly agree).
- 17% were negative (disagree or strongly disagree).

### Key findings

**Finding 1: Users are comfortable using Confluence.**

88% of users report they're comfortable using Confluence currently, with no users reporting they are not comfortable. This means

1. Users think they know how to use the tool, and
2. Because of this, we can rely on the rest of the survey data to accurately reflect the user experience.

**Finding 2: Search isn't great and information feels disorganized.**

Less than half (43%) of users can easily find the information they need, and only 19% of users think information is well-organized or easy to locate. This indicates that finding information (through search or organically) is hard, and verifies what we hear pretty often: Search in Confluence isn't great, and users find information to be disorganized.

**Finding 3: "Bad" content needs addressing.**

Only 55% of users are satisfied with the quality and accuracy of content, and nearly one-third (31%) of users find missing, outdated, or incorrect information more than "occasionally". This tells us that users tend to discover "bad" content more than they expect to, and they're not happy about it.

**Finding 4: Some users don't know how to get help for docs.**

1 in 5 (21%) of users don't know how to get help for documentation issues, (58% said they did). This means the Documentation Team can better inform users of how to reach them.

**Finding 5: Confluence aids internal team collaboration, but less so across teams.**

A decent amount (64%) of users think Confluence helps internal team collaboration, but only about half (55%) feel that this carries over to working with other teams. Confluence seems to help teams share info amongst themselves, but people feel a bit disconnected (information-wise) from teams they work with.

### Common themes among users

The following themes were identified based on details that users wrote in the comments section.

- Information is "bad": missing, outdated, unclear, or incorrect (6 people).
- Search is poor or difficult to use (3 people).
- We need better ways to organize information across teams (2 people).
- Our content has had a general improvement, and support does a good job (2 people).

### Additional comments (summarized)

Due to these comments containing information that might be linked to users or admins, only the summaries have been preserved here.

- We need to be able to access information across games.
- It would be helpful if we could have scripting support (to create or manage pages).
- We should be able to collaborate with other people (like in Google Docs).
- We should be able to use tabs on pages (to better organize information on the page).
- The way we structure content (hierarchy) and keep it to a space hurts the sharing of information.
- Our team was denied progress on a project by IT because the Documentation team "didn't finish templatizing our work".
- Widgets make editing page content unnecessarily difficult.

## Results from Space Admins

This section of the report focuses solely on the Admin questions.

For all questions:

- 67% of the responses were positive (agree or strongly agree).
- 5% were negative (disagree or strongly disagree).

### Key findings

**Finding 1: Admins can administer just fine.**

83% of admins find that [1] Confluence does what they need it to for their teams, [2] they can create and update content for their team easily, and [3] Confluence itself is reliable and performant.

In other words, the tool itself and the existing admin process seems to be working well.

**Finding 2: Maintenance and keeping content fresh works "ok".**

Only 33% of admins reported hierarchy maintenance and keeping content accurate and up-to-date being easy. With no negative responses or other comments, we can interpret this as "it's not simple, but we can manage".

**Finding 3: Collaborating with other teams is less easy than with internal teams.**

67% of admins reported a slightly higher score (67%) for internal team collaboration than external (50%). One admin specifically called out challenges around collaboration due to teams using multiple tools or platforms for storing information (Google Drive, Slack, Jira). Without a single source of knowledge, it is difficult to know where to get the best information for external teams.

### Common themes among admins

The following theme was identified based on details that admins wrote in the comments section.

- Other team's information is hard to find (2 people).

## Recommendations for improvement

My recommendations for enhancing both the admin and user experience with Confluence are as follows:

**Recommendation 1: Dedicate more resources to cleaning up existing information.**

Admins and users are telling us that information is too spread out, hard to find, and incorrect or outdated. The only solution here is to make the content better. The studio must dedicate additional resources to documentation cleanup and maintenance. As a company, we need to do better at removing or archiving outdated content, and locating, indexing, and cross-linking current content.

**Recommendation 2: Continue to promote migrating teams to their own spaces.**

High scores from existing space admins indicate that while there are some challenges to information management, this process is working well. With the dissolution of the current Documentation Team, the challenge of managing team content will increase, and handing this upkeep to the teams themselves seems like a smart way to handle it with limited resources.

**Recommendation 3: Consider "team content admins".**

For teams who cannot move to dedicated team spaces (and space admins), they should consider assigning a team content admin who performs similar functions for their team.

**Recommendation 4: Promote the documentation channel as a single support location for docs.**

Users need to know where to go for help or how to report bad content. While team spaces have a sidebar that identifies the space admin for that content, other docs do not. We should continue to promote the Doc Team as a support resource; perhaps adding a link to the Doc Team Slack channel as a footer on every page not managed by a space admin.

## Appendices

Note: Personally identifying information has been scrubbed from the below resources.

- Original survey
  - Questionnaire (PNG)
- Worksheet and date
  - Simplified data (PDF)
  - Raw response data (CSV)
  - Workboard (JPG)

## Acknowledgments

Thank you to everyone who participated and provided valuable data! Special thanks to a colleague, who contributed ideas, reviewed my work, and promoted the survey through Slack.

---

*Internal research report. Names, channels, studio, and product redacted.*
