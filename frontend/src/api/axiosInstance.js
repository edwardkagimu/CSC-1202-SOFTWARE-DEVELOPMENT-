import axios from 'axios';



const axiosInstance = axios.create({
    // The base URL for your local Django development server
    baseURL: 'http://127.0.0.1:8000/', 
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    },
});

axiosInstance.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        
        // If a token exists, add it to the Authorization header
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

 // Endpoints Mapping:using axiosInstance.post(ENDPOINTS.signup, data)
 
export const ENDPOINTS = {
    signup: 'accounts/signup/',
    login: 'accounts/token/login/',
    dashboard: 'dashboard/',
    weeklyLog: 'weekly-log/',
};

export default axiosInstance;