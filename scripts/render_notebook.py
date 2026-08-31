from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "iceberg.ipynb"
OUTPUT = ROOT / "site" / "notebook-rendered.html"


def main() -> None:
    nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    title = nb.get("metadata", {}).get("kernelspec", {}).get("display_name", "Notebook")
    cells_html = []
    for cell in nb.get("cells", []):
        source = "".join(cell.get("source", []))
        if cell.get("cell_type") == "markdown":
            rendered = (
                html.escape(source)
                .replace("\n\n", "</p><p>")
                .replace("\n", "<br>")
                .replace("# ", "<h1>")
            )
            cells_html.append(f'<section class="nb-cell markdown"><pre>{rendered}</pre></section>')
        else:
            outputs = []
            for out in cell.get("outputs", []):
                text = ""
                if out.get("output_type") == "stream":
                    text = "".join(out.get("text", []))
                elif out.get("output_type") in {"execute_result", "display_data"}:
                    data = out.get("data", {})
                    text = "".join(data.get("text/plain", [])) if isinstance(data.get("text/plain"), list) else str(data.get("text/plain", ""))
                elif out.get("output_type") == "error":
                    text = f"{out.get('ename', '')}: {out.get('evalue', '')}"
                if text:
                    outputs.append(f"<div class='nb-output'>{html.escape(text)}</div>")
            cells_html.append(
                f'<section class="nb-cell code"><pre>{html.escape(source)}</pre>{"".join(outputs)}</section>'
            )

    OUTPUT.write_text(
        f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Notebook Render</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    body{{margin:0;font-family:'Inter',sans-serif;background:#07111d;color:#e8f2ff}}
    .wrap{{max-width:1100px;margin:0 auto;padding:28px 24px 72px}}
    h1{{font-family:'Space Grotesk',sans-serif;margin:0 0 8px}}
    .meta{{color:#8ca4c3;font-family:'JetBrains Mono',monospace;font-size:12px;margin-bottom:20px}}
    .nb-cell{{margin-top:16px;padding:18px;border-radius:18px;border:1px solid rgba(138,168,209,.14);background:rgba(255,255,255,.03)}}
    .nb-cell pre{{margin:0;white-space:pre-wrap;word-break:break-word;font-family:'JetBrains Mono',monospace;font-size:13px;line-height:1.65}}
    .nb-output{{margin-top:12px;padding:14px;border-radius:14px;background:rgba(89,167,255,.08);border:1px solid rgba(89,167,255,.14);color:#dce9fb;white-space:pre-wrap}}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="meta">{html.escape(title)} · rendered notebook</div>
    <h1>Iceberg notebook</h1>
    <div class="meta">This rendered copy is generated from `iceberg.ipynb` and shown inside the site viewer.</div>
    {"".join(cells_html)}
  </div>
</body>
</html>""",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
