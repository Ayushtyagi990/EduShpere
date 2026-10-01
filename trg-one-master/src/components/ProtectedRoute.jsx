import { Navigate, Outlet } from "react-router";
import { useGlobalAuth } from "../context/AuthContext";

export default function ProtectedRoute() {
  const { user, loading } = useGlobalAuth();

  // Prevent redirect while restoring state
  if (loading) {
    return <div style={{ padding: "2rem" }}>Loading session...</div>;
  }

  // Redirect to login ONLY if loading is finished AND no user exists
  if (!user) {
    return <Navigate to="/" replace></Navigate>;
  }

  return <Outlet></Outlet>;
}
