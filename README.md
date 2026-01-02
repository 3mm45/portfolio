# UX Research & Data Analysis Portfolio  
**Three connected case studies:** Online survey design & psychometrics · Behavioral Analytics · Website Usability

**Role & tools:** UX Researcher / Data Analyst — Python (v3.14.4) (Pandas, NumPy, SciPy), Google Analytics, SPSS, Excel, LimeSurvey
**Domain:** Department of Psychology website (University)

---

## Executive summary — what this portfolio demonstrates
This portfolio consolidates three case studies from a single research program on an academic website. The work combines survey experimentation, psychometrics, web analytics, user feedback, and usability analysis to improve measurement validity and guide practical website improvements—showing how design choices in online surveys and websites affect data validity, user behavior, and prioritization decisions.

Controlled questionnaire variants were tested to quantify how interface-level design decisions affect data quality, response behavior, and measurement structure. Results were then cross-checked with Google Analytics to validate self-reports and establish realistic usage constraints (mobile-first, short visits). Finally, perceived usability and open-ended feedback were synthesized into an implementation-oriented recommendation set for site improvement.

### Strongest outcomes (what was delivered)
- Identified measurement instability caused by survey UI design, preventing misleading comparisons and broken benchmarks. Evidence-based survey-design guidance to protect data quality and measurement validity in web-based questionnaires (layout, open-ended input design, and matrix/question order implications).
- A survey + Google Analytics consistency check to validate self-reports, identify perception gaps, and highlight practical UX constraints (mobile-first, short visits).
- A mixed-method website usability evaluation translated into a prioritized improvement roadmap (with implementation status and expected impact).

**What teams get from this:** Clear, evidence-based guidance that prevents misleading metrics, noisy A/B tests, incorrect prioritization, and design decisions based on unstable data.

---

## Case studies at a glance
### Case Study 1 — Web-survey design & response quality
- Tests how **layout** (one-page vs. slide-by-slide) and **input field size** affect engagement (completion time, non-response, response length).
- Determines how **matrix question arrangement and item order** influence factor structure and inter-item correlations, assessing the impact of visual proximity on psychometric outcomes.

### Case Study 2 — Consistency check: Google Analytics vs. survey self-reports
- Assesses consistency between objective behavioral data (Google Analytics) and subjective self-reports to validate user perceptions.
- Compares aligned indicators (time-on-site, device mix, audience skew) to validate perceptions, identify gaps, and reduce decision risk.

### Case Study 3 — Website usability evaluation & improvement roadmap
- Evaluates and improves perceived usability of the Department of Psychology website based on quantitative user ratings and qualitative feedback.
- Translates findings into prioritized recommendations.

---

## Responsibilities
End-to-end ownership across research design, data preparation, statistical analysis, qualitative coding, synthesis, and recommendations.

- Designed the research structure across three case studies (survey architecture design in LimeSurvey; survey experiment + GA alignment + website usability evaluation).
- Cleaned and harmonized structurally different datasets across multiple survey variants in Python, including removal of incomplete responses, bot/outlier filtering, and format standardization to ensure data quality and cross-format comparability before analysis.
- Executed statistical analyses (Mann–Whitney U, chi-square, ANOVA, PCA/factor-structure evaluation, bootstrap comparisons).
- Defined alignment points (survey ↔ GA), compared patterns, interpreted discrepancies through cognitive and methodological lenses, and translated findings into UX implications.
- Designed the evaluation structure, analyzed usability ratings, coded open-ended feedback into themes, and quantified frequency patterns for prioritization.
- Synthesized results into decision-ready implications and a practical recommendation set with status tracking and expected impact.

---

# Case Study 1 — Web-survey design and response quality

## Why this matters
Web survey interfaces are not neutral containers: spacing, grouping, and item order can shape respondents’ behavior (engagement, non-response, response length), how they interpret questions, and how constructs emerge statistically—especially in matrix/grid designs (inter-item correlations, factor structure). This case study tested how survey layout and visual design choices influence response behavior and psychometric outcomes, and how they create hidden measurement differences across survey variants.

The goal is to provide practical guidelines for designing more effective web questionnaires to collect higher-quality and more reliable data, and to provide empirical evidence on the effects of visual design characteristics on respondent behavior during questionnaire completion.

