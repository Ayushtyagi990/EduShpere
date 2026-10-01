import React, { useState } from "react";
import {
  HiUserAdd,
  HiCloudUpload,
  HiIdentification,
  HiSave,
} from "react-icons/hi";

const RegisterStudent = () => {
  const [formData, setFormData] = useState({
    firstName: "",
    lastName: "",
    email: "",
    phone: "",
    dob: "",
    gender: "",
    course: "",
    address: "",
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Registering Student:", formData);
    // Add your API call here
  };

  return (
    <div className="max-w-4xl mx-auto">
      {/* Page Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-slate-800 flex items-center gap-2">
          <HiUserAdd className="text-indigo-600" />
          New Student Admission
        </h1>
        <p className="text-slate-500">
          Fill in the details below to enroll a new student into the system.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Section 1: Personal Information */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
          <h2 className="text-lg font-semibold text-slate-700 mb-4 flex items-center gap-2">
            <HiIdentification className="text-slate-400" />
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
                className="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
                placeholder="e.g. Rahul"
                onChange={handleChange}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">
                Last Name
              </label>
              <input
                type="text"
                name="lastName"
                className="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
                placeholder="e.g. Sharma"
                onChange={handleChange}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1 required">
                Date of Birth
              </label>
              <input
                type="date"
                name="dob"
                required
                className="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
                onChange={handleChange}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1 required">
                Gender
              </label>
              <select
                name="gender"
                required
                className="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
                onChange={handleChange}
              >
                <option value="">Select Gender</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
              </select>
            </div>
          </div>
        </div>

        {/* Section 2: Academic Details */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
          <h2 className="text-lg font-semibold text-slate-700 mb-4">
            Academic Selection
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1 required">
                Enrolling Course
              </label>
              <select
                name="course"
                required
                className="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
                onChange={handleChange}
              >
                <option value="0">Select a Course</option>
                <option value="1">Python</option>
                <option value="2">Machine Learning</option>
                <option value="3">Data Analytics</option>
                <option value="4">DevOps</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">
                Upload Photo
              </label>
              <div className="relative group cursor-pointer border-2 border-dashed border-slate-300 rounded-lg p-2 hover:border-indigo-400 transition">
                <input
                  type="file"
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                />
                <div className="flex items-center gap-2 text-slate-500 text-sm justify-center">
                  <HiCloudUpload className="text-xl text-indigo-500" />
                  <span>Click to upload JPEG/PNG</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Section 3: Contact Details */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
          <h2 className="text-lg font-semibold text-slate-700 mb-4">
            Contact Information
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1 required">
                Email Address
              </label>
              <input
                type="email"
                name="email"
                required
                className="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
                placeholder="student@college.edu"
                onChange={handleChange}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1 required">
                Phone Number
              </label>
              <input
                type="phone"
                name="phone"
                required
                className="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
                placeholder="(123) 456-7890"
                onChange={handleChange}
              />
            </div>
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-slate-700 mb-1 required">
                Address
              </label>
              <textarea
                name="address"
                rows="3"
                required
                className="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
                placeholder="Full residential address..."
                onChange={handleChange}
              ></textarea>
            </div>
          </div>
        </div>

        {/* Form Actions */}
        <div className="flex justify-end gap-3">
          <button
            type="button"
            className="px-2 py-2 text-sm rounded-lg border border-slate-300 text-slate-700 font-normal hover:bg-slate-300 transition duration-150 ease-in-out"
          >
            Cancel
          </button>
          <button
            type="submit"
            className="px-2 py-1 text-sm font-normal border border-blue-600 text-blue-600 rounded hover:bg-blue-600 hover:text-white transition-colors duration-500 ease-in-out"
          >
            Register Student
          </button>
        </div>
      </form>
    </div>
  );
};

export default RegisterStudent;
