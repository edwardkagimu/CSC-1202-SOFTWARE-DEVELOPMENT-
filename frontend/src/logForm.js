import React, { useState } from 'react';
import axios from 'axios';

const LogSubmission = ({ placementId }) => {
    const [log, setLog] = useState({ week_number: 1, activities: '' });

    // Add a loading state to disable the button during API calls
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();

        // 1. Basic Validation
        if (!log.activities.trim()) {
            alert("Please enter your activities before submitting.");
            return;
        }

        setLoading(true); // Start loading

        try {
            const response = await axios.post('/api/logs/', {
                ...log,
                week_number: parseInt(log.week_number), // Ensure it's a number
                placement: placementId,
                state: 'SUBMITTED' 
            });
            alert("Log submitted successfully!");
            
            // Optional: Clear the activities field after success
            setLog({ ...log, activities: '' });
        } catch (error) {
            console.error("Submission failed", error);
            alert("Failed to submit log. Please try again.");
        } finally {
            setLoading(false); // Stop loading regardless of success/fail
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <h3>Submit Weekly Log</h3>
            <input 
                type="number" 
                value={log.week_number}
                onChange={(e) => setLog({...log, week_number: e.target.value})} 
                placeholder="Week Number" 
                min="1"
            />
            <textarea 
                value={log.activities}
                onChange={(e) => setLog({...log, activities: e.target.value})} 
                placeholder="Describe your activities..."
                required
            />
            {/* 2. Disable button while loading */}
            <button type="submit" disabled={loading}>
                {loading ? "Submitting..." : "Submit to Supervisor"}
            </button>
        </form>
    );
};

export default LogSubmission;