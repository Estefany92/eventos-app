import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { productosApi } from "../api";

export default function ProductosPage({ user }) {
  const [productos, setProductos] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const esAdmin = user.rol === "admin";

  const cargar = () => {
    setCargando(true);
    productosApi
      .listar()
      .then((res) => setProductos(res.data))
      .catch(() => setError("No se pudo cargar el catálogo"))
      .finally(() => setCargando(false));
  };

  useEffect(cargar, []);

  const handleEliminar = async (id) => {
    if (!window.confirm("¿Eliminar este producto del catálogo?")) return;
    try {
      await productosApi.eliminar(id);
      setProductos((prev) => prev.filter((p) => p.id !== id));
    } catch (err) {
      alert(err.response?.data?.error || "No se pudo eliminar el producto");
    }
  };

  return (
    <div>
      <div className="page-header">
        <div>
          <h1>Catálogo de productos</h1>
          <p className="subtitle">
            {esAdmin
              ? "Como administrador puedes crear, editar y eliminar productos."
              : "Estos son los productos y servicios disponibles."}
          </p>
        </div>
        {esAdmin && (
          <Link to="/productos/nuevo" className="btn-primary btn-inline">
            + Nuevo producto
          </Link>
        )}
      </div>

      {error && <div className="alert-error">{error}</div>}

      {cargando ? (
        <p>Cargando...</p>
      ) : productos.length === 0 ? (
        <div className="empty-state">No hay productos en el catálogo.</div>
      ) : (
        <div className="card-grid">
          {productos.map((p) => (
            <div className="item-card" key={p.id}>
              <div className="title">{p.nombre}</div>
              <div className="meta">{p.tipo}</div>
              {p.descripcion && <div className="meta descripcion">{p.descripcion}</div>}
              <div className="precio">${p.precio}</div>

              {esAdmin && (
                <div className="card-actions">
                  <button
                    className="btn-link"
                    onClick={() => navigate(`/productos/${p.id}/editar`)}
                  >
                    Editar
                  </button>
                  <button
                    className="btn-link btn-link-danger"
                    onClick={() => handleEliminar(p.id)}
                  >
                    Eliminar
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