If layout-induced bias went unnoticed, usability scores could be misleading, leading to incorrect conclusions, broken benchmarks, and unreliable comparisons across studies or time.

## Research questions
- **RQ1:** Does a one-page vs. a slide presentation change completion time?
- **RQ2:** Do open-ended input field sizes affect (a) response participation and (b) response length?
- **RQ3:** Do matrix layout and item order change correlations and factor structure (measurement equivalence risk)?

## Analytical framework
### Hypothesis-driven analysis → results
- **H0:** No statistically significant difference in completion time between single-page and slides. ✅ Confirmed  
- **H1a:** Non-response proportion does not depend on input box size (open-ended). ❌ Not confirmed  
- **H1b:** Text length does not depend on input box size (open-ended). ⚠️ Partially confirmed  
- **H2:** Grid question order + presentation mode (one page vs. slides) results in different factor structures. ✅ Confirmed  
- **H3:** Grid question order + presentation mode (one page vs. slides) leads to different inter-item correlations. ✅ Confirmed  

### Quantitative analyses used
1. **Descriptive statistics:** summarize sample characteristics and response distributions.  
2. **H0:** **Mann–Whitney U test** — compare completion time across formats.  
3. **H1a:** **Chi-square test** — relationship between answer box size and number/length of open-ended responses.  
4. **H1b:** **ANOVA** — response length differences across format, order, and answer box size.  
5. **H2 (measurement structure checks):**  
   - **KMO** (sample adequacy)  
   - **Bartlett’s test** (suitability for factor analysis)  
   - **PCA** (latent structure among questionnaire items)  
6. **H3:**  
   - **Bootstrapping** — compare average strength of inter-item correlations between question groups  
   - **Heatmaps** — visualize inter-item correlations across questionnaire variants  

## Project context and dataset
**Survey instrument:** 21 questions (demographics + 13 usability items + 3 open-ended prompts)

**Four questionnaire variants combined:**
- Presentation format: **One page (1P)** vs **slide-by-slide (Sl)**
- Matrix item order: **Order A** vs **Order B**
- Open-ended input field: **Small** vs **Large** input box

**Data & sample:** 3,896 recorded accesses → after bot removal, **N = 500 usable responses**  
**Split:** 1P: 259 (51.8%), Sl: 241 (48.2%)  
Most respondents were students (73.7%); 80% were female; 74.2% reported a positive or very positive website impression.

## Key findings
### Finding 1 — Completion time was stable across formats
- Layout (1P vs. slides): efficiency was stable. Completion time did not differ meaningfully across layouts, indicating similar efficiency once users adapted.
- **Implication:** Format choice can be guided by UX constraints (screen size, interaction model) without assuming slower completion, but measurement equivalence still needs attention (see Finding 3).

### Finding 2 — Larger open-ended boxes improved participation; richer responses depended on format and box size
- Open-ended engagement was limited: 29.2% answered at least one open-ended question; 4.4% answered all three.
- Input-field size did not consistently increase responses for every open-ended item. However, the relationship between input size and answering at least one open-ended question was statistically significant: **χ²(1,500)=5.95, p=0.014**.
- For response length, neither format nor box size alone was significant; however, the interaction was significant: large boxes produced longer responses specifically in slide-based presentations: **F(1,106)=4.49, p=0.03**.

### Finding 3 — Matrix order and proximity changed inter-item correlations and factor structure
- Across variants, the scree plot suggested one dominant usability component, but factor loadings differed substantially between the four questionnaire variants. Items shifted between components depending on format/order.
- Bootstrap comparisons showed: within-variant correlations were much higher than between-variant correlations, indicating each variant was internally coherent but structurally different from the others.
- Heatmaps showed item proximity effects: when items were adjacent, the g04–g06 correlation was high in Order A (close placement) but lower in Order B (greater separation), indicating a drop as item distance increased.

## Implications — “Do / Don’t” guidance for survey design
- Use large open-ended inputs to increase the likelihood of capturing at least one written response.
- Use **Slides + Larger input field** when the goal is richer qualitative detail (longer responses).

