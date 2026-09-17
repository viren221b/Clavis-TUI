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

<img width="954" height="708" alt="image" src="https://github.com/user-attachments/assets/069be15e-84cf-4d17-9b4c-09805c5363ad" />

<img width="934" height="687" alt="image1" src="https://github.com/user-attachments/assets/b7bd7137-ec57-4dcc-bfdc-07a12464bd2f" />

<img width="936" height="687" alt="image2" src="https://github.com/user-attachments/assets/7ced5d49-c3a6-41c0-8e3c-5be9fb1629ea" />

<img width="946" height="687" alt="image3" src="https://github.com/user-attachments/assets/89e996ab-873f-43b3-8697-106069ff69e5" />

<img width="957" height="691" alt="image4" src="https://github.com/user-attachments/assets/6d83fe83-19ce-447e-a70a-6e31ded95c79" />

<img width="946" height="691" alt="image5" src="https://github.com/user-attachments/assets/01f03f11-d5b7-4807-aa28-195b8fc75b49" />

<img width="954" height="700" alt="image6" src="https://github.com/user-attachments/assets/258a6236-aa1e-4424-a23b-bf852a60d5e1" />

## Security

Clavis encrypts all entry data before saving it to disk. 
Your master password never gets stored — only a secure hash 
is kept to verify it. Without the correct password, 
the vault cannot be opened. (So please make sure you know your password)

## Platform

Built and tested on Arch Linux. Should work on any Linux 
distribution and macOS with Python 3.14+ installed.

## License

GPL-v3
