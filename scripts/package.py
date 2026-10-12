#!/usr/bin/env python3
"""Package explicit public paths, never personal runtime data or Git history."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
TOP_FILES = {"README.md", "LICENSE", "CONTRIBUTING.md", ".gitignore"}
TOP_DIRS = {"skills", "scripts", "docs", "examples", "evals", "tests", ".github"}
SUFFIXES = {".md", ".py", ".yaml", ".yml"}


def public_files():
    result = {}
    for path in sorted(ROOT.rglob("*")):
        relative = path.relative_to(ROOT)
        if any(part in {".git", "__pycache__"} for part in relative.parts):
            continue
        if relative.parts[0] not in TOP_FILES | TOP_DIRS:
            continue
        if path.is_symlink():
            raise ValueError(f"Refusing symlink: {relative}")
        if not path.is_file():
            continue
        if relative.as_posix() not in TOP_FILES and path.suffix not in SUFFIXES:
            raise ValueError(f"Unexpected public file type: {relative}")
        result[relative.as_posix()] = path.read_bytes()
    return result


def write_zip(path, files):
    if path.exists():
        raise ValueError(f"Output already exists: {path}")
    with zipfile.ZipFile(path, "x", compression=zipfile.ZIP_DEFLATED, strict_timestamps=False) as archive:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 10, 12, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", help="Existing or new output directory outside the public source tree")
    args = parser.parse_args()
    output = Path(args.output).expanduser().resolve()
    if output == ROOT or ROOT in output.parents:
        parser.error("Output must be outside the source tree.")
    source = public_files()
    output.mkdir(parents=True, exist_ok=True)
    manifest = {name: hashlib.sha256(data).hexdigest() for name, data in source.items()}
    full = {f"my-exobrain/{name}": data for name, data in source.items()}
    full["my-exobrain/SHA256SUMS.txt"] = "".join(f"{sha}  {name}\n" for name, sha in manifest.items()).encode()
    skill = {"my-exobrain/" + name.removeprefix("skills/my-exobrain/"): data
             for name, data in source.items() if name.startswith("skills/my-exobrain/")}
    skill["my-exobrain/LICENSE"] = source["LICENSE"]
    write_zip(output / "my-exobrain-v0.1.0.zip", full)
    write_zip(output / "my-exobrain-skill-v0.1.0.zip", skill)
    report = {"version": "0.1.0", "public_file_count": len(source), "files": manifest,
              "archives": {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                           for path in sorted(output.glob("*.zip"))}}
    (output / "manifest.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"public_file_count": len(source), "archives": report["archives"]}, indent=2))


if __name__ == "__main__":
    main()
