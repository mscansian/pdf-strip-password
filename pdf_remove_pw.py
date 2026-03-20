#!/usr/bin/env python3

import argparse
import getpass
import sys
import tempfile
from pathlib import Path

import argcomplete
from pypdf import PdfReader, PdfWriter


def strip_password(input_path: Path, output_path: Path, password: str) -> None:
    reader = PdfReader(str(input_path))

    result = reader.decrypt(password)
    if result == 0:
        raise ValueError("Invalid password or the PDF could not be decrypted.")

    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    if reader.metadata:
        writer.add_metadata(reader.metadata)

    with output_path.open("wb") as f:
        writer.write(f)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Open a password-protected PDF and save a copy without password protection."
    )
    parser.add_argument("input", help="Path to the input PDF")
    parser.add_argument("-o", "--output", help="Path to the output PDF (default: overwrite input)")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output) if args.output else input_path

    if not input_path.exists():
        print(f"Error: input file does not exist: {input_path}", file=sys.stderr)
        return 1

    reader = PdfReader(str(input_path))
    if not reader.is_encrypted:
        print("PDF is not password protected, nothing to do.")
        return 0

    password = getpass.getpass("PDF password: ")

    in_place = input_path.resolve() == output_path.resolve()
    tmp_path: Path | None = None

    try:
        if in_place:
            with tempfile.NamedTemporaryFile(
                dir=input_path.parent, suffix=".pdf", delete=False
            ) as tmp:
                tmp_path = Path(tmp.name)
            strip_password(input_path, tmp_path, password)
            tmp_path.replace(input_path)
            print(f"Stripped password from: {input_path}")
        else:
            strip_password(input_path, output_path, password)
            print(f"Saved decrypted PDF to: {output_path}")
        return 0
    except Exception as e:
        if tmp_path and tmp_path.exists():
            tmp_path.unlink()
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())