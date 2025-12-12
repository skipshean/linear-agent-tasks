# TRA-59: Create All Tags from Master List

## Task Details
- **Priority:** High (Score: 4/5)
- **Complexity:** Low-Medium
- **Type:** Tag & Naming
- **Parent:** TRA-23 (Finalize Tag Architecture)

## Requirements
- Create all tags from master list in ActiveCampaign
- Follow naming conventions
- Check for existing tags to avoid duplicates
- Coordinate with TRA-60 (bracket naming)

## Execution Steps

### Step 1: Fetch Task Details from Linear
- Get master tag list
- Get naming convention requirements
- Understand tag taxonomy structure

### Step 2: Retrieve Existing Tags
- Use ActiveCampaign API to list all existing tags
- Create mapping of existing tag names (case-insensitive check)
- Identify which tags already exist

### Step 3: Prepare Tag List
- Load master tag list
- Apply naming conventions
- Coordinate with TRA-60: Ensure bracket naming format `[Category] Tag Name`
- Filter out tags that already exist
- Create list of tags to create

### Step 4: Create Tags via ActiveCampaign API
- Batch create tags (respect API rate limits)
- Handle errors gracefully
- Log created tags vs skipped (duplicates)

### Step 5: Verify Tag Creation
- Query ActiveCampaign to confirm all tags created
- Verify naming conventions followed
- Check bracket naming for grouping (TRA-60)

### Step 6: Update Linear Issue
- Mark TRA-59 as complete
- Add comment with:
  - Number of tags created
  - Number of duplicates skipped
  - Tag list summary

## Acceptance Criteria
- [ ] All tags from master list created
- [ ] No duplicate tags created
- [ ] Naming conventions followed
- [ ] Bracket naming applied (coordinate with TRA-60)
- [ ] Linear issue updated

## Dependencies
- TRA-60: Bracket naming (should coordinate execution)
- TRA-23: Parent task (tag architecture)
- ActiveCampaign API access
- Master tag list
- Linear API access

## Important Notes
- **CRITICAL:** Check for existing tags with same name before creating
- Use case-insensitive comparison
- ActiveCampaign account: Trade Ideas
- Tags should use bracket naming: `[Category] Tag Name` for alphabetical grouping
- Respect API rate limits (batch operations)

## API Considerations
- ActiveCampaign API rate limits
- Batch operations for efficiency
- Error handling for duplicate detection
- Logging for audit trail
