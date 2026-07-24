"""Render the normative Markdown specification as informative HTML."""

from __future__ import annotations

import argparse
import hashlib
import html
import re
import unicodedata
from pathlib import Path

from markdown_it import MarkdownIt
from markdown_it.token import Token

REPOSITORY = Path(__file__).resolve().parent.parent
DEFAULT_SOURCE = REPOSITORY / "SPEC.md"
DEFAULT_OUTPUT = REPOSITORY / "SPEC.html"


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii").lower()
    return re.sub(r"[^a-z0-9]+", "-", ascii_text).strip("-") or "section"


def heading_text(tokens: list[Token], index: int) -> str:
    if index + 1 >= len(tokens) or tokens[index + 1].type != "inline":
        return "section"
    return tokens[index + 1].content


def add_heading_ids(tokens: list[Token]) -> list[tuple[int, str, str]]:
    used: dict[str, int] = {}
    headings: list[tuple[int, str, str]] = []
    for index, token in enumerate(tokens):
        if token.type != "heading_open":
            continue
        level = int(token.tag[1:])
        title = heading_text(tokens, index)
        base = slugify(title)
        occurrence = used.get(base, 0) + 1
        used[base] = occurrence
        identifier = base if occurrence == 1 else f"{base}-{occurrence}"
        token.attrSet("id", identifier)
        headings.append((level, title, identifier))
    return headings


def navigation(headings: list[tuple[int, str, str]]) -> str:
    items = [
        f'<li class="level-{level}"><a href="#{html.escape(identifier)}">'
        f"{html.escape(title)}</a></li>"
        for level, title, identifier in headings
        if level in {2, 3}
    ]
    return "<ol>" + "".join(items) + "</ol>"


def render(markdown: str) -> str:
    parser = MarkdownIt(
        "commonmark",
        {"html": False, "linkify": False, "typographer": False},
    ).enable("table")
    tokens = parser.parse(markdown)
    headings = add_heading_ids(tokens)
    body = parser.renderer.render(tokens, parser.options, {})
    fingerprint = hashlib.sha256(markdown.encode("utf-8")).hexdigest()
    title = headings[0][1] if headings else "Nano Markup specification"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="generator" content="Nano Markup tools/render_spec.py">
  <meta name="source-sha256" content="{fingerprint}">
  <title>{html.escape(title)}</title>
  <style>
    :root {{ color-scheme: light dark; --paper: #ffffff; --ink: #17202a;
      --muted: #586174; --line: #d8dee8; --accent: #3157a4;
      --code: #f4f6f9; --notice: #eef4ff; }}
    @media (prefers-color-scheme: dark) {{ :root {{ --paper: #12161d;
      --ink: #e7ebf2; --muted: #aab3c2; --line: #343c49;
      --accent: #8eb4ff; --code: #1b212b; --notice: #18243a; }} }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{ margin: 0; background: var(--paper); color: var(--ink);
      font: 16px/1.62 system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
      sans-serif; }}
    .layout {{ display: grid; grid-template-columns: minmax(14rem, 18rem) minmax(0, 1fr);
      gap: 3rem; max-width: 78rem; margin: 0 auto; padding: 2.5rem 2rem 5rem; }}
    nav {{ position: sticky; top: 1rem; align-self: start; max-height: calc(100vh - 2rem);
      overflow: auto; font-size: .88rem; }}
    nav strong {{ display: block; margin-bottom: .6rem; }}
    nav ol {{ list-style: none; margin: 0; padding: 0; }}
    nav li {{ margin: .18rem 0; }} nav .level-3 {{ margin-left: .75rem; }}
    main {{ min-width: 0; }}
    h1 {{ font-size: clamp(2rem, 5vw, 3rem); line-height: 1.1; margin-top: 0;
      overflow-wrap: anywhere; }}
    h2 {{ margin-top: 3.2rem; padding-bottom: .35rem; border-bottom: 1px solid var(--line); }}
    h3 {{ margin-top: 2.2rem; }}
    a {{ color: var(--accent); }}
    table {{ display: block; max-width: 100%; overflow-x: auto;
      border-collapse: collapse; margin: 1.25rem 0; }}
    th, td {{ border: 1px solid var(--line); padding: .55rem .7rem; text-align: left; }}
    pre {{ overflow-x: auto; background: var(--code); border: 1px solid var(--line);
      border-radius: .45rem; padding: 1rem; line-height: 1.45; }}
    code {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      font-size: .92em; }}
    :not(pre) > code {{ background: var(--code); border-radius: .25rem; padding: .1em .3em; }}
    blockquote {{ border-left: .25rem solid var(--line); margin-left: 0; padding-left: 1rem;
      color: var(--muted); }}
    .notice {{ background: var(--notice); border: 1px solid var(--line);
      border-radius: .5rem; padding: .85rem 1rem; margin: 0 0 2rem;
      overflow-wrap: anywhere; }}
    footer {{ border-top: 1px solid var(--line); color: var(--muted); margin-top: 4rem;
      padding-top: 1rem; font-size: .85rem; overflow-wrap: anywhere; }}
    @media (max-width: 800px) {{ .layout {{ display: block; padding: 1.5rem 1rem 4rem; }}
      nav {{ position: static; max-height: none; margin-bottom: 2rem; }} nav .level-3 {{ display: none; }} }}
    @media print {{ nav {{ display: none; }} .layout {{ display: block; max-width: none; padding: 0; }}
      body {{ color: #000; background: #fff; }} a {{ color: inherit; }} pre {{ white-space: pre-wrap; }} }}
  </style>
</head>
<body>
  <div class="layout">
    <nav aria-label="Specification sections">
      <strong>Contents</strong>
      {navigation(headings)}
    </nav>
    <main>
      <aside class="notice"><strong>Informative HTML rendering.</strong>
        <a href="SPEC.md">SPEC.md</a> at the corresponding immutable Git tag
        is the normative specification.</aside>
      {body}
      <footer>Generated deterministically from <code>SPEC.md</code>.
        Source SHA-256: <code>{fingerprint}</code>.</footer>
    </main>
  </div>
</body>
</html>
"""


def main() -> None:
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    argument_parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    argument_parser.add_argument("--check", action="store_true")
    arguments = argument_parser.parse_args()

    rendered = render(arguments.source.read_text(encoding="utf-8"))
    if arguments.check:
        if (
            not arguments.output.is_file()
            or arguments.output.read_text(encoding="utf-8") != rendered
        ):
            raise SystemExit(
                f"{arguments.output}: generated HTML is stale; run tools/render_spec.py"
            )
        print(f"{arguments.output.name} matches {arguments.source.name}")
        return
    arguments.output.write_text(rendered, encoding="utf-8", newline="\n")
    print(f"rendered {arguments.source} to {arguments.output}")


if __name__ == "__main__":
    main()
