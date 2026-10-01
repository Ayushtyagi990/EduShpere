import { useDispatch, useSelector } from "react-redux";
import { updateFormData, prevStep } from "../../../store/employeeSlice";
import useDepartment from "../../../hooks/useDepartment";
import useEmployee from "../../../hooks/useEmployee";
import { useEffect } from "react";

export default function JobProfile() {
  const dispatch = useDispatch();
  const formData = useSelector((state) => state.employee.formData);
  const { departments, getDepartmentLookups } = useDepartment();
  const { employeeLookups, getEmployeeLookups } = useEmployee();

  const handleChange = (e) => {
    dispatch(updateFormData({ [e.target.name]: e.target.value }));
  };

  useEffect(() => {
    getDepartmentLookups();
    getEmployeeLookups();
  }, []);

  return (
    <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
      <h2 className="text-lg font-semibold text-slate-700 mb-4">Job Profile</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">
            Department
          </label>
          <select
            name="departmentId"
            value={formData.departmentId}
            onChange={handleChange}
            className="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
          >
            <option value="" disabled>
              Select Department
            </option>
            {departments.length &&
              departments.map((department) => (
                <option
                  value={department.departmentId}
                  key={`dep${department.departmentId}`}
                >
                  {department.name}
                </option>
              ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">
            Job Title
          </label>
          <input
            type="text"
            name="jobTitle"
            value={formData.jobTitle}
            onChange={handleChange}
            placeholder="Senior Software Engineer"
            className="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">
            Reporting Manager
          </label>
          <select
            name="reportingManagerId"
            value={formData.reportingManagerId}
            onChange={handleChange}
            className="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
          >
            <option value="" disabled>
              Select Manager
            </option>
            {employeeLookups.length &&
              employeeLookups.map((employee) => (
                <option
                  value={employee.employeeId}
                  key={`emp-${employee.employeeId}`}
                >
                  {employee.fullName}
                </option>
              ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1 required">
            Date of Joining
          </label>
          <input
            type="date"
            name="dateOfJoining"
            required
            value={formData.dateOfJoining}
            onChange={handleChange}
            className="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">
            Annual CTC
          </label>
          <input
            type="number"
            name="salary"
            value={formData.salary}
            onChange={handleChange}
            placeholder="75000"
            className="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
          />
        </div>

        <div className="md:col-span-2">
          <label className="block text-sm font-medium text-slate-700 mb-1">
            Skill Set
          </label>
          <textarea
            name="skillSet"
            rows="3"
            value={formData.skillSet}
            onChange={handleChange}
            placeholder="React, C#, .NET Core, SQL Server..."
            className="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
          ></textarea>
        </div>
      </div>

      <div className="flex justify-between mt-6">
        <button
          type="button"
          onClick={() => dispatch(prevStep())}
          className="px-5 py-2.5 border border-slate-300 text-slate-700 rounded-lg hover:bg-slate-50 transition font-medium text-sm"
        >
          Back
        </button>
        <button
          type="submit"
          className="cursor-pointer px-5 py-2.5 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition font-medium text-sm"
        >
          Submit Employee
        </button>
      </div>
    </div>
  );
}
