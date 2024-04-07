import { useState, ReactNode, useMemo } from "react";
import { ConfigProvider, ThemeConfig, theme as AntdTheme } from "antd";
import { ThemeContext } from "context/ThemeContext";

export const ThemeProvider = ({ children }: { children: ReactNode }) => {
  const { defaultAlgorithm, darkAlgorithm } = AntdTheme;
  const [theme, setTheme] = useState("light");

  const toggleTheme = () => {
    setTheme((prevState) => (prevState === "light" ? "dark" : "light"));
  };

  const themeConfig: ThemeConfig = {
    algorithm: theme === "light" ? defaultAlgorithm : darkAlgorithm,
  };

  const contextValue = useMemo(
    () => ({
      theme,
      toggleTheme,
    }),
    [theme],
  );

  return (
    <ThemeContext.Provider value={contextValue}>
      <ConfigProvider theme={themeConfig}>{children}</ConfigProvider>
    </ThemeContext.Provider>
  );
};
