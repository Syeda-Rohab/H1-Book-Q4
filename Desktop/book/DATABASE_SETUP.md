# Database Setup Guide

This guide explains how to set up the database for multi-user support in the AI-Native Textbook.

## Overview

The textbook uses **Supabase** (PostgreSQL) for:
- User authentication
- Progress tracking across chapters
- Quiz score history
- Personalization settings sync

**Why Supabase?**
- Free tier with generous limits
- PostgreSQL database
- Built-in authentication
- Real-time subscriptions
- Easy to set up

## Step 1: Create a Supabase Account

1. Go to [supabase.com](https://supabase.com)
2. Sign up for a free account
3. Create a new project

## Step 2: Set Up Database Tables

Run the following SQL in the Supabase SQL Editor:

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- User Profiles Table
CREATE TABLE user_profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email TEXT UNIQUE NOT NULL,
  full_name TEXT,
  avatar_url TEXT,
  reading_speed TEXT DEFAULT 'medium' CHECK (reading_speed IN ('slow', 'medium', 'fast')),
  difficulty_level TEXT DEFAULT 'beginner' CHECK (difficulty_level IN ('beginner', 'intermediate', 'advanced')),
  notifications_enabled BOOLEAN DEFAULT false,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User Progress Table
CREATE TABLE user_progress (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES user_profiles(id) ON DELETE CASCADE NOT NULL,
  chapter_slug TEXT NOT NULL,
  completed BOOLEAN DEFAULT false,
  quiz_score INTEGER,
  time_spent INTEGER DEFAULT 0,
  last_visited TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(user_id, chapter_slug)
);

-- Quiz Attempts Table
CREATE TABLE quiz_attempts (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES user_profiles(id) ON DELETE CASCADE NOT NULL,
  chapter_slug TEXT NOT NULL,
  score INTEGER NOT NULL,
  total_questions INTEGER NOT NULL,
  time_taken INTEGER NOT NULL,
  answers JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for better query performance
CREATE INDEX idx_user_progress_user_id ON user_progress(user_id);
CREATE INDEX idx_user_progress_chapter ON user_progress(chapter_slug);
CREATE INDEX idx_quiz_attempts_user_id ON quiz_attempts(user_id);
CREATE INDEX idx_quiz_attempts_chapter ON quiz_attempts(chapter_slug);

-- Enable Row Level Security
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE quiz_attempts ENABLE ROW LEVEL SECURITY;

-- RLS Policies for user_profiles
CREATE POLICY "Users can view own profile"
  ON user_profiles FOR SELECT
  USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
  ON user_profiles FOR UPDATE
  USING (auth.uid() = id);

CREATE POLICY "Users can insert own profile"
  ON user_profiles FOR INSERT
  WITH CHECK (auth.uid() = id);

-- RLS Policies for user_progress
CREATE POLICY "Users can view own progress"
  ON user_progress FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own progress"
  ON user_progress FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own progress"
  ON user_progress FOR UPDATE
  USING (auth.uid() = user_id);

-- RLS Policies for quiz_attempts
CREATE POLICY "Users can view own quiz attempts"
  ON quiz_attempts FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own quiz attempts"
  ON quiz_attempts FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Function to automatically create user profile on signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.user_profiles (id, email, full_name)
  VALUES (
    NEW.id,
    NEW.email,
    NEW.raw_user_meta_data->>'full_name'
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger to call the function on user creation
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();
```

## Step 3: Get Your Credentials

1. In your Supabase project dashboard, go to **Settings** → **API**
2. Copy your **Project URL** (e.g., `https://xxxxx.supabase.co`)
3. Copy your **anon/public** key

## Step 4: Configure Environment Variables

Create a `.env.local` file in the `website` directory:

```bash
NEXT_PUBLIC_SUPABASE_URL=your_project_url_here
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key_here
```

**Important:** Never commit the `.env.local` file to version control!

Add to `.gitignore`:
```
.env.local
.env*.local
```

## Step 5: Install Dependencies

Add Supabase client to your project:

```bash
cd website
npm install @supabase/supabase-js
```

## Step 6: Test the Connection

The application will automatically detect if Supabase is configured:
- If configured: Full database features enabled
- If not configured: Falls back to localStorage (single-user mode)

## Features Enabled with Database

### 1. User Authentication
- Sign up / Sign in
- Password reset
- Email verification

### 2. Progress Sync
- Track completion across devices
- Save quiz scores
- Sync personalization settings

### 3. Multi-User Support
- Multiple users with separate progress
- User-specific recommendations
- Leaderboards (future feature)

### 4. Analytics
- Track popular chapters
- Average quiz scores
- Time spent per chapter

## Testing

1. **Sign Up**: Create a test account
2. **Progress**: Mark a chapter as complete
3. **Quiz**: Take a quiz and check if score is saved
4. **Sync**: Log in from different browser/device

## Free Tier Limits (Supabase)

- **Database**: 500 MB
- **Bandwidth**: 5 GB
- **API requests**: Unlimited
- **Users**: Unlimited

Perfect for educational projects!

## Troubleshooting

### Database connection fails
- Check environment variables are set correctly
- Verify Supabase project is active
- Check RLS policies are enabled

### Authentication not working
- Confirm email verification is set up
- Check auth settings in Supabase dashboard
- Verify redirect URLs are configured

### Data not syncing
- Open browser console for errors
- Check network tab for failed requests
- Verify user is authenticated

## Production Deployment

For production (e.g., Vercel):

1. Add environment variables in deployment platform
2. Enable Supabase production mode
3. Configure custom domain (optional)
4. Set up monitoring and backups

## Optional: Advanced Features

### Real-time Updates
Enable real-time subscriptions for collaborative features:

```typescript
supabase
  .channel('user_progress')
  .on('postgres_changes', { event: 'UPDATE', schema: 'public', table: 'user_progress' },
    payload => {
      console.log('Progress updated:', payload);
    }
  )
  .subscribe();
```

### Analytics Dashboard
Query aggregate stats:

```sql
-- Most popular chapters
SELECT chapter_slug, COUNT(*) as completions
FROM user_progress
WHERE completed = true
GROUP BY chapter_slug
ORDER BY completions DESC;

-- Average quiz scores
SELECT chapter_slug, AVG(score) as avg_score
FROM quiz_attempts
GROUP BY chapter_slug;
```

## Support

For issues:
1. Check [Supabase Documentation](https://supabase.com/docs)
2. Visit [Supabase Discord](https://discord.supabase.com)
3. Open an issue on GitHub

---

**Note:** The application works without database setup (using localStorage), but database integration enables cross-device sync and multi-user support.
