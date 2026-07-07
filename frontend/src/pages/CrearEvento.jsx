import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { eventosApi, productosApi } from "../api";

export default function CrearEvento() {
  const [fecha, setFecha] = useState("");
  const [hora, setHora] = useState("");
  const [direccion, setDireccion] = useState("");
  const [productos, setProductos] = useState([]);
  const [seleccionados, setSeleccionados] = useState({}); // { productoId: { cantidad, horas } }
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    productosApi.listar().then((res) => setProductos(res.data));
  }, []);

  const toggleProducto = (id) => {
    setSeleccionados((prev) => {
      const copia = { ...prev };
      if (copia[id]) {
        delete copia[id];
      } else {
        copia[id] = { cantidad: 1, horas: 1 };
      }
      return copia;
    });
  };

  const actualizarCampo = (id, campo, valor) => {
    setSeleccionados((prev) => ({
      ...prev,
      [id]: { ...prev[id], [campo]: Number(valor) || 1 },
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!fecha || !direccion) {
      setError("Fecha y dirección son obligatorias");
      return;
    }

    const detalles = Object.entries(seleccionados).map(([producto_id, datos]) => ({
      producto_id: Number(producto_id),
      cantidad: datos.cantidad,
      horas: datos.horas,
    }));

    setLoading(true);
    try {
      await eventosApi.crear({ fecha, hora, direccion, detalles });
      navigate("/");
    } catch (err) {
      setError(err.response?.data?.error || "No se pudo crear el evento");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="page-header">
        <div>
          <h1>Crear evento</h1>
          <p className="subtitle">Completa los datos y elige los productos que necesitas.</p>
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

        <div className="field">
          <label>Dirección</label>
          <input
            type="text"
            value={direccion}
            onChange={(e) => setDireccion(e.target.value)}
            placeholder="Dirección donde será el evento"
            required
          />
        </div>

        <h3>Productos y servicios</h3>
        {productos.length === 0 ? (
          <div className="empty-state">No hay productos en el catálogo todavía.</div>
        ) : (
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
        )}

        <div className="form-actions">
          <button type="button" className="btn-secondary" onClick={() => navigate("/")}>
            Cancelar
          </button>
          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? "Creando..." : "Crear evento"}
          </button>
        </div>
      </form>
    </div>
  );
}
