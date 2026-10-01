import { createContext, useContext, useState } from "react";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [user, setUser] = useState(null);

  const signIn = async (formData) => {
    setLoading(true);
    setError(null);

    try {
      // Replace this with your FastAPI login API
      console.log("Login data:", formData);

      // Example:
      // const response = await axios.post(
      //   "http://localhost:8000/api/auth/login",
      //   formData
      // );

      // setUser(response.data.user);
      // localStorage.setItem("access_token", response.data.access_token);

      return true;
    } catch (err) {
      console.error("Login error:", err);
      setError(err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const signOut = () => {
    setUser(null);
    localStorage.removeItem("access_token");
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        error,
        signIn,
        signOut,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useGlobalAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error(
      "useGlobalAuth must be used within an AuthProvider"
    );
  }

  return context;
}