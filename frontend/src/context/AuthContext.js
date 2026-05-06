import React, { createContext, useState, useEffect, useCallback } from 'react';

import axiosInstance, { ENDPOINTS } from '../api/axiosInstance';
import { useNavigate } from 'react-router-dom';

// Creating Context
export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {

    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    const navigate = useNavigate();

    // Logout Function
    const logout = useCallback(() => {
        localStorage.removeItem('access_token');
        setUser(null);
        navigate('/login');
    }, [navigate]);

    // Fetch User Profile
    const fetchUserProfile = useCallback(async () => {

        try {

            const response = await axiosInstance.get(ENDPOINTS.dashboard);

            console.log("DASHBOARD RESPONSE:", response.data);

            const userData = response.data.user;

            if (userData) {
                setUser(userData);
            }

        } catch (error) {

            console.log("Dashboard ERROR:", error);
            logout();

        } finally {

            setLoading(false);

        }

    }, [logout]);

    // Check if user is already logged in
    useEffect(() => {

        const token = localStorage.getItem('access_token');

        if (token) {
            fetchUserProfile();
        } else {
            setLoading(false);
        }

    }, [fetchUserProfile]);

    // Login Function
    const login = async (credentials) => {

        try {

            const response = await axiosInstance.post(
                ENDPOINTS.login,
                credentials
            );

            const data = response.data;

            console.log("LOGIN RESPONSE:", data);

            const token = data.access;

            if (!token) {
                throw new Error("No token returned from backend");
            }

            // Save token
            localStorage.setItem('access_token', token);

            await fetchUserProfile();

            navigate('/dashboard');

        } catch (error) {

            console.error("Login failed", error);
            throw error;

        }
    };

    // Signup Function
    const signup = async (data) => {

        try {

            const response = await axiosInstance.post(
                ENDPOINTS.signup,
                data
            );

            console.log("SIGNUP SUCCESS:", response.data);

            return response.data;

        } catch (error) {

            console.log("SIGNUP ERROR:", error.response?.data);
            throw error;

        }
    };

    return (
        <AuthContext.Provider
            value={{
                user,
                login,
                logout,
                signup,
                loading
            }}
        >
            {!loading && children}
        </AuthContext.Provider>
    );
};