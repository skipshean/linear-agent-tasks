# TRA-63 & TRA-64: Configuration Tasks

## TRA-63: Add 6 Emails (Copy Already Written)

### Task Details
- **Priority:** High (Score: 4/5)
- **Complexity:** Low
- **Type:** Configuration

### Requirements
- Add 6 emails to automation sequence
- Email copy already written
- Add to appropriate automation workflow

### Execution Steps
1. Fetch task details from Linear
   - Get email copy/content
   - Get automation workflow ID
   - Get email sequence order
2. Retrieve email content
   - Load 6 email copies
   - Verify content completeness
3. Add emails to ActiveCampaign automation
   - Use ActiveCampaign API to add email steps
   - Configure email content, subject lines
   - Set up timing/delays between emails
   - Position in automation sequence
4. Verify email configuration
   - Check email content matches requirements
   - Verify sequence order
   - Test email rendering
5. Update Linear issue
   - Mark TRA-63 as complete
   - Add comment with email IDs and automation details

### Acceptance Criteria
- [ ] All 6 emails added to automation
- [ ] Email content matches provided copy
- [ ] Sequence order correct
- [ ] Timing/delays configured
- [ ] Linear issue updated

---

## TRA-64: Add Upgrade Intent Tagging on Key Links

### Task Details
- **Priority:** High (Score: 4/5)
- **Complexity:** Low
- **Type:** Configuration

### Requirements
- Add tag triggers to key links
- Tag: "Upgrade Intent" (or similar)
- Identify which links need tagging

### Execution Steps
1. Fetch task details from Linear
   - Get list of key links to tag
   - Get tag name to apply
   - Get automation/workflow context
2. Identify links to tag
   - List of URLs/links that indicate upgrade intent
   - May include: pricing page, upgrade buttons, feature pages
3. Add tag triggers via ActiveCampaign API
   - Configure link tracking with tag trigger
   - Set up: When contact clicks link → Apply tag
   - Add to appropriate automations/emails
4. Verify tag triggers
   - Test link clicks trigger tag
   - Verify tag name correct
   - Check automation flow
5. Update Linear issue
   - Mark TRA-64 as complete
   - Add comment with tagged links and tag name

### Acceptance Criteria
- [ ] All key links have tag triggers
- [ ] Tag name matches requirements
- [ ] Triggers work correctly
- [ ] Links identified and documented
- [ ] Linear issue updated

---

## Combined Notes

### Dependencies
- ActiveCampaign API access
- Automation workflow access
- Email content/copy
- List of key links
- Linear API access

### Common Considerations
- Both tasks involve ActiveCampaign automation configuration
- May need to coordinate if emails contain the tagged links
- Verify API rate limits for bulk operations
- Test configurations before marking complete
