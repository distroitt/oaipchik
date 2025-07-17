# Linter for Qt Creator

---

## Description

**Linter** is a static code analysis tool that automatically checks source code for:
- errors;
- inconsistencies with coding style or standards;
- potential problems that worsen the quality of the code, but do not affect its execution.

### Why do you need a custom linter for Qt/Qt Creator?

Existing solutions either integrate poorly with Qt projects or do not take into account the specifics of working with the **Qt** library. The custom linter was created to:
- **Unify the code style** in student and team projects - this facilitates joint development and review;
- **Automatically detect errors specific to Qt** (for example, violations in working with signals/slots, components, macros);
- **Minimize subjectivity in reviews** with transparent and automated criteria;
- **Quickly modify to the needs of a course or a specific team:** easily add or change rules;
- **Save time for teachers and reviewers** on manual style and typical errors checking.

A custom linter simplifies standardization, speeds up checking, and improves the quality of Qt projects - something that cannot be achieved with standard tools.

---

# Installation

Before using the linter, make sure that **Qt6** and other necessary tools are installed on your system. Installation depends on your operating system.

# Installation on macOS

1. Make sure that **XCode** is installed.
2. Install **Qt** via **Homebrew**:
```bash
brew install qt
```
3. Install **Qt Creator**:
```bash
brew install --cask qt-creator
```
> **Note:**
> The `brew install --cask qt-creator` command downloads Qt Creator from the official website. If access to the resource is limited, use VPN or download the installation files manually.

# Installing on Linux (Ubuntu/Debian)

1. Install Qt base libraries:
```bash
sudo apt install -y qt6-base-dev
```
2. Install **Qt Creator**:
```bash
sudo apt install -y qtcreator
```
3. Run Qt Creator after installation is complete:
```bash
qtcreator
```

---

# Setting up the linter

1. Clone the repository with the linter:
```bash
git clone https://github.com/distroitt/oaipchik.git
```
2. Go to the folder with the linter:
```bash
cd oaipchik
```
3. Run the linter to analyze your Qt project:
```bash
python3 main.py
```
> **Note:**
> If `sudo apt install python3` and `brew install python3` fail, download Python 3 from the official site.
> This script will automatically configure everything needed for the installed QtCreator. You may need superuser privileges to install packages.

---

## Testing the linter

A test file **check.txt** has been added to the repository to check the linter's operation.

### What the `check.txt` file contains:
- Code examples for checking linting rules.
- Steps for running tests.

### How to test the linter:

1. Find the `check.txt` file in the root of the repository.
2. Follow the instructions in the file to run the tests.
3. Make sure the linter detects the expected errors and warnings.

---

## Updating the linter

If there are updates, do the following:

1. Go to the folder with the linter:
```bash
cd oaipchik
```
2. Enter the command again:
```bash
python3 main.py
```

---

## Contacts

If you have any questions or suggestions, contact us:

- **Telegram:** [distroit](https://t.me/distroit)
- **Telegram:** [v_k_walker](https://t.me/v_k_walker)
