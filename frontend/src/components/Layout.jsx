import { NavLink, useNavigate } from "react-router-dom";
import { authApi } from "../api";

export default function Layout({ user, onLogout, children }) {
  const navigate = useNavigate();
  const esAdmin = user.rol === "admin";

  const handleLogout = async () => {
    await authApi.logout();
    onLogout();
    navigate("/login");
  };

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="sidebar-brand">
          <span className="logo-dot" />
          <span>Eventos App</span>
        </div>

        <nav className="sidebar-nav">
          <NavLink to="/" end className="nav-link">
            Mis eventos
          </NavLink>
          <NavLink to="/eventos/nuevo" className="nav-link">
            Crear evento
          </NavLink>
          <NavLink to="/productos" className="nav-link">
            Productos
          </NavLink>
          {esAdmin && (
            <NavLink to="/reportes" className="nav-link">
              Reportes
            </NavLink>
          )}
        </nav>

        <div className="sidebar-footer">
          <div className="user-box">
            <span className="badge-rol">{user.rol}</span>
            <span className="user-name">{user.nombre}</span>
          </div>
          <button className="btn-secondary" onClick={handleLogout}>
            Cerrar sesión
          </button>
        </div>
      </aside>

      <main className="main-content">{children}</main>
    </div>
  );
}
