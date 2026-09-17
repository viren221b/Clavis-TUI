# Clavis

A terminal-based encrypted vault for journal entries and passwords. 
Built with Python and Textual, Clavis keeps your data secure and 
accessible entirely from the terminal.

## Features

- Encrypted vault with master password protection
- Add, view, edit, and delete entries
- Live search across all your entries
- Clean TUI with keyboard navigation
- Persistent theme selection (WIP)

## Requirements

- Python 3.14+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

## Installation

### Using uv (recommended)

```bash
git clone https://github.com/viren221b/clavis-tui
cd clavis-tui
uv tool install .
```

Then run it from anywhere:

```bash
clavis
```

### Using pip

```bash
git clone https://github.com/viren221b/clavis-tui
cd clavis-tui
pip install -r requirements.txt
python src/clavis_tui/clavis.py
```

## Usage

| Key | Action |
|-----|--------|
| `a` | Add entry |
| `e` | Edit selected entry |
| `d` | Delete selected entry |
| `ctrl+f` | Toggle search bar |
| `ctrl+w` | Save (in add/edit screens) |
| `esc` | Cancel / go back |
| `ctrl+p` | Command palette (change theme) |
| `q` | Quit |

## Security

Clavis encrypts all entry data before saving it to disk. 
Your master password never gets stored — only a secure hash 
is kept to verify it. Without the correct password, 
the vault cannot be opened. (So please make sure you know your password)

## Platform

Built and tested on Arch Linux. Should work on any Linux 
distribution and macOS with Python 3.14+ installed.

## License

gpl-v3