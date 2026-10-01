import { useSelector, useDispatch } from "react-redux";
import PersonalDetails from "./components/PersonalDetails";
import ContactDetails from "./components/ContactDetails";
import JobProfile from "./components/JobProfile";
import useEmployee from "../../hooks/useEmployee";
import { resetForm } from "../../store/employeeSlice";
import { Alert } from "../../components/Alert";

import { HiUserAdd } from "react-icons/hi";

export default function EmployeeCreate() {
  const dispatch = useDispatch();
  const { formData, currentStep } = useSelector((state) => state.employee);
  const { loading, successMessage, error, createEmployee } = useEmployee();

  const steps = [
    { number: 1, title: "Personal Details" },
    { number: 2, title: "Contact Details" },
    { number: 3, title: "Job Profile" },
  ];

  const handleFormSubmit = (e) => {
    e.preventDefault();
    const payload = {
      ...formData,
      reportingManagerId: formData.reportingManagerId
        ? Number(formData.reportingManagerId)
        : null,
      departmentId: formData.departmentId
        ? Number(formData.departmentId)
        : null,
      genderId: Number(formData.genderId),
      maritalStatusId: Number(formData.maritalStatusId),
      salary: Number(formData.salary),
    };
    createEmployee(payload);
    if (successMessage && !loading) {
      dispatch(resetForm());
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      {/* Page Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-slate-800 flex items-center gap-2">
          <HiUserAdd className="text-indigo-600" />
          New Employee
        </h1>
        <p className="text-slate-500">
          Fill in the details below to create a new employee into the system.
        </p>
      </div>
      {successMessage && (
        <Alert
          type="success"
          title="Employee Created!"
          message="New employee record has been successfully saved."
        />
      )}
      {error && (
        <Alert
          type="danger"
          title="Submission Error"
          message="Something went wrong"
        />
      )}
      <div className="max-w-4xl mx-auto p-4 md:p-8">
        {/* Step Indicator Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between relative">
            {steps.map((step) => (
              <div
                key={step.number}
                className="flex flex-col items-center z-10"
              >
                <div
                  className={`w-10 h-10 rounded-full flex items-center justify-center font-semibold text-sm transition ${
                    currentStep >= step.number
                      ? "bg-indigo-600 text-white"
                      : "bg-slate-100 text-slate-400 border border-slate-300"
                  }`}
                >
                  {step.number}
                </div>
                <span className="text-xs font-medium text-slate-600 mt-2">
                  {step.title}
                </span>
              </div>
            ))}

            {/* Stepper Connecting Bar */}
            <div className="absolute top-5 left-0 w-full h-0.5 bg-slate-200 z-0">
              <div
                className="h-full bg-indigo-600 transition-all duration-300"
                style={{ width: `${((currentStep - 1) / 2) * 100}%` }}
              ></div>
            </div>
          </div>
        </div>
        <form onSubmit={handleFormSubmit}>
          {/* Render Component Dynamically */}
          {currentStep === 1 && <PersonalDetails />}
          {currentStep === 2 && <ContactDetails />}
          {currentStep === 3 && <JobProfile isLoading={loading} />}
        </form>
      </div>
    </div>
  );
}
