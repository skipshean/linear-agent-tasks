# TRA-106, TRA-107, TRA-108: Forecast Subtasks

## Task Details
- **Parent:** TRA-49 (Intent-Based MRR Forecast)
- **Priority:** High (Score: 5/5 each)
- **Complexity:** Low
- **Type:** Data & Analytics

## TRA-106: Add Counts by Intent Segment

### Requirements
- Add COUNTIF formulas to count contacts by intent segment
- Simple formula addition task

### Execution Steps
1. Identify intent segment column in data
2. Add COUNTIF formulas for each segment
3. Formula format: `=COUNTIF(IntentColumn, "Segment Name")`
4. Update sheet with counts
5. Verify counts match data

### Acceptance Criteria
- [ ] COUNTIF formulas added for all intent segments
- [ ] Counts displayed correctly
- [ ] Formulas reference correct data range

---

## TRA-107: Apply Probability Weights from Drop 8

### Requirements
- Input probability weights from "Drop 8" data source
- Clear data input task

### Execution Steps
1. Retrieve probability weights from Drop 8 source
2. Create probability weights table in forecast sheet
3. Map weights to intent segments
4. Input values into sheet
5. Verify data accuracy

### Acceptance Criteria
- [ ] Probability weights table created
- [ ] All weights from Drop 8 applied
- [ ] Weights mapped to correct segments
- [ ] Data verified for accuracy

---

## TRA-108: Calculate 30-Day Forecasted MRR

### Requirements
- Implement forecast formula
- Calculate 30-day forecasted MRR based on intent segments and weights

### Execution Steps
1. Design forecast formula:
   - Formula: `SUM(Intent Segment Count × Probability Weight × Average MRR)`
   - Or: `SUMPRODUCT(Counts, Weights, MRR_Rates)`
2. Implement formula in forecast sheet
3. Calculate 30-day forecast
4. Add summary cell with total forecast
5. Verify calculation logic

### Acceptance Criteria
- [ ] Forecast formula implemented
- [ ] 30-day MRR forecast calculated
- [ ] Formula references correct data (counts, weights)
- [ ] Calculation verified

---

## Combined Execution Notes

### Dependencies
- TRA-49: Parent task (forecast sheet structure)
- Intent segment data available
- Probability weights from Drop 8
- Historical MRR data for validation

### Execution Order
1. TRA-106: Add counts (foundation data)
2. TRA-107: Apply weights (input data)
3. TRA-108: Calculate forecast (uses both above)

### Coordination
- All three tasks work on same forecast sheet
- Complete in sequence for proper dependencies
- Verify each step before moving to next
