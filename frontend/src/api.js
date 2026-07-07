import axios from "axios";

// Como usamos proxy en desarrollo y mismo origen en producción,
// siempre podemos usar rutas relativas "/api/...".
export const api = axios.create({
  baseURL: "/api",
  withCredentials: true, // IMPRESCINDIBLE: manda la cookie de sesión de Flask-Login
});

export const authApi = {
  login: (email, password) => api.post("/login", { email, password }),
  registro: (nombre, email, password) =>
    api.post("/registro", { nombre, email, password }),
  logout: () => api.post("/logout"),
  me: () => api.get("/me"),
};

export const eventosApi = {
  listar: () => api.get("/eventos"),
  obtener: (id) => api.get(`/eventos/${id}`),
  crear: (datos) => api.post("/eventos", datos),
  actualizar: (id, datos) => api.put(`/eventos/${id}`, datos),
  eliminar: (id) => api.delete(`/eventos/${id}`),
};

export const productosApi = {
  listar: () => api.get("/productos"),
  obtener: (id) => api.get(`/productos/${id}`),
  crear: (datos) => api.post("/productos", datos),
  actualizar: (id, datos) => api.put(`/productos/${id}`, datos),
  eliminar: (id) => api.delete(`/productos/${id}`),
};

export const reportesApi = {
  obtener: () => api.get("/reportes"),
};
