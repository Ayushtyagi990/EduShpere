import { useState, useEffect, useCallback } from "react";
import employeeService from "../services/employee";

const useEmployee = () => {
  const [employees, setEmployees] = useState([]);
  const [employeeLookups, setEmployeeLookups] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);

  const getEmployeeLookups = () => {
    setLoading(true);
    employeeService
      .getEmployeeLookups()
      .then((res) => {
        setEmployeeLookups(res.data);
      })
      .catch((err) => {
        setError(err);
      })
      .finally(() => setLoading(false));
  };

  const fetchEmployees = () => {
    setLoading(true);
    employeeService
      .getEmployees()
      .then((res) => {
        setEmployees(res.data);
      })
      .catch((err) => {
        setError(err);
      })
      .finally(() => {
        setLoading(false);
      });
  };

  const createEmployee = (formData) => {
    setLoading(true);
    return employeeService
      .createEmployee(formData)
      .then(() => {
        setSuccessMessage("Employee created!");
      })
      .catch((err) => {
        setError(err);
      })
      .finally(() => setLoading(false));
  };

  return {
    employees,
    employeeLookups,
    loading,
    successMessage,
    error,
    createEmployee,
    fetchEmployees,
    getEmployeeLookups,
  };
};

export default useEmployee;
