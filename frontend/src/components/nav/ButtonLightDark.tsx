import { Button } from 'antd';
import { SunOutlined, MoonOutlined} from '@ant-design/icons';
import { useTheme } from 'hooks/useTheme';


function ButtonLightDark() {
  const { theme, toggleTheme } = useTheme();

  return (
      <Button onClick={toggleTheme} icon={theme === 'light' ? <SunOutlined /> : <MoonOutlined />} />
  );
}

export default ButtonLightDark;