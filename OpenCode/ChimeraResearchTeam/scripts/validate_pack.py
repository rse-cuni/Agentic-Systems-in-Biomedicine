#!/usr/bin/env python3
"""Static validation for the OpenCode Research Lab Agent Pack."""

from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]

EXPECTED_AGENTS = {
    "lab-pi": ("primary", "einfra/agentic"),
    "research-specialist": ("subagent", "einfra/kimi-k2.6"),
    "programmer": ("subagent", "einfra/qwen3-coder"),
    "hpc-operator": ("subagent", "einfra/glm-5.1"),
    "data-analyst": ("subagent", "einfra/kimi-k2.6"),
    "methods-reviewer": ("subagent", "einfra/kimi-k2.6"),
    "reproducibility-officer": ("subagent", "einfra/kimi-k2.6"),
    "scientific-writer": ("subagent", "einfra/kimi-k2.6"),
    "research-critic": ("subagent", "einfra/thinker"),
    "code-critic": ("subagent", "einfra/thinker"),
    "methods-critic": ("subagent", "einfra/thinker"),
    "hpc-safety-critic": ("subagent", "einfra/thinker"),
    "reproducibility-critic": ("subagent", "einfra/thinker"),
}

EXPECTED_COMMANDS = {
    "lab-start": "lab-pi",
    "lab-delegate": "lab-pi",
    "lab-review": "lab-pi",
    "lab-close": "lab-pi",
    "lab-full-demo": "lab-pi",
    "lab-research": "lab-pi",
}

EXPECTED_SKILLS = [
    "lab-orchestration",
    "literature-context",
    "research-software",
    "hpc-lab-operations",
    "data-analysis",
    "methods-design",
    "reproducibility-audit",
    "scientific-writing",
    "critique-gate",
]

EXPECTED_AGENT_SKILLS = {
    "lab-pi": ["lab-orchestration", "critique-gate"],
    "research-specialist": ["literature-context"],
    "programmer": ["research-software"],
    "hpc-operator": [
        "hpc-lab-operations",
        "chimera-slurm-mcp",
        "chimera-filecompress-mcp",
        "chimera-cluster",
    ],
    "data-analyst": ["data-analysis", "reproducibility-audit"],
    "methods-reviewer": ["methods-design"],
    "reproducibility-officer": ["reproducibility-audit"],
    "scientific-writer": ["scientific-writing"],
    "research-critic": ["literature-context", "critique-gate"],
    "code-critic": ["research-software", "critique-gate"],
    "methods-critic": ["methods-design", "critique-gate"],
    "hpc-safety-critic": [
        "hpc-lab-operations",
        "chimera-slurm-mcp",
        "chimera-filecompress-mcp",
        "chimera-cluster",
        "critique-gate",
    ],
    "reproducibility-critic": ["reproducibility-audit", "critique-gate"],
}

EXPECTED_TEMPLATES = [
    "templates/lab_notebook.md",
    "templates/task_report.md",
    "templates/critique_report.md",
    "templates/handoff.md",
]

EXPECTED_EXAMPLE_FILES = [
    "examples/research-to-hpc-loop/lab_notebook.md",
    "examples/research-to-hpc-loop/tasks/t001-research-context/task_report.md",
    "examples/research-to-hpc-loop/tasks/t002-methods-plan/task_report.md",
    "examples/research-to-hpc-loop/tasks/t003-hpc-plan/task_report.md",
    "examples/research-to-hpc-loop/tasks/t004-analysis-code/task_report.md",
    "examples/research-to-hpc-loop/tasks/t005-reproducibility/task_report.md",
    "examples/research-to-hpc-loop/reviews/t001-research-context/research-critic.md",
    "examples/research-to-hpc-loop/reviews/t002-methods-plan/methods-critic.md",
    "examples/research-to-hpc-loop/reviews/t003-hpc-plan/hpc-safety-critic.md",
    "examples/research-to-hpc-loop/reviews/t004-analysis-code/code-critic.md",
    "examples/research-to-hpc-loop/reviews/t005-reproducibility/reproducibility-critic.md",
    "examples/research-to-hpc-loop/handoffs/t003-hpc-plan/hpc-to-programmer.md",
]


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_frontmatter(path: Path) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail(f"{path.relative_to(ROOT)} is missing opening frontmatter fence")
    end = text.find("\n---\n", 4)
    if end == -1:
        fail(f"{path.relative_to(ROOT)} is missing closing frontmatter fence")
    return text[4:end], text[end + 5 :]


