import React from 'react';
import Layout from '@theme/Layout';
import InteractiveSimulations from '@site/src/components/InteractiveSimulations';

export default function SimulationsPage(): JSX.Element {
  return (
    <Layout
      title="Interactive Simulations"
      description="Learn robotics concepts through interactive simulations"
    >
      <main style={{ minHeight: '80vh', paddingTop: '2rem', paddingBottom: '2rem' }}>
        <InteractiveSimulations />
      </main>
    </Layout>
  );
}