**Most decision-relevant (highest business risk):**
- Avoid mixing formats + item orders if the goal requires comparability/stability (e.g., before/after redesign, cohort comparisons, A/B tests). Minor presentation changes can shift inter-item correlations and factor structure, introducing measurement error and threatening equivalence.
- Don’t treat matrix layout and sequencing as “just UI.” Proximity and order can reshape correlations and factor structure. Treat UI as part of the measurement instrument (not a wrapper).
- **Note:** Factor loadings differed substantially across versions. This means the same “usability score” may represent different underlying constructs across versions, so comparing results across versions can introduce measurement error.

## Artifacts (Case Study 1)
- **Artifact A:** Python notebook (data harmonization + hypothesis tests): cleaning, bot/outlier filtering, dataset harmonization across formats, hypothesis testing
- **Artifact B:** Analysis tables: Mann–Whitney U, chi-square, ANOVA outputs, bootstrap correlation summary, factor structure and inter-item correlation visuals
- **Artifact C:** Psychometrics visuals:
  - Scree plot, factor loading summaries
  - Correlation heatmaps (visual comparison across variants)
  - Bootstrap correlation summary table (within-variant vs between-variant mean correlations)

---

# Case Study 2 — Consistency between Google Analytics and survey responses

## Objective
This analysis explored the relationship between users’ self-reported experiences and actual behavior on an academic website. Google Analytics data were combined with survey responses to assess how accurately users perceive their interaction patterns.

Each data type has limitations and requires cautious interpretation. Self-reported time estimates may be biased due to recall and perception limitations; log data may be affected by measurement and reliability issues.

**Goals:** validate self-reports, identify perception gaps, and improve confidence in conclusions through mutual cross-validation.

## What was compared (aligned indicators)
- **Time-on-site:** survey typical visit duration vs GA average session duration
- **Device usage:** survey primary device vs GA device distribution
- **Audience skew check:** survey gender vs GA gender distribution (as available in GA reporting)

## Key comparisons and interpretation
| Indicator | Survey (self-report) | Google Analytics (logs) | What it suggests |
|---|---:|---:|---|
| Typical time on site | Most reported 5–15 minutes | Avg session duration ≈ 5:30 | Practical alignment; small estimation bias expected due to recall limitations |
| Primary device | 55.8% mobile | 70.5% mobile | Mobile-first confirmed; self-report modestly underestimates habitual mobile use |
| Gender distribution (representativeness check) | 80% female | 68.7% female | Likely sampling differences (survey subset vs all traffic); directional agreement supports a plausible audience match |

## Implications
- Prioritize mobile-first usability because both measures point to mobile as the primary access channel.
- Optimize for short, task-oriented visits: navigation and information hierarchy should support fast orientation.
- Use GA as a representativeness check (e.g., gender, device mix) as a practical sanity check when a perfect sampling frame is not available.
- Use combined data sources for mutual cross-validation to reduce decision risk: scalable behavioral evidence (“what”) plus contextual user intent (“why”) strengthens prioritization and recommendations.
- Note: Log data can be affected by non-human traffic (bots/spiders), incomplete coverage due to consent and blocking, and event-based metric definitions.

**Next step:** repeat the consistency check after major design changes and track shifts in device usage and session patterns.

## Artifacts (Case Study 2)
- **Artifact D:** GA screenshot pack (sanitized): device distribution and session duration screenshots used to ground the cross-validation narrative

---

# Case Study 3 — Department of Psychology website usability evaluation

## Context
The Department of Psychology website served multiple audiences (students, faculty, professors, assistants, prospective students) but showed signs of friction and a need for further evolution: users struggled to find timely academic information, and key workflows (e.g., experiment registration) created confusion.

## Problem
Users reported friction in finding time-sensitive academic information and completing key workflows (notably experiment registration).

## Objective
Quantify perceived usability, identify recurring pain points through open-ended feedback, and translate findings into prioritized recommendations for information architecture, content governance, mobile experience, workflow feedback, and reliability.

**Focus:** perceived usability + qualitative feedback → actionable improvements

## Methods
- Structured usability survey (Likert ratings, 1–5 scale across core usability dimensions)
- Open-ended questions (problems, missing info, improvement suggestions)
- Data prep/analysis in Python; qualitative coding in Excel for frequency-based prioritization

## Key results
### Quantitative highlights
- **Strengths:** loading speed 4.51, navigation 4.34, learnability 4.36.
- **Opportunities (lower ratings):** course description usefulness 3.58, news/updates 3.74, experiment registration 3.64.

