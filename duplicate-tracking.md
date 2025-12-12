# Duplicate Issue Tracking

**Purpose:** Track potential duplicate issues from Fireflies integration and other sources.

---

## Confirmed Fireflies Issues

| Issue ID | Title | Fireflies Link | Created | Status | Notes |
|----------|-------|----------------|---------|--------|-------|
| COOS-8 | Build the new ActiveCampaign newsletter template | https://app.fireflies.ai/view/01K8NS2WS7HTJDV3HNA2B22SPP | 2025-10-28 | Todo | Meeting: "CooS weekly newsletter new process" |

---

## Potential Duplicates (Need Review)

### To Review Manually:

1. **COOS Newsletter Tasks**
   - Search Linear for: "newsletter", "ActiveCampaign template", "CooS"
   - Check if COOS-8 has duplicates

2. **Similar Titles Pattern**
   - Issues created on same day with similar titles
   - Issues with identical descriptions but different IDs

---

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
   - Use Linear's built-in duplicate detection
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

**Option 3: Use Issue Relations**
- Link issues as "duplicates" relation
- Linear will show relationship
- Can be unlinked if needed

**Recommended:** Use Option 1 (Labels) + Option 3 (Relations) for best visibility and reversibility.

---

## Fireflies Integration Recommendations

### Settings to Configure:

1. **In Fireflies:**
   - Enable duplicate detection
   - Set similarity threshold to 80%
   - Review mode instead of auto-create

2. **In Linear:**
   - Create "fireflies" label
   - Create "duplicate" and "original" labels
   - Set up automation to flag potential duplicates

3. **Process:**
   - Review Fireflies action items before sync
   - Merge duplicates in Fireflies before creating Linear issues
   - Weekly audit of new issues

---

## Action Items

- [ ] Create "fireflies" label in Linear
- [ ] Create "duplicate" and "original" labels
- [ ] Review COOS-8 for duplicates
- [ ] Configure Fireflies duplicate detection
- [ ] Set up weekly duplicate review process

