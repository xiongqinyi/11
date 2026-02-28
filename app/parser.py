from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path


class ResumeParseError(Exception):
    pass


def _run_command(cmd: list[str]) -> str:
    completed = subprocess.run(cmd, capture_output=True, text=True)
    if completed.returncode != 0:
        raise ResumeParseError(completed.stderr.strip() or "命令执行失败")
    return completed.stdout.strip()


def extract_text_from_pdf(content: bytes) -> str:
    with tempfile.TemporaryDirectory() as td:
        pdf_path = Path(td) / "resume.pdf"
        txt_path = Path(td) / "resume.txt"
        pdf_path.write_bytes(content)
        _run_command(["pdftotext", str(pdf_path), str(txt_path)])
        return txt_path.read_text(encoding="utf-8", errors="ignore").strip()


def extract_text_from_image(content: bytes) -> str:
    with tempfile.TemporaryDirectory() as td:
        img_path = Path(td) / "resume.png"
        out_base = Path(td) / "ocr"
        img_path.write_bytes(content)
        _run_command(["tesseract", str(img_path), str(out_base), "-l", "chi_sim+eng"])
        txt_path = Path(f"{out_base}.txt")
        if not txt_path.exists():
            raise ResumeParseError("OCR 输出为空")
        return txt_path.read_text(encoding="utf-8", errors="ignore").strip()


def parse_resume_bytes(filename: str, content: bytes) -> str:
    lower = filename.lower()
    if lower.endswith(".pdf"):
        return extract_text_from_pdf(content)
    if lower.endswith((".png", ".jpg", ".jpeg", ".bmp", ".webp")):
        return extract_text_from_image(content)
    raise ResumeParseError(f"不支持的文件类型: {filename}")