### Qualitative themes (recurring pain points)
1. **Content quality and freshness**
   - Outdated or incomplete information; limited file availability
   - Scattered details on projects, events, opportunities, extracurricular activities
2. **Information architecture and findability**
   - Exam results difficult to locate; poor visibility of key student information; lacking privacy controls
   - Faculty information, schedules, resources, and course materials perceived as disorganized/fragmented
3. **Mobile responsiveness and navigation consistency**
   - Inconsistent navigation patterns and weak mobile experience reduce efficiency for mobile-first users
4. **Workflow and system feedback issues**
   - Experiment registration perceived as disorganized; technical difficulties reported
   - Technical instability during peak periods (e.g., exam sessions)
   - Lack of notifications for important updates (exam results, news, deadlines)

## Recommendations (prioritized)
1. **Content governance:** update cadence, ownership, streamlined publishing workflow
2. **Information architecture:** dedicated high-visibility sections (exam results, course materials/resources, projects/activities, faculty info, calendars/deadlines, FAQ)
3. **Design improvements:** mobile-first responsiveness, clearer hierarchy and scannability, modernized UI visuals
4. **Experiment registration:** simplified flow, clearer steps, confirmations/errors, transparency improvements
5. **Enhancements:** notifications, English-language support

## Expected impact
- Clearer, expanded information architecture reduces search effort and improves findability
- Faster access to time-sensitive academic information (exams, deadlines, updates) through regular content updates
- Improved access to academic and faculty information (profiles, schedules, resources, contacts)
- Streamlined navigation and overall usability for students and faculty
- Responsive, mobile-friendly design and improved visual hierarchy
- Higher user trust and satisfaction through transparency, stability, and clearer system feedback/notifications
- More maintainable website via defined content ownership and update routines
- Modern, professional, inclusive web presence supporting the department’s academic mission

## What to do next (to strengthen impact)
- Add a prioritization model (Impact × Effort, frequency of use, risk) to guide sequencing.
- Validate redesigned flows with task-based usability testing:
  - Finding exam results
  - Locating course materials
  - Completing experiment registration  
  (Measure success rate, time-on-task, perceived clarity.)

## Artifacts (Case Study 3)
- **Artifact E:** Usability metrics summary table (1–5): single-page table + bar chart of top strengths vs key friction points
- **Artifact F:** Recommendations matrix (with status): category → recommendation → rationale → status (implemented/partial/excluded)
- **Artifact G:** Full questionnaire item list (items 1–21, including g01–g13)

---

# Core abilities demonstrated
- End-to-end UX research ownership: define research questions, select methods, execute analyses, deliver decision-ready outputs across experiments, behavioral analytics, and usability evaluation.
- Quantitative analysis and statistical judgment: clean/harmonize real datasets and apply appropriate statistical tests (Mann–Whitney U, chi-square, ANOVA), including correct interpretation of interaction effects and responsible claims.
- Survey-design and measurement expertise (differentiator): identify when UI choices affect not only response behavior but also measurement properties (inter-item correlations and factor structure), and translate this into practical guidance that protects comparability.
- Cross-validation with behavioral analytics: align self-reported behavior with Google Analytics, quantify perception gaps, and use the combined picture to support strategic priorities (e.g., mobile-first UX, support for short task-oriented visits).
- Mixed-method synthesis that leads to action: convert qualitative feedback into structured themes and synthesize with quantitative metrics to produce evidence-based recommendations.
- Product-minded recommendations and prioritization: translate findings into an actionable roadmap (information architecture, content governance, mobile UX, workflow feedback), including status tracking and expected impact.
- Technical fluency and reproducibility: package work into stakeholder-friendly artifacts (Python notebooks, analysis tables, heatmaps, coded theme sheets) supporting transparency, reuse, and collaboration.

---

