# ArtGen – API Documentation Page PRD

**Version:** 1.0   **Last Updated:** 26 Apr 2025

---
## 1 Purpose
Provide a clear, professional **API reference** so developers can integrate ArtGen within minutes, using a layout familiar from Swagger/ReDoc style guides.

---
## 2 Scope
**In‑scope**: Auto‑generated OpenAPI docs available at **/api** (ReDoc) and interactive Swagger UI at **/docs**; navigation link; light theming to match site.

**Out‑of‑scope**: SDKs, OAuth, rate‑limit dashboard, multi‑language examples.

---
## 3 Success Metrics
| KPI | Target |
|-----|--------|
|First API call success (no support) | ≥ 90 % of new devs |
|Time from docs open → first successful request | ≤ 5 min |
|Weekly dev support tickets | ≤ 1 |

---
## 4 Functional Requirements
| ID | Requirement | Details |
|----|-------------|---------|
|API‑01|Route `/api`|Serve ReDoc rendering of current `/openapi.json`. |
|API‑02|Route `/docs`|Expose FastAPI’s Swagger UI for interactive testing. |
|API‑03|Nav Link|Add **API** to top navigation. |
|API‑04|Code Samples|Include `x-codeSamples` (cURL, Python, JS) for the `/api/generate` endpoint. |
|API‑05|Theming|Apply custom CSS to match ArtGen gradient, dark mode default. |

---
## 5 Non‑Functional Requirements
- **Consistency** – Reflects latest backend automatically from FastAPI schema.  
- **Performance** – ReDoc static bundle loads ≤ 1 s on 3 G.  
- **Accessibility** – Keyboard navigation, contrast AA.  
- **Versioning** – CI auto‑rebuilds `/api` & `/docs` on each merge.

---
## 6 Architecture & Implementation
```python
# main.py additions
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

@app.get('/docs', include_in_schema=False)
async def swagger_ui():
    return get_swagger_ui_html(openapi_url='/openapi.json', title='ArtGen API Docs')

@app.get('/api', include_in_schema=False)
async def redoc_ui():
    return get_redoc_html(openapi_url='/openapi.json', title='ArtGen API Reference')
```
- **Code samples** – Annotate endpoints via `openapi_extra={'x-codeSamples': [...]}`.
- **Custom CSS** – Serve `/static/css/redoc-theme.css` to override fonts and accent color.

---
## 7 Timeline
| Day | Task | Owner |
|----:|------|-------|
|D0|Approve PRD | PM |
|D1|Add `/api` & `/docs` routes | BE Dev |
|D2|Inject code samples + custom CSS | BE Dev |
|D3|Nav link + responsive styling | FE Dev |
|D4|QA (endpoint accuracy, dark‑mode, mobile) | QA |
|D5|Go‑live | PM |

---
## 8 Risks & Mitigations
| Risk | Mitigation |
|------|-----------|
|OpenAPI drift | Add CI check + auto‑publish ReDoc |
|Large bundle size | Serve ReDoc JS via CDN; enable gzip |
|Nav overcrowding | Limit nav to Home · Help · API; collapse into burger menu on mobile |

---
## 9 Acceptance Checklist
- [ ] `/api` displays themed ReDoc with accurate schemas.  
- [ ] `/docs` interactive Swagger UI works and matches schema.  
- [ ] Example code samples copy correctly.  
- [ ] Navigation link visible and highlights active page.  
- [ ] Lighthouse accessibility score ≥ 90.

---
**End of Document**

