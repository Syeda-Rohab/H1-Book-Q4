/**
 * Translation Toggle Component
 *
 * Provides one-click translation to Urdu and other languages
 * using browser-based translation or Google Translate
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
    const currentUrl = window.location.href;
    // Use Google Translate for reliable translation
    const translateUrl = `https://translate.google.com/translate?sl=auto&tl=${langCode}&u=${encodeURIComponent(currentUrl)}`;
    window.open(translateUrl, '_blank');
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
      >
        <span className={styles.icon}>🌐</span>
        <span className={styles.label}>اردو Translate</span>
      </button>

      {/* More Languages Dropdown */}
      <div className={styles.dropdown}>
        <button
          className={styles.dropdownButton}
          onClick={() => setIsOpen(!isOpen)}
          aria-label="More languages"
          aria-expanded={isOpen}
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
