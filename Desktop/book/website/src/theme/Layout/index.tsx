import React from 'react';
import Layout from '@theme-original/Layout';
import TranslationToggle from '@site/src/components/TranslationToggle';

export default function LayoutWrapper(props) {
  return (
    <>
      <Layout {...props} />
      <TranslationToggle />
    </>
  );
}
