import React from 'react';
import Layout from '@theme/Layout';
import VideoGallery from '@site/src/components/VideoGallery';

export default function VideosPage(): JSX.Element {
  return (
    <Layout
      title="Video Demonstrations"
      description="Watch curated video demonstrations of Physical AI and Robotics concepts"
    >
      <main style={{ minHeight: '80vh', paddingTop: '2rem', paddingBottom: '2rem' }}>
        <VideoGallery />
      </main>
    </Layout>
  );
}
