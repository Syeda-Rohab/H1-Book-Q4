# Testing Guides

This document provides comprehensive testing guides for mobile performance, accessibility, and quality assurance.

## Mobile Performance Testing

### Prerequisites
- Chrome DevTools
- Lighthouse CLI
- Real mobile devices (optional but recommended)

### Testing Steps

#### 1. Chrome DevTools Mobile Emulation

```bash
# Start the development server
cd website
npm start
```

Open Chrome DevTools (F12) and:
1. Click the device toolbar icon (or Ctrl+Shift+M)
2. Select a mobile device (e.g., iPhone 12, Samsung Galaxy S21)
3. Test the following:
   - Page scrolling smoothness (target: 60 FPS)
   - Touch target sizes (minimum 48x48px)
   - Text readability (minimum 16px font size)
   - Image loading performance
   - Quiz interaction on mobile

#### 2. Lighthouse Performance Audit

```bash
# Build the production site first
npm run build

# Serve the production build
npm run serve

# Run Lighthouse (install if needed: npm install -g lighthouse)
lighthouse http://localhost:3000 --view --preset=desktop
lighthouse http://localhost:3000 --view --preset=mobile --throttling.rttMs=150 --throttling.throughputKbps=1638
```

**Target Scores:**
- Performance: > 90
- Accessibility: > 90
- Best Practices: > 90
- SEO: > 90

#### 3. Network Throttling Tests

In Chrome DevTools:
1. Go to Network tab
2. Select "Slow 3G" or "Fast 3G" throttling
3. Reload the page
4. Verify:
   - Initial load < 5 seconds
   - Time to Interactive (TTI) < 7 seconds
   - No layout shifts

#### 4. Real Device Testing (Recommended)

If you have access to real mobile devices:

**Android:**
```bash
# Enable USB debugging on your device
# Connect via USB
adb reverse tcp:3000 tcp:3000
# Open http://localhost:3000 on your mobile browser
```

**iOS:**
- Use Safari on iOS device
- Connect to same WiFi network as your computer
- Access http://[your-computer-ip]:3000

**Test Checklist:**
- [ ] Page loads in < 5 seconds on 3G
- [ ] Smooth scrolling (no jank)
- [ ] All buttons/links easily tappable
- [ ] Text is readable without zooming
- [ ] Images load progressively
- [ ] Quiz component works on touch
- [ ] No horizontal scrolling
- [ ] Chapter navigation works smoothly

---

## Accessibility Audit (WCAG 2.1 AA)

### Automated Testing

#### 1. Lighthouse Accessibility Audit

```bash
lighthouse http://localhost:3000 --only-categories=accessibility --view
```

**Check for:**
- ARIA labels on interactive elements
- Color contrast ratios (minimum 4.5:1)
- Alt text on images
- Semantic HTML structure
- Form labels

#### 2. axe DevTools

