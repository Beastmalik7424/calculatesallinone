from pathlib import Path
import ast
import difflib
import os
import re
import subprocess
import sys

BASE_COMMIT = "02a302020622ff3c4e2e6aa75f15a12fd9a5f830"
ROOT = Path(__file__).resolve().parents[1]

def literal_assignment(source, name):
    tree = ast.parse(source)
    matches = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            if any(isinstance(target, ast.Name) and target.id == name for target in node.targets):
                matches.append(node.value)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == name:
            matches.append(node.value)
    if len(matches) != 1:
        raise AssertionError(f"Expected one assignment for {name}, found {len(matches)}")
    return ast.literal_eval(matches[0])

def main():
    content_source = (ROOT / "content_v13.py").read_text(encoding="utf-8")
    build_source = (ROOT / "build.py").read_text(encoding="utf-8")
    hub_extra = literal_assignment(content_source, "HUB_EXTRA")
    health_sections = hub_extra["health"]
    health_body = "\n".join(
        paragraph
        for _heading, paragraphs in health_sections
        for paragraph in paragraphs
    )
    required = (
        "severe thinness",
        "moderate thinness",
        "mild thinness",
        "below 16.00",
        "16.00 to 16.99",
        "17.00 to 18.49",
    )
    for phrase in required:
        assert phrase in health_body.lower(), f"Health body missing {phrase!r}"

    hub_content = literal_assignment(build_source, "HUB_CONTENT")
    health_faq = hub_content["health"]["faq"]
    assert 6 <= len(health_faq) <= 8, f"Expected 6-8 health FAQs, got {len(health_faq)}"
    answers = [
        answer for question, answer in health_faq
        if question == "What are the WHO adult BMI categories?"
    ]
    assert len(answers) == 1, "Expected exactly one WHO adult BMI categories FAQ"
    faq_answer = answers[0]
    for phrase in required:
        assert phrase in faq_answer.lower(), f"WHO FAQ missing {phrase!r}"

    all_faq_text = "\n".join(question + " " + answer for question, answer in health_faq)
    for label, value in (("health body", health_body), ("health FAQ", all_faq_text)):
        for forbidden in ("—", ";", "*"):
            assert forbidden not in value, f"{label} contains forbidden {forbidden!r}"
        lowered = value.lower()
        for phrase in (
            "last reviewed", "reviewed by", "reviewer:", "reviewer name",
            "published on", "publication date", "review date",
        ):
            assert phrase not in lowered, f"{label} contains review/date text {phrase!r}"
        assert not re.search(r"\b(?:M\.?D\.?|M\.?B\.?B\.?S\.?|Ph\.?D\.?|R\.?D\.?)\b", value, re.I), (
            f"{label} contains a reviewer credential"
        )
        assert not re.search(r"(?i)reviewed\s+by\s+[A-Z][A-Za-z.'-]+", value), (
            f"{label} contains a reviewer name"
        )

    base_build = os.environ.get("HEALTH_AUDIT_BASE_BUILD")
    if base_build is None:
        base_build = subprocess.check_output(
            ["git", "show", f"{BASE_COMMIT}:build.py"],
            cwd=ROOT,
            text=True,
        )
    base_lines = base_build.splitlines()
    head_lines = build_source.splitlines()
    changes = [
        item for item in difflib.SequenceMatcher(
            a=base_lines, b=head_lines, autojunk=False
        ).get_opcodes() if item[0] != "equal"
    ]
    assert len(changes) == 1, f"Expected one build.py change group, got {changes!r}"
    tag, i1, i2, j1, j2 = changes[0]
    removed, added = base_lines[i1:i2], head_lines[j1:j2]
    assert tag == "replace" and len(removed) == 1 and len(added) == 1, (
        f"Expected one removed and one added FAQ tuple line, got {tag}: {removed!r} -> {added!r}"
    )
    assert "What are the WHO adult BMI categories?" in removed[0]
    assert "What are the WHO adult BMI categories?" in added[0]

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
    print("PASS: health_content_v8")
    sys.exit(0)
