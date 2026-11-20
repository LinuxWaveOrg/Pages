#!/usr/bin/env python3
"""把 Foreword 的 Markdown 转成静态页（只用标准库，一次性生成用）。

只认前言实际用到的语法：#/### 标题、段落、| 表格 |、``` 代码块、行内 `code` 与 **粗体**。
正文一律先转义再加标记，避免 `<pkg_name>`、`<占位符>` 这类内容被当成标签。
"""
import html
import re
import sys
from pathlib import Path

PAGE = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
    body {{
        background-color: #0a1b3f;
        color: #ffffff;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        line-height: 1.75;
        margin: 0;
    }}
    main {{ max-width: 860px; margin: 0 auto; padding: 40px 22px 80px; }}
    .back {{ display: inline-block; margin-bottom: 22px; color: #a0b0d0; text-decoration: none; font-size: 0.95rem; }}
    .back:hover {{ color: #ffffff; }}
    h1 {{ font-size: 1.9rem; line-height: 1.3; border-bottom: 2px solid #4a90e2; padding-bottom: 12px; }}
    h3 {{ font-size: 1.2rem; margin-top: 2.2em; color: #ffcc33; }}
    p {{ margin: 0.9em 0; }}
    a {{ color: #4a90e2; }}
    strong {{ color: #ffffff; }}
    code {{
        background-color: #0f1a30;
        padding: 2px 6px;
        border-radius: 4px;
        font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        font-size: 0.9em;
        word-break: break-word;
    }}
    pre {{
        background-color: #08122a;
        border: 1px solid #24365e;
        border-radius: 8px;
        padding: 14px 16px;
        overflow-x: auto;
        line-height: 1.6;
    }}
    pre code {{ background: none; padding: 0; font-size: 0.88rem; }}
    .table-wrap {{ overflow-x: auto; margin: 1.2em 0; }}
    table {{ border-collapse: collapse; width: 100%; font-size: 0.94rem; }}
    th, td {{ border: 1px solid #2a3f6f; padding: 8px 11px; text-align: left; vertical-align: top; min-width: 6.5em; }}
    th {{ background-color: #122a55; white-space: nowrap; }}
    td code {{ white-space: nowrap; }}
</style>
</head>
<body>
<main>
<a class="back" href="../">&larr; {back}</a>
{body}
</main>
</body>
</html>
"""

INLINE_CODE = re.compile(r"`([^`]+)`")
BOLD = re.compile(r"\*\*(.+?)\*\*")


def inline(text):
    """行内的 `code` 与 **粗体**；先占位再处理，避免互相吃掉。"""
    slots = []

    def keep(fragment):
        slots.append(fragment)
        return f"\x00{len(slots) - 1}\x00"

    text = INLINE_CODE.sub(lambda m: keep(f"<code>{html.escape(m.group(1))}</code>"), text)
    text = html.escape(text)
    text = BOLD.sub(lambda m: keep(f"<strong>{m.group(1)}</strong>"), text)
    # 占位可能嵌套（**`code`**）：反复展开，直到不再变化
    while "\x00" in text:
        text = re.sub(r"\x00(\d+)\x00", lambda m: slots[int(m.group(1))], text)
    return text


def render(markdown):
    lines = markdown.split("\n")
    out, index = [], 0
    while index < len(lines):
        line = lines[index]

        if line.startswith("```"):
            index += 1
            block = []
            while index < len(lines) and not lines[index].startswith("```"):
                block.append(lines[index])
                index += 1
            index += 1
            out.append(f"<pre><code>{html.escape(chr(10).join(block))}</code></pre>")
            continue

        heading = re.match(r"^(#{1,6})\s+(.*)$", line)
        if heading:
            level = len(heading.group(1))
            out.append(f"<h{level}>{inline(heading.group(2))}</h{level}>")
            index += 1
            continue

        if line.strip().startswith("|"):
            rows = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                rows.append(lines[index].strip())
                index += 1
            out.append(render_table(rows))
            continue

        if not line.strip():
            index += 1
            continue

        # 列表：`1. xxx` / `- xxx`。前言里的目录清单靠它才不会被压成一行。
        ordered = re.match(r"^(\d+)\.\s+(.*)$", line.strip())
        bullet = re.match(r"^[-*]\s+(.*)$", line.strip())
        if ordered or bullet:
            tag = "ol" if ordered else "ul"
            items = []
            while index < len(lines):
                current = lines[index].strip()
                hit = (re.match(r"^\d+\.\s+(.*)$", current) if ordered
                       else re.match(r"^[-*]\s+(.*)$", current))
                if not hit:
                    break
                items.append(hit.group(1))
                index += 1
            body = "".join(f"<li>{inline(item)}</li>" for item in items)
            out.append(f"<{tag}>{body}</{tag}>")
            continue

        # 段落：行尾两个空格是 Markdown 的硬换行，渲染成 <br>，其余换行折成空格。
        para = []
        while index < len(lines) and lines[index].strip() and not lines[index].strip().startswith("|"):
            if lines[index].startswith("```") or re.match(r"^(#{1,6})\s", lines[index]):
                break
            raw = lines[index]
            para.append((raw.strip(), raw.endswith("  ")))
            index += 1
        pieces = []
        for position, (text, hard) in enumerate(para):
            if position:
                pieces.append("<br>" if para[position - 1][1] else " ")
            pieces.append(inline(text))
        out.append(f"<p>{''.join(pieces)}</p>")

    return "\n".join(out)


def render_table(rows):
    def cells(row):
        return [c.strip() for c in row.strip().strip("|").split("|")]

    header = cells(rows[0])
    body = [cells(r) for r in rows[2:]] if len(rows) > 1 else []
    head = "".join(f"<th>{inline(c)}</th>" for c in header)
    body_rows = "".join(
        "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in row) + "</tr>" for row in body
    )
    return (
        '<div class="table-wrap"><table><thead><tr>'
        + head
        + "</tr></thead><tbody>"
        + body_rows
        + "</tbody></table></div>"
    )


def main():
    source, target, lang, title, back = sys.argv[1:6]
    body = render(Path(source).read_text())
    Path(target).write_text(PAGE.format(lang=lang, title=title, back=back, body=body))
    print(f"{target}  ({len(body.splitlines())} 行正文)")


if __name__ == "__main__":
    main()
