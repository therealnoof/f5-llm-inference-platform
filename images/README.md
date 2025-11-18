# Images Directory

This directory contains images and screenshots for the F5 AI Guardrails Coffee Shop application.

## Purpose

Store images for:
- Documentation screenshots
- User interface examples
- Configuration guides
- Architecture diagrams
- Demo screenshots

## Usage

### Adding Images

Simply copy or save images to this directory:

```bash
# Copy an image
cp /path/to/screenshot.png images/

# Or save directly from screenshots
# macOS: Cmd+Shift+4, then drag to save
```

### Referencing in Markdown

Use relative paths in your markdown files:

```markdown
![App Screenshot](images/screenshot.png)
![Configuration](images/config-example.png)
```

### Referencing in Documentation

From the root directory:
```markdown
![Example](./images/example.png)
```

From subdirectories:
```markdown
![Example](../images/example.png)
```

## Recommended Image Formats

- **Screenshots**: PNG (best quality, lossless)
- **Diagrams**: PNG or SVG
- **Photos**: JPG (smaller file size)
- **Icons**: PNG or SVG

## File Naming Conventions

Use descriptive, lowercase names with hyphens:

- `app-main-interface.png`
- `guardrails-config-step1.png`
- `blocked-prompt-example.png`
- `settings-sidebar.png`
- `architecture-diagram.svg`

## Current Images

(Add descriptions here as you add images)

---

**Note**: Keep images under 2MB when possible for faster repository cloning and documentation loading.
