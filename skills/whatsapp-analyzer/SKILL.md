---
name: whatsapp-analyzer
description: >-
  Use when the user provides WhatsApp chat export zip files and wants to extract,
  transcribe, and compile all information into a structured report. Triggers on
  mentions of WhatsApp exports, chat analysis, audio transcription from WhatsApp
  voice messages, or compiling conversation history from exported chats.
license: MIT
metadata:
  author: nacif
  version: "0.1.0"
---

# WhatsApp Chat Export Analyzer

## Purpose

Turn one or more WhatsApp chat export zips into a single structured report: full
conversation text, transcribed voice messages, OCR'd images (receipts,
screenshots), and extracted PDF contents, all cross-referenced on a timeline.

## When to use

- Use when: the user has `.zip` files exported from WhatsApp ("Export chat" with
  media) and wants the contents analyzed, transcribed, or summarized — e.g. for a
  dispute, a project history, or a financial reconciliation.
- Do not use when: the user has a live WhatsApp account to query (this skill works
  only on export files), or the audio is from another source (the opus→ogg
  conversion step is WhatsApp-specific).

## Inputs

- **WhatsApp export zip file(s)** — ask the user for the location/directory.
- **`OPENAI_API_KEY` env var** — required for voice transcription (Whisper API).
  Check with `test -n "$OPENAI_API_KEY"`; if unset, ask the user to export it.
  Never ask the user to paste the key into the conversation.
- **ffmpeg** — required for audio conversion. Check with `ffmpeg -version`;
  install via the system package manager (e.g. `brew install ffmpeg`).
- **`openai` Python package** — `pip install openai`.
- **Report focus** (optional) — ask what to prioritize: payments, dates,
  agreements, deliverables, etc.
- **Conversation language** (e.g. `en`, `pt`, `es`) — needed for accurate
  transcription; infer from `_chat.txt` if the user doesn't say.

## Procedure

### 1. Unzip exports

Each export zip contains:

- `_chat.txt` — the full text conversation
- `*.opus` — voice messages
- `*.jpg` / `*.png` — photos and screenshots
- `*.pdf` — shared documents
- `*.mp4` — videos (cannot be transcribed via Whisper; note their existence)

```bash
unzip -o "WhatsApp Chat - ContactName.zip" -d "chat_contactname"
```

### 2–5. Extract everything (in parallel)

After unzipping, launch steps 2–5 as **parallel background subagents** so
everything is processed simultaneously. Give each agent the full file list and
any context about the parties/project:

1. **Chat reader** — reads all `_chat.txt` files. Format is
   `[DD/MM/YY, HH:MM:SS] Sender: Message`; media appears as
   `<attached: filename.ext>`. Read large files in chunks (offset/limit).
2. **PDF reader** — reads every `.pdf` (contracts, invoices, quotes). Extract
   financial figures, terms, dates, and obligations.
3. **Image reader** — reads/OCRs every `.jpg`/`.png`. Look for payment and
   transfer receipts (date, amount, sender, recipient, transaction ID), order
   screenshots, and progress photos. Read ALL images — receipts often don't look
   like receipts from the filename.
4. **Audio transcriber** — runs `scripts/transcribe_audio.py` (see below) over
   every folder containing `.opus` files.

Wait for all four to complete before compiling.

### Transcribing audio

Whisper does not accept `.opus` directly; each file must be converted to `.ogg`
via ffmpeg first. `scripts/transcribe_audio.py` handles the whole loop:

```bash
python scripts/transcribe_audio.py chat_folder1 chat_folder2 \
  --language pt --output transcriptions.json
```

It writes a JSON map of `folder/filename → transcript` and records per-file
errors instead of aborting the batch.

**Identify speakers:** audio filenames embed timestamps
(`...AUDIO-YYYY-MM-DD-HH-MM-SS.opus`). Match them against `_chat.txt`:

```
[09/09/25, 16:23:42] Sam P.: <attached: 00000138-AUDIO-2025-09-09-16-23-42.opus>
```

tells you "Sam P." sent that audio at that timestamp.

### 6. Compile the report

Merge all four extraction outputs into one Markdown report with these sections
(adapt to the user's stated focus):

- **Parties & contacts** — names, roles, companies involved
- **Contracts & agreements** — dates, terms, scope, payment conditions, deadlines
- **Financial summary** — table of confirmed payments (from receipts), outstanding
  balances, payments without corresponding delivery
- **Services & deliverables** — contracted vs. delivered vs. pending
- **Chronological timeline** — key events, decisions (from text + audio), issues
  reported, schedule changes and reasons
- **Current status** — done / pending / blocked, open questions

Cross-reference payment images with the surrounding chat messages to identify
what each payment was for.

## Validation

- `transcriptions.json` exists and contains an entry per `.opus` file; grep it
  for `"ERROR:"` and retry or flag any failures.
- Every media file referenced as `<attached: ...>` in `_chat.txt` was either
  processed or explicitly listed as skipped (e.g. videos).
- Financial-summary amounts each trace back to a specific receipt image or PDF.

## Common failure modes

- Whisper API rejects `.opus` → always convert to `.ogg` via ffmpeg first (the
  script does this).
- Wrong-language transcripts → always pass `--language` explicitly; don't rely
  on auto-detection.
- Huge `_chat.txt` files → read in chunks with offset/limit, never all at once.
- Same audio appearing in multiple exports (forwarded messages) → dedupe by
  filename before transcribing.
- Attributing audio to the wrong person → match the filename timestamp against
  `_chat.txt`, don't guess from content.

## Supporting files

- `scripts/transcribe_audio.py` — batch opus→ogg→Whisper transcription helper.
