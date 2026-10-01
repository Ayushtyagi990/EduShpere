import { useState } from "react";
import departmentService from "../services/department";

const useDepartment = () => {
  const [departments, setDpartments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);

  const getDepartmentLookups = () => {
    setLoading(true);
    departmentService
      .getDepartmentLookups()
      .then((res) => {
        setDpartments(res.data);
      })
      .catch((err) => {
        setError(err);
      })
      .finally(() => setLoading(false));
  };

  const getAllDepartments = () => {
    setLoading(true);
    departmentService
      .getDepartments()
      .then((res) => {
        setDpartments(res.data);
      })
      .catch((err) => {
        setError(err);
      })
      .finally(() => setLoading(false));
  };

  const createDepartment = () => {
    setLoading(true);
    departmentService
      .departments()
      .then((res) => {
        setDpartments(res.data);
      })
      .catch((err) => {
        setError(err);
      })
      .finally(() => setLoading(false));
  };

  return {
    departments,
    loading,
    error,
    successMessage,
    getDepartmentLookups,
    getAllDepartments,
    createDepartment,
  };
};

export default useDepartment;
