# Smart Agricultural System

A beginner-friendly Python desktop app for managing crops, getting crop suggestions, recording sales and expenses, and viewing farm finances.

## Requirements

- Python 3.10 or newer
- Tkinter (normally included with Python)
- Git

## Complete setup

### 1. Download the project

```bash
git clone https://github.com/meherajmithun/sdp-project.git
cd sdp-project/SDP_200
```

### 2. Create a virtual environment

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install and run

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
```

Register an account, sign in, then add a crop from **Crop Management**. Press `Esc` to leave full-screen mode.

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Documentation

- [Improvement tracker](docs/IMPROVEMENTS.md)
- [Feature plan](docs/FEATURE_PLAN.md)
- [Crop management study plan](docs/CROP_MANAGEMENT_PLAN.md)

## Common problems

- `No module named customtkinter`: activate `.venv` and install the requirements again.
- `No module named tkinter`: install Python with Tkinter support, then recreate `.venv`.
- Do not use the included old `venv` folders; always create a fresh `.venv`.
