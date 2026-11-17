# Smart Agricultural System — Improvement Tracker

This file tracks planned improvements for `SDP_200`.

## How to update this tracker

- `[ ]` means the work is not finished.
- `[x]` means the implementation is complete and verified.
- Mark a subtask done in the same commit that implements it.
- Mark a numbered section done only when all of its subtasks are done.
- Run the relevant tests before marking anything complete.

## Planned improvements

- [ ] **1. Improve authentication**
  - [ ] Hash passwords instead of storing plaintext passwords.
  - [ ] Add password confirmation during registration.
  - [ ] Add minimum password-length validation.
  - [ ] Associate crops, sales, and expenses with the logged-in user.
  - [ ] Add a secure password-reset workflow.

- [ ] **2. Improve crop management**
  - [ ] Display saved crops in a table.
  - [ ] Allow users to edit a crop.
  - [ ] Allow users to delete a crop with confirmation.
  - [ ] Prevent accidental duplicate crops.
  - [ ] Provide useful sample crop data for new installations.

- [ ] **3. Improve crop suggestions**
  - [ ] Rank partial matches instead of requiring four exact matches.
  - [ ] Explain why each crop was recommended.
  - [ ] Add temperature as a suggestion input.
  - [ ] Add rainfall as a suggestion input.
  - [ ] Add location as a suggestion input.
  - [ ] Add soil pH as a suggestion input.

- [ ] **4. Improve the interface**
  - [ ] Use `customtkinter.CTk` as the main application window.
  - [ ] Avoid forced full-screen mode on startup.
  - [ ] Support scrolling and smaller screens.
  - [ ] Add clearer empty states and validation messages.
  - [ ] Add consistent confirmation dialogs for destructive actions.
  - [ ] Verify the interface on macOS, Windows, and Linux.

- [ ] **5. Improve finance features**
  - [ ] Allow users to edit sales records.
  - [ ] Allow users to edit expense records.
  - [ ] Add monthly revenue, expense, and balance charts.
  - [ ] Add expense-category summaries.
  - [ ] Add profit-trend reporting.
  - [ ] Add PDF export while keeping CSV export.

- [ ] **6. Improve engineering quality**
  - [ ] Add automated tests for authentication.
  - [ ] Add automated tests for crop management and suggestions.
  - [ ] Expand GUI workflow tests.
  - [ ] Add GitHub Actions to run tests automatically.
  - [ ] Choose and document a tested Python version.
  - [ ] Add formatting and linting checks.
  - [ ] Keep virtual environments, databases, backups, and build files out of Git.

- [ ] **7. Package and release the application**
  - [ ] Add an application icon and version number.
  - [ ] Build a macOS application package.
  - [ ] Build a Windows executable.
  - [ ] Test installation on a clean computer.
  - [ ] Publish downloadable files through GitHub Releases.

## Recommended next sprint

- [ ] Secure password storage.
- [ ] Add per-user data ownership.
- [ ] Add crop editing and deletion.
- [ ] Add automatic tests with GitHub Actions.

## Completed work log

Add a dated note here whenever a numbered section is completed.

| Date | Section | Commit |
| --- | --- | --- |
