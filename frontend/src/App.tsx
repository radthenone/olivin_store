import { RouterProvider } from "react-router-dom";
import router from "./routes.tsx";

const App = () => {
  return <RouterProvider router={router} />;
};

export default App;
