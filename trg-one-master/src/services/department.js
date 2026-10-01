import httpClient from "../lib/httpClient";

const departmentService = {
  getDepartmentLookups: () => httpClient.get("api/departments/lookups"),
  getDepartments: () => httpClient.get("api/departments"),
  getDepartmentById: (departmentId) =>
    httpClient.get(`api/departments/lookup/${departmentId}`),
  createDepartment: (department) =>
    httpClient.post("api/departments/create", department),
};

export default departmentService;
