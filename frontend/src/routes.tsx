import { createBrowserRouter, createRoutesFromElements, Route } from 'react-router-dom';
import Header from './components/nav/Header.tsx';
import HomePage from './pages/HomePage/HomePage.tsx';
import { LoginPage } from './pages/auth/LoginPage';
import { RegisterPage } from './pages/auth/RegisterPage';

const router = createBrowserRouter(
    createRoutesFromElements(
      <Route path="/" element={<Header />} >
        <Route index element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
      </Route>
    )
  );

  export default router
