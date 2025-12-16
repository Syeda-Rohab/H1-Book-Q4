# 🤖 AI-Native Textbook: Physical AI & Humanoid Robotics

[![Deploy](https://img.shields.io/badge/Deployed%20on-Vercel-00C7B7?logo=vercel)](https://h1-book-q4.vercel.app)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

An AI-powered textbook generation system that creates high-quality educational content on Physical AI and Humanoid Robotics. Built with Claude AI, Docusaurus, and following strict constitution-based quality standards.

**🌐 Live Site:** [https://h1-book-q4.vercel.app](https://h1-book-q4.vercel.app)

## 🌟 Features

### Content Generation
- ✅ **8 Complete Chapters** on Physical AI & Humanoid Robotics (including Safety/Ethics and Future Trends)
- ✅ **AI-Generated Content** with Claude Haiku (free-tier optimized)
- ✅ **Chapter Summaries** - 3-5 key takeaways per chapter
- ✅ **Self-Assessment Quizzes** - 5-7 multiple choice questions
- ✅ **Learning Boosters** - Analogies, examples, and explanations

### AI Features
- ✅ **RAG Chatbot** - Ask questions about textbook content with context-aware responses
- ✅ **Content Personalization** - Track progress, get recommendations, customize learning experience
- ✅ **One-Click Translation** - Instant translation to Urdu and 5+ other languages
- ✅ **Multi-User Support** - Database integration with Supabase for cross-device sync

### Interactive Learning
- ✅ **Video Demonstrations** - Curated video library of robotics concepts
- ✅ **Interactive Simulations** - Robot arm kinematics, sensor visualization, and more
- ✅ **Progress Dashboard** - Visual tracking of chapters completed and quiz scores
- ✅ **Personalized Recommendations** - AI-powered suggestions for next chapters

### Quality & Validation
- ✅ **Multi-Layer Validation** - Syntax, structure, content, build
- ✅ **Word Count Enforcement** (800-1200 words per chapter)
- ✅ **Constitution Compliance** - Automated validation script
- ✅ **Token Usage Tracking** - Cost monitoring and budgets

### Performance & Accessibility
- ✅ **Modern Homepage UI** - Gradient hero section, feature cards, chapter overview
- ✅ **Mobile-First Design** - Fully responsive Docusaurus framework
- ✅ **Fast Loading** - < 2s on 3G, optimized for low-end devices
- ✅ **WCAG 2.1 AA Ready** - Accessibility testing guides
- ✅ **Production-Optimized** - Built and tested, deployed on Vercel

### Developer Experience
- ✅ **Error Handling** - Comprehensive retry logic with exponential backoff
- ✅ **Structured Logging** - JSON logs for observability
- ✅ **Health Checks** - Backend monitoring endpoints
- ✅ **GitHub Pages Deployment** - Automated CI/CD workflows

## 📚 Table of Contents

### All Chapters

1. **Introduction to Physical AI** - Foundations of embodied intelligence
2. **Humanoid Robotics Fundamentals** - Anatomy, DOF, and balance
3. **Sensors and Perception** - Vision, tactile, IMUs, sensor fusion
4. **Actuators and Motion** - Motors, hydraulics, bipedal locomotion
5. **AI for Robot Control** - RL, imitation learning, sim-to-real
6. **Manipulation and Dexterity** - Grasp planning, dexterous hands
7. **Safety and Ethics** - Safety requirements, ethical considerations, human-robot interaction
8. **Future Trends** - VLA models, foundation models, advanced hardware, societal integration

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** for content generation
- **Node.js 18+** for Docusaurus
- **Anthropic API Key** for AI generation

### 1. Clone the Repository

```bash
git clone https://github.com/Syeda-Rohab/H1-Book-Q4.git
cd H1-Book-Q4
```

### 2. Set Up Environment

```bash
# Install Python dependencies
pip install anthropic markdown-it-py

# Install Node.js dependencies
cd website
npm install
cd ..
```

### 3. Configure API Key

```bash
# Set your Anthropic API key
export ANTHROPIC_API_KEY="your-api-key-here"

# Or create a .env file
echo "ANTHROPIC_API_KEY=your-api-key-here" > .env
```

### 4. Generate Content

```bash
# Generate all 6 chapters
python scripts/generate_chapters.py

# Or generate a single chapter
python scripts/generate_single.py 1
```

### 5. Run Development Server

```bash
cd website
npm start
```

Open [http://localhost:3000/](http://localhost:3000/) to view the textbook.

## 📦 Project Structure

```
ai-native-textbook/
├── .github/
│   └── workflows/          # GitHub Actions for CI/CD
│       ├── ci.yml         # Continuous integration
│       └── deploy.yml     # GitHub Pages deployment
├── .specify/
│   ├── memory/
│   │   └── constitution.md # Project principles & standards
│   └── templates/          # SDD templates
├── agents/
│   └── content_generator/      # AI generation logic
│       ├── llm_client.py       # Claude API client with retry logic
│       ├── chapter_generator.py # Chapter generation
│       ├── summary_generator.py # Summary generation
│       ├── quiz_generator.py    # Quiz generation
│       ├── booster_generator.py # Learning booster generation
│       ├── validator.py         # Multi-layer content validation
│       ├── token_tracker.py     # Token usage tracking & cost calc
│       └── markdown_writer.py   # Markdown file writer
├── backend/
│   └── src/
│       ├── models/              # Database models (ready for DB integration)
│       ├── services/            # Business logic
│       ├── routes/              # API endpoints (health checks, content)
│       └── utils/
│           └── logging.py       # Structured logging
├── scripts/
│   ├── generate_chapters.py     # Batch chapter generation
│   ├── generate_single.py       # Single chapter generation
│   ├── generate_summaries.py    # Chapter summaries
│   ├── generate_quizzes.py      # Self-assessment quizzes
│   ├── generate_boosters.py     # Learning aids
│   ├── validate_constitution.py # Constitution compliance check
│   └── validate_project.py      # Comprehensive project validation
├── website/                # Docusaurus frontend
│   ├── docs/              # Generated markdown chapters
│   ├── src/
│   │   ├── pages/         # Custom pages
│   │   │   ├── index.tsx  # Modern homepage with gradient UI
│   │   │   └── index.module.css # Homepage styling
│   │   └── css/           # Global styles
│   ├── static/            # Static assets
│   │   └── img/           # Logo, favicon, social card
│   ├── docusaurus.config.js # Docusaurus configuration
│   ├── sidebars.js        # Sidebar navigation
│   └── package.json       # Dependencies
├── vercel.json             # Vercel deployment config
├── history/
│   ├── prompts/           # Prompt History Records (PHRs)
│   └── adr/               # Architecture Decision Records
├── README.md
└── CLAUDE.md              # Claude Code instructions
```

## 🎯 Constitution Principles

This project follows 8 core principles:

1. **AI-Native Design** - AI-powered by default
2. **Speed & Simplicity** - Fast, minimal, accessible
3. **Free-Tier Architecture** - Works on free services
4. **Grounded RAG Responses** - Accurate, cited content
5. **Modular Backend Structure** - Clean separation of concerns
6. **Mobile-First Design** - Responsive and touch-friendly
7. **Content Quality Over Quantity** - 5-7 min chapters
8. **Observability** - Structured logging and health checks

See [`.specify/memory/constitution.md`](.specify/memory/constitution.md) for full details.

## 🛠️ Development

### Build for Production

```bash
cd website
npm run build
```

Output will be in `website/build/`.

### Serve Production Build Locally

```bash
cd website
npm run serve
```

### Lint and Format

```bash
cd website
npm run lint      # Check code quality
npm run format    # Auto-format code
```

## 🚢 Deployment

### Vercel (Production - Automated)

The site is deployed on Vercel with automatic deployments from the `main` branch.

**Live URL:** [https://h1-book-q4.vercel.app](https://h1-book-q4.vercel.app)

**Deployment Configuration:**
- Build command: `cd website && npm run build`
- Output directory: `website/build`
- Auto-deploys on every push to `main`

See [`vercel.json`](vercel.json) for full configuration.

### Alternative: GitHub Pages

```bash
cd website
GIT_USER=<Your GitHub username> npm run deploy
```

### Custom Domain

1. Configure custom domain in Vercel dashboard
2. Update `url` in `website/docusaurus.config.js`
3. Configure DNS settings with your domain provider

## 📊 Constitution Compliance

| Requirement | Status | Details |
|------------|--------|---------|
| Word Count | ✅ | 800-1200 words per chapter |
| Reading Time | ✅ | 5-7 minutes per chapter |
| Mobile-First | ✅ | Responsive design |
| Fast Loading | ✅ | < 2s on 3G |
| Free-Tier | ✅ | Anthropic API, GitHub Pages |
| AI-Native | ✅ | Claude-powered generation |

## 🧪 Testing

### Validation Scripts

```bash
# Constitution compliance validation
python scripts/validate_constitution.py

# Comprehensive project validation
python scripts/validate_project.py

# Build production site
cd website && npm run build
```

### Mobile Performance & Accessibility

See [TESTING_GUIDES.md](TESTING_GUIDES.md) for comprehensive testing instructions:
- Mobile performance testing (Lighthouse, real devices)
- Accessibility audit (WCAG 2.1 AA compliance)
- Keyboard navigation
- Screen reader testing
- Performance budgets

### Token Usage Tracking

```python
from agents.content_generator.token_tracker import get_global_tracker

# Track token usage
tracker = get_global_tracker()
tracker.print_summary()

# Check against budget
budget_status = tracker.check_budget(budget_usd=1.00)
print(f"Spent: ${budget_status['spent_usd']:.4f}")
print(f"Remaining: ${budget_status['remaining_usd']:.4f}")
```

## 📝 Content Generation Workflow

1. **Define Topic** - Chapter outline in constitution
2. **Generate Content** - AI creates chapter with Claude
3. **Validate** - Word count, structure, quality checks
4. **Write to Markdown** - Format for Docusaurus
5. **Review** - Human review and edits
6. **Deploy** - Auto-deploy via GitHub Actions

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Follow the constitution principles
4. Test your changes (`npm run build`)
5. Commit with clear messages
6. Push and create a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Claude AI** by Anthropic - Content generation
- **Docusaurus** by Meta - Static site framework
- **Spec-Driven Development** - Development methodology
- **Physical AI Community** - Domain expertise

## 📧 Contact

**Syeda Rohab Ali**
- GitHub: [@Syeda-Rohab](https://github.com/Syeda-Rohab)
- Project Repository: [H1-Book-Q4](https://github.com/Syeda-Rohab/H1-Book-Q4)
- Live Site: [h1-book-q4.vercel.app](https://h1-book-q4.vercel.app)

## 🗺️ Roadmap

### Phase 1: MVP ✅
- [x] 6 core chapters with AI-generated content
- [x] Word count validation (800-1200 words)
- [x] Docusaurus setup with responsive design
- [x] Vercel deployment with auto-deploy

### Phase 2: Interactive Features ✅
- [x] Chapter summaries (3-5 key takeaways)
- [x] Self-assessment quizzes (5-7 MCQs per chapter)
- [x] Learning boosters (analogies, examples, explanations)

### Phase 3: Modern UI & Polish ✅
- [x] Modern homepage with gradient hero section
- [x] Feature cards and chapter overview
- [x] Error handling with exponential backoff + jitter
- [x] Token usage tracking and cost monitoring
- [x] Constitution compliance validation
- [x] Mobile performance & accessibility testing guides

### Phase 4: AI Features ✅
- [x] RAG chatbot for Q&A
- [x] Content personalization
- [x] One-click Urdu translation
- [x] Database integration for multi-user support

### Phase 5: Extended Content ✅
- [x] Safety and Ethics chapter
- [x] Future Trends chapter
- [x] Video demonstrations
- [x] Interactive simulations

---

**Built with ❤️ using AI and Spec-Driven Development**

*Last Updated: 2025-12-16*
*Constitution Version: 1.0.0*
