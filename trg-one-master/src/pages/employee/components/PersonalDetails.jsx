import { useDispatch, useSelector } from "react-redux";
import { updateFormData, nextStep } from "../../../store/employeeSlice";

export default function PersonalDetails() {
  const dispatch = useDispatch();
  const formData = useSelector((state) => state.employee.formData);

  const handleChange = (e) => {
    dispatch(updateFormData({ [e.target.name]: e.target.value }));
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
      <h2 className="text-lg font-semibold text-slate-700 mb-4">
        Personal Details
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1 required">
            First Name
          </label>
          <input
            type="text"
            name="firstName"
            required
            value={formData.firstName}
            onChange={handleChange}
            placeholder="John"
            className="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">
            Last Name
          </label>
          <input
            type="text"
            name="lastName"
            required
            value={formData.lastName}
            onChange={handleChange}
            placeholder="Doe"
            className="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1 required">
            Date of Birth
          </label>
          <input
            type="date"
            name="dateOfBirth"
            required
            value={formData.dateOfBirth}
            onChange={handleChange}
            className="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1 required">
            Gender
          </label>
          <select
            name="genderId"
            required
            value={formData.genderId}
            onChange={handleChange}
            className="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
          >
            <option value="">Select Gender</option>
            <option value="1">Male</option>
            <option value="2">Female</option>
            <option value="3">Other</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">
            Father's Name
          </label>
          <input
            type="text"
            name="fatherName"
            required
            value={formData.fatherName}
            onChange={handleChange}
            placeholder="Robert Doe"
            className="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">
            Mother's Name
          </label>
          <input
            type="text"
            name="motherName"
            required
            value={formData.motherName}
            onChange={handleChange}
            placeholder="Mary Doe"
            className="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1 required">
            Marital Status
          </label>
          <select
            name="maritalStatusId"
            required
            value={formData.maritalStatusId}
            onChange={handleChange}
            className="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
          >
            <option value="">Select Status</option>
            <option value="1">Single</option>
            <option value="2">Married</option>
            <option value="3">Divorced</option>
          </select>
        </div>
      </div>

      <div className="flex justify-end mt-6">
        <button
          type="button"
          onClick={() => dispatch(nextStep())}
          className="cursor-pointer px-5 py-2.5 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition font-medium text-sm"
        >
          Next: Contact Details
        </button>
      </div>
    </div>
  );
}
