# AI-Native Textbook Website

Docusaurus-based static site for the Physical AI & Humanoid Robotics textbook.

## Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build

# Serve production build locally
npm run serve
```

## Development

- **Framework**: Docusaurus 3.x
- **Language**: TypeScript + React 18
- **Node Version**: >=18.0.0

## Scripts

- `npm start` - Start dev server (hot reload)
- `npm run build` - Create production build
- `npm run serve` - Serve production build locally
- `npm run typecheck` - Run TypeScript type checking
- `npm run lint` - Run ESLint
- `npm run format` - Format code with Prettier

## Structure

```
website/
├── docs/           # Generated textbook chapters (markdown)
├── src/
│   ├── components/ # React components (ChapterQuiz, LearningBooster)
│   └── css/        # Custom styles
├── docusaurus.config.js  # Docusaurus configuration
├── sidebars.js     # Sidebar navigation
└── package.json    # Dependencies
```

## Custom Components

### ChapterQuiz

Interactive multiple-choice quiz component for chapter assessments.

### LearningBooster

Callout component for analogies, examples, and simplified explanations.

## Configuration

See `docusaurus.config.js` for site configuration and `sidebars.js` for navigation structure.
