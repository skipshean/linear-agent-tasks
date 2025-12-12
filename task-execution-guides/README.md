# Task Execution Guides

This directory contains detailed execution guides for each High and Medium Priority agent task from the approved plan.

## Quick Reference

### Documentation Tasks
- [TRA-56](TRA-56-lifecycle-states.md) - Document all lifecycle states in Google Doc
- [TRA-54](TRA-54-SOP-manual.md) - Create "AC Operations SOP Manual" in Google Docs
- [TRA-109](TRA-54-SOP-manual.md#step-4-coordinate-with-subtasks) - Paste structure from SOP section (subtask of TRA-54)

### Foundation Tasks
- [TRA-41](TRA-41-base-data-tabs.md) - Build Base Data Tabs (Contacts, Events, Subscriptions)
- [TRA-59](TRA-59-create-tags.md) - Create all tags from master list
- [TRA-60](TRA-59-create-tags.md#step-3-prepare-tag-list) - Group tags using bracket naming (coordinate with TRA-59)

### Dashboard Tasks
- TRA-42: Build Engagement Dashboard (guide needed)
- TRA-43: Build Revenue Dashboard (guide needed)
- TRA-44: Build Cohort & Funnel Dashboard (guide needed)
- TRA-45: Build Intent Radar Dashboard (guide needed)
- TRA-46: Build Automation Performance Dashboard (guide needed)
- TRA-47: Build Suppression & Hygiene Monitor Dashboard (guide needed)
- TRA-48: Build Weekly Executive Summary Dashboard (guide needed)

### Forecast Tasks
- [TRA-49](TRA-49-forecast-sheet.md) - Implement Intent-Based MRR Forecast Sheet
- [TRA-106, TRA-107, TRA-108](TRA-106-107-108-forecast-subtasks.md) - Forecast subtasks

### Configuration Tasks
- [TRA-63, TRA-64](TRA-63-64-config-tasks.md) - Add emails and tag triggers
- [TRA-65](TRA-65-add-goal.md) - Add goal "Became Customer During Onboard"

### Medium Priority Tasks
- TRA-40: Connect AC & Stripe Data to Sheets (guide needed)
- TRA-51: Implement Global Naming Conventions (guide needed)
- TRA-52: Validate SPF/DKIM/DMARC (guide needed)
- TRA-53: Confirm AC Site Tracking (guide needed)

## Execution Order

### Phase 1: Quick Wins
1. TRA-56: Document lifecycle states
2. TRA-65: Add goal
3. TRA-109: Paste SOP structure
4. TRA-54: Create SOP Manual

### Phase 2: Foundation
1. TRA-41: Base Data Tabs (enables all dashboards)
2. TRA-59: Create tags
3. TRA-60: Bracket naming (coordinate with TRA-59)

### Phase 3: Dashboards
1. TRA-42-48: Build all dashboards (in parallel after TRA-41)

### Phase 4: Forecast
1. TRA-49: Forecast sheet structure
2. TRA-106: Add counts
3. TRA-107: Apply weights
4. TRA-108: Calculate forecast

### Phase 5: Configuration
1. TRA-63: Add emails
2. TRA-64: Add tag triggers
3. TRA-40: Data connection
4. TRA-51: Naming conventions
5. TRA-52: Domain validation
6. TRA-53: Tracking verification

## Guide Structure

Each guide includes:
- Task details (priority, complexity, type)
- Requirements
- Step-by-step execution instructions
- Acceptance criteria
- Dependencies
- Notes and considerations

## Usage

1. Review the guide for your task
2. Fetch task details from Linear
3. Gather required data sources
4. Execute steps in order
5. Verify acceptance criteria
6. Update Linear issue

## See Also

- [Execution Plan](../execution-plan.md) - Overall execution strategy
- [Execution Requirements](../execution-requirements.md) - API setup and prerequisites
- [Agent Task Analysis](../agent-task-analysis.md) - Original task analysis and prioritization
