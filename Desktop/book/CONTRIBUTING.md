# Contributing to AI-Native Textbook

Thank you for considering contributing to the AI-Native Textbook project! This document provides guidelines for contributing to the project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Contribution Workflow](#contribution-workflow)
- [Constitution Compliance](#constitution-compliance)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)

## 🤝 Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/). By participating, you are expected to uphold this code.

## 💡 How Can I Contribute?

### Reporting Bugs

- Check if the bug has already been reported in [Issues](https://github.com/Syeda-Rohab/ai-native-textbook/issues)
- Use the bug report template
- Include steps to reproduce, expected vs actual behavior
- Add relevant screenshots or error messages

### Suggesting Enhancements

- Check existing issues for similar suggestions
- Use the feature request template
- Explain the problem and proposed solution
- Consider constitution compliance

### Improving Documentation

- Fix typos, clarify explanations
- Add examples or diagrams
- Update outdated information
- Expand on unclear sections

### Adding Content

- Improve existing chapters
- Add learning boosters (analogies, examples)
- Create quizzes or summaries
- Ensure constitution compliance (word count, structure)

### Code Contributions

- Fix bugs in generation scripts
- Improve UI/UX of Docusaurus site
- Optimize performance
- Add tests

## 🛠️ Development Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- Git
- Anthropic API key (for content generation)

### Setup Steps

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/ai-native-textbook.git
   cd ai-native-textbook
   ```

2. **Add upstream remote**
   ```bash
   git remote add upstream https://github.com/Syeda-Rohab/ai-native-textbook.git
   ```

3. **Install dependencies**
   ```bash
   # Python dependencies
   pip install anthropic markdown-it-py

   # Node dependencies
   cd website
   npm install
   cd ..
   ```

4. **Set up environment**
   ```bash
   # Create .env file
   echo "ANTHROPIC_API_KEY=your-api-key" > .env
   ```

5. **Run development server**
   ```bash
   cd website
   npm start
   ```

## 🔄 Contribution Workflow

### 1. Sync with Upstream

```bash
git checkout main
git fetch upstream
git merge upstream/main
```

### 2. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Adding tests

### 3. Make Your Changes

- Follow the constitution principles
- Keep changes focused and atomic
- Write clear, self-documenting code
- Add comments for complex logic

### 4. Test Your Changes

```bash
# Test website build
cd website
npm run build

# Validate chapters (if applicable)
python scripts/validate_chapters.py

# Check constitution compliance
python scripts/check_compliance.py
```

### 5. Commit Your Changes

Follow [commit guidelines](#commit-guidelines) below.

### 6. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 7. Open a Pull Request

- Use the PR template
- Link related issues
- Describe what changed and why
- Add screenshots if UI changed

## 📜 Constitution Compliance

All contributions must adhere to the [project constitution](.specify/memory/constitution.md):

### Core Principles

1. **AI-Native Design** - Maintain AI-first approach
2. **Speed & Simplicity** - Keep it fast and minimal
3. **Free-Tier Architecture** - No paid dependencies
4. **Grounded RAG Responses** - Accurate, cited content
5. **Modular Backend** - Clean separation of concerns
6. **Mobile-First** - Responsive design
7. **Content Quality** - 800-1200 words, 5-7 min chapters
8. **Observability** - Logging and health checks

### Content Standards

- **Word Count**: 800-1200 words per chapter
- **Reading Time**: 5-7 minutes per chapter
- **Structure**: Clear sections with headers
- **Clarity**: Accessible to learners with basic technical knowledge
- **Accuracy**: Factually correct and current
- **Citations**: Reference sources where applicable

### Code Standards

- **Python**: Follow PEP 8, use type hints
- **JavaScript/React**: Follow Airbnb style guide
- **CSS**: Use Docusaurus theming, mobile-first
- **Tests**: Add tests for new functionality
- **Documentation**: Comment complex code

## 📝 Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Build process, dependencies

### Examples

```bash
feat(chapters): add chapter 7 on safety and ethics

- Add 1200-word chapter on robot safety
- Include ethical considerations section
- Add learning objectives and summary

Closes #42
```

```bash
fix(build): resolve broken links in navigation

- Update chapter links in intro.md
- Fix docusaurus.config.js GitHub URLs
- Test build passes successfully

Fixes #51
```

## 🚀 Pull Request Process

### Before Submitting

- [ ] Code follows constitution principles
- [ ] Tests pass (`npm run build`)
- [ ] Documentation updated (if applicable)
- [ ] Commits follow guidelines
- [ ] Branch is up-to-date with main

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring

## Constitution Compliance
- [ ] Follows speed & simplicity principle
- [ ] Mobile-first design (if UI change)
- [ ] Word count compliant (if content)
- [ ] Free-tier compatible (if infrastructure)

## Testing
Describe testing done

## Screenshots
If applicable

## Related Issues
Closes #123
```

### Review Process

1. **Automated Checks**: CI runs tests
2. **Maintainer Review**: Code review by maintainers
3. **Feedback**: Address review comments
4. **Approval**: At least one maintainer approval
5. **Merge**: Squash and merge to main

### After Merge

- Delete your feature branch
- Update your fork
- Celebrate! 🎉

## ❓ Questions?

- Open an issue with the "question" label
- Tag maintainers for urgent matters
- Be patient and respectful

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to the AI-Native Textbook! Your efforts help make quality education accessible to everyone.

**Happy Contributing! 🚀**
