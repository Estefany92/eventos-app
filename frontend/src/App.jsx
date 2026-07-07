import { useEffect, useState } from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { authApi } from "./api";
import Login from "./pages/Login";
import Registro from "./pages/Registro";
import EventosPage from "./pages/EventosPage";
import CrearEvento from "./pages/CrearEvento";
import EditarEvento from "./pages/EditarEvento";
import ProductosPage from "./pages/ProductosPage";
import CrearProducto from "./pages/CrearProducto";
import EditarProducto from "./pages/EditarProducto";
import Reportes from "./pages/Reportes";
import Layout from "./components/Layout";
import AdminRoute from "./components/AdminRoute";

export default function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Al cargar la app, revisamos si ya hay una sesión activa (cookie de Flask-Login)
    authApi
      .me()
      .then((res) => setUser(res.data))
      .catch(() => setUser(null))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div className="loading-screen">Cargando...</div>;
  }

  if (!user) {
    return (
      <Routes>
        <Route path="/login" element={<Login onAuth={setUser} />} />
        <Route path="/registro" element={<Registro onAuth={setUser} />} />
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    );
  }

  return (
    <Layout user={user} onLogout={() => setUser(null)}>
      <Routes>
        <Route path="/" element={<EventosPage user={user} />} />
        <Route path="/eventos/nuevo" element={<CrearEvento />} />
        <Route
          path="/eventos/:id/editar"
          element={
            <AdminRoute user={user}>
              <EditarEvento />
            </AdminRoute>
          }
        />
        <Route path="/productos" element={<ProductosPage user={user} />} />
        <Route
          path="/productos/nuevo"
          element={
            <AdminRoute user={user}>
              <CrearProducto />
            </AdminRoute>
          }
        />
        <Route
          path="/productos/:id/editar"
          element={
            <AdminRoute user={user}>
              <EditarProducto />
            </AdminRoute>
          }
        />
        <Route
          path="/reportes"
          element={
            <AdminRoute user={user}>
              <Reportes />
            </AdminRoute>
          }
        />
        <Route path="/login" element={<Navigate to="/" replace />} />
        <Route path="/registro" element={<Navigate to="/" replace />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Layout>
  );
}
