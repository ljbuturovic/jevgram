# jevgram

`jevgram` is a small command-line tool that estimates whether a document was primarily written by AI or by a human using JEV. It is intended as a lightweight, scriptable alternative for occasional authorship checks.

## Supported inputs

- Plain text and source-like text files, such as `.txt`, `.md`, `.tex`, and similar files
- PDF files
- DOCX files

PDF extraction uses `pypdf`. DOCX extraction is handled directly from the Word XML contained in the `.docx` file.

## Install

With `pipx`:

```bash
pipx install jevgram
```

With `uvx`:

```bash
uvx jevgram --help
```

## API key

`jevgram` calls the TypeSafe JEV API. Set one of these environment variables before running it:

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

## Notes

Authorship detection is probabilistic. Treat the result as one signal, not as proof. Results can vary with document length, extraction quality, formatting, and how much of the document is sent to JEV.
