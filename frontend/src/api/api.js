// api.js
import axios from "axios";

const baseURL = import.meta.env.VITE_API_URL;

const api = axios.create({
  baseURL,
});

export const get = (url, config = {}) => {
  return api.get(url, config);
};

export const post = (url, data, config = {}) => {
  return api.post(url, data, config);
};

export const put = (url, data, config = {}) => {
  return api.put(url, data, config);
};

export const del = (url, config = {}) => {
  return api.delete(url, config);
};
