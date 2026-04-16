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
            setUser(response.data.user); 
        } catch (error) {
            logout();
        } finally {
            setLoading(false);
        }
    };

    // Login Function
    const login = async (credentials) => {
        try {
            const response = await axiosInstance.post(ENDPOINTS.login, credentials);
            const { auth_token, user_data } = response.data;

            localStorage.setItem('access_token', auth_token);
            
            setUser(user_data);
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
};