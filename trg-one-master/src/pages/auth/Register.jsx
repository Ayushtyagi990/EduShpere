import { useReducer } from "react";
import { Link, useNavigate } from "react-router";
import useAuth from "../../hooks/useAuth";

const initialState = {
  firstName: "",
  lastName: "",
  email: "",
  password: "",
  role: 2,
};

function formReducer(state, action) {
  switch (action.type) {
    case "SET_FIELD":
      return {
        ...state,
        [action.field]: action.value,
      };

    case "RESET":
      return initialState;

    default:
      return state;
  }
}

export default function Register() {
  const [formData, dispatch] = useReducer(formReducer, initialState);

  const { user, sigunUp, loading, error } = useAuth();

  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;

    dispatch({
      type: "SET_FIELD",
      field: name,
      value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await sigunUp(formData);

      // Optional: reset after successful registration
      dispatch({ type: "RESET" });
    } catch (err) {
      console.error("Registration failed:", err);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
      <div className="max-w-md w-full space-y-8 bg-white p-10 rounded-xl shadow-lg border border-gray-100">
        <div className="text-center">
          <h2 className="text-3xl font-extrabold text-gray-900">
            Welcome to the Registration Page
          </h2>

          <p className="mt-2 text-sm text-gray-600">
            Please enter your details to create an account
          </p>

          <Link
            to="/"
            className="block py-2 px-3 text-sm rounded-md text-blue-700 hover:text-blue-900"
          >
            Go back to login page
          </Link>
        </div>

        {/* Error */}
        {error && (
          <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-sm text-red-600">
              {error?.response?.data?.message ||
                error?.message ||
                "Registration failed"}
            </p>
          </div>
        )}

        {/* Success */}
        {user && (
          <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
            <p className="text-sm text-green-700">
              Registration successful!
            </p>

            <p className="text-sm text-green-700 mt-1">
              You can now login with your registered email.
            </p>
          </div>
        )}

        <form
          className="mt-8 space-y-6"
          onSubmit={handleSubmit}
        >
          <div className="space-y-4">
            {/* First Name */}
            <div>
              <label className="block text-sm font-medium text-gray-700">
                First Name
              </label>

              <input
                type="text"
                name="firstName"
                required
                value={formData.firstName}
                onChange={handleChange}
                placeholder="First Name"
                className="appearance-none rounded-lg relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              />
            </div>

            {/* Last Name */}
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Last Name
              </label>

              <input
                type="text"
                name="lastName"
                required
                value={formData.lastName}
                onChange={handleChange}
                placeholder="Last Name"
                className="appearance-none rounded-lg relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              />
            </div>

            {/* Email */}
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Email Address
              </label>

              <input
                type="email"
                name="email"
                required
                value={formData.email}
                onChange={handleChange}
                placeholder="you@example.com"
                className="appearance-none rounded-lg relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              />
            </div>

            {/* Password */}
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Password
              </label>

              <input
                type="password"
                name="password"
                required
                value={formData.password}
                onChange={handleChange}
                placeholder="••••••••"
                className="appearance-none rounded-lg relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="cursor-pointer group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-lg text-white bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
          >
            {loading ? "Creating Account..." : "Create Account"}
          </button>
        </form>
      </div>
    </div>
  );
}