import { useEffect, useState, useCallback } from "react";
import { useParams } from "react-router-dom";
import axiosInstance from "../../api/axiosInstance";
import "../../App.css";
export default function AcademicEvaluation() {

  const { placementId } = useParams();

  const [workplaceComment, setWorkplaceComment] = useState("");

  const [technicalSkills, setTechnicalSkills] = useState("");
  const [reportQuality, setReportQuality] = useState("");
  const [problemSolving, setProblemSolving] = useState("");
  const [presentation, setPresentation] = useState("");

  const [comments, setComments] = useState("");

const fetchWorkplaceEvaluation = useCallback(async () => {
  try {
    const res = await axiosInstance.get(`workplace-comment/${placementId}/`);

    setWorkplaceComment(res.data.comments);

  } catch (err) {
    console.log(err.response?.data || err);
  }
}, [placementId]);

  useEffect(() => {
    fetchWorkplaceEvaluation();
  }, [fetchWorkplaceEvaluation]);
  
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
    <div className="placement-container">
       <div className="placement-card">

       <h2 className="mylogs-title" >Academic Evaluation</h2>

       <hr />

       <h3>Workplace Supervisor Comment</h3>

       <p>{workplaceComment}</p>
    
       <hr />

       <input
         className="form-input"
         type="number"
         placeholder="Technical Skills"
         onChange={(e) => setTechnicalSkills(e.target.value)}
       />

       <br /><br />

       <input
         className="form-input"
         type="number"
         placeholder="Report Quality"
         onChange={(e) => setReportQuality(e.target.value)}
       />

       <br /><br />

       <input
         className="form-input"
         type="number"
         placeholder="Problem Solving"
         onChange={(e) => setProblemSolving(e.target.value)}
       />

       <br /><br />

       <input
         className="form-input"
         type="number"
         placeholder="Presentation"
         onChange={(e) => setPresentation(e.target.value)}
       />

       <br /><br />

       <textarea
         className="form-input"
         placeholder="Academic Supervisor Comments"
         onChange={(e) => setComments(e.target.value)}
       />

       <br /><br />

       <button className="primary-btn" onClick={submitEvaluation}>
         Submit Evaluation
       </button>
      </div>
    </div>
  );
}