# Full questionnaire item list
1. Please indicate your gender.  
2. Please indicate your role during today’s visit to the Department of Psychology website.  
3. How often do you visit the Department’s website?  
4. How much time do you usually spend on the website during a typical visit?  
5. What is your overall impression of using the Department of Psychology website?  
6. (g01) The overall appearance and design of the website are attractive.  
7. (g02) The homepage provides a clear overview of the website’s structure and logic.  
8. (g03) I always know where to find the information I need.  
9. (g04) It was easy to learn how to navigate the website.  
10. (g05) The information provided on the website is useful, complete, and clear.  
11. (g06) The language and terminology used are easy to read and understand.  
12. (g07) Course descriptions are very helpful when choosing elective subjects.  
13. (g08) I find useful information in the “News and Updates” section.  
14. (g09) The website’s information is updated regularly.  
15. (g10) I can easily and quickly book an appointment for experiments.  
16. (g11) I think future students can easily learn how to use the website.  
17. (g12) I am satisfied with the website’s loading speed.  
18. (g13) I access the website more often from a mobile device than from a computer.  
19. Have you encountered any problems or negative experiences while using the website? If yes, which ones?  
20. What type of information should be added to the website?  
21. Do you have any specific suggestions for improving the Department of Psychology website?  

📁 /artifacts/README.md
# Research Artifacts

This folder contains supporting tables, figures, and summaries referenced across the three case studies.
All artifacts are presented in Markdown-friendly formats for transparency and reproducibility.

## Contents
- Case Study 1: Survey UX & Measurement Stability
- Case Study 2: Google Analytics vs Survey Consistency
- Case Study 3: Website Usability Metrics & Recommendations


📊 Case Study 1 — Quantitative Tables (Markdown)
/artifacts/tables/cs1-mann-whitney-time.md
## Table 7. Questionnaire Completion Time by Format

**Test:** Mann–Whitney U  
**Purpose:** Compare completion time between questionnaire formats

| Question Format | N | Median Time | Mann–Whitney U | p-value |
|-----------------|---|-------------|----------------|---------|
| One page (total) | 257 | 151.00 | 28143.5 | 0.86 |
| Slides (total) | 217 | 153.00 | — | — |
| One page (OP+) | 85 | 259.00 | 2351.5 | 0.64 |
| Slides (OP+) | 58 | 286.00 | — | — |
| One page (OP−) | 172 | 124.00 | 13329.9 | 0.69 |
| Slides (OP−) | 159 | 131.00 | — | — |

**Finding:**  
Completion time did not differ meaningfully between single-page and slide-based formats after excluding outliers.

**Implication:**  
Layout choice does not affect efficiency, but efficiency alone does not guarantee measurement equivalence.


/artifacts/tables/cs1-chi-square-nonresponse.md
## Table 8. Open-Ended Response Rate by Answer Box Size

**Test:** Chi-square (χ²)  
**Purpose:** Assess relationship between answer-box size and response participation

| Question | χ² | p-value | Phi (φ) |
|--------|----|---------|---------|
| Problems / Negative Experiences | 0.748 | 0.387 | 0.039 |
| Additional Information | 2.201 | 0.138 | 0.066 |
| Suggestions for Improvement | 3.786 | 0.052 | 0.087 |
| **All Questions (Total Sample)** | **5.951** | **0.014** | **0.110** |

**Finding:**  
Larger answer boxes increased the likelihood that respondents answered at least one open-ended question.

**Implication:**  
Input field size influences participation and should be treated as a behavioral design lever, not a cosmetic choice.


/artifacts/tables/cs1-anova-response-length.md
## Table 9. Response Length — Two-Way ANOVA

**Purpose:** Test effects of format and answer-box size on response length

| Source | SS | df | MS | F | p |
|------|----|----|----|---|---|
| Question format | 84,432.29 | 1 | 84,432.29 | 2.82 | 0.09 |
| Answer-box size | 17,477.57 | 1 | 17,477.57 | 0.58 | 0.45 |
| Format × Box size | 134,274.45 | 1 | 134,274.45 | 4.49 | 0.03 |
| Residuals | 3.17e6 | 106 | 29,925.69 | — | — |

**Finding:**  
Neither format nor box size alone affected response length, but their interaction did.

**Implication:**  
Larger input fields produce longer responses primarily in slide-based presentations, highlighting interaction effects that simple averages would miss.


🧠 Factor Analysis & Correlations (Markdown + Images)
/artifacts/figures/cs1-factor-structure.md
## Factor Structure Across Questionnaire Variants

![Factor Loadings Heatmaps](../figures/cs1-factor-heatmap.png)

**Suitability checks:**
- KMO = 0.88
- Bartlett’s test χ² = 1424.59, p < 0.01

**Finding:**  
Although a dominant usability component appeared across variants, factor loadings differed substantially by format and item order.

