/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  textbookSidebar: [
    {
      type: 'doc',
      id: 'intro',
      label: '📚 Welcome'
    },
    {
      type: 'category',
      label: '📖 Chapters',
      collapsed: false,
      items: [
        'chapter-01-physical-ai-intro',
        'chapter-02-humanoid-robotics-fundamentals',
        'chapter-03-sensors-perception',
        'chapter-04-actuators-motion',
        'chapter-05-ai-robot-control',
        'chapter-06-manipulation-dexterity',
      ]
    },
  ],
};
module.exports = sidebars;
