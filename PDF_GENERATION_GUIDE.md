# 📄 PDF Generation Workflow Guide

## Overview

This workflow automates the conversion of markdown resumes to professional PDFs.

### Workflow Steps

1. **Trigger**: When you push/edit `.md` files to `output/`
2. **Convert**: Markdown → HTML → Professional PDF
3. **Review**: Automatic PR created for your review
4. **Store**: PDFs saved to `output/pdfs/` and GitHub artifacts
5. **Download**: 30-day artifact retention

---

## 📥 How to Use

### Step 1: Generate/Edit Markdown
Claude generates CV markdown files → Pushes to `output/` folder

### Step 2: Workflow Runs Automatically
- GitHub Actions automatically triggers
- Converts all `.md` files to `.pdf`
- Creates a Pull Request

### Step 3: Review & Edit
- Review the markdown content
- Edit `.md` files if needed
- PDFs auto-regenerate on each change

### Step 4: Download PDFs
**Option A - From Artifacts (Fastest)**
1. Go to **Actions** tab
2. Select the latest workflow run
3. Click **Artifacts** → `resume-pdfs`
4. Download the ZIP file

**Option B - From Repository**
1. After merging the PR
2. Navigate to `output/pdfs/` folder
3. Download individual PDF files

---

## 🔧 Configuration

### Edit the Workflow
File: `.github/workflows/resume-to-pdf.yml`

Key settings you can modify:
```yaml
# Trigger on file changes
paths:
  - 'output/*.md'

# PDF margins (in inches)
--margin-top 0.75in
--margin-bottom 0.75in
--margin-left 0.75in
--margin-right 0.75in

# Page size
--page-size A4

# Artifact retention (days)
retention-days: 30
```

### Customize Styling
File: `.github/resume-style.css`

Modify:
- Fonts
- Colors
- Spacing
- Font sizes
- Line heights

---

## 🐛 Troubleshooting

### PDFs not generating?
1. Check **Actions** tab for error logs
2. Verify `.md` files are in `output/` folder
3. Ensure markdown is valid

### PDF looks wrong?
1. Edit `.github/resume-style.css`
2. Push the changes
3. Run workflow again: `workflow_dispatch`

### Artifacts not available?
- Artifacts auto-delete after 30 days
- Merge the PR to save PDFs permanently to repo
- Check `output/pdfs/` folder after merge

---

## 📋 File Structure

```
repo/
├── .github/
│   ├── workflows/
│   │   └── resume-to-pdf.yml      ← Main workflow
│   └── resume-style.css            ← PDF styling
├── output/
│   ├── YourName_Resume.md          ← Input (markdown)
│   ├── YourName_Resume.html        ← Intermediate (HTML)
│   └── pdfs/
│       └── YourName_Resume.pdf     ← Output (PDF)
└── ...
```

---

## ⚙️ Advanced Options

### Manual Trigger
Click **Actions** → Select workflow → **Run workflow**

### Change PDF Format
Edit `.github/workflows/resume-to-pdf.yml`:
```yaml
# Change from A4 to Letter
--page-size Letter
```

### Add More Styling
Edit `.github/resume-style.css` to customize appearance

---

## 📞 Need Help?

Check the workflow logs:
1. Go to **Actions** tab
2. Click the failed workflow run
3. Expand **Convert markdown to PDF** step
4. View error messages

---

*Last updated: 2026-05-20*
