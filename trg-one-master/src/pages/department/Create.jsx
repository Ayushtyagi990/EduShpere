import { useState, useEffect } from "react";
import useEmployee from "../../hooks/useEmployee";
import { Alert } from "../../components/Alert";
import { HiUserAdd } from "react-icons/hi";

const initialState = {
  name: "",
  code: "",
  hodId: "",
};

export default function DepartmentCreate() {
  const [formData, setFormData] = useState(initialState);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(false);

  const { employeeLookups, getEmployeeLookups } = useEmployee();

  useEffect(() => {
    getEmployeeLookups();
  }, []);

  const handleFormSubmit = (e) => {
    e.preventDefault();

    setLoading(true);
    setError(null);
    setSuccessMessage(false);

    try {
      // TODO:
      // Add your department API call here.
      // Example:
      // await departmentService.createDepartment(formData);

      console.log("Department Data:", formData);

      setSuccessMessage(true);
      setFormData(initialState);
    } catch (err) {
      console.error("Department creation failed:", err);
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  return (
    <div className="max-w-4xl mx-auto">
      {/* Page Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-slate-800 flex items-center gap-2">
          <HiUserAdd className="text-indigo-600" />
          New Department
        </h1>

        <p className="text-slate-500">
          Fill in the details below to create a new department into the
          system.
        </p>
      </div>

      {/* Success Message */}
      {successMessage && (
        <Alert
          type="success"
          title="Department Created!"
          message="New department record has been successfully saved."
        />
      )}

      {/* Error Message */}
      {error && (
        <Alert
          type="danger"
          title="Submission Error"
          message="Something went wrong"
        />
      )}

      <div className="max-w-4xl mx-auto p-4 md:p-8">
        <form onSubmit={handleFormSubmit}>
          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
            <h2 className="text-lg font-semibold text-slate-700 mb-4">
              Job Profile
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Department Name */}
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  Name
                </label>

                <input
                  type="text"
                  name="name"
                  required
                  value={formData.name}
                  onChange={handleChange}
                  placeholder="Human Resource"
                  className="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
                />
              </div>

              {/* Department Code */}
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  Code
                </label>

                <input
                  type="text"
                  name="code"
                  required
                  value={formData.code}
                  onChange={handleChange}
                  placeholder="HR"
                  className="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
                />
              </div>

              {/* HOD */}
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  Head Of The Department
                </label>

                <select
                  name="hodId"
                  value={formData.hodId}
                  onChange={handleChange}
                  className="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
                >
                  <option value="">
                    Select Manager
                  </option>

                  {employeeLookups?.map((employee) => (
                    <option
                      value={employee.employeeId}
                      key={employee.employeeId}
                    >
                      {employee.fullName}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {/* Submit */}
            <div className="flex justify-between mt-6">
              <button
                type="submit"
                disabled={loading}
                className="cursor-pointer px-5 py-2.5 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 disabled:bg-emerald-400 disabled:cursor-not-allowed transition font-medium text-sm"
              >
                {loading ? "Saving..." : "Submit Department"}
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}
