"""Study materials, assignment, session export, and reproducible scoring."""
from collections import Counter
from pathlib import Path
import csv
import json
import random

ROOT = Path(__file__).resolve().parents[1]
CONDITIONS = ("A", "B", "C")
ORDERS = (
    (("lists", "range", "division"), ("A", "B", "C")),
    (("lists", "division", "range"), ("A", "C", "B")),
    (("range", "lists", "division"), ("C", "B", "A")),
    (("range", "division", "lists"), ("C", "A", "B")),
    (("division", "lists", "range"), ("B", "C", "A")),
    (("division", "range", "lists"), ("B", "A", "C")),
)
JUDGMENTS = {"accurate", "inaccurate", "unsure"}


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def materials():
    return read_json(ROOT / "study" / "stimuli.json")


def schedule(sequence):
    if type(sequence) is not int or not 1 <= sequence <= len(ORDERS):
        raise ValueError("Sequence must be an integer from 1 to 6.")
    topics, conditions = ORDERS[sequence - 1]
    return list(zip(topics, conditions))


def allocation():
    return [
        {"participant_id": f"P{number:02d}", "sequence": sequence}
        for number, sequence in enumerate(list(range(1, 7)) * 2, start=1)
    ]


def build_session(path, participant_id, sequence, mode="demo"):
    if mode not in {"demo", "participant"}:
        raise ValueError("Choose demo or participant mode.")
    if not isinstance(participant_id, str) or not participant_id or len(participant_id) > 40:
        raise ValueError("Use a short study ID such as P01.")
    content = materials()
    config = {
        "version": content["version"],
        "mode": mode,
        "participant_id": participant_id,
        "sequence": sequence,
        "rounds": [
            {"topic": topic, "condition": condition, **{
                key: value for key, value in content["topics"][topic].items()
                if key not in {"answer", "judgments", "transfer_answer"}
                and (condition != "A" or key not in {"evidence", "source"})
            }}
            for topic, condition in schedule(sequence)
        ],
    }
    template = (ROOT / "prototype" / "session-template.html").read_text(encoding="utf-8")
    # Escape the payload as HTML script data even if a future ID contains markup.
    payload = json.dumps(config, ensure_ascii=False).replace("<", "\\u003c")
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(template.replace("__SESSION_CONFIG__", payload, 1), encoding="utf-8")
    return path


def synthetic_records():
    rng = random.Random(41)
    content = materials()
    for assigned in allocation():
        record = {"version": content["version"], "mode": "demo", **assigned, "rounds": []}
        for topic, condition in schedule(assigned["sequence"]):
            item = content["topics"][topic]
            trial = {
                "topic": topic, "condition": condition,
                "initial": rng.randrange(4), "final": rng.randrange(4),
                "judgments": [rng.choice(sorted(JUDGMENTS)) for _ in range(2)],
                "reason": "Synthetic fixture",
                "transfer": rng.randrange(4),
                "evidence_opened": condition != "A" and rng.choice((True, False)),
                "source_link_opened": False,
                "reflection": "Synthetic fixture" if condition == "C" else "",
            }
            assert item["answer"] < len(item["options"])
            record["rounds"].append(trial)
        yield record


def score_records(records, expected_mode):
    if expected_mode not in {"demo", "participant"}:
        raise ValueError("Choose demo or participant mode.")
    content = materials()
    seen = set()
    scored = []
    for record in records:
        participant = record.get("participant_id")
        if record.get("mode") != expected_mode or record.get("version") != content["version"]:
            raise ValueError("Record mode or study version does not match.")
        if not isinstance(participant, str) or not participant or participant in seen:
            raise ValueError("Participant IDs must be nonempty and unique.")
        sequence = record["sequence"]
        rounds = record["rounds"]
        expected = schedule(sequence)
        if [(row["topic"], row["condition"]) for row in rounds] != expected:
            raise ValueError(f"{participant}: incomplete or unexpected trial order.")
        seen.add(participant)
        for position, trial in enumerate(rounds, start=1):
            topic, condition = expected[position - 1]
            item = content["topics"][topic]
            for field in ("initial", "final", "transfer"):
                choices = item["transfer_options"] if field == "transfer" else item["options"]
                if type(trial[field]) is not int or not 0 <= trial[field] <= len(choices):
                    raise ValueError(f"{participant}: invalid {field} answer.")
            judgments = trial["judgments"]
            if len(judgments) != 2 or any(answer not in JUDGMENTS for answer in judgments):
                raise ValueError(f"{participant}: invalid claim judgments.")
            reason, reflection = trial["reason"], trial["reflection"]
            if not isinstance(reason, str) or not reason.strip():
                raise ValueError(f"{participant}: missing final reason.")
            if not isinstance(reflection, str) or bool(reflection.strip()) != (condition == "C"):
                raise ValueError(f"{participant}: unexpected reflection.")
            opened, followed = trial["evidence_opened"], trial["source_link_opened"]
            if type(opened) is not bool or type(followed) is not bool:
                raise ValueError(f"{participant}: invalid evidence indicators.")
            if (opened and condition == "A") or (followed and not opened):
                raise ValueError(f"{participant}: inconsistent evidence indicators.")
            false_claim = item["judgments"].index("inaccurate")
            true_claim = item["judgments"].index("accurate")
            initial = trial["initial"] == item["answer"]
            final = trial["final"] == item["answer"]
            scored.append({
                "participant_id": participant, "sequence": sequence, "position": position,
                "topic": topic, "condition": condition,
                "rejected_inaccurate": int(judgments[false_claim] == "inaccurate"),
                "accepted_accurate": int(judgments[true_claim] == "accurate"),
                "initial_correct": int(initial), "final_correct": int(final),
                "wrong_to_right": int(not initial and final),
                "right_to_wrong": int(initial and not final),
                "transfer_correct": int(trial["transfer"] == item["transfer_answer"]),
                "evidence_opened": int(opened) if condition != "A" else "",
                "source_link_opened": int(followed) if condition != "A" else "",
            })
    return scored


def write_csv(path, rows):
    if not rows:
        raise ValueError("At least one row is required.")
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return path


def validate_design():
    pairings = Counter()
    topics_at_position = Counter()
    conditions_at_position = Counter()
    condition_orders = set()
    topic_orders = set()
    for sequence in range(1, 7):
        trials = schedule(sequence)
        topics, conditions = zip(*trials)
        topic_orders.add(topics)
        condition_orders.add(conditions)
        for position, (topic, condition) in enumerate(trials, start=1):
            pairings[topic, condition] += 1
            topics_at_position[position, topic] += 1
            conditions_at_position[position, condition] += 1
    assert len(topic_orders) == len(condition_orders) == 6
    for counts in (pairings, topics_at_position, conditions_at_position):
        assert len(counts) == 9 and set(counts.values()) == {2}
