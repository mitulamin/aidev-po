# 08 — Functional Specification Document (FSD): Lantern Lane Tool Library — Loans & Reservations

> Fictional demo. Lantern Lane Tool Library, its people and its data are invented for the aidev-po worked example. Items tagged Simulated come from simulated personas and are not evidence; every other tag is used as it would be in a real product, inside the fiction.

- **Product slug**: `tool-library-loans`
- **Stage**: `fsd`
- **Standard**: One-Page PRD + ISO/IEC/IEEE 29148 + INVEST/Given-When-Then/EARS + ISO/IEC 25010
- **Status**: `gate-approved` (reopened and approved again by rerun RR-001 on 2026-11-12: `US-007`, `AC-011`, `REQ-004` rebuilt; `AC-014`, `REQ-008` added)
- **Run ID**: `run-20261102093000-8b08`; rerun `run-20261112093000-9c09`
- **Register**: `.po/register.jsonl`
<!-- TRACE_RESERVE: item_id_prefixes=FSD,US,REQ,NFR,AC; trace_file=.po/traces.jsonl; fields=item_id,run,stage,agent,step,skill_versions,template_versions,upstream_ids,evidence_tag,register_refs -->

---

## Part 0 — One-Page PRD (Executive Summary)

- **Problem (`FSD-001`)**: loans live on paper cards and a shared spreadsheet; overdue tools go unnoticed and the coordinator spends about three hours a week phoning borrowers. `[Stated — IDEA-001, IDEA-002; Validated — AUD-003]`
- **Target Audience & Actors (`FSD-002`)**: about 310 members (primary), 14 desk volunteers (operators), the coordinator (administrator), the treasurer (read-only reports). `[Stated — AUD-001, ACT-001 to ACT-013]`
- **Desired Outcome & Success Metrics (`FSD-003`)**: loans more than a week overdue fall from about 12 to 4 or fewer a month by the end of the first season; no member reports a wasted trip in the end-of-season survey. `[Assumed — AUD-007, r-20261005104001-200c]`
- **Solution Summary — Slice 1 Only (`FSD-004`)**: catalogue with availability and 48-hour holds; desk check-out and check-in with deposits; reminder and overdue emails; overdue dashboard; the late-return house rule (`SCP-010`); one-off import from the spreadsheet. `[Inferred — SCP-005 to SCP-011]`
- **Explicit Non-Goals (`FSD-005`)**: `PARK-001` online deposits, `PARK-002` SMS, `PARK-003` member self-edit, `PARK-004` barcodes, `PARK-005` condition photos, `PARK-006` delivery, `PARK-007` offline mode, `PARK-008` funder report, `PARK-009` second site; each with a revisit trigger in its stage file.
- **Key Risks & Dependencies (`FSD-006`)**: volunteers drifting back to paper (tested, `WKS-004`); duplicate members before import (`FSD-015`); email deliverability from the library mailbox (`SYS-014`).
- **Locked Decisions Summary (`FSD-007`)**: `DEC-001` to `DEC-009` bind this specification.

---

## 1. Purpose & Scope (ISO/IEC/IEEE 29148 §5.1–5.2)

- **1.1 Product Identification & Purpose (`FSD-008`)**: "Lantern Lane Loans", a web app for a volunteer-run tool library to lend tools, take holds and remind borrowers. `[Inferred — IDEA-008, SYS-001]`
- **1.2 System Boundaries (`FSD-009`)**: in scope, Slice 1 (`SCP-005` to `SCP-011`). Out of scope, every `PARK-NNN` above and membership administration beyond what loans need (`DEC-001`). `[Stated — DEC-001, DEC-006]`

## 2. Product Perspective (ISO/IEC/IEEE 29148 §5.3)

- **2.1 System Context (`FSD-010`)**: see `04-systems.md`, `SYS-001` to `SYS-006`. `[Inferred — SYS-001]`
- **2.2 External Interfaces & Failure Modes (`FSD-011`)**: one-off CSV import with all-or-nothing validation (`SYS-004`); outbound SMTP through the library mailbox, three retries then a dashboard alert (`SYS-005`). `[Assumed — r-20261016113001-2030, r-20261005104004-200f]`
- **2.3 Operational & Deployment Constraints (`FSD-012`)**: runs in a current phone or tablet browser; the desk tablet uses the hall Wi-Fi; no app-store app. `[Assumed — r-20261102140003-205d]`