Install the [axe DevTools Extension](https://www.deque.com/axe/devtools/) for Chrome/Firefox.

1. Open the page
2. Open DevTools
3. Go to the "axe DevTools" tab
4. Click "Scan ALL of my page"
5. Review and fix all Critical and Serious issues

#### 3. WAVE Browser Extension

Install [WAVE Extension](https://wave.webaim.org/extension/).

1. Open any page
2. Click the WAVE icon
3. Review:
   - Errors (must be 0)
   - Contrast errors (must be 0)
   - Alerts (should be minimal)
   - Structural elements (proper heading hierarchy)

### Manual Testing

#### Keyboard Navigation

Test navigation using only the keyboard:

```
Tab       - Move to next interactive element
Shift+Tab - Move to previous interactive element
Enter     - Activate buttons/links
Space     - Toggle checkboxes/radio buttons
Esc       - Close modals/dialogs
```

**Checklist:**
- [ ] All interactive elements are reachable via Tab
- [ ] Focus indicator is clearly visible
- [ ] Logical tab order (top to bottom, left to right)
- [ ] No keyboard traps
- [ ] Skip to content link available

#### Screen Reader Testing

**Windows (NVDA - Free):**
1. Download [NVDA](https://www.nvaccess.org/download/)
2. Install and launch
3. Navigate the site with NVDA active
4. Verify all content is announced correctly

**macOS (VoiceOver - Built-in):**
1. Press Cmd+F5 to enable VoiceOver
2. Use VO+arrow keys to navigate
3. Verify announcements

**Test Cases:**
- [ ] Page title is announced
- [ ] Headings are announced with levels
- [ ] Links announce their purpose
- [ ] Images announce alt text
- [ ] Forms announce labels and instructions
- [ ] Quiz questions are readable
- [ ] Navigation landmarks are announced

#### Color Contrast

Use [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/):

**Requirements (WCAG AA):**
- Normal text (< 18pt): 4.5:1 minimum
- Large text (≥ 18pt or 14pt bold): 3:1 minimum
- UI components: 3:1 minimum

**Test:**
1. Check text against background colors
2. Check link colors
3. Check button colors
4. Check focus indicators

#### Text Resize

Test text scaling:

1. Browser zoom to 200%
2. Verify:
   - [ ] No horizontal scrolling
   - [ ] No text overlap
   - [ ] All content remains visible
   - [ ] Layout doesn't break

#### Mobile Accessibility

- [ ] Touch targets ≥ 48x48px
- [ ] Orientation (portrait and landscape) both work
- [ ] No pinch-zoom disabled
- [ ] Text remains readable at native zoom

---

## Accessibility Checklist (WCAG 2.1 AA)

### Level A (Must Have)

- [ ] **1.1.1 Non-text Content**: All images have alt text
- [ ] **1.3.1 Info and Relationships**: Semantic HTML (headings, lists, etc.)
- [ ] **1.4.1 Use of Color**: Information not conveyed by color alone
- [ ] **2.1.1 Keyboard**: All functionality via keyboard
- [ ] **2.4.1 Bypass Blocks**: Skip navigation link
- [ ] **2.4.2 Page Titled**: Each page has a descriptive title
- [ ] **3.1.1 Language of Page**: HTML lang attribute set
- [ ] **4.1.1 Parsing**: Valid HTML
- [ ] **4.1.2 Name, Role, Value**: Proper ARIA attributes

### Level AA (Must Have)

- [ ] **1.4.3 Contrast (Minimum)**: 4.5:1 for normal text, 3:1 for large text
- [ ] **1.4.5 Images of Text**: Avoid images of text (use actual text)
- [ ] **2.4.6 Headings and Labels**: Descriptive headings
- [ ] **2.4.7 Focus Visible**: Keyboard focus indicator visible
- [ ] **3.2.3 Consistent Navigation**: Navigation order consistent across pages
- [ ] **3.3.3 Error Suggestion**: Form errors provide suggestions
- [ ] **3.3.4 Error Prevention**: Reversible/confirmable actions

---

## Performance Budget

Establish performance budgets to prevent regression:

### Page Weight Budget

| Resource | Budget | Current | Status |
|----------|--------|---------|--------|
| HTML | 50 KB | TBD | - |
| CSS | 100 KB | TBD | - |
| JavaScript | 200 KB | TBD | - |
| Images | 500 KB | TBD | - |
| Total | 850 KB | TBD | - |

### Timing Budget

| Metric | Budget | Current | Status |
|--------|--------|---------|--------|
| First Contentful Paint (FCP) | < 1.8s | TBD | - |
| Largest Contentful Paint (LCP) | < 2.5s | TBD | - |
| Time to Interactive (TTI) | < 3.5s | TBD | - |
| Total Blocking Time (TBT) | < 200ms | TBD | - |
| Cumulative Layout Shift (CLS) | < 0.1 | TBD | - |

### Measuring Current Performance

```bash
# Generate performance report
cd website
npm run build

# Use Lighthouse CI
npx lighthouse-ci autorun --config=./lighthouserc.json

# Or manual Lighthouse
npx lighthouse http://localhost:3000 --output=json --output-path=./lighthouse-report.json
```

---

## Continuous Testing

### Pre-commit Hooks

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/sh
# Run accessibility and performance checks before commit

echo "Running accessibility checks..."
cd website
npm run build
npx lighthouse http://localhost:3000 --only-categories=accessibility --quiet

if [ $? -ne 0 ]; then
  echo "Accessibility checks failed. Please fix before committing."
  exit 1
fi

echo "All checks passed!"
```

### CI/CD Integration

Add to `.github/workflows/test.yml`:

```yaml
name: Accessibility & Performance Tests

on: [push, pull_request]

jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: 18
      - name: Install dependencies
        run: cd website && npm ci
      - name: Build
        run: cd website && npm run build
      - name: Run Lighthouse CI
        run: |
          npm install -g @lhci/cli
          cd website && npm run serve &
          sleep 5
          lhci autorun
```

---

## Issue Tracking

When you find accessibility or performance issues:

1. **Document the issue:**
   - What: Description of the problem
   - Where: Page/component affected
   - WCAG criterion: Which guideline is violated (e.g., 1.4.3)
   - Severity: Critical/Major/Minor
   - Steps to reproduce

2. **Create a GitHub issue** with label `accessibility` or `performance`

3. **Prioritize:**
   - Critical (Level A violations): Fix immediately
   - Major (Level AA violations): Fix before next release
   - Minor (AAA or performance optimizations): Nice to have

---

## Resources

### Tools
- [Lighthouse](https://developers.google.com/web/tools/lighthouse)
- [axe DevTools](https://www.deque.com/axe/devtools/)
- [WAVE](https://wave.webaim.org/)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [NVDA Screen Reader](https://www.nvaccess.org/)

### Documentation
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Web Vitals](https://web.dev/vitals/)
- [Inclusive Components](https://inclusive-components.design/)
- [A11Y Project](https://www.a11yproject.com/)

### Testing Checklists
- [WebAIM WCAG Checklist](https://webaim.org/standards/wcag/checklist)
- [A11Y Project Checklist](https://www.a11yproject.com/checklist/)
