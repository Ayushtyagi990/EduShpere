import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  currentStep: 1,
  formData: {
    // Step 1: Personal Details
    firstName: "",
    lastName: "",
    dateOfBirth: "",
    genderId: "",
    fatherName: "",
    motherName: "",
    maritalStatusId: "",

    // Step 2: Contact Details
    officialEmail: "",
    personalEmail: "",
    phoneNumber: "",
    alternatePhone: "",
    addressLine1: "",
    addressLine2: "",
    city: "",
    state: "",
    zipCode: "",

    // Step 3: Job Profile
    departmentId: "",
    jobTitle: "",
    reportingManagerId: "",
    skillSet: "",
    dateOfJoining: "",
    salary: "",
  },
};

const employeeSlice = createSlice({
  name: "employeeForm",
  initialState,
  reducers: {
    updateFormData: (state, action) => {
      state.formData = { ...state.formData, ...action.payload };
    },
    nextStep: (state) => {
      if (state.currentStep < 3) state.currentStep += 1;
    },
    prevStep: (state) => {
      if (state.currentStep > 1) state.currentStep -= 1;
    },
    resetForm: () => initialState,
  },
});

export const { updateFormData, nextStep, prevStep, resetForm } =
  employeeSlice.actions;
export default employeeSlice.reducer;
