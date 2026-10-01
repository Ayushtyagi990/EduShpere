import { useEffect, useState } from "react";
import authService from "../services/auth";

const useAuth = () => {
  const [user, setUser] = useState(() => {
    const token = localStorage.getItem("token");
    const username = localStorage.getItem("username");
    return username && token ? { username, token } : null;
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const storedToken = localStorage.getItem("token");
    const storedUsername = localStorage.getItem("username");
    if (storedToken && storedUsername) {
      setUser({ username: storedUsername, token: storedToken });
    }
    setLoading(false);
  }, []);

  const signIn = (credentials) => {
    setLoading(true);
    setError(null);

    return authService
      .signIn(credentials)
      .then((res) => {
        const { token, username } = res.data;
        localStorage.setItem("token", token);
        localStorage.setItem("username", username);

        setUser({ username: username, token: token });
      })
      .catch((err) => {
        setError(err);
        throw err;
      })
      .finally(() => {
        setLoading(false);
      });
  };

  const sigunUp = (userData) => {
    setLoading(true);
    setError(null);

    return authService
      .signUp(userData)
      .then((res) => {
        setUser(res.data);
      })
      .catch((err) => {
        console.error("Error during sign-up:", err);
        setError(err);
      })
      .finally(() => {
        setLoading(false);
      });
  };

  const signOut = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    setUser(null);
    setError(null);
  };

  return { user, loading, error, signIn, sigunUp, signOut };
};

export default useAuth;
