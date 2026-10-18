# Reviewer walkthrough and practice example

This walkthrough helps a specialist inspect the evidence and return an attributable assessment. No named scholar has participated. The filled teaching example is project-authored and simulated; it is not a submitted review or evidence of expert validation.

## 1. Open the question and inspect the scope

Read [the follow-up packet](../review/followup-packet.json), then [the native source register](../research/city-reference-crosswalk-2026-10-18.json). The packet records what remains missing and links the exact source locators. A nontechnical reviewer can read these files directly on GitHub without installing software.

## 2. Check the cited sources independently

Use the URLs and locators in the register. Record the version you actually consulted, whether you saw original pages or a text rendition, your access/reuse basis and any shared source dependence. Do not claim inspection of a PDF, object or full article from a summary. Preserve competing possibilities and uncertainty. Read [the earlier source-study guide](SOURCE-STUDY-2026-10-17.md) for rights and the historical study boundary.

## 3. Compare with the completed practice assessment

Open [the teaching example](../review/teaching-example.json). Its `practice_decision` is `MORE_SOURCE_REQUIRED`; `reviewer` is null and `human_review_occurred` is false. It illustrates how to identify an unresolved source requirement. It does not prescribe your decision or stand in for your independent work. Do not copy it into the real response and represent it as your own review.

## 4. Return your own assessment

Download or copy [the blank response form](../review/followup-response.json). Complete your identity, affiliation, relevant expertise, identity reference, conflicts, source dependence and date; list each source actually consulted with citation, locator, accessed version, access rights and dependence. Supply your decision, reasoning, confidence, counterevidence and unresolved objections. Once completed, set `status` to `SUBMITTED_FOR_MAINTAINER_CHECK`. Leave the acceptance/change flags false. Return it to the project maintainer through a mutually agreed channel; this repository does not send it automatically.

The maintainer must authenticate the reviewer and assess the substance and any dissent before admitting a change. A structurally complete form is not authenticated expertise or accepted epigraphy. Source authorship does not imply project participation or endorsement.

## 5. Optional reproducibility checks

Download the repository using **Code → Download ZIP**, extract it, and open a terminal in that folder with Python3.12 installed. Run:

```sh
python scripts/review_walkthrough.py --check
python scripts/test_review_walkthrough.py
python scripts/research_delivery.py --dossier "HL-CITY-REFERENCE-CROSSWALK-20261018" --collection city-reference-crosswalk
```

The first command prints `PASS_DOCUMENTARY_REPLAY_AND_DEMONSTRATION_SEPARATION`. The next runs five software checks; they do not judge epigraphic truth. The last prints the source-bound native dossier. [The saved audit](../analysis/review-walkthrough-audit.json) records the code/spec/profile bindings.

After completing a real form locally, validate its structure using:

```sh
python scripts/research_delivery.py --validate-review review/followup-response.json
```

The unfilled form and the teaching example intentionally fail real-submission validation. A completed real form can pass structure checks while reviewer identity, expertise, independence and scientific acceptance remain unverified. Do not publish personal contact details or source payloads without permission.
