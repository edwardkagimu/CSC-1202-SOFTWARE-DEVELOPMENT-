import { useEffect, useState } from "react";
import axiosInstance from "../../api/axiosInstance";
import { useNavigate } from "react-router-dom";

export default function AssignedStudents() {

  const [students, setStudents] = useState([]);

  const navigate = useNavigate();

  useEffect(() => {
    fetchStudents();
  }, []);

  const fetchStudents = async () => {
    try {
      const res = await axiosInstance.get("assigned-students/");
      setStudents(res.data);
    } catch (err) {
      console.log(err);

    }
  };

  return (
    <div style={{ padding: 20 }}>

      <h2>Assigned Students</h2>

      {students.map((s) => (

        <div key={s.placement_id}>

          <p>{s.username}</p>

          <p>{s.reg_no}</p>

          <button onClick={() =>
            navigate(
              `/workplace-evaluation/${s.placement_id}`
            )
          }>

            Evaluate

          </button>

        </div>

      ))}

    </div>
  );
}