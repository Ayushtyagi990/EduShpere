import useEmployee from "../../hooks/useEmployee";
import { useState, useEffect } from "react";
import {
  HiOutlineTrash,
  HiOutlinePencilAlt,
  HiEye,
  HiChevronLeft,
  HiChevronRight,
} from "react-icons/hi";

export default function EmployeeIndex() {
  const { employees, loading, error, fetchEmployees } = useEmployee();

  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 5; // Adjust how many employees to show per page

  useEffect(() => {
    fetchEmployees();
  }, []);

  const totalPages = Math.ceil((employees?.length || 0) / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const currentEmployees = employees.slice(
    startIndex,
    startIndex + itemsPerPage,
  );

  const handlePageChange = (page) => {
    if (page >= 1 && page <= totalPages) {
      setCurrentPage(page);
    }
  };

  return (
    <div className="p-4">
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <div className="p-6 border-b border-slate-100 flex justify-between items-center">
          <h3 className="text-lg font-semibold text-slate-700">
            All Employees
          </h3>
          <span className="text-indigo-600 text-sm font-medium cursor-pointer">
            View All
          </span>
        </div>

        <div className="overflow-x-auto">
          {loading ? (
            <p>Loading...</p>
          ) : error ? (
            <p>Error: {error?.message}</p>
          ) : employees.length === 0 ? (
            <p>No employees found.</p>
          ) : (
            <>
              <table className="w-full text-left">
                <thead className="bg-slate-50 text-slate-500 text-sm uppercase">
                  <tr>
                    <th className="px-6 py-4 font-medium">Employee Id</th>
                    <th className="px-6 py-4 font-medium">Department</th>
                    <th className="px-6 py-4 font-medium">Name</th>
                    <th className="px-6 py-4 font-medium">Job Title</th>
                    <th className="px-6 py-4 font-medium">Email</th>
                    <th className="px-6 py-4 font-medium">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {currentEmployees.map((employee, index) => (
                    <tr
                      key={employee.employeeID || index}
                      className="hover:bg-slate-50 transition"
                    >
                      <td className="px-6 py-4 font-medium text-slate-900">
                        {employee.employeeID}
                      </td>
                      <td className="px-6 py-4 text-slate-600">
                        {employee.departmentName}
                      </td>
                      <td className="px-6 py-4 text-slate-600">
                        {employee.fullName}
                      </td>
                      <td className="px-6 py-4 text-slate-600">
                        {employee.jobTitle}
                      </td>
                      <td className="px-6 py-4 text-slate-600">
                        {employee.email}
                      </td>
                      <td>
                        <div className="flex items-center gap-2">
                          <HiEye className="text-blue-500" />
                          <HiOutlinePencilAlt className="text-teal-500" />
                          <HiOutlineTrash className="text-red-500" />
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>

              <div className="px-6 py-4 border-t border-slate-100 flex items-center justify-between">
                <span className="text-sm text-slate-500">
                  Showing{" "}
                  <span className="font-semibold">{startIndex + 1}</span> to{" "}
                  <span className="font-semibold">
                    {Math.min(startIndex + itemsPerPage, employees.length)}
                  </span>{" "}
                  of <span className="font-semibold">{employees.length}</span>{" "}
                  entries
                </span>

                <div className="flex items-center gap-1">
                  <button
                    onClick={() => handlePageChange(currentPage - 1)}
                    disabled={currentPage === 1}
                    className="p-2 border rounded-md text-slate-600 hover:bg-slate-50 disabled:opacity-40 disabled:cursor-not-allowed"
                  >
                    <HiChevronLeft className="w-5 h-5" />
                  </button>

                  {Array.from({ length: totalPages }, (_, i) => i + 1).map(
                    (page) => (
                      <button
                        key={page}
                        onClick={() => handlePageChange(page)}
                        className={`px-3 py-1 text-sm border rounded-md font-medium transition ${
                          currentPage === page
                            ? "bg-indigo-600 text-white border-indigo-600"
                            : "text-slate-600 hover:bg-slate-50"
                        }`}
                      >
                        {page}
                      </button>
                    ),
                  )}

                  <button
                    onClick={() => handlePageChange(currentPage + 1)}
                    disabled={currentPage === totalPages || totalPages === 0}
                    className="p-2 border rounded-md text-slate-600 hover:bg-slate-50 disabled:opacity-40 disabled:cursor-not-allowed"
                  >
                    <HiChevronRight className="w-5 h-5" />
                  </button>
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
