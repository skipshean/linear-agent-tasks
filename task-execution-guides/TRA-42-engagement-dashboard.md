# TRA-42: Build Engagement Dashboard

## Task Details
- **Priority:** High (Score: 4/5)
- **Complexity:** Medium
- **Type:** Data & Analytics
- **Dependency:** Requires TRA-41 (Base Data Tabs)

## Requirements
- Create Engagement Dashboard in Google Sheets
- Formulas and structure clearly defined
- Track engagement metrics
- Data accuracy needs verification

## Execution Steps

### Step 1: Fetch Task Details from Linear
- Get dashboard specifications
- Get formula definitions
- Get metric calculations
- Understand data sources

### Step 2: Design Dashboard Structure

#### Engagement Metrics to Track
- Email open rates
- Email click rates
- Website visit frequency
- Event engagement (form submissions, downloads, etc.)
- Last activity date
- Engagement score/segment

#### Dashboard Layout
```
# Engagement Dashboard

## Summary Metrics
- Total Active Contacts
- Average Engagement Score
- Email Open Rate (30 days)
- Email Click Rate (30 days)
- Website Visit Rate (30 days)

## Engagement Segments
- Highly Engaged (count, %)
- Moderately Engaged (count, %)
- Low Engagement (count, %)
- Inactive (count, %)

## Trends
- Engagement over time (chart)
- Segment distribution (chart)

## Detailed View
- Contact-level engagement data
```

### Step 3: Create Dashboard Sheet
- Use Google Sheets API to create new sheet or add tab
- Set up structure with summary metrics at top
- Create sections for segments and trends
- Add formulas for calculations

### Step 4: Implement Formulas
- Engagement Score Calculation:
  - Formula based on email opens, clicks, website visits, events
  - Weight different activities
- Segment Classification:
  - COUNTIF formulas based on engagement score thresholds
  - Percentage calculations
- Rate Calculations:
  - Email open rate: Opens / Sends
  - Click rate: Clicks / Opens
  - Visit rate: Visitors / Total contacts

### Step 5: Connect to Base Data (TRA-41)
- Reference Contacts tab for contact data
- Reference Events tab for engagement events
- Use formulas to pull and aggregate data
- Set up data refresh mechanism

### Step 6: Add Visualizations
- Create charts for trends
- Add conditional formatting for engagement segments
- Format dashboard professionally

### Step 7: Verify Data Accuracy
- Test formulas with sample data
- Verify calculations match expected results
- Check data connections to base tabs

### Step 8: Update Linear Issue
- Mark TRA-42 as complete
- Add comment with sheet link
- Note any data accuracy concerns

## Acceptance Criteria
- [ ] Dashboard created with proper structure
- [ ] All engagement metrics calculated
- [ ] Formulas implemented correctly
- [ ] Connected to base data tabs (TRA-41)
- [ ] Visualizations added
- [ ] Data accuracy verified
- [ ] Sheet accessible to team
- [ ] Linear issue updated

## Dependencies
- TRA-41: Base Data Tabs (must complete first)
- Google Sheets API access
- Linear API access
- Dashboard specifications from task requirements

## Notes
- Dashboard should update automatically as base data refreshes
- Consider data refresh frequency
- May need to adjust formulas based on actual data structure
- Engagement scoring algorithm should be documented
