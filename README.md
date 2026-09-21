# jevgram

`jevgram` is a small command-line tool that checks if a document is AI-generated. Similar to pangram but a lot cheaper. You need API key from TYPESAFE_API_KEY (super easy, couple of clicks)

## Supported inputs

- Plain text and source-like text files, such as `.txt`, `.md`, `.tex`, and similar files
- PDF files
- DOCX files

## Minimal example:

```bash
$ export TYPESAFE_API_KEY=apikey_...
$ pipx install jevgram
$ jevgram README.md # this document
File: README.md
Type: text
Characters extracted: 1957
Characters sent to JEV: 1957
Model: jev-1.13.0
Prediction: AI
Probability AI: 87.00%
Probability human: 13.00%
Confidence: 74.00%
```

PDF extraction uses `pypdf`. DOCX extraction is handled directly from the Word XML contained in the `.docx` file.

# Detailed instructions

## Install

With `pipx` (MacOS, Linux):

```bash
pipx install jevgram
```

With `uvx`:

```bash
uvx jevgram --help
```

## API key

`jevgram` uses TypeSafe JEV API. Set one of these environment variables before running it:

```bash
export TYPESAFE_API_KEY="your-key"
# or
export JEV_API_KEY="your-key"
```

You can also pass a key directly with `--api-key`, but environment variables are safer for shell history and scripts.

## Usage

```bash
jevgram document.txt
jevgram paper.pdf
jevgram manuscript.docx --json
```

By default, long files are sampled down to 32,000 characters using the beginning, middle, and end of the extracted text. To send the whole extracted document, use:

```bash
jevgram document.txt --max-chars 0
```

To inspect extraction without calling JEV:

```bash
jevgram document.pdf --extract-only
```

To inspect the request body without calling JEV:

```bash
jevgram document.txt --dump-request
```

## Output

Human-readable output includes the predicted class, AI probability, human probability, confidence when provided by JEV, and whether the input was truncated. `--json` produces machine-readable output for scripts.

## Cost

This app is open-source/free on my end, but it uses JEV API, which is
not free. Works like this: once you create a TYPESAFE account and API
key, you get a credit for $5 free usage. jevgram is intended for
personal use, and you can check a lot of documents for $5. Once you
use up the free credit, jevgram will fail and politely tell you to add
credit card number to TYPESAFE (to be fair, this is untested because I
have not reached that point yet)

## Notes

Authorship detection is probabilistic.

This document is mostly AI :-) 