**Plain-English meaning:**  
The same “usability score” can represent different underlying constructs across versions, so comparing results across versions can introduce measurement error.


/artifacts/figures/cs1-correlation-heatmaps.md
## Inter-Item Correlation Heatmaps

![Correlation Heatmaps](../figures/cs1-correlation-heatmaps.png)

**Finding:**  
Items placed closer together showed stronger correlations than the same items placed farther apart.

**Implication:**  
Visual proximity and item order reshape correlation strength, confirming that layout decisions affect measurement structure.


/artifacts/tables/cs1-bootstrap-correlations.md
## Bootstrap Analysis — Mean Inter-Item Correlations

**Method:** 1,000 bootstrap resamples (60% of each sample)

| Comparison | Mean | 2.5% | 97.5% |
|-----------|------|------|-------|
| Within same variant | 0.62 | 0.49 | 0.73 |
| Between variants | 0.30 | 0.18 | 0.41 |

**Finding:**  
Correlations within the same questionnaire variant were consistently higher than between variants.

**Implication:**  
Variants are internally coherent but structurally different, reinforcing comparability risk when mixing formats or orders.


📈 Case Study 2 — GA vs Survey (Markdown)
/artifacts/tables/cs2-session-duration.md
## Table 13. Average Session Duration by Device and Gender (GA)

| Device | Female | Male |
|------|--------|------|
| Mobile | 00:00:41 | 00:01:27 |
| Desktop | 00:01:40 | 00:02:13 |

**Finding:**  
Sessions are short and task-oriented, especially on mobile.

**Implication:**  
Navigation and information hierarchy should prioritize fast orientation and quick task completion.


/artifacts/tables/cs2-self-reported-time.md
## Table 14. Self-Reported Time Spent per Visit

| Time range | N | % |
|-----------|---|---|
| < 5 min | 202 | 40.4 |
| 5–15 min | 228 | 45.6 |
| 15–30 min | 42 | 8.4 |
| > 30 min | 11 | 2.2 |
| No response | 17 | 3.4 |

**Finding:**  
Self-reported estimates align well with GA averages, with expected recall bias.


🧭 Case Study 3 — Usability & Recommendations (Markdown)
/artifacts/tables/cs3-usability-ratings.md
## Usability Metrics Summary (Likert 1–5)

| Code | Aspect | Mean |
|-----|--------|------|
| G01 | Design attractiveness | 3.55 |
| G02 | Homepage structure clarity | 4.12 |
| G03 | Ease of finding information | 3.89 |
| G04 | Ease of navigation | 4.34 |
| G05 | Information usefulness | 4.13 |
| G06 | Language clarity | 4.33 |
| G07 | Course descriptions | 3.74 |
| G08 | News & updates | 3.58 |
| G09 | Information freshness | 3.90 |
| G10 | Experiment booking | 3.64 |
| G11 | Learnability (future students) | 4.36 |
| G12 | Page loading speed | 4.51 |
| G13 | Mobile access frequency | 3.65 |


/artifacts/tables/cs3-recommendation-matrix.md

# Recommendation Matrix with Status (Website Usability)

This matrix translates quantitative usability ratings and qualitative user feedback into a decision-ready improvement backlog.  
Statuses reflect whether a recommendation was implemented, partially implemented, or excluded.

**Legend:** ✅ Implemented · ⚠️ Partially implemented · ❌ Excluded / not planned

---

## Summary of Priorities
- **Highest impact themes:** Content freshness & ownership, Information Architecture (findability), Mobile-first responsiveness, Workflow clarity (experiment booking), Feedback/notifications.
- **Primary user context:** Mobile-first usage and short, task-oriented visits → prioritize fast orientation, clear pathways, and time-sensitive information access.

---

## Recommendation Matrix (Detailed)

