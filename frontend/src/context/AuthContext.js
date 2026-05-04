import React, { createContext, useState, useEffect } from 'react';
import axiosInstance, { ENDPOINTS } from '../api/axiosInstance';
import { useNavigate } from 'react-router-dom';

// Creating Context
export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    // for checking if user is already logged in when the app loads
    useEffect(() => {
        const token = localStorage.getItem('access_token');
        if (token) {
            
            fetchUserProfile();
        } else {
            setLoading(false);
        }
    }, []);

    const fetchUserProfile = async () => {
        try {
            
            const response = await axiosInstance.get(ENDPOINTS.dashboard);
            console.log("DASHBOARD RESPONSE:", response.data);
            
            const userData = response.data.user
            if (userData){
                setUser(userData);
            }
        } catch (error) {
            console.log("Dashboard ERROR:",error);
            logout();
        } finally {
            setLoading(false);
        }
    };

    // Login Function
    const login = async (credentials) => {
        try {
            const response = await axiosInstance.post(ENDPOINTS.login, credentials);

            const data  = response.data;

            console.log("LOGIN RESPONSE:", data); //for debugging

            const token = data.access  
            
            if (!token) {
               throw new Error("No token returned from backend");
            }
            localStorage.setItem('access_token', token);  //Save token
            await fetchUserProfile();
            
            navigate('/dashboard');
        } catch (error) {
            console.error("Login failed", error);
            throw error;
        }
    };

    // Logout Function
    const logout = () => {
        localStorage.removeItem('access_token');
        setUser(null);
        navigate('/login');
    };

    return (
        <AuthContext.Provider value={{ user, login, logout, loading }}>
            {!loading && children}
        </AuthContext.Provider>
    );

    //signing up
    const signup = async (data) => {
        try {
          const response = await axiosInstance.post(ENDPOINTS.signup, data);

          console.log("SIGNUP SUCCESS:", response.data);

          return response.data;

        } catch (error) {
         console.log("SIGNUP ERROR:", error.response?.data);
         throw error;
        }
    };
    return(
        <AuthContext.Provider
        value={{user,setUser}}>{children}</AuthContext.Provider>
    )

};


