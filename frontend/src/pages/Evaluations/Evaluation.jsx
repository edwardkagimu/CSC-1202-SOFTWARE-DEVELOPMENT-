import { useEffect, useState } from "react";
import axiosInstance from "../../api/axiosInstance";
import { useParams } from "react-router-dom";

export default function CreateEvaluation() {
  const [criteria, setCriteria] = useState([]);
  const [scores, setScores] = useState({});
  const [comments, setComments] = useState("");
  const { placementId } = useParams();

  useEffect(() => {
    fetchCriteria();
  }, []);

  const fetchCriteria = async () => {
    try {
      const res = await axiosInstance.get("evaluation/criteria/");
      setCriteria(res.data);
    } catch (err) {
      console.log(err);
    }
  };

  const handleScoreChange = (id, value) => {
    setScores({ ...scores, [id]: value });
  };

  const submitEvaluation = async () => {
     // check all scores entered
     for (let c of criteria) {
     if (!scores[c.id]) {
          alert(`Enter score for ${c.name}`);
          return;
        }
  }
    try {
      for (let c of criteria) {
        await axiosInstance.post("evaluation/create/", {
          placement: placementId,
          criteria: c.id,
          score: scores[c.id],
          comments: comments
        });
      }

      alert("Evaluation submitted");
    } catch (err) {
      console.log(err.response?.data || err);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Evaluate Student</h2>

      {criteria.map((c) => (
        <div key={c.id}>
          <p>{c.name} (Weight: {c.weight})</p>
          <input
            type="number"
            placeholder="Score"
            onChange={(e) => handleScoreChange(c.id, e.target.value)}
          />
        </div>
      ))}

      <br />

      <textarea
        placeholder="General comments"
        onChange={(e) => setComments(e.target.value)}
      />

      <br /><br />

      <button onClick={submitEvaluation}>
        Submit Evaluation
      </button>
    </div>
  );
}