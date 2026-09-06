# Publishing This Project to GitHub

Follow these steps from inside the `orangehrm-qa` project folder.

## 1. Create the GitHub repository
1. Go to https://github.com and log in.
2. Click the **+** icon (top right) → **New repository**.
3. Repository name: `orangehrm-qa` (or any name you prefer).
4. Set visibility to **Public** (so you can share the link with a recruiter) or **Private** if you'll invite the reviewer directly.
5. **Do not** check "Add a README" or "Add .gitignore" — this project already has both, and initializing them on GitHub would conflict with the local ones when you push.
6. Click **Create repository**. GitHub will show you a page with setup commands — keep it open, you'll need the URL it gives you.

## 2. Folder structure and files
If you're following this guide, the folder structure and all files (Python source, `requirements.txt`, `README.md`, `.gitignore`, `pytest.ini`, `docs/`) already exist locally in `orangehrm-qa/`. Nothing further to create here.

## 3. Initialize Git locally and commit

```bash
cd path/to/orangehrm-qa
git init
git add .
git status
```

Check the `git status` output before committing — confirm no unexpected files (like a stray `venv/` folder, if `.gitignore` didn't catch it) are staged.

```bash
git commit -m "Initial commit: OrangeHRM QA assignment (manual test cases + Selenium POM automation)"
```

## 4. Connect to the GitHub remote and push

GitHub will show you the exact remote URL after creating the repo; it looks like this:

```bash
git remote add origin https://github.com/<your-username>/orangehrm-qa.git
git branch -M main
git push -u origin main
```

If prompted for credentials, GitHub now requires a **Personal Access Token** (not your account password) or signing in via the Git Credential Manager / GitHub CLI (`gh auth login`) if you have it installed.

## 5. Verify

Refresh the repository page on GitHub. You should see:
- `pages/`, `tests/`, `utils/`, `docs/`, `screenshots/` folders
- `requirements.txt`, `pytest.ini`, `README.md`, `.gitignore`

## 6. Get the repository URL

Your repository URL will be:

```
https://github.com/<your-username>/orangehrm-qa
```

This is the link to paste into the assignment document (Section 7 — GitHub Repository) and to share with the recruiter.

## 7. (Optional) Keep it updated

Any time you make further changes locally:

```bash
git add .
git commit -m "Describe what changed"
git push
```
