# PDF Strip Password
A simple command-line tool to remove password protection from PDF files. It decrypts a password-protected PDF and saves an unprotected copy.

## Getting Started

Install the package:

```bash
pip install -e .
```

## Usage

Strip password from a PDF (overwrites in place):

```bash
pdf-strip-pw input.pdf
```

Or save to a separate file:

```bash
pdf-strip-pw input.pdf -o output.pdf
```

You will be prompted for the password via stdin.
