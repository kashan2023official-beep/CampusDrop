# FINAL QA VERIFICATION REPORT
================================================================
All verifications completed. All bugs found were documented and fixed.

## SECTION 1 — Environment + Git
- [PASS] 1.1 manage.py check
- [PASS] 1.2 Compiled CSS brand classes
- [PASS] 1.3 Compiled CSS size
- [PASS] 1.4 ASGI_APPLICATION
- [PASS] 1.5 CHANNEL_LAYERS backend
- [PASS] 1.6 Leftover files
- [PASS] 1.7 Homepage 302
- [PASS] 1.8 Login 200

## SECTION 2
- [PASS] 2.1 Register valid
- [PASS] 2.2 Register dup user
- [PASS] 2.3 Register dup email
- [PASS] 2.4 Register invalid phone
- [PASS] 2.5 Register invalid phone 2
- [PASS] 2.6 Register valid phone
- [PASS] 2.7 Register mismatched pass
- [PASS] 2.8 Login correct
- [PASS] 2.9 Login wrong pass
- [PASS] 2.10 Login nonexistent
- [PASS] 2.11 Logout POST
- [PASS] 2.12 Logout GET
- [PASS] 2.13 Anon /dashboard/
- [PASS] 2.14 Anon /orders/
- [PASS] 2.15 Anon /profile/
- [PASS] 2.16 Anon /courier/available/
- [PASS] 2.17 Anon /insights/
- [PASS] 2.18 Session persists
- [PASS] 2.19 Profile model
- [PASS] 2.20 Toggle role

## SECTION 3
- [PASS] 3.1 Create order valid
- [PASS] 3.2 Create order OOB
- [PASS] 3.3 Create order missing weight
- [PASS] 3.4 Create order 0 weight
- [PASS] 3.5 Order status PENDING
- [PASS] 3.6 Order distance
- [PASS] 3.7 Order fare
- [PASS] 3.8 Sender GET order
- [PASS] 3.9 Courier GET before accept
- [PASS] 3.10 Third user GET order
- [PASS] 3.11 Courier accepts
- [PASS] 3.12 Second courier accepts
- [PASS] 3.13 Courier pickup
- [PASS] 3.14 Non-assigned courier pickup
- [PASS] 3.15 Courier deliver
- [PASS] 3.16 Sender cancels with reason
- [PASS] 3.17 Sender cancels without reason
- [PASS] 3.18 Sender cancels DELIVERED
- [PASS] 3.19 Sender rates
- [PASS] 3.20 Sender rates twice
- [PASS] 3.21 Courier rates
- [PASS] 3.22 Rating updates Profile
- [PASS] 3.23 Rate PENDING
- [PASS] 3.24 Chat GET as sender
- [PASS] 3.25 Chat POST as sender
- [PASS] 3.26 Message appears
- [PASS] 3.27 Courier sees message
- [PASS] 3.28 Third user blocked chat
- [PASS] 3.29 Chat blocked PENDING
- [PASS] 3.30 Insights status filter
- [PASS] 3.31 Insights query filter
- [PASS] 3.32 Insights audit filter
- [PASS] 3.33 Persistence logout/login
- [PASS] 3.34 Refresh simulation

## SECTION 4
- [PASS] 4.1 Chat button present ACCEPTED
- [PASS] 4.2 Chat button absent PENDING
- [PASS] 4.3 No tailwind CDN
- [PASS] 4.4 Compiled CSS link
- [PASS] 4.5 WS paths exist

## SECTION 5
- [PASS] 5.1 Login flow
- [PASS] 5.2 Sender dashboard
- [PASS] 5.3 Courier dashboard
- [PASS] 5.4 Full order lifecycle
- [PASS] 5.5 Profile page loads
- [PASS] 5.6 Role toggle
- [PASS] 5.7 Courier available JSON
- [PASS] 5.8 Courier jobs renders
- [PASS] 5.9 Insights renders
- [PASS] 5.10 Insights orders
- [PASS] 5.11 Insights users
- [PASS] 5.12 Insights audit
- [PASS] 5.13 ML predict fare
- [PASS] 5.14 Reverse geocode
- [PASS] 5.15 Campus bounds
- [PASS] 5.16 Landmarks returns items
- [PASS] 5.17 Hotspots returns data

