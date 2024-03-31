import { useState } from 'react';
import {
  Route,
  createBrowserRouter,
  createRoutesFromElements,
  RouterProvider,
} from 'react-router-dom';
import HomePage from './pages/HomePage/HomePage';
import Header from './components/nav/Header';
import { LoginPage } from './pages/auth/LoginPage';
import { RegisterPage } from './pages/auth/RegisterPage';
import { ConfigProvider, theme } from 'antd';

const App = () => {
  const [isDarkMode, setIsDarkMode] = useState(false);

  const { defaultAlgorithm, darkAlgorithm } = theme;

  const toggleDarkMode = () => {
    setIsDarkMode((previousValue) => !previousValue);
  };

  const router = createBrowserRouter(
    createRoutesFromElements(
      <Route path="/" element={<Header toggleDarkMode={toggleDarkMode} isDarkMode={isDarkMode} />} >
        <Route index element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
      </Route>
    )
  );

  return (
    <ConfigProvider theme={{ algorithm: isDarkMode ? darkAlgorithm : defaultAlgorithm }}>
      <RouterProvider router={router} />
    </ConfigProvider>
  );
};

export default App;
