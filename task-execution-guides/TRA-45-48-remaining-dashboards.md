# TRA-45 through TRA-48: Remaining Dashboards

## Overview
These four dashboard tasks follow similar patterns to TRA-42-44. Each builds on TRA-41 (Base Data Tabs) and creates specialized analytics dashboards.

---

## TRA-45: Build Intent Radar Dashboard

### Task Details
- **Priority:** High (Score: 4/5)
- **Complexity:** Medium
- **Type:** Data & Analytics

### Requirements
- Track intent signals and signals
- Formulas and structure defined
- Verify intent signal accuracy

### Key Metrics
- Intent signals by type (upgrade, trial, demo, etc.)
- Intent score/strength
- Contacts by intent segment
- Intent signal trends over time
- Intent-to-conversion rates

### Execution Steps
1. Fetch task details (intent signal definitions, formulas)
2. Design dashboard structure (intent segments, signal tracking)
3. Create dashboard sheet
4. Implement intent scoring formulas
5. Connect to base data (Events tab for intent signals)
6. Add visualizations (intent radar chart, trends)
7. Verify intent signal accuracy
8. Update Linear issue

### Dependencies
- TRA-41: Base Data Tabs (Events tab)
- Intent signal definitions
- Intent scoring algorithm

---

## TRA-46: Build Automation Performance Dashboard

### Task Details
- **Priority:** High (Score: 4/5)
- **Complexity:** Medium
- **Type:** Data & Analytics

### Requirements
- Track automation performance metrics
- Clear metrics and structure
- Verify automation data sources

### Key Metrics
- Automation completion rates
- Email performance (opens, clicks) by automation
- Goal completion rates
- Automation ROI
- Drop-off points in automations
- Automation engagement trends

### Execution Steps
1. Fetch task details (automation metrics, formulas)
2. Design dashboard structure (automation list, performance metrics)
3. Create dashboard sheet
4. Implement performance calculation formulas
5. Connect to base data (Events tab for automation events)
6. Add visualizations (automation performance charts)
7. Verify automation data sources
8. Update Linear issue

### Dependencies
- TRA-41: Base Data Tabs (Events tab)
- Automation event tracking
- Performance metric definitions

---

## TRA-47: Build Suppression & Hygiene Monitor Dashboard

### Task Details
- **Priority:** High (Score: 4/5)
- **Complexity:** Medium
- **Type:** Data & Analytics

### Requirements
- Monitor suppression lists and data hygiene
- Well-defined metrics
- Verify suppression logic

### Key Metrics
- Suppressed contacts count (by reason)
- Bounce rates (hard/soft)
- Unsubscribe rates
- Invalid email addresses
- Duplicate contacts
- Data quality score
- Hygiene trends over time

### Execution Steps
1. Fetch task details (suppression rules, hygiene criteria)
2. Design dashboard structure (suppression categories, hygiene metrics)
3. Create dashboard sheet
4. Implement suppression and hygiene formulas
5. Connect to base data (Contacts tab)
6. Add visualizations (hygiene trends, suppression breakdown)
7. Verify suppression logic
8. Update Linear issue

### Dependencies
- TRA-41: Base Data Tabs (Contacts tab)
- Suppression list definitions
- Data hygiene criteria

---

## TRA-48: Build Weekly Executive Summary Dashboard

### Task Details
- **Priority:** High (Score: 4/5)
- **Complexity:** Medium
- **Type:** Data & Analytics

### Requirements
- Aggregate data from other dashboards
- Clear structure and data sources
- Weekly summary format

### Key Metrics (Aggregated from other dashboards)
- Top-line metrics (MRR, customers, engagement)
- Key trends (week over week)
- Highlights and lowlights
- Action items
- Performance vs. goals

### Execution Steps
1. Fetch task details (summary format, key metrics to include)
2. Design dashboard structure (summary sections, weekly view)
3. Create dashboard sheet
4. Implement aggregation formulas (pull from other dashboards)
5. Connect to other dashboards (TRA-42 through TRA-47)
6. Add visualizations (summary charts, trend indicators)
7. Verify aggregation logic
8. Update Linear issue

### Dependencies
- TRA-42: Engagement Dashboard
- TRA-43: Revenue Dashboard
- TRA-44: Cohort & Funnel Dashboard
- TRA-45: Intent Radar Dashboard
- TRA-46: Automation Performance Dashboard
- TRA-47: Suppression & Hygiene Monitor
- Summary format requirements

---

## Common Execution Pattern

All dashboard tasks follow this pattern:

1. **Fetch Requirements** - Get specifications from Linear
2. **Design Structure** - Plan dashboard layout and metrics
3. **Create Sheet** - Use Google Sheets API
4. **Implement Formulas** - Add calculations
5. **Connect Data** - Link to TRA-41 base tabs
6. **Add Visualizations** - Charts and formatting
7. **Verify** - Test and validate
8. **Update Linear** - Mark complete

## Notes

- All dashboards depend on TRA-41 being complete
- Can be built in parallel after TRA-41 is done
- Each dashboard should be self-contained but can reference others
- Consider data refresh frequency and automation
- Document formula logic for future maintenance
