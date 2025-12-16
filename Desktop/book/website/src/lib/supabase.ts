/**
 * Supabase Database Configuration
 *
 * Free-tier database integration for multi-user support
 * Features:
 * - User authentication
 * - Progress tracking
 * - Quiz scores
 * - Personalization data sync
 */

import { createClient, SupabaseClient } from '@supabase/supabase-js';

// Database types
export interface UserProgress {
  id: string;
  user_id: string;
  chapter_slug: string;
  completed: boolean;
  quiz_score?: number;
  time_spent: number;
  last_visited: string;
  created_at: string;
  updated_at: string;
}

export interface UserProfile {
  id: string;
  email: string;
  full_name?: string;
  avatar_url?: string;
  reading_speed: 'slow' | 'medium' | 'fast';
  difficulty_level: 'beginner' | 'intermediate' | 'advanced';
  notifications_enabled: boolean;
  created_at: string;
  updated_at: string;
}

export interface QuizAttempt {
  id: string;
  user_id: string;
  chapter_slug: string;
  score: number;
  total_questions: number;
  time_taken: number;
  answers: Record<string, any>;
  created_at: string;
}

// Supabase configuration
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || '';
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || '';

let supabase: SupabaseClient | null = null;

/**
 * Initialize Supabase client
 */
export function initSupabase(): SupabaseClient {
  if (!supabase) {
    if (!supabaseUrl || !supabaseAnonKey) {
      console.warn('Supabase credentials not configured. Database features will be disabled.');
      // Return a mock client for development
      return createMockClient();
    }
    supabase = createClient(supabaseUrl, supabaseAnonKey);
  }
  return supabase;
}

/**
 * Mock client for development without database
 */
function createMockClient(): any {
  console.warn('Using mock Supabase client. Set up environment variables for full functionality.');
  return {
    from: () => ({
      select: () => Promise.resolve({ data: [], error: null }),
      insert: () => Promise.resolve({ data: null, error: null }),
      update: () => Promise.resolve({ data: null, error: null }),
      delete: () => Promise.resolve({ data: null, error: null }),
    }),
    auth: {
      signUp: () => Promise.resolve({ data: null, error: null }),
      signIn: () => Promise.resolve({ data: null, error: null }),
      signOut: () => Promise.resolve({ error: null }),
      getUser: () => Promise.resolve({ data: { user: null }, error: null }),
    },
  };
}

/**
 * Database API Functions
 */

// User Progress
export async function getUserProgress(userId: string): Promise<UserProgress[]> {
  const client = initSupabase();
  const { data, error } = await client
    .from('user_progress')
    .select('*')
    .eq('user_id', userId);

  if (error) {
    console.error('Error fetching user progress:', error);
    return [];
  }

  return data || [];
}

export async function updateProgress(
  userId: string,
  chapterSlug: string,
  updates: Partial<UserProgress>
): Promise<boolean> {
  const client = initSupabase();

  const { error } = await client
    .from('user_progress')
    .upsert({
      user_id: userId,
      chapter_slug: chapterSlug,
      ...updates,
      updated_at: new Date().toISOString(),
    });

  if (error) {
    console.error('Error updating progress:', error);
    return false;
  }

  return true;
}

// User Profile
export async function getUserProfile(userId: string): Promise<UserProfile | null> {
  const client = initSupabase();
  const { data, error } = await client
    .from('user_profiles')
    .select('*')
    .eq('id', userId)
    .single();

  if (error) {
    console.error('Error fetching user profile:', error);
    return null;
  }

  return data;
}

export async function updateUserProfile(
  userId: string,
  updates: Partial<UserProfile>
): Promise<boolean> {
  const client = initSupabase();

  const { error } = await client
    .from('user_profiles')
    .update({
      ...updates,
      updated_at: new Date().toISOString(),
    })
    .eq('id', userId);

  if (error) {
    console.error('Error updating user profile:', error);
    return false;
  }

  return true;
}

// Quiz Attempts
export async function saveQuizAttempt(attempt: Omit<QuizAttempt, 'id' | 'created_at'>): Promise<boolean> {
  const client = initSupabase();

  const { error } = await client
    .from('quiz_attempts')
    .insert({
      ...attempt,
      created_at: new Date().toISOString(),
    });

  if (error) {
    console.error('Error saving quiz attempt:', error);
    return false;
  }

  return true;
}

export async function getQuizHistory(userId: string, chapterSlug?: string): Promise<QuizAttempt[]> {
  const client = initSupabase();

  let query = client
    .from('quiz_attempts')
    .select('*')
    .eq('user_id', userId)
    .order('created_at', { ascending: false });

  if (chapterSlug) {
    query = query.eq('chapter_slug', chapterSlug);
  }

  const { data, error } = await query;

  if (error) {
    console.error('Error fetching quiz history:', error);
    return [];
  }

  return data || [];
}

// Authentication helpers
export async function signUp(email: string, password: string, fullName?: string) {
  const client = initSupabase();
  const { data, error } = await client.auth.signUp({
    email,
    password,
    options: {
      data: {
        full_name: fullName,
      },
    },
  });

  return { data, error };
}

export async function signIn(email: string, password: string) {
  const client = initSupabase();
  const { data, error } = await client.auth.signInWithPassword({
    email,
    password,
  });

  return { data, error };
}

export async function signOut() {
  const client = initSupabase();
  const { error } = await client.auth.signOut();
  return { error };
}

export async function getCurrentUser() {
  const client = initSupabase();
  const { data: { user } } = await client.auth.getUser();
  return user;
}

// Export the client
export default initSupabase;
