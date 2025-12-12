# TRA-65: Add Goal "Became Customer During Onboard"

## Task Details
- **Priority:** High (Score: 5/5)
- **Complexity:** Low
- **Type:** Configuration

## Requirements
- Add goal to ActiveCampaign automation
- Goal name: "Became Customer During Onboard"
- Configure in appropriate automation workflow

## Execution Steps

### Step 1: Fetch Task Details from Linear
- Get automation workflow ID/name
- Get goal configuration details
- Understand trigger conditions

### Step 2: Identify Automation Workflow
- Find onboarding automation in ActiveCampaign
- Verify workflow structure
- Identify where goal should be added

### Step 3: Create Goal via ActiveCampaign API
- Create goal with name: "Became Customer During Onboard"
- Configure goal type (likely "Contact becomes customer" or custom)
- Set up trigger conditions if needed

### Step 4: Add Goal to Automation
- Add goal step to automation workflow
- Position appropriately in workflow sequence
- Configure conditions for goal completion

### Step 5: Verify Configuration
- Test goal trigger (if possible)
- Verify goal appears in automation
- Check goal tracking in reports

### Step 6: Update Linear Issue
- Mark TRA-65 as complete
- Add comment with goal ID and automation details

## Acceptance Criteria
- [ ] Goal created in ActiveCampaign
- [ ] Goal added to automation workflow
- [ ] Goal name matches: "Became Customer During Onboard"
- [ ] Goal triggers correctly
- [ ] Linear issue updated

## Dependencies
- ActiveCampaign API access
- Automation workflow access
- Linear API access

## Notes
- Simple configuration task
- Should be quick to complete
- May need to verify goal type options in ActiveCampaign
- Consider testing goal trigger after creation
