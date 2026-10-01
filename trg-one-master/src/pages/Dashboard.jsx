import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
} from "recharts";

import { MdOutlineCelebration } from "react-icons/md";

// --- Mock Data ---
const monthlyData = [
  { name: "May", presence: 92 },
  { name: "Jun", presence: 95 },
  { name: "Jul", presence: 96 },
  { name: "Aug", presence: 98 },
];

const techStack = [
  { name: "Engineering", value: 370 },
  { name: "Data Analytics", value: 200 },
  { name: "AI", value: 175 },
  { name: "DevOps", value: 120 },
  { name: "Management", value: 67 },
  { name: "QA", value: 135 },
];

const COLORS = [
  "#4F46E5",
  "#10B981",
  "#F59E0B",
  "#EF4444",
  "#7a0303",
  "#0eaed6",
];

const Dashboard = () => {
  return (
    <div className="space-y-8">
      {/* Header Section */}
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-slate-800">
          Dashboard Overview
        </h1>
        <button className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700 transition">
          Generate Report
        </button>
      </div>

      {/* --- Charts Grid --- */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Monthly Registration Chart */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
          <h3 className="text-lg font-semibold mb-4 text-slate-700">
            Attendance Summary
          </h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={monthlyData}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="name" stroke="#94a3b8" fontSize={12} />
                <YAxis stroke="#94a3b8" fontSize={12} />
                <Tooltip />
                <Line
                  type="monotone"
                  dataKey="presence"
                  stroke="#4F46E5"
                  strokeWidth={3}
                  dot={{ r: 6 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Course-wise Distribution */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
          <h3 className="text-lg font-semibold mb-4 text-slate-700">
            Department Wise Strength
          </h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={techStack}
                  innerRadius={60}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {techStack.map((entry, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={COLORS[index % COLORS.length]}
                    />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="flex justify-center gap-4 mt-2">
            {techStack.map((item, i) => (
              <div
                key={i}
                className="flex items-center gap-1 text-xs text-slate-500"
              >
                <span
                  className="w-3 h-3 rounded-full"
                  style={{ backgroundColor: COLORS[i] }}
                ></span>
                {item.name}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* --- Data List Section --- */}
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <div className="p-6 border-b border-slate-100 flex justify-between items-center">
          <h3 className="text-lg font-semibold text-slate-700">
            Celebration this Month
            <MdOutlineCelebration />
          </h3>
          <span className="text-indigo-600 text-sm font-medium cursor-pointer">
            View All
          </span>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead className="bg-slate-50 text-slate-500 text-sm uppercase">
              <tr>
                <th className="px-6 py-4 font-medium">Employee Id</th>
                <th className="px-6 py-4 font-medium">Name</th>
                <th className="px-6 py-4 font-medium">Department</th>
                <th className="px-6 py-4 font-medium">Event</th>
                <th className="px-6 py-4 font-medium">Date</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {[
                {
                  id: "E121",
                  name: "Rahul Sharma",
                  department: "Engineering",
                  event: "Birthday",
                  date: "26 Sep 2026",
                },
                {
                  id: "E57",
                  name: "Priya Verma",
                  department: "Management",
                  event: "Work Anniversary",
                  date: "28 Sep 2026",
                },
                {
                  id: "E201",
                  name: "Amit Negi",
                  department: "Engineering",
                  event: "Birthday",
                  date: "30 Sep 2026",
                },
              ].map((student, index) => (
                <tr key={index} className="hover:bg-slate-50 transition">
                  <td className="px-6 py-4 font-medium text-slate-900">
                    {student.id}
                  </td>
                  <td className="px-6 py-4 font-medium text-slate-900">
                    {student.name}
                  </td>
                  <td className="px-6 py-4 text-slate-600">
                    {student.department}
                  </td>
                  <td className="px-6 py-4 text-slate-600">{student.event}</td>
                  <td className="px-6 py-4">{student.date}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
