// src/axios.js
import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/v1/',
  timeout: 10000, // Timeout de 10 segundos
});

export default axiosInstance;
