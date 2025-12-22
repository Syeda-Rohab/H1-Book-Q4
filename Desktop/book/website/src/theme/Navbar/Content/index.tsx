import React from 'react';
import Content from '@theme-original/Navbar/Content';
import NavigationIcons from '@site/src/components/NavigationIcons';
import styles from './styles.module.css';

export default function ContentWrapper(props) {
  return (
    <div className={styles.navbarWrapper}>
      <Content {...props} />
      <NavigationIcons />
    </div>
  );
}
