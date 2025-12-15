/**
 * ChapterQuiz React Component
 *
 * Interactive quiz component for textbook chapters with:
 * - Multiple choice questions (4 options each)
 * - Immediate feedback on answers
 * - Score tracking
 * - Answer randomization (T055)
 * - Mobile-responsive design
 *
 * Based on tasks.md: T050 - ChapterQuiz React component
 */

import React, { useState, useEffect } from 'react';
import styles from './ChapterQuiz.module.css';

interface QuizQuestion {
  question_text: string;
  options: string[];
  correct_index: number;
  difficulty?: 'easy' | 'medium' | 'hard';
  topic?: string;
}

interface ChapterQuizProps {
  questions: QuizQuestion[];
  chapterTitle?: string;
}

interface QuestionState {
  selectedAnswer: number | null;
  isCorrect: boolean | null;
  shuffledOptions: string[];
  shuffledCorrectIndex: number;
}

/**
 * Shuffle array using Fisher-Yates algorithm (T055: Answer randomization)
 */
function shuffleArray<T>(array: T[]): T[] {
  const shuffled = [...array];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
}

/**
 * Shuffle quiz options while tracking correct answer index (T055)
 */
function shuffleOptions(options: string[], correctIndex: number): {
  shuffledOptions: string[];
  shuffledCorrectIndex: number;
} {
  const indices = options.map((_, i) => i);
  const shuffledIndices = shuffleArray(indices);

  return {
    shuffledOptions: shuffledIndices.map(i => options[i]),
    shuffledCorrectIndex: shuffledIndices.indexOf(correctIndex),
  };
}

export default function ChapterQuiz({ questions, chapterTitle }: ChapterQuizProps): JSX.Element {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [score, setScore] = useState(0);
  const [showResults, setShowResults] = useState(false);
  const [questionStates, setQuestionStates] = useState<QuestionState[]>([]);

  // Initialize question states with shuffled options (T055)
  useEffect(() => {
    const initialStates = questions.map(q => {
      const { shuffledOptions, shuffledCorrectIndex } = shuffleOptions(
        q.options,
        q.correct_index
      );
      return {
        selectedAnswer: null,
        isCorrect: null,
        shuffledOptions,
        shuffledCorrectIndex,
      };
    });
    setQuestionStates(initialStates);
  }, [questions]);

  if (questionStates.length === 0) {
    return <div>Loading quiz...</div>;
  }

  const handleAnswerClick = (answerIndex: number) => {
    const state = questionStates[currentQuestion];

    // Prevent changing answer after submission
    if (state.selectedAnswer !== null) {
      return;
    }

    const isCorrect = answerIndex === state.shuffledCorrectIndex;

    // Update question state
    const newStates = [...questionStates];
    newStates[currentQuestion] = {
      ...state,
      selectedAnswer: answerIndex,
      isCorrect,
    };
    setQuestionStates(newStates);

    // Update score
    if (isCorrect) {
      setScore(score + 1);
    }
  };

  const handleNext = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    } else {
      setShowResults(true);
    }
  };

  const handleRestart = () => {
    setCurrentQuestion(0);
    setScore(0);
    setShowResults(false);

    // Re-shuffle options for restart (T055)
    const newStates = questions.map(q => {
      const { shuffledOptions, shuffledCorrectIndex } = shuffleOptions(
        q.options,
        q.correct_index
      );
      return {
        selectedAnswer: null,
        isCorrect: null,
        shuffledOptions,
        shuffledCorrectIndex,
      };
    });
    setQuestionStates(newStates);
  };

  if (showResults) {
    const percentage = Math.round((score / questions.length) * 100);
    const passed = percentage >= 70;

    return (
      <div className={styles.quizContainer}>
        <div className={styles.resultsContainer}>
          <h3 className={styles.resultsTitle}>Quiz Complete!</h3>

          <div className={`${styles.scoreDisplay} ${passed ? styles.passed : styles.failed}`}>
            <div className={styles.scorePercentage}>{percentage}%</div>
            <div className={styles.scoreText}>
              {score} out of {questions.length} correct
            </div>
          </div>

          <div className={styles.resultsFeedback}>
            {passed ? (
              <p className={styles.passMessage}>
                🎉 Great job! You've demonstrated a solid understanding of the material.
              </p>
            ) : (
              <p className={styles.failMessage}>
                📚 Keep studying! Review the chapter and try again.
              </p>
            )}
          </div>

          <button className={styles.restartButton} onClick={handleRestart}>
            Retake Quiz
          </button>
        </div>
      </div>
    );
  }

  const question = questions[currentQuestion];
  const state = questionStates[currentQuestion];
  const progress = ((currentQuestion + 1) / questions.length) * 100;

  return (
    <div className={styles.quizContainer}>
      {/* Progress Bar */}
      <div className={styles.progressBar}>
        <div className={styles.progressFill} style={{ width: `${progress}%` }} />
      </div>

      {/* Question Counter */}
      <div className={styles.questionCounter}>
        Question {currentQuestion + 1} of {questions.length}
        {question.difficulty && (
          <span className={`${styles.difficulty} ${styles[question.difficulty]}`}>
            {question.difficulty}
          </span>
        )}
      </div>

      {/* Question Text */}
      <h3 className={styles.questionText}>{question.question_text}</h3>

      {/* Answer Options */}
      <div className={styles.optionsContainer}>
        {state.shuffledOptions.map((option, index) => {
          const isSelected = state.selectedAnswer === index;
          const isCorrect = index === state.shuffledCorrectIndex;
          const showFeedback = state.selectedAnswer !== null;

          let optionClass = styles.option;
          if (showFeedback) {
            if (isSelected && isCorrect) {
              optionClass += ` ${styles.correct}`;
            } else if (isSelected && !isCorrect) {
              optionClass += ` ${styles.incorrect}`;
            } else if (isCorrect) {
              optionClass += ` ${styles.correctAnswer}`;
            } else {
              optionClass += ` ${styles.disabled}`;
            }
          } else if (isSelected) {
            optionClass += ` ${styles.selected}`;
          }

          return (
            <button
              key={index}
              className={optionClass}
              onClick={() => handleAnswerClick(index)}
              disabled={state.selectedAnswer !== null}
              aria-label={`Option ${index + 1}`}
            >
              <span className={styles.optionLetter}>
                {String.fromCharCode(65 + index)}
              </span>
              <span className={styles.optionText}>{option}</span>
              {showFeedback && isCorrect && (
                <span className={styles.checkmark}>✓</span>
              )}
              {showFeedback && isSelected && !isCorrect && (
                <span className={styles.crossmark}>✗</span>
              )}
            </button>
          );
        })}
      </div>

      {/* Feedback Message */}
      {state.selectedAnswer !== null && (
        <div className={`${styles.feedback} ${state.isCorrect ? styles.correctFeedback : styles.incorrectFeedback}`}>
          {state.isCorrect ? (
            <p>✓ Correct! Well done.</p>
          ) : (
            <p>✗ Incorrect. The correct answer was highlighted above.</p>
          )}
        </div>
      )}

      {/* Next Button */}
      {state.selectedAnswer !== null && (
        <button className={styles.nextButton} onClick={handleNext}>
          {currentQuestion < questions.length - 1 ? 'Next Question' : 'See Results'}
        </button>
      )}

      {/* Score Tracker */}
      <div className={styles.scoreTracker}>
        Current Score: {score}/{currentQuestion + (state.isCorrect ? 1 : 0)}
      </div>
    </div>
  );
}
