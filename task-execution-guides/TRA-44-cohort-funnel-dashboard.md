# TRA-44: Build Cohort & Funnel Dashboard

## Task Details
- **Priority:** High (Score: 4/5)
- **Complexity:** Medium-High
- **Type:** Data & Analytics
- **Dependency:** Requires TRA-41 (Base Data Tabs)

## Requirements
- Create Cohort & Funnel Dashboard in Google Sheets
- Clear structure, formula-based
- Track cohort analysis and funnel metrics
- Verify cohort logic

## Execution Steps

### Step 1: Fetch Task Details from Linear
- Get cohort analysis requirements
- Get funnel stage definitions
- Get formula specifications
- Understand cohort grouping logic

### Step 2: Design Dashboard Structure

#### Cohort Analysis
- Cohort by signup month
- Retention rates by cohort
- Revenue by cohort
- Cohort size over time

#### Funnel Analysis
- Funnel stages (e.g., Visitor → Lead → MQL → Customer)
- Conversion rates between stages
- Drop-off analysis
- Time to convert between stages

#### Dashboard Layout
```
# Cohort & Funnel Dashboard

## Cohort Analysis
### Retention Matrix
- Rows: Cohorts (by signup month)
- Columns: Months since signup
- Values: Retention % or Customer count

### Cohort Summary
- Cohort size
- Retention rate (30/60/90 days)
- Revenue per cohort

## Funnel Analysis
### Funnel Stages
- Stage 1: Visitors (count)
- Stage 2: Leads (count, conversion %)
- Stage 3: MQLs (count, conversion %)
- Stage 4: Customers (count, conversion %)

### Conversion Rates
- Visitor → Lead: X%
- Lead → MQL: X%
- MQL → Customer: X%
- Overall: Visitor → Customer: X%

### Trends
- Funnel performance over time (chart)
- Conversion rate trends (chart)
```

### Step 3: Create Dashboard Sheet
- Use Google Sheets API to create new sheet or add tab
- Set up cohort retention matrix
- Create funnel stage sections
- Add formulas for calculations

### Step 4: Implement Cohort Formulas
- Cohort Identification:
  - Group contacts by signup/created date (month)
- Retention Calculation:
  - For each cohort, calculate active contacts in each subsequent month
  - Formula: COUNTIFS for cohort + month + active status
- Retention Rate:
  - Active in month N / Original cohort size

### Step 5: Implement Funnel Formulas
- Stage Counts:
  - COUNTIF formulas based on lifecycle stage or tags
- Conversion Rates:
  - Next Stage Count / Current Stage Count
- Drop-off Calculation:
  - Current Stage Count - Next Stage Count

### Step 6: Connect to Base Data (TRA-41)
- Reference Contacts tab for cohort grouping
- Reference Events tab for funnel stage transitions
- Use formulas to calculate cohorts and funnels
- Set up date-based filtering

### Step 7: Add Visualizations
- Create cohort retention heatmap
- Add funnel visualization (chart)
- Create trend charts
- Format dashboard professionally

### Step 8: Verify Cohort Logic
- Test cohort grouping with sample data
- Verify retention calculations
- Check funnel stage definitions
- Validate conversion rate calculations

### Step 9: Update Linear Issue
- Mark TRA-44 as complete
- Add comment with sheet link
- Note cohort logic verification results

## Acceptance Criteria
- [ ] Dashboard created with proper structure
- [ ] Cohort analysis implemented
- [ ] Funnel analysis implemented
- [ ] Formulas implemented correctly
- [ ] Connected to base data tabs (TRA-41)
- [ ] Cohort logic verified
- [ ] Visualizations added
- [ ] Sheet accessible to team
- [ ] Linear issue updated

## Dependencies
- TRA-41: Base Data Tabs (Contacts and Events)
- Google Sheets API access
- Linear API access
- Cohort and funnel definitions from task requirements

## Notes
- Cohort analysis can be complex - ensure date grouping is correct
- Funnel stages should match actual customer journey
- Consider time-based cohorts vs. event-based cohorts
- May need to handle edge cases (contacts in multiple cohorts, etc.)
