# TRA-40, TRA-51, TRA-52, TRA-53: Medium Priority Tasks

## Overview
These tasks can be partially automated but require human review and approval for certain steps.

---

## TRA-40: Connect AC & Stripe Data to Sheets

### Task Details
- **Priority:** Medium (Score: 3/5)
- **Complexity:** Medium
- **Type:** Data & Analytics
- **Dependency:** Requires TRA-41 (Base Data Tabs structure)

### Requirements
- Connect ActiveCampaign and Stripe data to Google Sheets
- Manual/CSV export to start
- Create sheet structure, document process
- Initial data exports need manual steps

### Execution Steps

#### Automated Steps
1. Fetch task details from Linear
2. Document data export process
3. Create import templates in Sheets
4. Set up data connection structure
5. Create import formulas/scripts

#### Manual Steps Required
1. Export contacts from ActiveCampaign (CSV)
2. Export subscriptions from Stripe (CSV)
3. Upload CSVs to Google Sheets
4. Verify data import
5. Set up refresh schedule (manual or automated)

### Implementation
- Create import templates with proper column mapping
- Document CSV export steps for AC and Stripe
- Set up IMPORTRANGE or manual import process
- Create data validation and cleaning formulas
- Document refresh process

### Acceptance Criteria
- [ ] Sheet structure created
- [ ] Import templates ready
- [ ] Process documented
- [ ] Initial data imported (manual)
- [ ] Data connections verified
- [ ] Linear issue updated

### Dependencies
- TRA-41: Base Data Tabs (structure must exist)
- ActiveCampaign access for exports
- Stripe access for exports
- Google Sheets API access

### Notes
- This is a foundation task for dashboards
- Future automation can use APIs instead of CSV
- Document manual steps clearly for repeatability

---

## TRA-51: Implement Global Naming Conventions in AC

### Task Details
- **Priority:** Medium (Score: 3/5)
- **Complexity:** Medium
- **Type:** Configuration

### Requirements
- Implement global naming conventions across ActiveCampaign
- Can document and create mapping
- Bulk updates need verification
- Human review required

### Execution Steps

#### Automated Steps
1. Fetch task details (naming convention rules)
2. Query ActiveCampaign for all items (tags, lists, automations, etc.)
3. Create mapping document of items to rename
4. Generate rename plan
5. Document changes

#### Manual Steps Required
1. Review mapping document
2. Approve bulk changes
3. Verify renamed items
4. Test automations/workflows after rename

### Implementation
- Create naming convention rules document
- Query AC API for all items
- Compare current names to conventions
- Generate rename mapping
- Create bulk update script (with dry-run mode)
- Document all changes

### Acceptance Criteria
- [ ] Naming conventions documented
- [ ] Mapping document created
- [ ] Rename plan approved
- [ ] Bulk updates executed (with verification)
- [ ] Items verified after rename
- [ ] Linear issue updated

### Dependencies
- ActiveCampaign API access
- Naming convention rules
- Approval for bulk changes
- Linear API access

### Notes
- Coordinate with TRA-59/TRA-60 (tag naming)
- Use dry-run mode first
- Backup important items before bulk updates
- Test in staging if available

---

## TRA-52: Validate SPF/DKIM/DMARC & Domain Health

### Task Details
- **Priority:** Medium (Score: 3/5)
- **Complexity:** Medium
- **Type:** Infrastructure

### Requirements
- Validate email authentication records
- Can run checks and document
- DNS changes need approval

### Execution Steps

#### Automated Steps
1. Fetch task details (domains to check)
2. Run SPF validation tools
3. Run DKIM validation tools
4. Run DMARC validation tools
5. Check domain health (blacklists, reputation)
6. Document findings
7. Generate report

#### Manual Steps Required
1. Review validation findings
2. Approve DNS changes if needed
3. Implement DNS changes (or coordinate with IT)
4. Re-validate after changes

### Implementation
- Use DNS validation tools (dmarcian, MXToolbox, etc.)
- Check SPF records (syntax, includes, mechanisms)
- Check DKIM records (public keys, selectors)
- Check DMARC records (policy, reporting)
- Check domain reputation and blacklists
- Generate validation report
- Document recommended changes

### Acceptance Criteria
- [ ] SPF records validated
- [ ] DKIM records validated
- [ ] DMARC records validated
- [ ] Domain health checked
- [ ] Findings documented
- [ ] DNS changes approved and implemented (if needed)
- [ ] Re-validated after changes
- [ ] Linear issue updated

### Dependencies
- Domain access or DNS records
- DNS validation tools/APIs
- Approval for DNS changes
- Linear API access

### Notes
- DNS changes may require IT team coordination
- Document current state before making changes
- Some changes may have propagation delays
- Consider impact on email deliverability

---

## TRA-53: Confirm AC Site Tracking & Key Events

### Task Details
- **Priority:** Medium (Score: 3/5)
- **Complexity:** Medium
- **Type:** Configuration

### Requirements
- Verify ActiveCampaign site tracking setup
- Can verify setup, check tracking script
- Code changes need review

### Execution Steps

#### Automated Steps
1. Fetch task details (tracking requirements, key events)
2. Check if AC tracking script is installed
3. Verify tracking script configuration
4. Test tracking script functionality
5. Verify key events are firing
6. Document current setup
7. Generate verification report

#### Manual Steps Required
1. Review tracking setup
2. Approve code changes if needed
3. Implement code changes (or coordinate with dev team)
4. Test after changes
5. Verify events in AC dashboard

### Implementation
- Check for AC tracking script on website
- Verify script placement and configuration
- Test event tracking (page views, form submissions, etc.)
- Verify key events are configured in AC
- Check event data in AC dashboard
- Document tracking setup
- Identify any missing events or issues

### Acceptance Criteria
- [ ] AC tracking script verified
- [ ] Script configuration checked
- [ ] Key events verified
- [ ] Event data confirmed in AC
- [ ] Setup documented
- [ ] Code changes implemented (if needed)
- [ ] Tracking verified after changes
- [ ] Linear issue updated

### Dependencies
- Website access or codebase access
- ActiveCampaign dashboard access
- Key event definitions
- Approval for code changes
- Linear API access

### Notes
- May require coordination with development team
- Test in staging environment first if possible
- Document all tracking events for future reference
- Consider privacy/GDPR implications of tracking

---

## Common Patterns for Medium Priority Tasks

### Automation Boundaries
- **Can Automate:** Data gathering, validation, documentation, report generation
- **Requires Human:** Approvals, DNS changes, code changes, verification

### Execution Approach
1. Automate data gathering and analysis
2. Generate reports and recommendations
3. Present findings for human review
4. Execute approved changes
5. Verify and document results

### Risk Management
- Use dry-run modes where possible
- Document current state before changes
- Test in staging if available
- Get approvals before making changes
- Verify after changes
