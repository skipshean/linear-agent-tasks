# TRA-43: Build Revenue Dashboard

## Task Details
- **Priority:** High (Score: 4/5)
- **Complexity:** Medium
- **Type:** Data & Analytics
- **Dependency:** Requires TRA-41 (Base Data Tabs, specifically Subscriptions tab)

## Requirements
- Create Revenue Dashboard in Google Sheets
- Well-defined metrics and formulas
- Track revenue metrics from Stripe
- Validate Stripe data connections

## Execution Steps

### Step 1: Fetch Task Details from Linear
- Get revenue metric definitions
- Get formula specifications
- Understand Stripe data structure
- Get calculation requirements

### Step 2: Design Dashboard Structure

#### Revenue Metrics to Track
- MRR (Monthly Recurring Revenue)
- ARR (Annual Recurring Revenue)
- New MRR (this month)
- Churned MRR (this month)
- Net New MRR
- Revenue by plan/product
- Customer count
- Average revenue per customer (ARPU)
- Churn rate
- Revenue growth rate

#### Dashboard Layout
```
# Revenue Dashboard

## Summary Metrics
- Current MRR
- ARR
- Net New MRR (this month)
- Churn Rate (this month)
- Growth Rate (MoM)

## Revenue Breakdown
- MRR by Plan
- MRR by Customer Segment
- Revenue Trend (chart)

## Customer Metrics
- Total Customers
- New Customers (this month)
- Churned Customers (this month)
- ARPU

## Historical Trends
- MRR over time (chart)
- Churn over time (chart)
- Customer growth (chart)
```

### Step 3: Create Dashboard Sheet
- Use Google Sheets API to create new sheet or add tab
- Set up structure with summary metrics
- Create sections for breakdowns and trends
- Add formulas for calculations

### Step 4: Implement Formulas
- MRR Calculation:
  - SUM of all active subscription MRR values
  - Filter by status = 'active'
- ARR Calculation:
  - MRR × 12
- Net New MRR:
  - New MRR - Churned MRR
- Churn Rate:
  - Churned MRR / Starting MRR
- ARPU:
  - Total MRR / Active Customer Count

### Step 5: Connect to Base Data (TRA-41)
- Reference Subscriptions tab for revenue data
- Use formulas to aggregate subscription data
- Filter by status, date ranges
- Calculate monthly trends

### Step 6: Add Visualizations
- Create charts for revenue trends
- Add charts for churn analysis
- Format dashboard professionally
- Use conditional formatting for key metrics

### Step 7: Validate Stripe Data Connections
- Verify data is pulling from Subscriptions tab correctly
- Check data format matches expectations
- Test with sample data
- Document any data quality issues

### Step 8: Update Linear Issue
- Mark TRA-43 as complete
- Add comment with sheet link
- Note Stripe data connection status

## Acceptance Criteria
- [ ] Dashboard created with proper structure
- [ ] All revenue metrics calculated
- [ ] Formulas implemented correctly
- [ ] Connected to base data tabs (TRA-41 Subscriptions)
- [ ] Stripe data connections validated
- [ ] Visualizations added
- [ ] Sheet accessible to team
- [ ] Linear issue updated

## Dependencies
- TRA-41: Base Data Tabs (Subscriptions tab must exist)
- TRA-40: Data connection (may need Stripe data connected)
- Google Sheets API access
- Linear API access
- Stripe data structure understanding

## Notes
- Dashboard depends on Subscriptions tab having correct data structure
- May need to coordinate with TRA-40 for data connection
- Revenue calculations should handle edge cases (prorations, refunds, etc.)
- Consider timezone handling for monthly calculations
