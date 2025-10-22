# Planning Center People Analytics App - Project Plan

## Overview
Build a focused analytics application that integrates with the Planning Center People API to provide insights on volunteers and teams. The app features a Material Design 3 interface with teal and gray color scheme.

---

## Phase 1: Remove Services Functionality ✅
**Goal**: Clean up the codebase by removing all services-related code and pages.

- [x] Remove services page and services state
- [x] Remove services navigation item from sidebar
- [x] Update dashboard to focus only on people metrics
- [x] Clean up unused imports and references

---

## Phase 2: Implement Full API Pagination for People Data ✅
**Goal**: Add comprehensive pagination logic to fetch ALL people records from the Planning Center API, handling multiple pages automatically.

- [x] Implement paginated fetching in PeopleState to handle API pagination
- [x] Add logic to follow API pagination links and aggregate all results
- [x] Update fetch_all_people to loop through all pages until complete
- [x] Add progress indicators during multi-page data fetching
- [x] Test with real API to ensure all records are retrieved

---

## Phase 3: Enhanced People Analytics
**Goal**: Expand people analytics with more detailed insights now that services are removed.

- [ ] Add people growth charts showing new members over time
- [ ] Create detailed volunteer status breakdown (active, inactive, pending)
- [ ] Add search and filtering capabilities for the volunteer roster
- [ ] Implement sorting options (by name, join date, team)
- [ ] Add detailed person cards with more information on click

---

## Notes
- ✅ Removed all services-related functionality per user request
- ✅ Focus entirely on People and Teams analytics
- ✅ Implemented proper API pagination to fetch ALL records, not just first 100
- Planning Center API uses link-based pagination with 'next' URL in response
- Using async loops to efficiently handle multiple page requests