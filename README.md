# jevgram

`jevgram` is a command-line tool that checks if a document is AI-generated. Similar to pangram but a lot cheaper (you'll need API key from <https://console.typesafe.ai/login> - free, super easy, couple of clicks)

## Supported inputs

- Plain text and source-like text files, such as `.txt`, `.md`, `.tex`, and similar files
- PDF files
- DOCX files

## Minimal example:

```bash
Go to https://typesafe.ai and get an API key. Copy the key
$ export TYPESAFE_API_KEY=apikey_...
$ pipx install jevgram
$ jevgram README.md # try jevgram on this document
File: README.md
Type: text
Characters extracted: 3044
Characters sent to JEV: 3044
Model: jev-1.13.0
Prediction: AI
Probability AI: 79.00%
Probability human: 21.00%
Confidence: 58.00%
```

PDF extraction uses `pypdf`. DOCX extraction is handled directly from the Word XML contained in the `.docx` file.

# Detailed instructions


## Install (MacOS, Linux; Windows coming up)

```bash
pipx install jevgram
```

## Get a TypeSafe API key

   `jevgram` needs a TypeSafe API key to call JEV.

1. Login to TypeSafe: <https://console.typesafe.ai/login>

   (if you don't have an account, create one, for example just clicking on "Login with Google")

2. Click **API Keys** on the left, then **Create API key** on the right

3. Copy the key and save it somewhere private.

4. Set the key in your terminal:

```bash
export TYPESAFE_API_KEY="paste-your-key-here"
```

To avoid setting the key every time, add the export TYPESAFE_API_KEY=... line to your shell profile, such as ~/.bashrc or ~/.zshrc.

You can also pass a key directly with `--api-key`, but environment variables are safer/easier.

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
not free. Works like this: once you create a TypeSafe account and API
key, you may get a credit for $5 free usage. jevgram is intended for
personal use, and you can check a lot of documents for $5 (I tried
dozens so far, I have yet to spend 1 cent). Once you use up the free
credit, jevgram will fail and politely tell you to add credit card
number to TypeSafe (to be fair, this is untested because I have not
reached that point yet)

## Notes

Authorship detection is probabilistic, so if you run jevgram multiple
times on the same document, you'll get different (though pretty
similar) probablities

