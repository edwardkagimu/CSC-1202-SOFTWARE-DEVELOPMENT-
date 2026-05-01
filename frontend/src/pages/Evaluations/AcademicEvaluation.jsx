import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axiosInstance from "../../api/axiosInstance";

export default function AcademicEvaluation() {

  const { placementId } = useParams();

  const [workplaceComment, setWorkplaceComment] = useState("");

  const [technicalSkills, setTechnicalSkills] = useState("");
  const [reportQuality, setReportQuality] = useState("");
  const [problemSolving, setProblemSolving] = useState("");
  const [presentation, setPresentation] = useState("");

  const [comments, setComments] = useState("");

  useEffect(() => {
    fetchWorkplaceEvaluation();
  }, []);

  const fetchWorkplaceEvaluation = async () => {
    try {
      const res = await axiosInstance.get(`workplace-comment/${placementId}/`);

      setWorkplaceComment(res.data.comments);

    } catch (err) {
      console.log(err.response?.data || err);
    }
  };

  const submitEvaluation = async () => {
    try {

      await axiosInstance.post(
        `academic-evaluation/${placementId}/`,
        {
          technical_skills: technicalSkills,
          report_quality: reportQuality,
          problem_solving: problemSolving,
          presentation: presentation,
          comments: comments
        }
      );

      alert("Academic Evaluation Submitted");

    } catch (err) {
      console.log(err.response?.data || err);
      alert("Error submitting evaluation");
    }
  };

  return (
    <div style={{ padding: "20px" }}>

      <h2>Academic Evaluation</h2>

      <hr />

      <h3>Workplace Supervisor Comment</h3>

      <p>{workplaceComment}</p>
    
      <hr />

      <input
        type="number"
        placeholder="Technical Skills"
        onChange={(e) => setTechnicalSkills(e.target.value)}
      />

      <br /><br />

      <input
        type="number"
        placeholder="Report Quality"
        onChange={(e) => setReportQuality(e.target.value)}
      />

      <br /><br />

      <input
        type="number"
        placeholder="Problem Solving"
        onChange={(e) => setProblemSolving(e.target.value)}
      />

      <br /><br />

      <input
        type="number"
        placeholder="Presentation"
        onChange={(e) => setPresentation(e.target.value)}
      />

      <br /><br />

      <textarea
        placeholder="Academic Supervisor Comments"
        onChange={(e) => setComments(e.target.value)}
      />

      <br /><br />

      <button onClick={submitEvaluation}>
        Submit Evaluation
      </button>

    </div>
  );
}