## 3. User Characteristics & Roles (ISO/IEC/IEEE 29148 §5.4)

| Actor ID | Role | Goals & Context | Permissions / Forbidden Actions | Evidence Tag & Source | Upstream IDs |
| --- | --- | --- | --- | --- | --- |
| `ACT-006` | Coordinator | Sees overdue loans and review flags; administers. | Everything, including deposit waivers and suspensions. | `[Stated]` | `03-actors.md` |
| `ACT-007` | Desk volunteer | Checks out and in on the tablet, Saturdays. | No refunds, waivers, suspensions or membership changes. | `[Stated]` | `03-actors.md` |
| `ACT-008` | Member | Browses, holds, borrows on their own phone. | Own loans and reservations only. | `[Stated / Assumed]` | `03-actors.md` |
| `ACT-012` | Treasurer | Reconciles deposits monthly. | Read-only deposit report. | `[Stated]` | `03-actors.md` |

## 4. Constraints, Assumptions & Dependencies (ISO/IEC/IEEE 29148 §5.5)

| ID | Type | Statement | Register ID | Evidence Tag |
| --- | --- | --- | --- | --- |
| `FSD-013` | Constraint | Release 1 is built within the £6,000 grant and live before 2027-03-01 (`SCP-001`). | `r-20261005090800-2004` | `[Stated]` |
| `FSD-014` | Assumption | Hosting and running costs stay under £30 a month. | `r-20261102140000-205a` | `[Assumed]` |
| `FSD-015` | Dependency | The coordinator merges about 25 duplicate member rows before the import (`WKS-006`). | `r-20261016113002-2031` | `[Stated]` |

## 5. Specific Functional Requirements & INVEST User Stories

### 5.1 User Stories (INVEST) & Acceptance Criteria (Given/When/Then)

#### `US-001`: Browse the catalogue with availability
- **Story**: As a member (`ACT-008`), I want to see which tools are in right now, so that I do not make a wasted trip.
- **Upstream**: `SCP-005`, `ACT-011` | **Evidence**: `[Inferred]`
- **INVEST check**: `PASS`
- **Acceptance Criteria**:
  - `AC-001`: Given a drill is checked in, When a member opens its catalogue page, Then it shows "In" and a Reserve button.
  - `AC-002`: Given a drill is on loan, When a member opens its page, Then it shows "Out" and its due date, and no member's name.

#### `US-002`: Reserve a tool for 48 hours
- **Story**: As a member, I want to hold a tool that is in, so that it is still there when I arrive.
- **Upstream**: `SCP-006`, `SYS-008`, `DEC-004` | **Evidence**: `[Stated — r-20261016113000-202f]`
- **INVEST check**: `PASS`
- **Acceptance Criteria**:
  - `AC-003`: Given a tool is in, When a member reserves it, Then it shows "Held" to everyone else and the member gets a confirmation email.
  - `AC-004`: Given a reservation is 48 hours old and not collected, When the hourly check runs, Then the hold is released, the tool shows "In", and the member is emailed.

#### `US-003`: Check a tool out at the desk
- **Story**: As a desk volunteer (`ACT-007`), I want to check a tool out on the tablet in one step, so that I record the loan once.
- **Upstream**: `SCP-007`, `SYS-009`, `ACT-010` | **Evidence**: `[Inferred; Validated — WKS-004]`
- **INVEST check**: `PASS`
- **Acceptance Criteria**:
  - `AC-005`: Given a power tool with a £20 deposit, When a volunteer checks it out, Then the check-out cannot finish until a £20 cash deposit is recorded.
  - `AC-006`: Given a volunteer is logged in, When they try to waive a deposit, Then the waiver is not offered; when the coordinator waives one, a reason is required.

#### `US-004`: Check a tool in and record late returns
- **Story**: As a desk volunteer, I want checking a tool in to record whether it was late, so that nobody has to work it out later.
- **Upstream**: `SCP-007`, `SYS-011` | **Evidence**: `[Inferred]`
- **INVEST check**: `PASS`
- **Acceptance Criteria**:
  - `AC-007`: Given a loan due on Saturday, When it is checked in the following Monday, Then a late return is recorded against the member with both dates.