| ID | Category | User Problem / Signal | Evidence (Survey + Qual) | Recommendation | Priority | Effort | Owner | KPI / Success Metric | Validation Plan | Dependencies | Status |
|---:|----------|------------------------|--------------------------|----------------|:--------:|:------:|-------|----------------------|-----------------|--------------|:------:|
| 01 | Content governance | Information feels outdated; users cannot rely on updates | Lower ratings for News/Updates & information freshness; open-ended comments request regular updates | Define content ownership + update cadence (weekly/monthly), and publish update guidelines | High | Med | Content lead / Admin | Increased freshness ratings; reduced “outdated info” mentions | Re-run usability pulse; compare “freshness” item pre/post | Roles/permissions; editorial workflow | ✅ |
| 02 | Information architecture | Hard to find time-sensitive academic info (exams, deadlines) | Findability not top-rated; qual feedback mentions scattered exam info | Create “Student Hub” with clear entry points: exams, deadlines, materials, contacts | High | Med | UX + Content | Reduced time-to-find; fewer “can’t find” comments | Task-based test: find exam results / deadline | IA redesign; content inventory | ⚠️ |
| 03 | Exam results | Exam results are difficult to locate and track | Qual feedback: “exam results not organized”; time-sensitive pain point | Dedicated exam results page + filtering by course/date + consistent naming | High | Med | Content + Dev | Higher satisfaction for academic tasks; fewer support requests | Usability test + analytics event tracking | Data source availability; permissions | ⚠️ |
| 04 | Course descriptions | Elective/course descriptions insufficient | Lower rating for course descriptions; qual requests more details | Standardize elective/course template (outcomes, syllabus, assessment, prerequisites) | Med | Low | Content | Increased “course description usefulness” rating | Spot-check + usability pulse | Faculty input | ✅ |
| 05 | News & updates | News section not useful / not maintained | Low rating for News/Updates; qual requests relevant updates | Improve News: categories, pinned critical updates, archive, editorial calendar | Med | Low–Med | Content | Increased engagement with News; improved rating | Analytics: clicks/scroll depth + survey | Content workflow | ✅ |
| 06 | Mobile responsiveness | Mobile experience weak or inconsistent | Mobile is primary channel (GA); qual requests responsive version | Mobile-first responsive redesign (navigation, spacing, typography, cards) | High | High | UX + Dev | Reduced bounce on mobile; improved navigation ratings | Pre/post analytics + mobile usability test | Front-end capacity | ✅ |
| 07 | Navigation clarity | Users need fast orientation for short sessions | Short sessions in GA; qualitative “hard to find” | Simplify primary nav; add quick links and breadcrumb structure | High | Med | UX | Higher findability rating; fewer backtracks | Tree test + first-click test | IA decisions | ✅ |
| 08 | Experiment booking | Booking experiments is unclear / frictionful | Lower rating for booking; qual mentions workflow issues | Redesign booking flow: steps, requirements, confirmation, error states | High | Med | UX + Dev | Higher booking success rate; fewer failures | Funnel tracking + usability test | System integration | ✅ |
| 09 | System feedback | Lack of clear confirmations and messages | Qual feedback about uncertainty and missing guidance | Add confirmations, status messages, and clearer instructions | Med | Low | Dev + Content | Fewer drop-offs in workflows | Event tracking (errors/confirmations) | UX copy | ✅ |
| 10 | File access | Files expire too quickly / not accessible | Qual feedback: limited availability and timing | Extend file availability window + central file repository per semester | Med | Med | Content + IT | Lower complaints about access; higher satisfaction | Survey pulse + support logs | Storage policies | ⚠️ |
| 11 | Faculty visibility | Faculty info is not centralized | Qual feedback: need clearer faculty info | Faculty directory: profiles, office hours, contacts, research areas | Med | Med | Content | Improved access to faculty info | Task test: find contact/office hours | Content collection | ⚠️ |
| 12 | Notifications | Users miss critical updates | Qual requests notifications (exams, deadlines, news) | Add notification system: email list / RSS / site banner alerts | Med | Med | Content + IT | Increased awareness; fewer missed deadlines complaints | Survey item + click tracking | Consent/comms policy | ❌ |
| 13 | Language support | Limited accessibility for non-native users | Mentioned as improvement area | Add English version for key pages (programs, contacts, admissions) | Low–Med | High | Content | Increased accessibility; usage by language | Track EN page usage | Translation capacity | ❌ |

---

## Status Notes (Optional)
- ✅ Implemented: completed and publicly available
- ⚠️ Partially implemented: started but missing key components (e.g., no filtering, incomplete content coverage)
- ❌ Excluded: not prioritized due to effort, scope, or constraints

---

## How to Maintain This Matrix
- Review monthly with stakeholders
- Update status and KPIs after releases
- Keep links to live pages or tickets (Jira/Trello/GitHub Issues) in the “Dependencies” column if available



