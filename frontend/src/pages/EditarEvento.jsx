import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { eventosApi, productosApi } from "../api";

const ESTADOS = ["pendiente", "confirmado", "cancelado", "finalizado"];

export default function EditarEvento() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [fecha, setFecha] = useState("");
  const [hora, setHora] = useState("");
  const [direccion, setDireccion] = useState("");
  const [estado, setEstado] = useState("pendiente");
  const [productos, setProductos] = useState([]);
  const [seleccionados, setSeleccionados] = useState({});
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [cargando, setCargando] = useState(true);

  useEffect(() => {
    Promise.all([eventosApi.obtener(id), productosApi.listar()])
      .then(([evRes, prRes]) => {
        const evento = evRes.data;
        setFecha(evento.fecha || "");
        setHora(evento.hora || "");
        setDireccion(evento.direccion || "");
        setEstado(evento.estado || "pendiente");
        setProductos(prRes.data);

        const iniciales = {};
        (evento.detalles || []).forEach((d) => {
          iniciales[d.producto_id] = { cantidad: d.cantidad || 1, horas: d.horas || 1 };
        });
        setSeleccionados(iniciales);
      })
      .catch(() => setError("No se pudo cargar el evento"))
      .finally(() => setCargando(false));
  }, [id]);

  const toggleProducto = (pid) => {
    setSeleccionados((prev) => {
      const copia = { ...prev };
      if (copia[pid]) {
        delete copia[pid];
      } else {
        copia[pid] = { cantidad: 1, horas: 1 };
      }
      return copia;
    });
  };

  const actualizarCampo = (pid, campo, valor) => {
    setSeleccionados((prev) => ({
      ...prev,
      [pid]: { ...prev[pid], [campo]: Number(valor) || 1 },
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    const detalles = Object.entries(seleccionados).map(([producto_id, datos]) => ({
      producto_id: Number(producto_id),
      cantidad: datos.cantidad,
      horas: datos.horas,
    }));

    setLoading(true);
    try {
      await eventosApi.actualizar(id, { fecha, hora, direccion, estado, detalles });
      navigate("/");
    } catch (err) {
      setError(err.response?.data?.error || "No se pudo actualizar el evento");
    } finally {
      setLoading(false);
    }
  };

  if (cargando) return <p>Cargando...</p>;

  return (
    <div>
      <div className="page-header">
        <div>
          <h1>Editar evento</h1>
          <p className="subtitle">Solo los administradores pueden editar eventos.</p>
        </div>
      </div>

      {error && <div className="alert-error">{error}</div>}

      <form onSubmit={handleSubmit} className="form-card">
        <div className="field-row">
          <div className="field">
            <label>Fecha</label>
            <input type="date" value={fecha} onChange={(e) => setFecha(e.target.value)} required />
          </div>
          <div className="field">
            <label>Hora</label>
            <input type="time" value={hora} onChange={(e) => setHora(e.target.value)} />
          </div>
        </div>

        <div className="field-row">
          <div className="field" style={{ flex: 2 }}>
            <label>Dirección</label>
            <input
              type="text"
              value={direccion}
              onChange={(e) => setDireccion(e.target.value)}
              required
            />
          </div>
          <div className="field">
            <label>Estado</label>
            <select value={estado} onChange={(e) => setEstado(e.target.value)}>
              {ESTADOS.map((es) => (
                <option key={es} value={es}>
                  {es}
                </option>
              ))}
            </select>
          </div>
        </div>

        <h3>Productos y servicios</h3>
        <div className="producto-select-list">
          {productos.map((p) => {
            const activo = Boolean(seleccionados[p.id]);
            return (
              <div key={p.id} className={`producto-select-item ${activo ? "activo" : ""}`}>
                <label className="producto-checkbox">
                  <input
                    type="checkbox"
                    checked={activo}
                    onChange={() => toggleProducto(p.id)}
                  />
                  <span>
                    {p.nombre} <span className="meta">— ${p.precio} / {p.tipo}</span>
                  </span>
                </label>

                {activo && (
                  <div className="producto-select-inputs">
                    <label>
                      Cantidad
                      <input
                        type="number"
                        min="1"
                        value={seleccionados[p.id].cantidad}
                        onChange={(e) => actualizarCampo(p.id, "cantidad", e.target.value)}
                      />
                    </label>
                    <label>
                      Horas
                      <input
                        type="number"
                        min="1"
                        value={seleccionados[p.id].horas}
                        onChange={(e) => actualizarCampo(p.id, "horas", e.target.value)}
                      />
                    </label>
                  </div>
                )}
              </div>
            );
          })}
        </div>

        <div className="form-actions">
          <button type="button" className="btn-secondary" onClick={() => navigate("/")}>
            Cancelar
          </button>
          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? "Guardando..." : "Guardar cambios"}
          </button>
        </div>
      </form>
    </div>
  );
}
