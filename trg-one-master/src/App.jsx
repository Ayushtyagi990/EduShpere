import "./App.css";
import {
  createBrowserRouter,
  Navigate,
  RouterProvider,
} from "react-router-dom";

import Login from "./pages/auth/Login";
import Register from "./pages/auth/Register";
import Dashboard from "./pages/Dashboard";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Navigate to="/login" replace />,
  },

  {
    path: "/login",
    element: <Login />,
  },

  {
    path: "/register",
    element: <Register />,
  },

  {
    path: "/dashboard",
    element: <Dashboard />,
  },

  {
    path: "*",
    element: <Navigate to="/login" replace />,
  },
]);

function App() {
  return <RouterProvider router={router} />;
}

export default App;
