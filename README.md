# Evaluating AI Explanations in Introductory Python

A notebook-led HCI pilot prototype for studying how beginner programmers inspect evidence, detect inaccurate AI claims, revise initial answers, and apply concepts to new problems.

**Project status:** Prototype and analysis walkthrough. The included records are synthetic software fixtures. Participant recruitment and data collection are pending.

## Run in Google Colab

1. Download the repository ZIP and extract it locally so you can select a notebook. Open [Google Colab](https://colab.research.google.com/) and use **File → Upload notebook** to open one of the five notebooks.
2. Run its setup cell and upload the **original ZIP** when prompted. If this repository is public on GitHub, set `REPO_URL` to its clone URL in the setup cell instead. Each notebook initializes the project independently, so a fresh Colab runtime can run any notebook.
3. Use **Run all**. Notebook 03 generates a standalone session HTML file. Download it from Colab and open it in a browser. Notebook 04 can score the bundled synthetic fixtures without a completed session. A browser walkthrough is also available in `demo/demo-session.html`.

| Notebook | Purpose |
|---|---|
| [01 · Study design](01_Study_Design.ipynb) | Research question, conditions, allocation, and counterbalance checks |
| [02 · Stimuli and validation](02_Stimuli_and_Validation.ipynb) | Three Python topics, documentation, and executable answer checks |
| [03 · Browser prototype](03_Browser_Prototype.ipynb) | Generates the three-round session and explains JSON export |
| [04 · Data and scoring](04_Data_and_Scoring.ipynb) | Validates response records, scores outcomes, and exports a trial-level CSV |
| [05 · Analysis and reporting](05_Analysis_and_Reporting.ipynb) | Descriptive comparisons, paired primary outcomes, and a reproducible figure |

## Study design

Each learner sees explanation only (A), explanation plus official Python evidence (B), and explanation plus evidence and a required reflection prompt (C). The explanation text is fixed by topic, with one accurate target claim and one deliberately inaccurate target claim. The bundled materials are curated study stimuli with embedded errors. The interface does not call an LLM.

Six sequences balance topic, condition, and presentation position. Each learner makes an initial prediction, evaluates two claims, revises their answer, and attempts a new application item with the explanation hidden. The primary outcome is correct rejection of the inaccurate claim. B − A describes the contrast associated with offering evidence. C − B describes the contrast associated with adding the required reflection task, which also adds effort and time.

See the [session guide](study/session-guide.md) for recruitment prerequisites, debriefing, and the manual evidence-use coding rule. Keep real participant files outside the public repository. The analysis supports a feasibility pilot. With one trial per condition per learner, it cannot establish lasting learning or separate each interface feature from all mechanisms through which it operates.

## Technical layout

- `study/stimuli.json` contains the versioned task text and scoring keys.
- `prototype/session-template.html` is the browser interface template.
- `src/pilot.py` implements allocation, session generation, record validation, and scoring.
- `demo/` contains a prebuilt browser walkthrough and deterministic synthetic records.

The Python pipeline runs on CPU. The browser walkthrough works locally and exports JSON to the browser's downloads folder. Notebook 05 uses Matplotlib, which is available in Colab.

## References

- Buçinca, Malaya, and Gajos (2021), [To Trust or to Think](https://doi.org/10.1145/3449287).
- Chi, de Leeuw, Chiu, and LaVancher (1994), [Eliciting Self-Explanations Improves Understanding](https://doi.org/10.1207/s15516709cog1803_3).
- Python documentation on [lists](https://docs.python.org/3/tutorial/introduction.html#lists), [range](https://docs.python.org/3/tutorial/controlflow.html#the-range-function), and [arithmetic expressions](https://docs.python.org/3/reference/expressions.html#binary-arithmetic-operations).
