/**
 * Translation Toggle Component
 * Simple and reliable translation using Google Translate
 */

import React, { useState } from 'react';
import styles from './TranslationToggle.module.css';

interface TranslationToggleProps {
  languages?: { code: string; name: string; nativeName: string }[];
}

const DEFAULT_LANGUAGES = [
  { code: 'ur', name: 'Urdu', nativeName: 'اردو' },
  { code: 'ar', name: 'Arabic', nativeName: 'العربية' },
  { code: 'hi', name: 'Hindi', nativeName: 'हिन्दी' },
  { code: 'es', name: 'Spanish', nativeName: 'Español' },
  { code: 'fr', name: 'French', nativeName: 'Français' },
  { code: 'zh', name: 'Chinese', nativeName: '中文' },
];

export default function TranslationToggle({
  languages = DEFAULT_LANGUAGES,
}: TranslationToggleProps): JSX.Element {
  const [isOpen, setIsOpen] = useState(false);

  const handleTranslate = (langCode: string) => {
    if (typeof window === 'undefined') return;

    // Get the page URL - use Vercel URL for production-like behavior
    const isLocalhost = window.location.hostname === 'localhost' ||
                       window.location.hostname === '127.0.0.1';

    let pageUrl = window.location.href;

    // If on localhost, use Vercel URL instead (Google Translate requires public URL)
    if (isLocalhost) {
      pageUrl = 'https://h1-book-q4.vercel.app' + window.location.pathname;
    }

    // Open Google Translate with the page
    const translateUrl = `https://translate.google.com/translate?sl=en&tl=${langCode}&u=${encodeURIComponent(pageUrl)}`;
    window.open(translateUrl, '_blank', 'noopener,noreferrer');

    setIsOpen(false);
  };

  const handleUrduTranslate = () => {
    handleTranslate('ur');
  };

  return (
    <div className={styles.container}>
      {/* Quick Urdu Translation Button */}
      <button
        className={styles.urduButton}
        onClick={handleUrduTranslate}
        aria-label="Translate to Urdu"
        title="Translate this page to Urdu"
      >
        <span className={styles.icon}>🌐</span>
        <span className={styles.label}>اردو</span>
      </button>

      {/* More Languages Dropdown */}
      <div className={styles.dropdown}>
        <button
          className={styles.dropdownButton}
          onClick={() => setIsOpen(!isOpen)}
          aria-label="More languages"
          aria-expanded={isOpen}
          title="Choose another language"
        >
          <span className={styles.dropdownIcon}>▼</span>
        </button>

        {isOpen && (
          <div className={styles.dropdownMenu}>
            <div className={styles.dropdownHeader}>
              <strong>Translate to:</strong>
            </div>
            {languages.map((lang) => (
              <button
                key={lang.code}
                className={styles.languageOption}
                onClick={() => handleTranslate(lang.code)}
                title={`Translate to ${lang.name}`}
              >
                <span className={styles.langName}>{lang.name}</span>
                <span className={styles.langNative}>{lang.nativeName}</span>
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Close dropdown when clicking outside */}
      {isOpen && (
        <div
          className={styles.backdrop}
          onClick={() => setIsOpen(false)}
          aria-hidden="true"
        />
      )}
    </div>
  );
}
