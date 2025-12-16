# 🚀 Deployment Guide - AI-Native Textbook

This guide will help you deploy your textbook to GitHub Pages and get a public link.

## 📋 Prerequisites

- GitHub account (you have: Syeda-Rohab)
- Git installed and configured
- Code committed locally ✅ (Done!)

## 🌐 Current Status

**Local Link:** http://localhost:3000/

**Target Public Link:** https://syeda-rohab.github.io/ai-native-textbook/

---

## 🎯 Quick Deployment Steps

### Step 1: Create GitHub Repository

1. Go to: https://github.com/new
2. Repository name: **ai-native-textbook**
3. Description: **AI-Native Textbook on Physical AI & Humanoid Robotics**
4. Make it **Public**
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click **Create repository**

### Step 2: Update Git Remote

Run these commands in your terminal:

```bash
# Remove old remote
git remote remove origin

# Add new remote for ai-native-textbook
git remote add origin https://github.com/Syeda-Rohab/ai-native-textbook.git

# Verify it's correct
git remote -v
```

### Step 3: Create Main Branch and Push

```bash
# Create and switch to main branch
git checkout -b main

# Push your current branch first (optional - to keep work history)
git push -u origin 005-textbook-generation

# Switch back to main
git checkout main

# Merge your work into main
git merge 005-textbook-generation

# Push to main branch
git push -u origin main
```

### Step 4: Enable GitHub Pages

1. Go to your repository: https://github.com/Syeda-Rohab/ai-native-textbook
2. Click **Settings** (top menu)
3. Click **Pages** (left sidebar)
4. Under **Source**, select:
   - Source: **GitHub Actions**
5. The deployment workflow will run automatically
6. Wait 2-3 minutes for the first deployment

### Step 5: Get Your Public Link

Once deployment completes, your textbook will be live at:

**🔗 https://syeda-rohab.github.io/ai-native-textbook/**

---

## 🔄 Automatic Deployment

Every time you push to the `main` branch, GitHub Actions will automatically:

1. Build the Docusaurus site
2. Deploy to GitHub Pages
3. Update your live site

You can monitor deployments at:
https://github.com/Syeda-Rohab/ai-native-textbook/actions

---

## 🛠️ Alternative: Manual Deployment Commands

If you prefer, you can also run these commands to push everything at once:

```bash
# Set new remote
git remote set-url origin https://github.com/Syeda-Rohab/ai-native-textbook.git

# Create main from current branch
git checkout -b main

# Push to GitHub
git push -u origin main

# Also push your feature branch
git push origin 005-textbook-generation
```

---

## 📊 Checking Deployment Status

### Via GitHub Website:
1. Go to: https://github.com/Syeda-Rohab/ai-native-textbook/actions
2. Look for the **Deploy to GitHub Pages** workflow
3. Green check = Success ✅
4. Yellow circle = In progress ⏳
5. Red X = Failed ❌

### Via Command Line:
```bash
gh run list --repo Syeda-Rohab/ai-native-textbook
```

---

## 🔗 Share Your Textbook

Once deployed, share your textbook with these links:

**Main Site:**
- https://syeda-rohab.github.io/ai-native-textbook/

**Individual Chapters:**
- https://syeda-rohab.github.io/ai-native-textbook/chapter-01-physical-ai-intro
- https://syeda-rohab.github.io/ai-native-textbook/chapter-02-humanoid-robotics-fundamentals
- https://syeda-rohab.github.io/ai-native-textbook/chapter-03-sensors-perception
- https://syeda-rohab.github.io/ai-native-textbook/chapter-04-actuators-motion
- https://syeda-rohab.github.io/ai-native-textbook/chapter-05-ai-robot-control
- https://syeda-rohab.github.io/ai-native-textbook/chapter-06-manipulation-dexterity

**GitHub Repository:**
- https://github.com/Syeda-Rohab/ai-native-textbook

---

## 🎨 Custom Domain (Optional)

Want a custom domain like **textbook.yourdomain.com**?

1. Buy a domain from any registrar
2. Add a `CNAME` file to `website/static/` with your domain
3. Update `url` in `docusaurus.config.js`
4. Configure DNS settings with your registrar
5. Enable HTTPS in GitHub Pages settings

---

## 🐛 Troubleshooting

### Problem: 404 Errors on Deployed Site

**Solution:** Make sure baseUrl in `docusaurus.config.js` uses:
```javascript
baseUrl: process.env.NODE_ENV === 'production'
  ? '/ai-native-textbook/'
  : '/',
```

### Problem: GitHub Actions Failing

**Solution:**
1. Check `.github/workflows/deploy.yml` exists
2. Verify Node.js version is 18+
3. Check build logs for errors

### Problem: Site Not Updating

**Solution:**
1. Clear browser cache (Ctrl+Shift+Delete)
2. Wait 2-3 minutes for deployment
3. Check GitHub Actions completed successfully

---

## 💡 Tips

- **Use branches** for development work
- **Merge to main** only when ready to deploy
- **Check Actions tab** to monitor deployments
- **Test locally first** with `npm run build`

---

## 📞 Need Help?

- GitHub Pages Docs: https://docs.github.com/pages
- Docusaurus Deployment: https://docusaurus.io/docs/deployment
- GitHub Actions: https://github.com/features/actions

---

**Author:** Syeda Rohab Ali
**Last Updated:** 2025-12-15
**Status:** Ready to Deploy! 🚀
