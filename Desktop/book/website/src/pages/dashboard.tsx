import React from 'react';
import Layout from '@theme/Layout';
import PersonalizationDashboard from '@site/src/components/PersonalizationDashboard';

export default function DashboardPage(): JSX.Element {
  return (
    <Layout
      title="Learning Dashboard"
      description="Track your progress and personalize your learning experience"
    >
      <main style={{ minHeight: '80vh', paddingTop: '2rem', paddingBottom: '2rem' }}>
        <PersonalizationDashboard />
      </main>
    </Layout>
  );
}