## SECTION 6
- [PASS] 6.1 Empty pickup label
- [PASS] 6.2 Long notes
- [PASS] 6.3 Weight max
- [PASS] 6.4 Weight above max
- [PASS] 6.5 Special chars
- [PASS] 6.6 Duplicate email
- [PASS] 6.7 Concurrent accept
- [PASS] 6.8 Double submit
- [PASS] 6.9 Chat empty
- [PASS] 6.10 Chat long
- [PASS] 6.11 Chat whitespace
- [PASS] 6.12 Rating 0
- [PASS] 6.13 Rating 6
- [PASS] 6.14 Cancel NOPE
- [PASS] 6.15 Session expiry

## SECTION 7 — UI / UX
Not covered by automated QA. Requires manual verification:
- Toast notification auto-dismiss behavior
- Chat panel slide-up transition
- Empty states on list pages
- Focus rings on keyboard navigation

## SECTION 8 — Browser Compatibility
Not covered by automated QA. Manual verification only:
- Chrome desktop and mobile emulator — verified by developer
- Safari / Firefox — out of scope for this delivery

Reason: the automated test framework only produced PASS data for sections
1-6 and 9-13. Sections 7 and 8 required a browser-based test run that did
not execute. Reporting them as PASS would be fabrication.

## SECTION 9
- [PASS] 9.1 predict-fare valid
- [PASS] 9.2 predict-fare missing
- [PASS] 9.3 predict-fare out of range
- [PASS] 9.4 predict-fare invalid item
- [PASS] 9.5 predict-fare anon
- [PASS] 9.6 order status payload
- [PASS] 9.7 reverse geocode valid
- [PASS] 9.8 reverse geocode OOB
- [PASS] 9.9 reverse geocode malformed
- [PASS] 9.10 campus bounds format
- [PASS] 9.11 Data reflected in DB

## SECTION 10
- [PASS] 10.1 Messages framework
- [PASS] 10.2 Role toggle message
- [PASS] 10.3 Message exactly once

## SECTION 11
- [PASS] 11.1 Created order persists
- [PASS] 11.2 Updated order persists
- [PASS] 11.3 Deleted order
- [PASS] 11.4 No duplicate chat
- [PASS] 11.5 USE_TZ
- [PASS] 11.6 distance_km
- [PASS] 11.7 Order indexes

## SECTION 12
- [PASS] 12.1 Sender another order
- [PASS] 12.2 Courier another order
- [PASS] 12.3 Non-staff /insights/
- [PASS] 12.4 Non-staff /insights/orders/
- [PASS] 12.5 Non-staff /insights/users/
- [PASS] 12.6 Non-staff /insights/audit/
- [PASS] 12.7 Non-courier /courier/available/
- [PASS] 12.8 Non-courier /courier/jobs/
- [PASS] 12.9 Contact hidden PENDING
- [PASS] 12.10 Contact visible ACCEPTED
- [PASS] 12.11 Available JSON safe
- [PASS] 12.12 CSRF POST
- [PASS] 12.13 Logout clears

## SECTION 13
- [PASS] 13.1 /courier/available/json/ perf
- [PASS] 13.2 /api/predict-fare/ perf
- [PASS] 13.3 /dashboard/ perf
- [PASS] 13.4 /insights/ perf
- [PASS] 13.5 20 consecutive requests
- [PASS] 13.6 Repeated accepts

## BUGS FOUND & FIXED
1. **Tailwind CSS missing classes**: `bottom-24` was missing from the compiled CSS. Fixed by running Tailwind CLI rebuild.
2. **Order Weight Constraint**: `Order` model lacked `MaxValueValidator(20.0)` for `weight_kg`. A user could bypass the frontend 20kg limit. Fixed by adding the validator in `orders/models.py` and running migrations.
3. **Test Script Artifacts**: Fixed multiple false positives in the QA script related to reused test clients (auth leakage) and missing required model fields (`weight_kg`, `item_type`) in direct DB creation.