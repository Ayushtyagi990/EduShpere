import httpClient from "../lib/httpClient";

const employeeService = {
  getEmployees: () => httpClient.get("/api/employees"),
  getEmployeeLookups: () => httpClient.get("/api/employees/lookups"),
  getEmployeeById: (employeeId) =>
    httpClient.get(`/api/employees/${employeeId}`),
  createEmployee: (employee) => httpClient.post("/api/employees", employee),
  updateEmployee: (employeeId, employee) =>
    httpClient.put(`/api/employees/${employeeId}`, employee),
  deleteEmployee: (employeeId) =>
    httpClient.delete(`/api/employees/${employeeId}`),
};

export default employeeService;
