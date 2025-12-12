# TRA-41: Build Base Data Tabs (Contacts, Events, Subscriptions)

## Task Details
- **Priority:** High (Score: 4/5)
- **Complexity:** Medium
- **Type:** Data & Analytics
- **Foundation Task:** Yes (enables all other dashboards)

## Requirements
- Create Google Sheets with base data tabs
- Tabs: Contacts, Events, Subscriptions
- Clear schema defined
- Formula-based structure
- Ready for data connection

## Execution Steps

### Step 1: Fetch Task Details from Linear
- Get schema definitions, column requirements, formula specifications
- Understand data source connections (AC, Stripe, etc.)

### Step 2: Design Sheet Structure

#### Contacts Tab Schema
```
| Column | Type | Description | Source |
|--------|------|-------------|--------|
| Contact ID | Text | Unique identifier | AC |
| Email | Text | Email address | AC |
| First Name | Text | First name | AC |
| Last Name | Text | Last name | AC |
| Created Date | Date | Contact creation | AC |
| Last Activity | Date | Last activity date | AC |
| Lifecycle Stage | Text | Current lifecycle | AC |
| Tags | Text | Comma-separated tags | AC |
| Custom Fields | Various | Custom field values | AC |
```

#### Events Tab Schema
```
| Column | Type | Description | Source |
|--------|------|-------------|--------|
| Event ID | Text | Unique identifier | AC |
| Contact ID | Text | Related contact | AC |
| Event Type | Text | Event category | AC |
| Event Name | Text | Specific event | AC |
| Timestamp | DateTime | When occurred | AC |
| Properties | Text | JSON or key-value | AC |
```

#### Subscriptions Tab Schema
```
| Column | Type | Description | Source |
|--------|------|-------------|--------|
| Subscription ID | Text | Unique identifier | Stripe |
| Contact ID | Text | Related contact | AC |
| Customer ID | Text | Stripe customer | Stripe |
| Plan Name | Text | Subscription plan | Stripe |
| Status | Text | Active/Canceled/etc | Stripe |
| MRR | Number | Monthly recurring | Stripe |
| Created Date | Date | Start date | Stripe |
| Canceled Date | Date | End date | Stripe |
| Next Billing | Date | Next charge | Stripe |
```

### Step 3: Create Google Sheet
- Use Google Sheets API to create new spreadsheet
- Create three tabs: Contacts, Events, Subscriptions
- Set up column headers with proper formatting
- Apply data validation where appropriate
- Freeze header rows

### Step 4: Set Up Formulas (if specified)
- Add any required formulas for calculations
- Set up data validation rules
- Configure conditional formatting for data quality

### Step 5: Prepare for Data Connection
- Document data source locations
- Set up import formulas or connection placeholders
- Note: TRA-40 will handle actual data connection

### Step 6: Update Linear Issue
- Mark TRA-41 as complete
- Add comment with sheet link
- Note dependencies for TRA-40 (data connection)

## Acceptance Criteria
- [ ] Three tabs created: Contacts, Events, Subscriptions
- [ ] Schema matches requirements
- [ ] Headers formatted and frozen
- [ ] Ready for data connection (TRA-40)
- [ ] Sheet accessible to team
- [ ] Linear issue updated

## Dependencies
- TRA-40: Data connection (follows this task)
- All dashboard tasks (TRA-42 through TRA-48) depend on this
- Google Sheets API access
- Linear API access
- Schema definitions from task requirements

## Notes
- This is a foundation task - must complete before dashboards
- Data will be connected manually/CSV initially (TRA-40)
- May need to adjust schema based on actual data structure
- Consider data refresh frequency and automation
