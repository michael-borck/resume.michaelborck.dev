#!/usr/bin/env python3
"""
Generate llms.txt from cv-data.yml
Creates a structured plain-text file optimized for LLM ingestion.
Follows the llms.txt convention (like robots.txt but for AI).
"""

import yaml
import os
from datetime import datetime


def load_cv_data():
    """Load CV data from YAML file"""
    cv_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'cv-data.yml')
    try:
        with open(cv_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: CV data file not found at {cv_file}")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        return None


def generate_llms_txt(cv):
    """Generate llms.txt content from CV data"""
    lines = []

    # Header
    lines.append(f"# {cv['personal']['name']}")
    lines.append("")
    lines.append(f"> {cv['summary']['main']}")
    lines.append("")
    lines.append("This file contains structured resume/CV data for LLM consumption.")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d')}")
    lines.append(f"Source: https://resume.borck.dev")
    lines.append("")

    # Contact
    p = cv['personal']
    lines.append("## Contact")
    lines.append("")
    lines.append(f"- Location: {p['location']}")
    lines.append(f"- Email: {p['email']}")
    lines.append(f"- LinkedIn: {p['linkedin']}")
    lines.append(f"- GitHub: {p['github']}")
    lines.append(f"- Portfolio: {p['portfolio']}")
    if p.get('education_platform'):
        lines.append(f"- Education: {p['education_platform']}")
    lines.append("")

    # Key Achievements
    if cv.get('achievements'):
        lines.append("## Key Achievements")
        lines.append("")
        for a in cv['achievements']:
            lines.append(f"- {a}")
        lines.append("")

    # Experience
    if cv.get('experience'):
        lines.append("## Experience")
        lines.append("")
        for exp in cv['experience']:
            lines.append(f"### {exp['title']}")
            lines.append(f"{exp['organization']} | {exp['location']} | {exp['period']}")
            lines.append("")
            for r in exp.get('responsibilities', []):
                lines.append(f"- {r}")
            if exp.get('projects'):
                lines.append("")
                lines.append("Projects:")
                for proj in exp['projects']:
                    lines.append(f"- {proj}")
            lines.append("")

    # Education
    if cv.get('education'):
        lines.append("## Education")
        lines.append("")
        for edu in cv['education']:
            line = f"- {edu['degree']}, {edu['institution']} ({edu['year']})"
            if edu.get('thesis'):
                line += f" — Thesis: {edu['thesis']}"
            lines.append(line)
        lines.append("")

    # Teaching
    if cv.get('teaching'):
        t = cv['teaching']
        lines.append("## Teaching")
        lines.append("")
        if t.get('philosophy'):
            lines.append(f"Philosophy: {t['philosophy'].get('core', '')}")
            lines.append(f"Framework: {t['philosophy'].get('framework', '')}")
            lines.append(f"Approach: {t['philosophy'].get('approach', '')}")
            lines.append("")
        if t.get('satisfaction'):
            for s in t['satisfaction']:
                lines.append(f"- {s['metric']}: {s['details']}")
            lines.append("")
        if t.get('feedback'):
            lines.append("Student feedback:")
            for fb in t['feedback']:
                lines.append(f'- "{fb}"')
            lines.append("")

    # Skills
    if cv.get('skills'):
        lines.append("## Skills")
        lines.append("")
        sk = cv['skills']
        if sk.get('programming'):
            prog = sk['programming']
            if prog.get('core'):
                lines.append(f"Core: {', '.join(prog['core'])}")
            if prog.get('web'):
                lines.append(f"Web: {', '.join(prog['web'])}")
            if prog.get('ai_ml'):
                lines.append(f"AI/ML: {', '.join(prog['ai_ml'])}")
            if prog.get('educational'):
                lines.append(f"Educational: {', '.join(prog['educational'])}")
        lines.append("")

    # Publications
    if cv.get('publications'):
        lines.append("## Publications")
        lines.append("")
        pubs = cv['publications']
        if pubs.get('books'):
            lines.append("### Books")
            for b in pubs['books']:
                lines.append(f"- {b['title']} — {b['description']} ({b.get('license', '')})")
            lines.append("")
        if pubs.get('thesis'):
            lines.append("### Thesis")
            for th in pubs['thesis']:
                lines.append(f"- {th['title']} ({th['year']}) — {th.get('description', '')}")
            lines.append("")
        if pubs.get('conferences'):
            lines.append("### Conference Papers")
            for c in pubs['conferences']:
                lines.append(f"- {c['authors']} ({c['year']}). {c['title']}. {c['venue']}, {c.get('location', '')}.")
            lines.append("")

    # Projects
    if cv.get('projects'):
        lines.append("## Projects")
        lines.append("")
        for proj in cv['projects']:
            year = f" ({proj['year']})" if proj.get('year') else ""
            desc = f" — {proj['description']}" if proj.get('description') else ""
            lines.append(f"- {proj['name']}{year}{desc}")
        lines.append("")

    # Certifications
    if cv.get('certifications'):
        lines.append("## Certifications")
        lines.append("")
        for cert in cv['certifications']:
            lines.append(f"- {cert['name']} ({cert['year']})")
        lines.append("")

    # Memberships
    if cv.get('memberships'):
        lines.append("## Professional Memberships")
        lines.append("")
        for m in cv['memberships']:
            note = f" — {m['note']}" if m.get('note') else ""
            lines.append(f"- {m['organization']}, {m['status']} ({m['year']}){note}")
        lines.append("")

    # Interests
    if cv.get('interests'):
        lines.append("## Interests")
        lines.append("")
        lines.append(', '.join(cv['interests']))
        lines.append("")

    # References
    if cv.get('references'):
        lines.append("## References")
        lines.append("")
        lines.append(cv['references'])
        lines.append("")

    return '\n'.join(lines)


def main():
    cv_data = load_cv_data()
    if not cv_data:
        return

    content = generate_llms_txt(cv_data)

    # Write to public directory (served by Astro)
    output_paths = [
        os.path.join(os.path.dirname(__file__), '..', 'public-astro', 'llms.txt'),
        os.path.join(os.path.dirname(__file__), '..', 'output', 'llms.txt'),
    ]

    for path in output_paths:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Generated: {path}")

    # Also copy to project root for local dev
    root_path = os.path.join(os.path.dirname(__file__), '..', 'llms.txt')
    with open(root_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Generated: {root_path}")


if __name__ == '__main__':
    main()
