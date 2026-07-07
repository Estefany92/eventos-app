import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { eventosApi } from "../api";

export default function EventosPage({ user }) {
  const [eventos, setEventos] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const esAdmin = user.rol === "admin";

  const cargar = () => {
    setCargando(true);
    eventosApi
      .listar()
      .then((res) => setEventos(res.data))
      .catch(() => setError("No se pudieron cargar los eventos"))
      .finally(() => setCargando(false));
  };

  useEffect(cargar, []);

  const handleEliminar = async (id) => {
    if (!window.confirm("¿Eliminar este evento? Esta acción no se puede deshacer.")) {
      return;
    }
    try {
      await eventosApi.eliminar(id);
      setEventos((prev) => prev.filter((e) => e.id !== id));
    } catch (err) {
      alert(err.response?.data?.error || "No se pudo eliminar el evento");
    }
  };

  return (
    <div>
      <div className="page-header">
        <div>
          <h1>{esAdmin ? "Todos los eventos" : "Mis eventos"}</h1>
          <p className="subtitle">
            {esAdmin
              ? "Como administrador puedes ver, editar y eliminar cualquier evento."
              : "Estos son los eventos que has creado."}
          </p>
        </div>
        <Link to="/eventos/nuevo" className="btn-primary btn-inline">
          + Crear evento
        </Link>
      </div>

      {error && <div className="alert-error">{error}</div>}

      {cargando ? (
        <p>Cargando...</p>
      ) : eventos.length === 0 ? (
        <div className="empty-state">Todavía no hay eventos creados.</div>
      ) : (
        <div className="card-grid">
          {eventos.map((e) => (
            <div className="item-card" key={e.id}>
              <div className="title">{e.direccion}</div>
              <div className="meta">
                {e.fecha} {e.hora ? `— ${e.hora}` : ""}
              </div>
              <span className={`status-pill status-${e.estado}`}>{e.estado}</span>

              {e.detalles && e.detalles.length > 0 && (
                <div className="detalle-lista">
                  {e.detalles.length} producto(s) asociado(s)
                </div>
              )}

              {esAdmin && (
                <div className="card-actions">
                  <button
                    className="btn-link"
                    onClick={() => navigate(`/eventos/${e.id}/editar`)}
                  >
                    Editar
                  </button>
                  <button
                    className="btn-link btn-link-danger"
                    onClick={() => handleEliminar(e.id)}
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
