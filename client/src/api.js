import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:5050',
});

export const useApi = (client) => {
  apiClient.interceptors.request.use(async (config) => {
    const token = await client.getAccessTokenSilently();
    config.headers.Authorization = `Bearer ${token}`;
    return config;
  });

  return apiClient;
};

export default useApi;