def scalar(frontmatter: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.+?)\s*$", frontmatter, re.MULTILINE)
    if not match:
        fail(f"frontmatter is missing `{key}`")
    return match.group(1).strip().strip('"').strip("'")


def validate_agents() -> None:
    agents_dir = ROOT / ".opencode" / "agents"
    for name, (expected_mode, expected_model) in EXPECTED_AGENTS.items():
        path = agents_dir / f"{name}.md"
        if not path.exists():
            fail(f"missing agent {path.relative_to(ROOT)}")
        frontmatter, body = read_frontmatter(path)
        if re.search(r"^\s*tools\s*:", frontmatter, re.MULTILINE):
            fail(f"{path.relative_to(ROOT)} uses deprecated `tools` frontmatter")
        mode = scalar(frontmatter, "mode")
        model = scalar(frontmatter, "model")
        description = scalar(frontmatter, "description")
        if mode != expected_mode:
            fail(f"{path.relative_to(ROOT)} mode is {mode}, expected {expected_mode}")
        if model != expected_model:
            fail(f"{path.relative_to(ROOT)} model is {model}, expected {expected_model}")
        if len(description) < 20:
            fail(f"{path.relative_to(ROOT)} description is too short")
        if "current project folder" not in body.lower():
            fail(f"{path.relative_to(ROOT)} must state the current project folder boundary")
        for skill in EXPECTED_AGENT_SKILLS[name]:
            if f'"{skill}"' not in frontmatter:
                fail(f"{path.relative_to(ROOT)} permission.skill must include {skill}")
            if f"${skill}" not in body:
                fail(f"{path.relative_to(ROOT)} body must instruct the agent to load ${skill}")
    print(f"validated {len(EXPECTED_AGENTS)} agents")


def validate_skills() -> None:
    skills_dir = ROOT / ".opencode" / "skills"
    name_pattern = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
    for name in EXPECTED_SKILLS:
        path = skills_dir / name / "SKILL.md"
        if not path.exists():
            fail(f"missing skill {path.relative_to(ROOT)}")
        frontmatter, body = read_frontmatter(path)
        declared_name = scalar(frontmatter, "name")
        description = scalar(frontmatter, "description")
        if declared_name != name:
            fail(f"{path.relative_to(ROOT)} declares name {declared_name}, expected {name}")
        if not name_pattern.fullmatch(declared_name):
            fail(f"{path.relative_to(ROOT)} has invalid skill name {declared_name}")
        if len(description) > 1024:
            fail(f"{path.relative_to(ROOT)} description is too long")
        if len(body.strip()) < 200:
            fail(f"{path.relative_to(ROOT)} body is too short to be useful")
    print(f"validated {len(EXPECTED_SKILLS)} skills")


def validate_commands() -> None:
    commands_dir = ROOT / ".opencode" / "commands"
    for name, expected_agent in EXPECTED_COMMANDS.items():
        path = commands_dir / f"{name}.md"
        if not path.exists():
            fail(f"missing command {path.relative_to(ROOT)}")
        frontmatter, body = read_frontmatter(path)
        agent = scalar(frontmatter, "agent")
        description = scalar(frontmatter, "description")
        if agent != expected_agent:
            fail(f"{path.relative_to(ROOT)} agent is {agent}, expected {expected_agent}")
        if len(description) < 15:
            fail(f"{path.relative_to(ROOT)} description is too short")
        if "$ARGUMENTS" not in body:
            fail(f"{path.relative_to(ROOT)} should use $ARGUMENTS")
    print(f"validated {len(EXPECTED_COMMANDS)} commands")


def validate_paths(paths: list[str], label: str) -> None:
    missing = [path for path in paths if not (ROOT / path).exists()]
    if missing:
        fail(f"missing {label}: {', '.join(missing)}")
    print(f"validated {len(paths)} {label}")


def main() -> None:
    validate_agents()
    validate_skills()
    validate_commands()
    validate_paths(EXPECTED_TEMPLATES, "templates")
    validate_paths(EXPECTED_EXAMPLE_FILES, "example files")
    print("pack validation passed")


if __name__ == "__main__":
    main()
