# Duplicate Issue Tracking

**Purpose:** Track potential duplicate issues from Fireflies integration and other sources.

---

## Confirmed Fireflies Issues

| Issue ID | Title | Fireflies Link | Created | Status | Notes |
|----------|-------|----------------|---------|--------|-------|
| COOS-8 | Build the new ActiveCampaign newsletter template | https://app.fireflies.ai/view/01K8NS2WS7HTJDV3HNA2B22SPP | 2025-10-28 | Todo | Meeting: "CooS weekly newsletter new process" | ✅ Tagged with "fireflies" label 2025-12-12 |

---

## Potential Duplicates (Need Review)

### Duplicate Review Results (2025-12-12):

**COOS-8 Review:**
- ✅ Searched Linear for: "newsletter", "ActiveCampaign template", "CooS"
- ✅ Reviewed issues created on same day (2025-10-28)
- ✅ Result: No duplicates found. COOS-8 is unique.
- ✅ Related issues from same meeting (COOS-1, COOS-2, COOS-3, COOS-5, COOS-7, COOS-9) have different tasks

### Duplicate Review Results (2025-12-12 - Comprehensive Review with Business Plan):

**Review Scope:** Analyzed all issues from last 30 days (Nov 12 - Dec 12, 2025) focusing on:
- Fireflies-created issues from same meetings
- Issues with similar titles/descriptions
- Issues created on same day with overlapping keywords

**⚠️ POTENTIAL DUPLICATES FOUND:**

**1. 16W-521 vs 16W-527** ⚠️ **LIKELY DUPLICATE**
- **16W-521:** "Guide Suzanna on website backend editing, schema markup setup, and SEO improvements"
- **16W-527:** "Assist Suzanna in analyzing and fixing website backend schema and SEO improvements after admin access is granted"
- **Evidence:**
  - Same meeting: "Meeting with Skip Shean" (Dec 9, 2025 9:59 AM CST)
  - Same Fireflies link: https://app.fireflies.ai/view/01KC1XE326EMC2GS2WJAAC99HH
  - Same "Time Mentioned": 07:44
  - Both mention: Suzanna, website backend, schema markup, SEO improvements
  - Created within 1 minute of each other (17:34:13 vs 17:35:26)
- **Recommendation:** Mark as duplicate using Issue Relations. Keep 16W-527 as canonical (more specific, mentions admin access condition). Merge 16W-521 into 16W-527.

**2. Related but NOT duplicates:**
- **16W-460** (Dec 3): "Analyze Suzanna's website AI optimization..." - Different meeting, broader scope, earlier date - likely precursor task
- **16W-585** (Dec 12): "Assist with setting up FAQ schema markup..." - Different meeting, more specific (FAQ schema only)
- Issues from Dec 12 meeting (16W-581 through 16W-588) - All from same meeting but have distinct, non-overlapping tasks

**Action Required:**
- [x] Review 16W-521 and 16W-527 to confirm they are duplicates ✅ Confirmed 2025-12-12
- [x] Status updated to "Duplicate" ✅ Completed 2025-12-12
- [x] Comment added to 16W-521 documenting duplicate relationship ✅ Completed 2025-12-12
- [ ] **TODO:** Use Issue Relations in Linear UI to link 16W-521 → 16W-527 (press `M` + `M` on 16W-521, select 16W-527) to complete the relation and enable merge

### To Review Manually (Future):

2. **Similar Titles Pattern**
   - Issues created on same day with similar titles
   - Issues with identical descriptions but different IDs

---

## Linear's Automatic Duplicate Detection Features

Linear offers several built-in features to automatically detect and manage duplicate issues:

### 1. Similar Issues Detection (Available to All Plans)
- **What it does:** When creating a new issue, Linear's AI automatically analyzes the title and description to find similar existing issues
- **How it works:** Suggestions appear under the issue modal as you type
- **Action:** Review suggested issues before saving - you can convert your new issue draft into a comment on the existing issue
- **Best practice:** Always check Similar Issues suggestions before creating new issues, especially from Fireflies

### 2. Triage Intelligence (Business & Enterprise Plans Only)
- **What it does:** Automatically analyzes incoming issues and suggests properties, relationships, and potential duplicates
- **How it works:** Uses AI to assess new issues as they're created and suggests duplicate relationships
- **Action:** Review suggestions in the triage view and accept/reject duplicate relationships
- **Availability:** Requires Business or Enterprise plan subscription

