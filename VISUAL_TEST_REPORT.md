# PM Mentor Visual Test Report

**Report date:** 28 November 2026
**Result:** **PASS**

Word edition: [VISUAL_TEST_REPORT.docx](VISUAL_TEST_REPORT.docx)

## Scope and setup

The local application was opened in the integrated browser using an isolated Flask app, temporary SQLite storage, and no model credentials. Screens were reviewed in demo mode at:

- Desktop viewport: **875 × 674**
- Mobile viewport: **390 × 844**

Practice and Quiz questions were started, incorrect answers were submitted, and the feedback panels and progress display were reviewed. No screenshots are included because the requested deliverable formats are Markdown and Word only.

## Visual checks

| Check | Observation | Result |
|---|---|---|
| Initial desktop workspace | Sidebar, topic header, welcome content, suggested actions, composer, and provider status were visible and aligned | Pass |
| Practice question | Question, difficulty, and A–D choices appeared in the chat panel | Pass |
| Quiz question | Quiz label and question content were distinct from Practice | Pass |
| Incorrect-answer feedback | Hint, correct answer, explanation, personalized feedback, and topic best-practice tip were visible in one feedback card | Pass |
| Option-letter answer entry | Lowercase choice letters with a trailing period are accepted by the updated browser regression test | Pass |
| Desktop chat behavior | Chat panel scrolls vertically when conversation content exceeds its viewport | Pass |
| Mobile layout | Bottom mode navigation remains fixed; chat content remains scrollable; feedback is readable after scrolling to the newest message | Pass |
| Mobile horizontal overflow | At 390 px viewport width, document width was 390 px and chat content width was approximately 375 px | Pass |

## Resolved finding

The initial manual fallback-mode check found that the PERT answer **B. 6 days** was marked incorrect when only its letter was submitted. Answer evaluation was updated to map letters A–D, regardless of case and with an optional trailing period, to the displayed choices. The browser regression test now submits the correct answer as a lowercase letter with a period.

## Limits

- This was a focused manual visual review at two viewport sizes, not a screenshot-based pixel-diff test.
- Only the integrated browser and the local demo-mode application were checked; no live provider or deployed service was used.
- Firefox, WebKit, assistive technology, and a comprehensive accessibility audit were not tested.
- Automated browser regression results are in [REGRESSION_TEST_REPORT.md](REGRESSION_TEST_REPORT.md); broader experience constraints are in [USER_EXPERIENCE_REPORT.md](USER_EXPERIENCE_REPORT.md).