#### `US-005`: Reminder and overdue emails
- **Story**: As a member, I want an email before my loan is due and if it is late, so that I bring it back on time.
- **Upstream**: `SCP-008`, `SYS-010` | **Evidence**: `[Inferred]`
- **INVEST check**: `PASS`
- **Acceptance Criteria**:
  - `AC-008`: Given a loan is due tomorrow, When the daily run happens at 09:00, Then the member gets one reminder email naming the tool and the due date.
  - `AC-009`: Given the mailbox rejects a send three times, When the last retry fails, Then the coordinator's dashboard lists the email, the member and the error.

#### `US-006`: Overdue dashboard
- **Story**: As the coordinator (`ACT-006`), I want one page listing every overdue loan, so that I stop searching the spreadsheet.
- **Upstream**: `SCP-009`, `ACT-009` | **Evidence**: `[Inferred]`
- **INVEST check**: `PASS`
- **Acceptance Criteria**:
  - `AC-010`: Given three loans are overdue, When the coordinator opens the dashboard, Then all three are listed, oldest first, with the member's phone number and email.

#### `US-007`: Review a member's third late return
- **Story**: As the coordinator, I want a member's third late return in 12 months flagged for my review, so that I can speak to them before deciding on any suspension.
- **Upstream**: `SCP-010`, `SYS-012` | **Evidence**: `[Stated — r-20261112090500-2069]`
- **INVEST check**: `PASS`
- **Acceptance Criteria**:
  - `AC-011`: Given a member has two late returns in the last 12 months, When a third late return is checked in, Then the member is flagged on the coordinator's dashboard, their borrowing is not blocked, and no email about suspension is sent.
  - `AC-014`: Given a flagged member, When the coordinator records a suspension with a reason and an end date, Then the member cannot borrow until that date and the flag is cleared.

#### `US-008`: Import from the spreadsheet
- **Story**: As the coordinator, I want to import members, tools and open loans once, so that nobody re-keys them.
- **Upstream**: `SCP-011`, `SYS-004` | **Evidence**: `[Inferred]`
- **INVEST check**: `PASS`
- **Acceptance Criteria**:
  - `AC-012`: Given a cleaned CSV export, When the coordinator imports it, Then every valid row is created and a summary shows the counts.
  - `AC-013`: Given a CSV with one invalid row, When the coordinator imports it, Then nothing is imported and the invalid row is listed with the reason.

### 5.2 System & Edge-Case Requirements (EARS)

| ID | EARS Pattern | Requirement | Evidence Tag & Source | Upstream IDs |
| --- | --- | --- | --- | --- |
| `REQ-001` | Event-driven | When a reservation has not been collected within 48 hours, the system shall release it and email the member. | `[Stated — r-20261016113000-202f]` | `US-002`, `SYS-008` |
| `REQ-002` | Event-driven | When a loan is due the next day, the system shall send the member one reminder email at 09:00. | `[Inferred]` | `US-005`, `SYS-010` |
| `REQ-003` | Event-driven | When a loan is one day overdue, the system shall send the member one overdue email at 09:00. | `[Inferred]` | `US-005`, `SYS-010` |
| `REQ-004` | Event-driven | When a member's third late return within 12 months is recorded, the system shall flag the member for the coordinator's review and shall not change the member's borrowing status. | `[Stated — r-20261112090500-2069]` | `US-007`, `SYS-012` |
| `REQ-005` | Unwanted behaviour | If an email send fails three times within an hour, then the system shall list the email, the member and the error on the coordinator's dashboard. | `[Assumed — r-20261016113001-2030]` | `US-005`, `SYS-005` |
| `REQ-006` | Optional feature | Where a tool is marked as a power tool, the system shall not complete a check-out until a deposit is recorded or waived by the coordinator. | `[Stated — r-20261005090900-2005]` | `US-003`, `SYS-009` |
| `REQ-007` | Ubiquitous | The system shall let only the coordinator waive a deposit, and shall record her reason. | `[Stated — WKS-005]` | `WKS-005`, `DEC-007` |
| `REQ-008` | Ubiquitous | The system shall let only the coordinator set or lift a suspension, with a reason and an end date no more than 30 days ahead. | `[Stated — r-20261112090500-2069]` | `US-007`, `SYS-018`, `ACT-009` |

