import React from 'react';
import styles from './styles.module.css';
import { logout } from '../../contexts/firebase';
import { useThemeConfig } from '@docusaurus/theme-common';

const CustomLogoutButton = props => {
  const { releaseTag } = useThemeConfig();
  return (
    <div className={styles.logout_div}>
      <p>{releaseTag}</p>
      <button className={styles.logout_button} onClick={() => {
        logout()
      }}>Logout</button>
    </div>
  );
};

export default CustomLogoutButton;