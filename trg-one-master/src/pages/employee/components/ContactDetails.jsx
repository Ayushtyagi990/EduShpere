import { useDispatch, useSelector } from "react-redux";
import {
  updateFormData,
  nextStep,
  prevStep,
} from "../../../store/employeeSlice";

export default function ContactDetails() {
  const dispatch = useDispatch();
  const formData = useSelector((state) => state.employee.formData);

  const handleChange = (e) => {
    dispatch(updateFormData({ [e.target.name]: e.target.value }));
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
      <h2 className="text-lg font-semibold text-slate-700 mb-4">
        Contact Information
      </h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1 required">
            Official Email Address
          </label>
          <input
            type="email"
            name="officialEmail"
            required
            value={formData.officialEmail}
            onChange={handleChange}
            placeholder="john.doe@company.com"
            className="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1 required">
            Personal Email Address
          </label>
          <input
            type="email"
            name="personalEmail"
            required
            value={formData.personalEmail}
            onChange={handleChange}
            placeholder="john.doe@gmail.com"
            className="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1 required">
            Phone Number
          </label>
          <input
            type="tel"
            name="phoneNumber"
            required
            value={formData.phoneNumber}
            onChange={handleChange}
            placeholder="(123) 456-7890"
            className="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">
            Alternate Phone Number
          </label>
          <input
            type="tel"
            name="alternatePhone"
            value={formData.alternatePhone}
            onChange={handleChange}
            placeholder="(123) 456-7890"
            className="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
          />
        </div>

        <div className="md:col-span-2">
          <label className="block text-sm font-medium text-slate-700 mb-1 required">
            Address Line 1
          </label>
          <input
            type="text"
            name="addressLine1"
            required
            value={formData.addressLine1}
            onChange={handleChange}
            placeholder="Street address, P.O. box"
            className="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
          />
        </div>

        <div className="md:col-span-2">
          <label className="block text-sm font-medium text-slate-700 mb-1">
            Address Line 2
          </label>
          <input
            type="text"
            name="addressLine2"
            value={formData.addressLine2}
            onChange={handleChange}
            placeholder="Apartment, suite, unit, building, floor"
            className="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1 required">
            City
          </label>
          <input
            type="text"
            name="city"
            required
            value={formData.city}
            onChange={handleChange}
            placeholder="City"
            className="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1 required">
            State
          </label>
          <input
            type="text"
            name="state"
            required
            value={formData.state}
            onChange={handleChange}
            placeholder="State"
            className="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1 required">
            PIN / ZIP Code
          </label>
          <input
            type="text"
            name="zipCode"
            required
            value={formData.zipCode}
            onChange={handleChange}
            placeholder="10001"
            className="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
          />
        </div>
      </div>

      <div className="flex justify-between mt-6">
        <button
          type="button"
          onClick={() => dispatch(prevStep())}
          className="cursor-pointer px-5 py-2.5 border border-slate-300 text-slate-700 rounded-lg hover:bg-slate-50 transition font-medium text-sm"
        >
          Back
        </button>
        <button
          type="button"
          onClick={() => dispatch(nextStep())}
          className="cursor-pointer px-5 py-2.5 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition font-medium text-sm"
        >
          Next: Job Profile
        </button>
      </div>
    </div>
  );
}
