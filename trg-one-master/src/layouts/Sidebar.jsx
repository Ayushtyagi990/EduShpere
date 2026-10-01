import { useState } from "react";
import {
  HiUserGroup,
  HiBookOpen,
  HiCurrencyRupee,
  HiAcademicCap,
  HiChevronDown,
  HiChevronRight,
  HiChartBar,
  HiLibrary,
  HiOutlineLogout,
  HiUserCircle,
  HiCalendar,
  HiInboxIn,
} from "react-icons/hi";
import { IoNewspaperOutline } from "react-icons/io5";
import { FaRegHandshake } from "react-icons/fa6";
import { GrCertificate } from "react-icons/gr";
import { LuNotebookPen } from "react-icons/lu";
import { HiOutlinePresentationChartBar } from "react-icons/hi2";
import { AiTwotoneSafetyCertificate } from "react-icons/ai";
import { NavLink, useNavigate } from "react-router";
import { useGlobalAuth } from "../context/AuthContext";

const Sidebar = () => {
  const [openMenus, setOpenMenus] = useState({});

  const toggleMenu = (menu) => {
    setOpenMenus((prev) => ({ ...prev, [menu]: !prev[menu] }));
  };

  const { user, signOut } = useGlobalAuth();

  const menuItems = [
    { title: "Dashboard", icon: <HiChartBar />, path: "/dashboard" },
    {
      title: "Organization",
      icon: <HiUserGroup />,
      subMenu: [
        { title: "All Departments", path: "/dashboard/departments" },
        { title: "New Department", path: "/dashboard/departments/create" },
        { title: "All Employees", path: "/dashboard/employees" },
        { title: "New Employee", path: "/dashboard/employees/create" },
      ],
    },
    {
      title: "Academic",
      icon: <HiOutlinePresentationChartBar />,
      subMenu: [
        { title: "Fields of Study ", path: "/dashboard/employees" },
        { title: "Courses", path: "/dashboard/employees/create" },
      ],
    },
    {
      title: "Student",
      icon: <HiAcademicCap />,
      subMenu: [
        { title: "All Students", path: "/dashboard/employees" },
        { title: "New Student", path: "/dashboard/employees/create" },
      ],
    },
    {
      title: "Attendance",
      icon: <HiCalendar />,
      subMenu: [
        { title: "Employee", path: "/dashboard" },
        { title: "Absence Request", path: "/dashboard" },
        { title: "Student", path: "/dashboard" },
      ],
    },
    {
      title: "Project",
      icon: <HiInboxIn />,
      subMenu: [
        { title: "All Projects", path: "/dashboard" },
        { title: "New Projects", path: "/dashboard" },
        { title: "Resource Tracker", path: "/dashboard" },
      ],
    },
    {
      title: "Account",
      icon: <HiCurrencyRupee />,
      subMenu: [
        { title: "Run Payroll", path: "/dashboard" },
        { title: "Payslip Batches", path: "/dashboard" },
        { title: "Bonuses and Rembursement", path: "/dashboard" },
        { title: "Vendor Invoices", path: "/dashboard" },
      ],
    },
    {
      title: "Career",
      icon: <FaRegHandshake />,
      subMenu: [
        { title: "Job Applications", path: "/dashboard" },
        { title: "New Job", path: "/dashboard" },
      ],
    },
    {
      title: "News",
      icon: <IoNewspaperOutline />,
      subMenu: [
        { title: "Thanks Giving", path: "/dashboard" },
        { title: "Shining Star", path: "/dashboard" },
      ],
    },
    {
      title: "Rewards",
      icon: <GrCertificate />,
      subMenu: [
        { title: "Thanks Giving", path: "/dashboard" },
        { title: "Shining Star", path: "/dashboard" },
      ],
    },
    {
      title: "Examination",
      icon: <LuNotebookPen />,
      subMenu: [
        { title: "Thanks Giving", path: "/dashboard" },
        { title: "Shining Star", path: "/dashboard" },
      ],
    },
    {
      title: "Policies",
      icon: <AiTwotoneSafetyCertificate />,
      subMenu: [
        { title: "Thanks Giving", path: "/dashboard" },
        { title: "Shining Star", path: "/dashboard" },
      ],
    },
  ];

  return (
    <aside className="w-64 bg-slate-900 h-screen text-gray-300 flex flex-col transition-all duration-300 shadow-xl">
      {/* Brand Logo */}
      <div className="p-6 flex items-center gap-3 border-b border-slate-800">
        <div className="bg-indigo-600 p-2 rounded-lg">
          <HiLibrary className="text-white text-2xl" />
        </div>
        <span className="text-xl font-bold text-white tracking-tight">
          iHRMS
        </span>
      </div>

      {/* Nav Links */}
      <nav className="flex-1 overflow-y-auto py-4 px-3 space-y-1 custom-scrollbar">
        {menuItems.map((item, idx) => (
          <div key={idx}>
            {item.subMenu ? (
              // Dropdown Parent
              <div>
                <button
                  onClick={() => toggleMenu(item.title)}
                  className="w-full flex items-center justify-between p-3 rounded-lg hover:bg-slate-800 hover:text-white transition-colors group"
                >
                  <div className="flex items-center gap-3">
                    <span className="text-xl group-hover:text-indigo-400">
                      {item.icon}
                    </span>
                    <span className="font-medium">{item.title}</span>
                  </div>
                  {openMenus[item.title] ? (
                    <HiChevronDown />
                  ) : (
                    <HiChevronRight />
                  )}
                </button>

                {/* Submenu Items */}
                {openMenus[item.title] && (
                  <div className="mt-1 ml-9 space-y-1 border-l border-slate-700 pl-4">
                    {item.subMenu.map((sub, sIdx) => (
                      <NavLink
                        key={sIdx}
                        to={sub.path}
                        className="block py-2 px-3 text-sm rounded-md hover:text-indigo-400 hover:bg-slate-800 transition-all"
                      >
                        {sub.title}
                      </NavLink>
                    ))}
                  </div>
                )}
              </div>
            ) : (
              // Simple Single Link
              <NavLink
                to={item.path}
                className="flex items-center gap-3 p-3 rounded-lg hover:bg-slate-800 hover:text-white transition-colors group"
              >
                <span className="text-xl group-hover:text-indigo-400">
                  {item.icon}
                </span>
                <span className="font-medium">{item.title}</span>
              </NavLink>
            )}
          </div>
        ))}
      </nav>

      {/* User Footer Section */}
      <div className="p-4 border-t border-slate-800 bg-slate-950/50">
        <div className="flex items-center gap-3">
          <div className="flex items-center justify-center">
            <HiUserCircle className="text-white text-5xl" />
          </div>
          <div>
            <p className="text-sm font-semibold text-white">{user?.username}</p>
            <button
              type="button"
              onClick={signOut}
              className="cursor-pointer group relative flex justify-center py-1 px-2 mt-1 border border-transparent rounded-md text-white bg-slate-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
            >
              <HiOutlineLogout className="text-white text-2xl" />
            </button>
          </div>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
