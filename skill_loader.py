# pyrefly: ignore [missing-import]
from pathlib import Path

import yaml
from pydantic import BaseModel


class Skill(BaseModel):
    name: str
    description: str
    instructions: str
    directory: Path


def load_skill(skill_file: Path) -> Skill:
    raw_content = skill_file.read_text(encoding="utf-8")

    if not raw_content.startswith("---"):
        raise ValueError(
            f"{skill_file} does not contain YAML frontmatter"
        )

    parts = raw_content.split("---", maxsplit=2)

    if len(parts) != 3:
        raise ValueError(
            f"{skill_file} has invalid YAML frontmatter"
        )

    metadata = yaml.safe_load(parts[1])
    instructions = parts[2].strip()

    return Skill(
        name=metadata["name"],
        description=metadata["description"],
        instructions=instructions,
        directory=skill_file.parent,
    )


def discover_skills(skills_directory: Path) -> dict[str, Skill]:
    skills: dict[str, Skill] = {}

    for skill_file in skills_directory.glob("*/SKILL.md"):
        skill = load_skill(skill_file)
        skills[skill.name] = skill

    return skills