### 3. Issue Relations - Merge Duplicates
- **What it does:** Allows you to merge duplicate issues into a canonical issue
- **How it works:** 
  - Mark issue as duplicate using Issue Relations
  - Press `M` then `M` keyboard shortcut to merge
  - Duplicate issue status automatically changes to "Canceled"
  - All comments, attachments, and relationships are preserved
- **Best practice:** Always merge duplicates rather than just linking them to keep the issue tracker clean

### 4. Third-Party Integrations
- **DryMerge:** Cross-references new issues with existing data to identify duplicates and send notifications
- **Other automation tools:** Can use Linear API to detect duplicates based on custom rules

### Recommended Workflow:
1. **Prevention:** When creating issues (especially from Fireflies), check Similar Issues suggestions first
2. **Detection:** Use Triage Intelligence (if available) to catch duplicates automatically
3. **Resolution:** Use Issue Relations (`M` + `M`) to merge duplicates into canonical issues
4. **Review:** Weekly manual audit to catch any duplicates that slipped through

## Duplicate Detection Strategy

### Manual Review Process:

1. **Weekly Review:**
   - Review all new issues created in past week
   - Look for similar titles/descriptions
   - Check creation dates (same-day duplicates likely)

2. **Fireflies Pattern Detection:**
   - Issues with meeting links in description
   - Issues with "Time Mentioned" metadata
   - Issues with "Meeting Details" sections

3. **Title Similarity:**
   - Use Linear's Similar Issues Detection (AI-powered, appears when creating issues)
   - Use Linear's Triage Intelligence (Business/Enterprise plans) for automatic suggestions
   - Manually compare similar-sounding titles
   - Check if tasks are actually different or duplicates

### Marking Duplicates (Reversible Method):

**Option 1: Use Labels**
- Create "duplicate" label
- Create "original" label
- Tag duplicates with "duplicate" + link to original

**Option 2: Use Comments**
- Add comment: "Potential duplicate of [ISSUE-ID]"
- Link to original issue
- Can be removed if not actually duplicate

**Option 3: Use Issue Relations** ⭐ **PREFERRED METHOD**
- Link issues as "duplicates" relation
- **Merge duplicates:** Press `M` then `M` to merge duplicate into canonical issue
- Merging automatically changes duplicate's status to "Canceled"
- Linear will show relationship in the issue view
- Can be unlinked if needed
- Uses Linear's native duplicate relationship feature

**Selected Method:** Option 3 (Issue Relations) - Use Linear's built-in "duplicates" relationship to link and merge duplicate issues. To merge: press `M` then `M` on the duplicate issue. This is the preferred approach for all future duplicate marking and combining.

---

## Fireflies Integration Recommendations

### Important Note:
Fireflies.ai does not currently offer built-in duplicate detection for action items or Linear issues. Duplicate detection must be handled through Linear's built-in features or manual processes.

### Settings to Configure:

1. **In Fireflies:**
   - Note: Fireflies does not have built-in duplicate detection for action items
   - Review action items before they sync to Linear
   - Manually merge or delete duplicate action items in Fireflies if found

2. **In Linear:**
   - Create "fireflies" label ✅ Done
   - Create "duplicate" and "original" labels ✅ Done (available if needed, but prefer Issue Relations)
   - Use Issue Relations "duplicates" for marking and merging duplicates (preferred method)
   - **Similar Issues Detection:** When creating new issues, Linear's AI will automatically suggest similar existing issues - review these before saving
   - **Triage Intelligence:** (Business/Enterprise plans only) Automatically suggests duplicates and properties for incoming issues
   - **Merge duplicates:** Use `M` + `M` keyboard shortcut to merge duplicate into canonical issue
   - Consider third-party integrations like DryMerge for automated duplicate detection and notifications

3. **Process:**
   - Review Fireflies action items before they create Linear issues
   - After issues are created, use manual review process (see below) to identify duplicates
   - Weekly audit of new issues to catch duplicates
   - Use Linear Issue Relations to link duplicates when found

---

## Action Items

- [x] Create "fireflies" label in Linear ✅ Completed 2025-12-12
- [x] Create "duplicate" and "original" labels ✅ Completed 2025-12-12
- [x] Review COOS-8 for duplicates ✅ Completed 2025-12-12 - No duplicates found
- [x] Tag COOS-8 with fireflies label ✅ Completed 2025-12-12
- [x] ~~Configure Fireflies duplicate detection~~ ✅ Not applicable - Fireflies doesn't have this feature
- [ ] Set up weekly duplicate review process (process documented, needs implementation)



