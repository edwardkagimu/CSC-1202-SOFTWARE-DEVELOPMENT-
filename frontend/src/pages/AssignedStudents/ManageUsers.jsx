import { useEffect, useState } from "react";
import axiosInstance from "../../api/axiosInstance";

export default function ManageUsers() {

  const [users, setUsers] = useState([]);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {const res = await axiosInstance.get("manage-users/");
      
      console.log("USERS:", res.data);
      setUsers(Array.isArray(res.data) ? res.data:[]);

    } catch (err) {
      console.log(err.response?.data || err);
      setUsers([]);
    }
  };

  const deleteUser = async (id) => {
    try {
      await axiosInstance.delete(
        `api/delete-user/${id}/`
      );
      alert("User deleted");
      fetchUsers();
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <div style={{ padding: "20px" }}>

      <h2>Manage Users</h2>

      {users.map((u) => (

        <div
          key={u.id}
          style={{
            border: "1px solid #ccc",
            margin: "10px",
            padding: "10px"
          }}
        >

          <p><b>Username:</b> {u.username}</p>

          <p><b>Role:</b> {u.role}</p>

          {u.reg_no && (
            <p><b>Reg No:</b> {u.reg_no}</p>
          )}

          {u.workplace_supervisor && (
            <p>
              <b>Workplace Supervisor:</b>
              {u.workplace_supervisor}
            </p>
          )}

          {u.academic_supervisor && (
            <p>
              <b>Academic Supervisor:</b>
              {u.academic_supervisor}
            </p>
          )}

          <button onClick={() => deleteUser(u.id)}>
            Delete User
          </button>

        </div>

      ))}

    </div>
  );
}