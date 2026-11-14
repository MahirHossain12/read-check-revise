# Session guide

## Setup

Confirm applicable institutional research requirements before recruiting or collecting participant responses. This guide is a starting point for approved materials, with recruitment, withdrawal, retention, and contact details to be filled in for the actual study. Aim for 12 consenting adult beginners with limited Python experience and allow about 15–20 minutes. Record broad prior experience privately if the approved protocol permits it. Use the next available slot in the six-sequence rotation. Assign a new ID if a session is restarted and document why.

Suggested opening, subject to the approved protocol:

> We are studying how people use explanations while solving introductory Python tasks. You will predict outcomes, read example explanations that may contain mistakes, judge claims, and answer new questions. Participation is voluntary. You may stop at any time. We collect your responses and whether you open reference material. Please leave your name and contact details out of your answers. At the end we will explain the correct Python behavior.

Run the session with the browser file generated for the assigned ID. Ask the learner to work independently, with the resources supplied in the interface. Avoid answering topic questions until the debrief. Download the response JSON after the three rounds and store it in an access-controlled location. Keep any consent records separate from the response IDs. Log incomplete sessions and how they were handled. Refrain from uploading real response data, consent records, recruitment logs, or small-sample quotations to GitHub.

## Debrief

The final screen explains all three corrections. If someone stops early, provide the corrections for any explanations already seen. Explain that inaccuracies were deliberately embedded to study claim evaluation.

## Scoring

The primary outcome is correct rejection of the inaccurate target claim. Other outcomes are correct acceptance of the accurate claim, initial and final correctness, wrong-to-right and right-to-wrong changes, and immediate transfer. The prediction and application options include “Unsure,” which counts as incorrect for accuracy and remains available in the private raw record. Evidence use is assessed by the expandable panel and by the final written reason. A source-link click only records that the learner followed the link. It cannot establish that they read it.

For an optional manual review, code final reasons as **explicit evidence use** when the learner identifies a source detail and connects it to the claim or answer, **source mention only** when a source is named without a link to the decision, and **no source reference** when the learner gives no source attribution. A correct rule alone is insufficient to infer that the learner used the documentation. Keep coding notes private and report the review procedure actually used.
