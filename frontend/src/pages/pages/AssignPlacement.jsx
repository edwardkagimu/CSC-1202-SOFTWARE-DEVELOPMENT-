import { useEffect, useState } from "react";
import axiosInstance, { ENDPOINTS } from "../../api/axiosInstance";

export default function AssignPlacement() {
  const [students, setStudents] = useState([]);
  const [workplaces, setWorkplaces] = useState([]);
  const [academics, setAcademics] = useState([]);

  const [student, setStudent] = useState("");
  const [workplace, setWorkplace] = useState("");
  const [academic, setAcademic] = useState("");

  const [companyName, setCompanyName] = useState("");
  const [companyAddress, setCompanyAddress] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      console.log("Fetching users...");
      const res = await axiosInstance.get(ENDPOINTS.users);

      console.log("USERS RESPONSE:", res.data);  // for debuging
       
      setStudents(res.data.students);
      setWorkplaces(res.data.workplace_supervisors);
      setAcademics(res.data.academic_supervisors);
    } catch (err) {
      console.log(err);
    }
  };

  const handleAssign = async () => {
    if (
      !student ||
      !workplace ||
      !academic ||
      !companyName ||
      !companyAddress ||
      !startDate ||
      !endDate
    ) {
      alert("All fields are required");
      return;
    }

    try {
      await axiosInstance.post(ENDPOINTS.assignPlacement, {
        student_id: student,
        workplace_supervisor_id: workplace,
        academic_supervisor_id: academic,
        company_name: companyName,
        company_address: companyAddress,
        start_date: startDate,
        end_date: endDate,
      });

      alert("Placement assigned successfully");

      // reset form (optional)
      setStudent("");
      setWorkplace("");
      setAcademic("");
      setCompanyName("");
      setCompanyAddress("");
      setStartDate("");
      setEndDate("");

    } catch (err) {
      console.log(err.response?.data || err);
      alert("Error assigning placement");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Assign Internship Placement</h2>

      {/* STUDENT */}
      <label>Student</label>
      <br />
      <select value={student} onChange={(e) => setStudent(e.target.value)}>
        <option value="">Select Student</option>
        {students.map((s) => (
          <option key={s.id} value={s.id}>
            {s.reg_no} - {s.username}
          </option>
        ))}
      </select>

      <br /><br />

      {/* WORKPLACE SUPERVISOR */}
      <label>Workplace Supervisor</label>
      <br />
      <select value={workplace} onChange={(e) => setWorkplace(e.target.value)}>
        <option value="">Select Workplace Supervisor</option>
        {workplaces.map((w) => (
          <option key={w.id} value={w.id}>
            {w.username}
          </option>
        ))}
      </select>

      <br /><br />

      {/* ACADEMIC SUPERVISOR */}
      <label>Academic Supervisor</label>
      <br />
      <select value={academic} onChange={(e) => setAcademic(e.target.value)}>
        <option value="">Select Academic Supervisor</option>
        {academics.map((a) => (
          <option key={a.id} value={a.id}>
            {a.username}
          </option>
        ))}
      </select>

      <br /><br />

      {/* COMPANY DETAILS */}
      <label>Company Name</label>
      <br />
      <input
        type="text"
        value={companyName}
        onChange={(e) => setCompanyName(e.target.value)}
      />

      <br /><br />

      <label>Company Address</label>
      <br />
      <input
        type="text"
        value={companyAddress}
        onChange={(e) => setCompanyAddress(e.target.value)}
      />

      <br /><br />

      {/* DATES */}
      <label>Start Date</label>
      <br />
      <input
        type="date"
        value={startDate}
        onChange={(e) => setStartDate(e.target.value)}
      />

      <br /><br />

      <label>End Date</label>
      <br />
      <input
        type="date"
        value={endDate}
        onChange={(e) => setEndDate(e.target.value)}
      />

      <br /><br />

      <button onClick={handleAssign}>Assign Placement</button>
    </div>
  );
}