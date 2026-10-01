import { NavLink } from "react-router";

export default function ErrorPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
      <div className="max-w-md w-full space-y-8 bg-white p-10 rounded-xl shadow-lg border border-gray-100">
        <div className="text-center">
          <h2 className="text-3xl font-extrabold text-red-900">
            Error: Page not found.
          </h2>
          <NavLink
            key="home-link"
            to="/"
            className="block py-2 px-3 text-sm rounded-md hover:text-slate-800 hover:bg-slate-200 transition-all"
          >
            Home
          </NavLink>
        </div>
      </div>
    </div>
  );
}
