import httpClient from "../lib/httpClient";

const auth = {
  signIn: (credentials) => httpClient.post("/api/auth/login", credentials),
  signUp: (userData) => httpClient.post("/api/auth/signup", userData),
  signOut: () => httpClient.post("/api/auth/logout"),
};

export default auth;
