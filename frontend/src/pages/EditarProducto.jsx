import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { productosApi } from "../api";

const TIPOS = ["comida", "maquinaria", "animacion", "mobiliario", "otro"];

export default function EditarProducto() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [nombre, setNombre] = useState("");
  const [tipo, setTipo] = useState("comida");
  const [precio, setPrecio] = useState("");
  const [descripcion, setDescripcion] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [cargando, setCargando] = useState(true);

  useEffect(() => {
    productosApi
      .obtener(id)
      .then((res) => {
        const p = res.data;
        setNombre(p.nombre || "");
        setTipo(p.tipo || "comida");
        setPrecio(p.precio ?? "");
        setDescripcion(p.descripcion || "");
      })
      .catch(() => setError("No se pudo cargar el producto"))
      .finally(() => setCargando(false));
  }, [id]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await productosApi.actualizar(id, {
        nombre,
        tipo,
        precio: Number(precio),
        descripcion,
      });
      navigate("/productos");
    } catch (err) {
      setError(err.response?.data?.error || "No se pudo actualizar el producto");
    } finally {
      setLoading(false);
    }
  };

  if (cargando) return <p>Cargando...</p>;

  return (
    <div>
      <div className="page-header">
        <div>
          <h1>Editar producto</h1>
        </div>
      </div>

      {error && <div className="alert-error">{error}</div>}

      <form onSubmit={handleSubmit} className="form-card">
        <div className="field">
          <label>Nombre</label>
          <input type="text" value={nombre} onChange={(e) => setNombre(e.target.value)} required />
        </div>

        <div className="field-row">
          <div className="field">
            <label>Tipo</label>
            <select value={tipo} onChange={(e) => setTipo(e.target.value)}>
              {TIPOS.map((t) => (
                <option key={t} value={t}>
                  {t}
                </option>
              ))}
            </select>
          </div>
          <div className="field">
            <label>Precio</label>
            <input
              type="number"
              min="0"
              step="0.01"
              value={precio}
              onChange={(e) => setPrecio(e.target.value)}
              required
            />
          </div>
        </div>

        <div className="field">
          <label>Descripción</label>
          <textarea rows={3} value={descripcion} onChange={(e) => setDescripcion(e.target.value)} />
        </div>

        <div className="form-actions">
          <button type="button" className="btn-secondary" onClick={() => navigate("/productos")}>
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
