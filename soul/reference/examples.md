# Soul Examples

Two worked examples follow the locked templates—one **search**, one **build**. The search finds an invoicing product spending its expression budget in the wrong places, and the build treats the moment the search ranked first. These set the bar for length, specificity, and tone; the build route owns the workflow, state inventory, and template.

---

## Example 1—Search: an invoicing tool that "feels generic"

**Input:** *"Users say the product feels like every other invoicing app. Make it more delightful?"* Screenshots and a walkthrough: freelancers compose and send invoices, clients pay, payments land as OS-default notifications. The product has a mascot that appears on error dialogs saying "Whoops! Gremlins!", confetti on every invoice send, and a hidden breakout game on the 404 page that the team is proud of.

**Soul's output:**

```
**Verdict:** misplaced and anonymous · the product's highest-consequence outcome is a system-default notification · **5/12**

**Product:** invoicing for freelancers · **Path:** 7 beats, bookmark → payment landed · **Ends feeling:** unnamed—relief is the obvious candidate, and nobody has chosen it
**Readiness:** Ready · the default path reaches payment clearly enough for Soul work; failure recovery still needs a restraint fix
**Screen:** dashboard, invoice composer, payment notification, and 404
**Flow:** invoice-to-payment
**State:** recurring default, invoice-send success, payment success notification, failed-send error, and invalid-route recovery
**Lifecycle:** first run, recurring use, first value, re-entry, and accidental off-path visit
**Coverage:** recurring default path, first-run dashboard, invoice-send success, payment success notification, failed-send error, and 404 · gaps: payment failure, notifications disabled, re-entry after lapse, and later milestones not triggered
**Basis:** observed from a screenshot or artifact · confirm with: trigger a real payment and read the actual notification—the claim the verdict rests on
**Blocker:** None observed. The failed-send copy is inappropriate, but the artifact does not show blocked recovery, lost work, or material harm that would justify P0.

## The path
| # | Beat | Touchpoint | Frequency | Stakes | Verdict |
|---|---|---|---|---|---|
| 1 | Enters from bookmark | web app | every-run | low | Expected |
| 2 | Sees dashboard—outstanding and recent | screen | every-run (first run: once) | low | Net-New (Moment 3, first run) |
| 3 | Understands who owes what | screen | every-run | medium | Elevated |
| 4 | Composes invoice—client, items, due date | screen | recurring | medium | Expected |
| 5 | Sends—confirmation appears | screen | recurring | medium | Net-New (Moment 2) |
| 6 | Payment lands—notification | push/email | recurring | high | Net-New (Moment 1) |
| 7 | Sees dashboard updated—paid, month total | screen | recurring | medium | Elevated |

## Scorecard
| Gate | Score | Why this score | What raises it one point |
|---|---:|---|---|
| Placement | 2/4 | Confetti exists on the path but is unchosen, while the strongest craft lives on a 404; expressive effort is materially misplaced away from the payment outcome and the beats with the clearest user consequence. Recall was not tested, so any peak or ending effect remains a hypothesis. | Compare payment, send, and first-run candidates on reach, utility, stakes, frequency, cost, and a delayed-recall check before moving the budget. |
| Proportion | 2/4 | Most of the path stays restrained, but recurring confetti overplays a routine send while the payment outcome is silent; one material mismatch keeps intensity from fitting frequency and magnitude dependably. | Remove recurring confetti, then give the payment outcome proportionate, record-first treatment and test repeat comprehension. |
| Signature | 1/4 | Swap the logo and the product is indistinguishable; the mascot is generic and the ending feeling is unnamed, so no authored moment identifies the product. | Choose the ending feeling and build one distinctive payment or completion moment around it. |
| **Total** | **5/12 · 1.7/4** | **Significant rework; exact sum of justified component scores** | Weakest-gate ceiling applied |

## The moments (Net-New, up to 3, ranked by contextual reach × likely memory)
### Moment 1—Payment lands (beat 6), relief
- **At:** screen: payment notification and dashboard · flow: invoice-to-payment · state: successful payment · lifecycle: first and recurring value realization
- Why here: payment is the product's outcome and carries a concrete money consequence for the freelancer; the notification is currently "Invoice #1042 was paid." Its recall advantage over send or first run is a hypothesis, so compare reach and utility with a delayed-recall check.
- Expected: notification names client, invoice, and amount · Elevated: amount-first copy, a paid-receipt block, the outstanding total visibly settling to its new value · Net-New: a Paid ledger—a year-view that fills with each payment and exports clean at tax time
- Constraints: money moment—records and amounts precede any feeling; no sound.

### Moment 2—Send (beat 5), confidence
- **At:** screen: invoice send confirmation · flow: invoice-to-payment · state: successful send · lifecycle: recurring invoice creation
- Why here: sending is where the freelancer's effort and uncertainty concentrate; the confirmation answers a different question than "does it look professional to my client?" Compare this candidate with payment on reach, stakes, frequency, and build cost rather than assuming either is the stronger memory cue.
- Expected: "Sent to client@" with timestamp · Elevated: preview exactly as the client sees it, then a delivered state · Net-New: a client-facing invoice page polished enough to be the freelancer's storefront
- Constraints: nothing may delay the send action itself.

### Moment 3—First-run dashboard (beat 2, first pass), possibility
- **At:** screen: first-run dashboard · flow: invoice-to-payment · state: empty state · lifecycle: first run
- Why here: the intended first-run dashboard reaches each new freelancer once and can carry more expression than recurring beats, subject to a test that the new onboarding improves comprehension and completion.
- Expected: "No invoices yet" plus a button · Elevated: an empty state that starts the work—a sample invoice and "your first takes 2 minutes" · Net-New: composing the first invoice is the onboarding; the form is the tour
- Constraints: one primary action; the sample must be deletable in one tap.

## The small things (Elevated)
- **At:** screen: dashboard outstanding summary · flow: invoice-to-payment · state: populated recurring state · lifecycle: recurring use · Beat 3—say it in the freelancer's words: "Who owes you: $4,200 across 3 invoices" instead of "Outstanding: $4,200."
- **At:** screen: updated dashboard · flow: invoice-to-payment · state: payment-settled state · lifecycle: post-payment re-entry · Beat 7—paid rows settle to the bottom with a quiet check; the outstanding total counts down to its new value, and reduced motion gets the delta in text.

## Issues (most severe first)
- **[P1 · off-path restraint]** **At:** screen: Invoice send · flow: invoice-to-payment · state: failed-send error · lifecycle: recurring invoice creation. Wit at failure—the mascot grins through a failed send with "Whoops! Gremlins!" while delivery is uncertain. The tone materially damages confidence at a consequential moment, but no blocked recovery or financial loss is shown, so it is not P0. **Fix:** plain error—what happened, whether the invoice is safe, and what to do next. If failed sends are frequent, hand the relationship leak to Flywheel.
- **[P1 · beat 6]** **At:** screen: Payment landed notification · flow: invoice-to-payment · state: successful payment · lifecycle: first and recurring value realization. The money outcome is a system-default notification, so the user gets little record or product-specific context at a consequential point. **Fix:** treat as Moment 1; validate whether amount-first feedback improves comprehension and delayed recall before scoping the ledger.
- **[P2 · beat 5]** **At:** screen: Invoice send confirmation · flow: invoice-to-payment · state: successful send with confetti · lifecycle: steady-state recurring use. Repeat value is untested, and confetti may become wallpaper while spending celebration the payment outcome does not get. **Fix:** replace with a sent-state whose preview, delivered check, and done status can be perceived and understood on later runs; validate before adding ceremony.
- **[P2 · off-path]** **At:** screen: 404 page · flow: invoice-to-payment · state: invalid-route recovery · lifecycle: accidental off-path visit. The misdirected budget—the 404 minigame is the most-crafted surface in the product, reached by accident, in annoyance. Its reach is limited and recovery still exists, so this is misplaced effort rather than a major path failure. **Fix:** relocate the craft to Moment 2 or 3; the game itself is cut, not polished.

## Kept Expected, on purpose
Beats 1 and 4 stay standard. Beat 4 is load-bearing convention—a weekly form freelancers fill from muscle memory, where novelty costs speed. Beat 1 is an every-run entry; its observed pace is acceptable, but latency, failure feedback, and repeat comprehension still need a live check before calling speed a signature.

## Next
- **Now**: **At:** screen: payment notification and dashboard · flow: invoice-to-payment · state: successful payment · lifecycle: first and recurring value realization · the small things and Moment 1's Elevated interim—amount-first notification, receipt block, the settling total—ship while the Net-New ledger is scoped.
- **After it lands**: **At:** screen: Paid ledger and first-run dashboard · flow: invoice-to-payment · state: payment-settled and empty states · lifecycle: first value and first run · Moment 1's Net-New ledger, then Moment 3—the only `once` beat on the path, currently spending nothing.
- **Hand off**: **At:** screen: invoice send error branch · flow: invoice-to-payment · state: failed-send error · lifecycle: recurring invoice creation · None. (If failed sends turn out to be frequent, route the error branch to Flywheel as a leak.)
```

