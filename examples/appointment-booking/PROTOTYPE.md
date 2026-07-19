# Progressive Prototype: QuickBook Appointment

> Status: Example | Language: English | Last updated: 2026-07-19

## 1. Product Snapshot

| Item | Definition |
|---|---|
| Primary user | A customer booking a local service on mobile |
| Problem | Calling a business to find an available time is slow and uncertain |
| Intended outcome | Book a suitable appointment with a clear confirmation in under two minutes |
| Success signal | A customer reaches confirmation without staff assistance |

## 2. Scope and Assumptions

### Must have

- Select a service and an available time.
- Enter contact details and confirm the booking.
- Recover when a selected time becomes unavailable.

### Non-goals

- Staff calendar management, payment, accounts, and loyalty programs.

### Constraints

- Mobile-first and usable without signing in.

### Assumptions and open decisions

| ID | Type | Statement | Status |
|---|---|---|---|
| D-01 | Assumption | The business can hold a selected slot for five minutes | Open |
| D-02 | Decision | Whether phone or email is the required confirmation channel | Open |

## 3. Experience Map

| Stage | User intent | Related flows |
|---|---|---|
| Choose | Find the right service and time | F-01 |
| Confirm | Provide contact details and secure the slot | F-01 |
| Recover | Pick another time if availability changes | F-01 |

## 4. User Flows

### F-01 Book an appointment

```mermaid
flowchart LR
    START([Start]) --> S01[S-01 Service and time]
    S01 -->|Continue| S02[S-02 Booking details]
    S02 -->|Slot available| S03[S-03 Confirmation]
    S02 -->|Slot taken| S01
    S03 --> SUCCESS([Success])
```

## 5. Screen Inventory

| ID | Screen | Purpose | Entry | Primary action | Relevant states | Fidelity |
|---|---|---|---|---|---|---|
| S-01 | Service and time | Choose a bookable option | F-01 start or recovery | Continue | loading, empty, error, selected | detailed |
| S-02 | Booking details | Identify the customer and verify the slot | S-01 | Confirm booking | default, validation, submitting, slot-taken | detailed |
| S-03 | Confirmation | Prove that the appointment exists | S-02 | Add to calendar | success | deferred |

## 6. Detailed Screens

### S-01 Service and time

**Decision being tested:** Can the user compare service duration and availability without navigating between pages?

```text
+--------------------------------------------------+
| Book an appointment                              |
| [Service v]                                      |
| Duration and price summary                       |
|                                                  |
| < Previous day   Tue 21 Jul   Next day >         |
| [09:00] [10:30] [13:00] [15:30]                 |
|                                                  |
| Selected: 10:30                                  |
|                                      [Continue]  |
+--------------------------------------------------+
```

**Interaction notes — outside the screen**

| ID | Trigger | Condition | Result | Failure/recovery |
|---|---|---|---|---|
| I-01 | Change service | A service is selected | Refresh S-01 availability without losing the date | Show S-01 error; Retry reloads availability |
| I-02 | Select a time and continue | The time is available | Open S-02 with the slot held | If availability changed, keep S-01 visible and ask for another time |
| I-03 | Change date | Previous or next date exists | Refresh the tiled S-01 default state | Empty results show the tiled S-01 empty state |

**Rules and deferred detail**

- Visual styling and final service descriptions are deferred.

### S-02 Booking details

**Decision being tested:** Can the user understand why contact information is required without being forced to create an account?

```text
+--------------------------------------------------+
| Your booking                                     |
| Service · Tue 21 Jul · 10:30            [Change] |
|                                                  |
| Name  [_______________________________]          |
| Phone [_______________________________]          |
| We use this only for booking updates.            |
|                                                  |
|                                  [Confirm]       |
+--------------------------------------------------+
```

**Interaction notes — outside the screen**

| ID | Trigger | Condition | Result | Failure/recovery |
|---|---|---|---|---|
| I-04 | Change selection | A slot is held | Return to S-01 with the current service and date | If refresh fails, show the tiled S-01 error state |
| I-05 | Confirm | Contact fields are valid and the slot is available | Open the tiled S-03 success state | Invalid fields show S-02 validation; expired slot opens the tiled S-01 recovery state |

**Rules and deferred detail**

- Consent copy and regional phone formatting are deferred pending D-02.

## 7. State Coverage

| Screen | Loading | Empty | Error | Permission | Recovery | Success |
|---|---|---|---|---|---|---|
| S-01 | Required | Required | Required | N/A | Required | Required |
| S-02 | Required | N/A | Required | N/A | Required | Required |
| S-03 | N/A | N/A | N/A | N/A | N/A | Required |

## 8. Decisions and Change Impact

### Open decisions

| ID | Decision | Why it matters | Owner/next step |
|---|---|---|---|
| D-01 | Confirm the slot-hold duration | Controls expiry and recovery behavior | Validate with scheduling API owner |
| D-02 | Choose the required contact channel | Changes validation and confirmation delivery | Product decision |

### Resolved decisions

| ID | Resolution | Reason |
|---|---|---|
| D-03 | Guest booking is allowed | Account creation is outside the core booking outcome |

### Change impact

| Date | Request | Affected IDs | Conflicts resolved | Follow-up |
|---|---|---|---|---|
| 2026-07-19 | Establish initial example | F-01, S-01, S-02, S-03 | Guest booking removed account dependency | Resolve D-01 and D-02 |

### Logic audit

| Flow | Reachable start | Success/end | Branch coverage | Failure/recovery | Non-terminal dead ends | Result |
|---|---|---|---|---|---|---|
| F-01 | Covered from START | Covered at SUCCESS through S-03 | Slot available/taken and input validation are explicit | Availability, validation, expiry, and retry paths return to visible states | None | Pass |

### Presentation audit

| Check | Result | Evidence |
|---|---|---|
| User-visible copy only inside screens | Pass | Wireframes contain product UI copy; rationale and rules remain outside |
| All screens and states tiled | Pass | Default, success, loading, empty, error, validation, and recovery destinations are specified as visible frames |
| Interaction notes outside screens | Pass | I-01 through I-05 are documented outside the wireframes |

### Visual outputs

| Target | Location | Status/version | Detailed screens | Updated |
|---|---|---|---|---|
| Document | ./PROTOTYPE.md | v0.2.1 example | S-01, S-02 | 2026-07-19 |
