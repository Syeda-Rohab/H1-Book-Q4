# Feature Guide: Quick Reference

This guide provides quick instructions for using all the new features in the AI-Native Textbook.

---

## 🤖 AI Chat Assistant

**Access:** Click "🤖 AI Chat" in the navigation bar

**How to Use:**
1. Type your question about Physical AI or Robotics in the input box
2. Press Enter or click the send button
3. The AI will search through all 8 chapters and provide relevant answers
4. Click suggested questions for quick starts

**Example Questions:**
- "What is Physical AI?"
- "How do sensors work in robots?"
- "What are the safety concerns in robotics?"
- "Tell me about future trends in AI"

**Tips:**
- Be specific in your questions
- Questions about chapter topics work best
- The AI cites sources from the textbook

---

## 🌐 Translation Feature

**Access:** Floating button at bottom-right corner (appears on all pages)

**How to Use:**
1. **For Urdu:** Click the green "اردو Translate" button
2. **For Other Languages:** Click the dropdown arrow next to the Urdu button
3. Select your language from the menu
4. The translated page opens in a new tab

**Supported Languages:**
- Urdu (اردو)
- Arabic (العربية)
- Hindi (हिन्दी)
- Spanish (Español)
- French (Français)
- Chinese (中文)

**Notes:**
- Uses Google Translate for reliability
- Translation quality varies by language
- Works on all pages including chapters and features

---

## 📊 Learning Dashboard

**Access:** Click "📊 Dashboard" in the navigation bar

### Features:

#### Progress Tracking
- Check boxes next to chapters to mark as complete
- View overall progress percentage
- See estimated time remaining

#### Statistics
- **Chapters Completed:** Track your progress
- **Time Remaining:** Based on your reading speed
- **Overall Progress:** Visual progress bar

#### Recommendations
- Get personalized chapter suggestions
- See what to read next
- Track which chapters you've started

#### Preferences
- **Reading Speed:** Slow / Medium / Fast
- **Difficulty Level:** Beginner / Intermediate / Advanced
- **Learning Reminders:** Enable/disable notifications

**How to Use:**
1. Switch between tabs: Progress / Recommendations / Preferences
2. Check boxes to mark chapters complete
3. Adjust preferences to customize your experience
4. Click "Reset All Data" to start fresh (if needed)

**Data Storage:**
- Saved in your browser's local storage
- Persists across sessions
- Can be synced to database (see DATABASE_SETUP.md)

---

## 🎥 Video Demonstrations

**Access:** Click "🎥 Videos" in the navigation bar

**How to Use:**
1. Browse the video gallery
2. Filter by chapter using the filter buttons
3. Click on any video card to watch
4. Use the close button (✕) to return to the gallery

**Video Categories:**
- Introduction to Physical AI
- Humanoid Robotics
- Sensors and Perception
- Manipulation
- AI Control
- Safety

**Features:**
- Duration displayed on each thumbnail
- Difficulty badges (Beginner/Intermediate/Advanced)
- Responsive video player
- YouTube integration

**Notes:**
- Videos open in a modal player
- Currently uses placeholder content (replace with actual educational videos)

---

## 🎮 Interactive Simulations

**Access:** Click "🎮 Simulations" in the navigation bar

### Available Simulations:

#### 1. Robot Arm Kinematics
**Difficulty:** Intermediate

**How to Use:**
1. Click the "Robot Arm Kinematics" card
2. Adjust "Joint 1 Angle" slider to rotate the first link
3. Adjust "Joint 2 Angle" slider to rotate the second link
4. Watch the arm move in real-time
5. See the end position coordinates update

**Learning Goal:** Understand forward kinematics and how joint angles affect end effector position

#### 2. Sensor Range Visualization
**Difficulty:** Beginner

**How to Use:**
1. Click the "Sensor Range Visualization" card
2. Adjust "Sensor Angle" to rotate the sensor
3. Adjust "Sensor Range" to increase/decrease detection distance
4. Watch obstacles turn red when detected
5. See how sensor cone affects what's detected

