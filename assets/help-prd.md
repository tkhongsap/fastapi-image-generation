# ArtGen – Help Page (User Manual) PRD

**Version:** 1.0   **Last Updated:** 26 Apr 2025

---
## 1 Purpose
Provide a single, easy‑to‑find **Help** page that teaches new users how to generate images successfully in ≤3 minutes and answers common questions—without adding any backend complexity.

---
## 2 Scope
**In‑scope**: Static HTML/Markdown content served at **/help**; navigation link; consistent styling with existing site.  
**Out‑of‑scope**: API docs, changelog, login, search, multilanguage.

---
## 3 Success Metrics
| KPI | Target |
|-----|--------|
|Support tickets about “how to use” | ≤2 per week |
|Avg. time on /help | ≥60 s |
|Bounce rate after landing on /help | ≤40 % |

---
## 4 Functional Requirements
| ID | Requirement | Details |
|----|-------------|---------|
|HLP‑01|Route `/help`|Returns rendered HTML of the manual (template or Markdown→HTML). |
|HLP‑02|Nav Link|Add **Help** to top nav; active state underline. |
|HLP‑03|Content Sections|1) Quick Start (4 steps) 2) Prompt Tips 3) Advanced Options Explained 4) Download & Rights 5) Troubleshooting 6) Contact. |
|HLP‑04|Formatting|Use Tailwind `prose` classes, dark‑mode friendly, max‑width 3xl, responsive. |
|HLP‑05|Anchored TOC (opt.)|Small “On this page” list auto‑links to each H2. |

---
## 5 Non‑Functional Requirements
- Loads ≤1 s on 3G (static file).  
- Accessibility: semantic headings, focusable links, contrast AA.  
- Editable in Markdown so non‑devs can update quickly.

---
## 6 Architecture & Implementation
```python
# route in main.py
@app.get('/help', response_class=HTMLResponse)
async def help_page(request: Request):
    html = markdown.markdown(Path('docs/help.md').read_text(), extensions=['fenced_code','tables'])
    return templates.TemplateResponse('base.html', {
        'request': request,
        'title': 'Help',
        'body': html
    })
```
- **Source**: `docs/help.md` (Markdown).  
- **Template**: reuse `base.html`; wrap body in `<article class="prose ...">`.

---
## 7 Timeline
| Day | Task | Owner |
|----:|------|-------|
|D0|Approve PRD | PM |
|D1|Create route + template skeleton | BE Dev |
|D2|Draft Markdown content | Tech Writer |
|D3|Style & Nav integration | FE Dev |
|D4|QA (mobile/a11y/Lighthouse) | QA |
|D5|Go‑live | PM |

---
## 8 Risks & Mitigations
| Risk | Mitigation |
|------|-----------|
|Content becomes outdated | Markdown editable by anyone; set quarterly review reminder |
|Extra nav clutter | Keep nav to max 4 links; collapse into burger on mobile |

---
## 9 Acceptance Checklist
- [ ] `/help` renders with no console errors.  
- [ ] Content matches section list.  
- [ ] Link visible on both desktop & mobile.  
- [ ] Dark/light themes consistent.

---
**End of Document**

