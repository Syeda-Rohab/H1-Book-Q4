---
id: 007
title: Fix 404 Error BaseUrl
stage: misc
date: 2025-12-15
surface: agent
model: claude-sonnet-4-5-20250929
feature: 005-textbook-generation
branch: 005-textbook-generation
user: Dell
command: none
labels: ["bugfix", "404", "baseurl", "config", "docusaurus"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - website/docusaurus.config.js
tests:
  - HTTP 200 response on localhost:3001
---

## Prompt

this link page on 404 error please solve this error quickly

## Response snapshot

Fixed 404 error by configuring environment-specific baseUrl in docusaurus.config.js:

**Problem**:
- baseUrl was set to `/ai-native-textbook/` (for GitHub Pages deployment)
- Local development requires baseUrl of `/`
- All pages were showing 404 errors in local dev server

**Solution**:
Updated `docusaurus.config.js` to use conditional configuration based on NODE_ENV:

```javascript
url: process.env.NODE_ENV === 'production'
  ? 'https://syeda-rohab.github.io'
  : 'http://localhost:3000',
baseUrl: process.env.NODE_ENV === 'production'
  ? '/ai-native-textbook/'
  : '/',
```

**Result**:
- Local development: baseUrl = `/` (works on localhost)
- Production deployment: baseUrl = `/ai-native-textbook/` (works on GitHub Pages)
- No more 404 errors locally
- Deployment configuration preserved

Server restarted on port 3001 (port 3000 was occupied).

## Outcome

- ✅ Impact: 404 errors resolved; local development works correctly; production deployment unaffected
- 🧪 Tests: HTTP 200 response confirmed on localhost:3001
- 📁 Files: Modified docusaurus.config.js
- 🔁 Next prompts: Continue development or push to GitHub for deployment
- 🧠 Reflection: Environment-specific configuration is essential for projects deploying to subdirectories; conditional baseUrl solves the local vs production path mismatch

## Evaluation notes (flywheel)

- Failure modes observed: Fixed baseUrl caused 404 in local dev but needed for GitHub Pages deployment
- Graders run and results (PASS/FAIL): Homepage test PASS (HTTP 200)
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Consider using environment variables or build flags for other environment-specific configs
