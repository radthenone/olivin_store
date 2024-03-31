import { HomeTwoTone, EditTwoTone, CheckCircleTwoTone } from '@ant-design/icons';
import { Menu } from 'antd';
import { NavLink, Outlet } from 'react-router-dom';
import './Header.css';
import ButtonLightDark from '../nav/ButtonLightDark';
import { useState } from 'react';

interface HeaderProps {
  toggleDarkMode: () => void;
  isDarkMode: boolean;
}

const Header = ({ toggleDarkMode, isDarkMode } : HeaderProps) => {
  const [current, setCurrent] = useState<string>('home-key');

  const onClick = (key: string) => {
    setCurrent(key);
  };

  return (
    <>
      <Menu onClick={({ key }) => onClick(key)} selectedKeys={[current]} mode="horizontal">
        <Menu.Item key="home-key" icon={<HomeTwoTone />}>
          <NavLink to="/">Home</NavLink>
        </Menu.Item>
        <Menu.SubMenu
          key="auth-key"
          icon={<EditTwoTone />}
          title="Auth"
          style={{ marginLeft: 'auto' }}
        >
          <Menu.Item key="register-key" icon={<EditTwoTone />}>
            <NavLink to="/register">Register</NavLink>
          </Menu.Item>
          <Menu.Item key="login-key" icon={<CheckCircleTwoTone />}>
            <NavLink to="/login">Login</NavLink>
          </Menu.Item>
        </Menu.SubMenu>
        <Menu.Item><ButtonLightDark toggleDarkMode={toggleDarkMode} isDarkMode={isDarkMode} /></Menu.Item>
      </Menu>
      <Outlet />
    </>
  );
};

export default Header;