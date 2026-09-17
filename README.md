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

## Documentation:

<img width="731" height="665" alt="image" src="https://github.com/user-attachments/assets/8851e5f1-09a6-4772-8e45-d9b35320d480" />

<img width="960" height="1057" alt="image1" src="https://github.com/user-attachments/assets/13c4664b-5df5-41ed-97f0-f4a9a49786ed" />

<img width="961" height="1056" alt="image2" src="https://github.com/user-attachments/assets/59df6701-0306-4661-9b1d-b2a0ead0e094" />

<img width="946" height="1050" alt="image3" src="https://github.com/user-attachments/assets/7478540b-3578-40f2-a27e-1ee5deb88d4f" />

<img width="957" height="1056" alt="image4" src="https://github.com/user-attachments/assets/9e64d84b-e0bf-41a5-9e02-65d2bcb9799c" />

<img width="954" height="1053" alt="image5" src="https://github.com/user-attachments/assets/3b0ce8ed-ed71-438a-8b5d-319dc0a264a3" />

<img width="960" height="1059" alt="image6" src="https://github.com/user-attachments/assets/333b4b2b-531b-48b9-a356-167ff00fff01" />

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
