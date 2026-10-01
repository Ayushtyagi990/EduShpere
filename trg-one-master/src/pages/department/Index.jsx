import { useDepartment } from "../../hooks/useDepartment";
import { useState, useEffect } from "react";

import {
  HiOutlineTrash,
  HiOutlinePencilAlt,
  HiEye,
  HiChevronLeft,
  HiChevronRight,
} from "react-icons/hi";

export default function DepartmentIndex() {
  const {
    departments = [],
    loading,
    error,
    getAllDepartments,
  } = useDepartment();

  const [currentPage, setCurrentPage] = useState(1);

  const itemsPerPage = 5;

  useEffect(() => {
    getAllDepartments();
  }, []);

  // Total pages
  const totalPages = Math.ceil(departments.length / itemsPerPage);

  // Starting index
  const startIndex = (currentPage - 1) * itemsPerPage;

  // Departments for current page
  const currentDepartments = departments.slice(
    startIndex,
    startIndex + itemsPerPage
  );

  // Change page
  const handlePageChange = (page) => {
    if (page >= 1 && page <= totalPages) {
      setCurrentPage(page);
    }
  };

  // Reset page if current page becomes invalid
  useEffect(() => {
    if (totalPages > 0 && currentPage > totalPages) {
      setCurrentPage(1);
    }
  }, [totalPages, currentPage]);

  return (
    <div className="p-4">
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        {/* Header */}
        <div className="p-6 border-b border-slate-100 flex justify-between items-center">
          <h3 className="text-lg font-semibold text-slate-700">
            All Departments
          </h3>

          <span className="text-indigo-600 text-sm font-medium cursor-pointer">
            View All
          </span>
        </div>

        {/* Content */}
        <div className="overflow-x-auto">
          {/* Loading */}
          {loading && (
            <div className="p-6 text-center text-slate-500">
              Loading departments...
            </div>
          )}

          {/* Error */}
          {!loading && error && (
            <div className="p-6 text-center text-red-500">
              Error:{" "}
              {error?.response?.data?.message ||
                error?.message ||
                "Something went wrong"}
            </div>
          )}

          {/* Empty */}
          {!loading && !error && departments.length === 0 && (
            <div className="p-6 text-center text-slate-500">
              No departments found.
            </div>
          )}

          {/* Table */}
          {!loading && !error && departments.length > 0 && (
            <>
              <table className="w-full text-left">
                <thead className="bg-slate-50 text-slate-500 text-sm uppercase">
                  <tr>
                    <th className="px-6 py-4 font-medium">
                      Department Id
                    </th>

                    <th className="px-6 py-4 font-medium">
                      Name
                    </th>

                    <th className="px-6 py-4 font-medium">
                      Code
                    </th>

                    <th className="px-6 py-4 font-medium">
                      HOD
                    </th>

                    <th className="px-6 py-4 font-medium">
                      Total Employees
                    </th>

                    <th className="px-6 py-4 font-medium">
                      Action
                    </th>
                  </tr>
                </thead>

                <tbody className="divide-y divide-slate-100">
                  {currentDepartments.map((department, index) => (
                    <tr
                      key={department.departmentId || index}
                      className="hover:bg-slate-50 transition"
                    >
                      {/* Department ID */}
                      <td className="px-6 py-4 font-medium text-slate-900">
                        {department.departmentId || "-"}
                      </td>

                      {/* Name */}
                      <td className="px-6 py-4 font-medium text-slate-900">
                        {department.name || "-"}
                      </td>

                      {/* Code */}
                      <td className="px-6 py-4 text-slate-600">
                        {department.code || "-"}
                      </td>

                      {/* HOD */}
                      <td className="px-6 py-4 text-slate-600">
                        {department.headOfDepartment || "-"}
                      </td>

                      {/* Employee Count */}
                      <td className="px-6 py-4 text-slate-600">
                        {department.employeeCount ?? 0}
                      </td>

                      {/* Actions */}
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-3">
                          <button
                            type="button"
                            title="View"
                            className="text-blue-500 hover:text-blue-700"
                          >
                            <HiEye className="w-5 h-5" />
                          </button>

                          <button
                            type="button"
                            title="Edit"
                            className="text-teal-500 hover:text-teal-700"
                          >
                            <HiOutlinePencilAlt className="w-5 h-5" />
                          </button>

                          <button
                            type="button"
                            title="Delete"
                            className="text-red-500 hover:text-red-700"
                          >
                            <HiOutlineTrash className="w-5 h-5" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>

              {/* Pagination */}
              <div className="px-6 py-4 border-t border-slate-100 flex items-center justify-between">
                {/* Entry information */}
                <span className="text-sm text-slate-500">
                  Showing{" "}
                  <span className="font-semibold">
                    {startIndex + 1}
                  </span>{" "}
                  to{" "}
                  <span className="font-semibold">
                    {Math.min(
                      startIndex + itemsPerPage,
                      departments.length
                    )}
                  </span>{" "}
                  of{" "}
                  <span className="font-semibold">
                    {departments.length}
                  </span>{" "}
                  entries
                </span>

                {/* Pagination buttons */}
                <div className="flex items-center gap-1">
                  {/* Previous */}
                  <button
                    type="button"
                    onClick={() =>
                      handlePageChange(currentPage - 1)
                    }
                    disabled={currentPage === 1}
                    className="p-2 border rounded-md text-slate-600 hover:bg-slate-50 disabled:opacity-40 disabled:cursor-not-allowed"
                  >
                    <HiChevronLeft className="w-5 h-5" />
                  </button>

                  {/* Page numbers */}
                  {Array.from(
                    { length: totalPages },
                    (_, i) => i + 1
                  ).map((page) => (
                    <button
                      type="button"
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
                  ))}

                  {/* Next */}
                  <button
                    type="button"
                    onClick={() =>
                      handlePageChange(currentPage + 1)
                    }
                    disabled={
                      currentPage === totalPages ||
                      totalPages === 0
                    }
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