## 6. Non-Functional Requirements — ISO/IEC 25010 Quality Matrix

| ID | ISO 25010 Characteristic | Target Metric & Condition | Verification Method | Evidence Tag & Source | Upstream IDs |
| --- | --- | --- | --- | --- | --- |
| `NFR-001` | Functional Suitability | Every Slice 1 acceptance criterion passes before launch. | Acceptance test run | `[Inferred]` | `US-001`, `US-008` |
| `NFR-002` | Performance Efficiency | A check-out completes within 2 seconds of the volunteer confirming, on the hall Wi-Fi. | Timed test at the desk | `[Inferred — WKS-004]` | `WKS-004` |
| `NFR-003` | Compatibility | Works in the current and previous major versions of the common phone and tablet browsers. | Browser test matrix | `[Assumed — r-20261102140003-205d]` | `FSD-012` |
| `NFR-004` | Interaction Capability / Usability | A first-time volunteer completes a check-out in under 2 minutes; text scales to 200% without loss. | Repeat the workshop timing; accessibility check | `[Validated — WKS-004]` | `WKS-004`, `ACT-007` |
| `NFR-005` | Reliability | Reminder emails for a day are sent by 10:00 on 99% of days in a season. | Send log review monthly | `[Inferred]` | `REQ-002` |
| `NFR-006` | Security | Each person has their own login (`DEC-003`); members see only their own loans; volunteer and coordinator actions are logged with who and when. | Role-based test cases; log review | `[Stated — DEC-003, ACT-011]` | `ACT-009`, `ACT-010`, `ACT-011` |
| `NFR-007` | Maintainability | A volunteer developer can change the email wording without a code change. | Walkthrough with the build team | `[Inferred]` | `REQ-002` |
| `NFR-008` | Flexibility / Portability | Data can be exported to CSV at any time. | Export test | `[Inferred]` | `SYS-004` |
| `NFR-009` | Safety | `N/A — no physical or safety-critical function; tool safety stays with the desk briefing.` | Not applicable | `[Inferred]` | `FSD-009` |

## 7. Verification & Traceability Matrix

| Upstream ID | FSD Item | Acceptance / Verification | Evidence Tag |
| --- | --- | --- | --- |
| `SCP-005` | `US-001` | `AC-001`, `AC-002` | `[Inferred]` |
| `SCP-006` | `US-002`, `REQ-001` | `AC-003`, `AC-004` | `[Stated]` |
| `SCP-007` | `US-003`, `US-004`, `REQ-006`, `REQ-007` | `AC-005`, `AC-006`, `AC-007` | `[Inferred]` |
| `SCP-008` | `US-005`, `REQ-002`, `REQ-003`, `REQ-005` | `AC-008`, `AC-009` | `[Inferred]` |
| `SCP-009` | `US-006` | `AC-010` | `[Inferred]` |
| `SCP-010` | `US-007`, `REQ-004`, `REQ-008` | `AC-011`, `AC-014` | `[Stated]` |
| `SCP-011` | `US-008` | `AC-012`, `AC-013` | `[Inferred]` |

## 8. Decision Sheet (Locked)

| Decision ID | Choice | Who Decided | Why | Register ID |
| --- | --- | --- | --- | --- |
| `DEC-009` | Release 1 sends email only; SMS stays parked (`PARK-002`). | `user` | No evidence yet that members lack email; SMS costs per message. | `r-20261103100100-2060` |

## 9. Parked Items & Explicit Non-Goals

| Park ID | Item | Why It Can Wait | Revisit Trigger | Register ID |
| --- | --- | --- | --- | --- |
| `PARK-009` | A second lending site | There is one site and no plan for another. | The board agrees to open a second site. | `r-20261102140002-205c` |

## Assumptions and open questions

=== REGISTER REQUESTS ===
[ASSUMPTION: Hosting and running costs stay under £30 a month.]
[QUESTION: Email only for Release 1? Recommend: yes; SMS stays parked (PARK-002).]
[QUESTION: Support a second lending site? Recommend: no; park.]
[ASSUMPTION: Members use current phone browsers; no app-store app is needed.]
=== END REGISTER REQUESTS ===
