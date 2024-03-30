import { HomeTwoTone, EditTwoTone, CheckCircleTwoTone } from '@ant-design/icons';
import { Menu } from 'antd';
import { useState } from 'react';
import { NavLink, Outlet } from 'react-router-dom';
import './Header.css';

const Header = () => {
  const [current, setCurrent] = useState<string>('home');

  const onClick = (key: string) => {
    setCurrent(key);
  };

  return (
    <>
      <Menu onClick={({ key }) => onClick(key)} selectedKeys={[current]} mode="horizontal">
        <Menu.Item key="h" icon={<HomeTwoTone />}>
          <NavLink to="/">Home</NavLink>
        </Menu.Item>
        <Menu.Item key="r" icon={<EditTwoTone />} style={{ marginLeft: 'auto' }}>
          <NavLink to="/register">Register</NavLink>
        </Menu.Item>
        <Menu.Item key="l" icon={<CheckCircleTwoTone />}>
          <NavLink to="/login">Login</NavLink>
        </Menu.Item>
      </Menu>
      <Outlet />
    </>
  );
};

export default Header;