---

## Example 2—Build: the payment moment

**Input:** "Design the payment-landed moment the search ranked first."

**Soul's output:**

```
**Moment:** Payment lands—for a freelancer, on each successful payment.
**Feeling:** relief · **Frequency:** recurring · **Stakes:** medium · **Target:** Net-New

## Why this moment
- On the path: beat 6, reached by a client when an invoice is paid.
- Budget decision: payment has clear user consequence and a candidate for useful records. Its recall advantage over send or first run is untested, so the ledger remains a hypothesis to validate against reach, stakes, cost, and later use.
- Today: an OS-default notification—"Invoice #1042 was paid."—and a dashboard that shows the change only after a manual refresh. Observed from the artifact.

## Applicable states
| State or occurrence | Status | Applicability reason, evidence, or next check |
|---|---|---|
| Completion | Applicable | The paid notification and dashboard update expose the successful payment outcome. |
| Partial failure | Not shown—walk partial settlement, chargeback, and notification failure | The artifact does not show whether a payment can settle partially or whether notification delivery can fail. |
| Permission | Not shown—check notification and amount-visibility permissions | OS-default notifications are shown, but permission and shared-device behavior are not evidenced. |
| Recovery / retry | Not shown—test delayed payment and notification retry | The artifact does not expose retry, revalidation, or recovery after an interrupted payment update. |
| Cancel / exit | N/A—payment-landed is post-submit confirmation | Cancellation belongs before settlement; this beat only confirms the outcome. |
| Repeated use | Applicable—replay later payments and inspect ledger comprehension | Payments recur, but later-run utility and comprehension still need validation. |
| Reduced motion / low-motion | Applicable | The proposed total settle has a text delta equivalent; verify it with the user's reduced-motion setting. |

## The rungs
- **Expected:** notification carries client, invoice number, and amount; the dashboard row flips to Paid on next load. Shippable as-is.
- **Elevated:** the interim ship—the notification leads with what matters: "$1,850 from Meridian Co · Invoice #1042 paid." Opening it lands on the invoice with a paid-receipt block: date, method, a record that exists somewhere. The outstanding total settles to its new value with one 400ms count-down; reduced motion gets the delta in text—"Outstanding: $4,200 → $2,350."
- **Net-New:** the Paid ledger—each payment could land as a row in a year-view, with month totals and a clean tax-time export. It gives relief a record to build on; validate whether that utility remains clear and worth returning to on later payments.

## Held constant
- The notification must be complete in text alone—no motion, sound, or color required to know you were paid—and its behavior under OS truncation at 60 characters still needs verification.
- Records reachable in one tap from the notification, at every rung.
- Nothing celebrates before the amount is stated—money moments put reassurance before feeling.

## Constraints for the pick
- No sound at any rung. No confetti in this proposal: recurring frequency and a money outcome make record-first feedback the safer tested choice.
- Notifications appear on shared and locked screens; amount-first copy is the point, so a "hide amounts" preference ships alongside whichever rung is chosen.

## Gates
- [x] On the default path—reached without hunting
- [x] One feeling, named—"soul" and "delight" appear nowhere as specs
- [Not shown—replay later payments and test comprehension] Survives its frequency—the ledger's repeat value is proposed, not observed
- [x] Proportionate to the moment's magnitude
- [Not shown—test response timing, failure feedback, and primary-action latency] Speed, comprehension, and the primary action untouched
- [x] Honest without motion and without sound
```

---

**Why these two:** the search refuses the question as asked. The user said "make it more delightful" and the answer is that expressive effort already exists—in a 404 game and a failure mascot—and the job is relocation, not addition. The verdict names a misplacement, not an absence. Note the tiers doing the restraint: three candidates clear the initial selection bar, while the recall check remains open; two small things are elevated because their ceilings allow only craft, and two beats stay standard with reasons on record. The build then shows the full range on one moment—Expected floor, Elevated interim, Net-New target—so the caller can land anywhere on the ladder, while proportionality at a money moment stays record-first and leaves repeat value to validation.

Note what never appears: confetti at any tier, the mascot polished rather than cut, or a quota-driven fourth moment. The first-run empty state is the only place one-shot expressive treatment is considered because it is the only `once` beat on the path.