**Learning Goal:** Understand sensor field of view and detection ranges

#### 3. Path Planning (Coming Soon)
Will demonstrate A* algorithm for optimal pathfinding

#### 4. Balance Control (Coming Soon)
Will let you tune PID parameters for an inverted pendulum

**Tips:**
- Experiment with different parameter values
- Observe how changes affect the visualization
- Use the "Back to Simulations" button to try different simulations

---

## 💾 Database Integration (Optional)

**Setup Required:** See `DATABASE_SETUP.md` for full instructions

**Benefits:**
- Sync progress across devices
- Multi-user support
- Cloud backup of your data
- Advanced analytics

**Quick Setup:**
1. Create a free Supabase account
2. Run the SQL setup script
3. Add environment variables
4. Install dependencies with `npm install`

**Without Database:**
- App works normally with localStorage
- Single-device only
- No cross-device sync

---

## 📖 New Chapters

### Chapter 7: Safety and Ethics
**Topics Covered:**
- Safety requirements for physical AI
- Ethical considerations
- Privacy and surveillance
- Human-robot interaction guidelines
- Regulatory frameworks

**Access:** Sidebar → Chapter 7 → Safety and Ethics

### Chapter 8: Future Trends
**Topics Covered:**
- Vision-Language-Action models
- Foundation models for robotics
- Soft robotics and neuromorphic computing
- Human-robot collaboration
- Timeline predictions (2025-2040+)

**Access:** Sidebar → Chapter 8 → Future Trends

---

## 🎯 Quick Start Workflow

**For New Users:**
1. Start with Chapter 1 (Introduction)
2. Mark chapters complete as you finish them in the Dashboard
3. Take quizzes at the end of each chapter
4. Use the AI Chat to ask questions
5. Watch related videos for visual learning
6. Try simulations to understand concepts hands-on

**For Returning Users:**
1. Check your Dashboard for recommendations
2. Continue where you left off
3. Review quiz scores to identify weak areas
4. Use translation if needed for better understanding

---

## 📱 Mobile Usage

All features are mobile-responsive:
- **Navigation:** Collapsible hamburger menu
- **Chatbot:** Full-screen on mobile
- **Dashboard:** Stacked layout
- **Videos:** Responsive grid
- **Simulations:** Touch-friendly controls
- **Translation:** Adapted floating button

---

## 🔧 Troubleshooting

### AI Chat not responding
- Check your internet connection
- Try refreshing the page
- Clear browser cache if needed

### Dashboard not saving progress
- Ensure JavaScript is enabled
- Check browser storage permissions
- Try a different browser if issues persist

### Videos not loading
- Check YouTube is accessible
- Disable ad blockers temporarily
- Try a different browser

### Simulations not displaying
- Ensure canvas is supported in your browser
- Try a modern browser (Chrome, Firefox, Safari, Edge)
- Disable hardware acceleration if glitchy

### Translation button not visible
- Scroll to bottom-right corner
- Check if JavaScript is enabled
- Try zooming out if on mobile

---

## 💡 Tips & Best Practices

1. **Use the Dashboard:** Track your progress consistently
2. **Ask Questions:** The AI Chat is there to help
3. **Watch Videos:** Visual learning reinforces concepts
4. **Try Simulations:** Hands-on practice aids understanding
5. **Take Quizzes:** Test your knowledge after each chapter
6. **Translate if Needed:** Don't struggle with language barriers
7. **Set Preferences:** Customize reading speed and difficulty
8. **Explore All Features:** Each feature enhances learning differently

---

## 📞 Need Help?

- **Documentation:** Check README.md and DATABASE_SETUP.md
- **Issues:** Report bugs on GitHub
- **Questions:** Use the AI Chat feature
- **Setup Help:** Follow IMPLEMENTATION_SUMMARY.md

---

**Enjoy your learning journey! 🚀**
