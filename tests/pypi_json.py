"""Recorded PyPI metadata and the browser's actual JS trimmers, shared by driver and CLI parity tests."""

import json
import subprocess
from pathlib import Path


def recorded_project():
    return json.loads(Path(__file__).with_name("pypi-project.json").read_text(encoding="utf-8"))["project"]


def trim_json(data, *, releases=False):
    """Trim a lookup map (or a map of release maps) in Node, not a second implementation in Python."""
    script = """
        import fs from 'node:fs';
        import { trimProject, trimReleases } from './site/check/check-logic.mjs';
        const trim = process.argv[1] === 'releases' ? trimReleases : trimProject;
        const data = JSON.parse(fs.readFileSync(0, 'utf8'));
        process.stdout.write(JSON.stringify(Object.fromEntries(Object.entries(data).map(([k, v]) => [k, trim(v)]))));
    """
    done = subprocess.run(
        ["node", "--input-type=module", "-e", script, "releases" if releases else "project"],
        cwd=Path(__file__).resolve().parent.parent,
        input=json.dumps(data), capture_output=True, text=True, check=True, timeout=30,
    )
    return json.loads(done.stdout)
