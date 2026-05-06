import { useState } from "react";
import { useParams } from "react-router-dom";
import axiosInstance from "../../api/axiosInstance";
import { useNavigate } from "react-router-dom";
export default function WorkplaceEvaluation() {

  const { placementId } = useParams();

  const [punctuality, setPunctuality] = useState("");
  const [teamwork, setTeamwork] = useState("");
  const [communication, setCommunication] = useState("");
  const [smartness, setSmartness] = useState("");
  const [discipline, setDiscipline] = useState("");

  const [comments, setComments] = useState("");
  
  
  const submitEvaluation = async () => {

    try {

      await axiosInstance.post(
        `workplace-evaluation/${placementId}/`,
        {
          punctuality,
          teamwork,
          communication,
          smartness,
          discipline,
          comments
        }
      );

      alert("Evaluation submitted successfully");

    } catch (err) {

      console.log(
        "ERROR:",
        err.response?.data || err
      );

      alert("Error submitting evaluation");
      alert(err);
    }
  };

  return (
    <div style={{ padding: "20px" }}>

      <h2>Workplace Evaluation</h2>

      <input
        type="number"
        placeholder="Punctuality"
        onChange={(e) =>
          setPunctuality(e.target.value)
        }
      />

      <br /><br />

      <input
        type="number"
        placeholder="Teamwork"
        onChange={(e) =>
          setTeamwork(e.target.value)
        }
      />

      <br /><br />

      <input
        type="number"
        placeholder="Communication"
        onChange={(e) =>
          setCommunication(e.target.value)
        }
      />

      <br /><br />

      <input
        type="number"
        placeholder="Smartness"
        onChange={(e) =>
          setSmartness(e.target.value)
        }
      />

      <br /><br />

      <input
        type="number"
        placeholder="Discipline"
        onChange={(e) =>
          setDiscipline(e.target.value)
        }
      />

      <br /><br />

      <textarea
        placeholder="Supervisor Comments"
        onChange={(e) =>
          setComments(e.target.value)
        }
      />

      <br /><br />

      <button onClick={submitEvaluation}>
        Submit Evaluation
      </button>

    </div>
  );
}