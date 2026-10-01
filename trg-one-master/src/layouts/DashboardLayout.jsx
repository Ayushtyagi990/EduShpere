import React from "react";
import { Outlet } from "react-router";
import Header from "./Header";
import Footer from "./Footer";
import Sidebar from "./Sidebar";

export default function DashboardLayout({ children }) {
  return (
    <div className="flex h-screen bg-gray-100 overflow-hidden">
      {/* Sidebar - Fixed width on large screens */}
      <Sidebar />

      {/* Main Content Area */}
      <div className="flex flex-col flex-1 w-0 overflow-hidden">
        <Header />

        {/* Scrollable Content Section */}
        <main className="flex-1 relative overflow-y-auto focus:outline-none p-6">
          <div className="container mx-auto">
            <Outlet /> {/* Your page content renders here */}
          </div>
        </main>

        <Footer />
      </div>
    </div>
  );
}
