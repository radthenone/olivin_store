import { Button } from 'antd';
import { SunOutlined, MoonOutlined} from '@ant-design/icons';

interface ButtonLightDarkProps {
  readonly toggleDarkMode: () => void;
  readonly isDarkMode: boolean;
}

function ButtonLightDark({ toggleDarkMode, isDarkMode }: ButtonLightDarkProps) {

  const handleClick = () => {
    toggleDarkMode();
  };
  return (
    <Button onClick={handleClick} icon={isDarkMode ? <SunOutlined /> : <MoonOutlined />} />
  );
}

export default ButtonLightDark;