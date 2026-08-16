import tempfile
from pathlib import Path

from convert_docx_posts import convert_docx


ROOT = Path(__file__).resolve().parents[1]

with tempfile.TemporaryDirectory() as directory:
    output = Path(directory)
    convert_docx(ROOT / "posts-docx" / "network.docx", "network", output)
    markdown = (output / "network.md").read_text(encoding="utf-8")
    images = list((output / "assets" / "network").iterdir())
    assert markdown.count("![Network image") == 11
    assert len(images) == 11
