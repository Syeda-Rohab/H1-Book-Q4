import React from 'react';
import TranslationToggle from '@site/src/components/TranslationToggle';

// Root component that wraps the entire application
export default function Root({ children }): JSX.Element {
  return (
    <>
      {children}
      <TranslationToggle />
    </>
  );
}
