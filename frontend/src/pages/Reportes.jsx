import { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";
import { reportesApi } from "../api";

export default function Reportes() {
  const [datos, setDatos] = useState(null);
  const [error, setError] = useState("");
  const [cargando, setCargando] = useState(true);

  useEffect(() => {
    reportesApi
      .obtener()
      .then((res) => setDatos(res.data))
      .catch(() => setError("No se pudieron cargar los reportes"))
      .finally(() => setCargando(false));
  }, []);

  if (cargando) return <p>Cargando reportes...</p>;
  if (error) return <div className="alert-error">{error}</div>;
  if (!datos) return null;

  const ingresosData = Object.entries(datos.ingresos_por_estado || {}).map(
    ([estado, total]) => ({ estado, total })
  );

  return (
    <div>
      <div className="page-header">
        <div>
          <h1>Reportes y analítica</h1>
          <p className="subtitle">Visión general del negocio (solo administradores).</p>
        </div>
      </div>

      <h2>Ingresos por estado de evento</h2>
      {ingresosData.length === 0 ? (
        <div className="empty-state">Aún no hay datos de ingresos.</div>
      ) : (
        <div className="chart-card">
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={ingresosData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey="estado" />
              <YAxis />
              <Tooltip formatter={(value) => `$${value}`} />
              <Bar dataKey="total" fill="#4f46e5" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      <h2>Top 5 productos más alquilados</h2>
      {!datos.top_productos || datos.top_productos.length === 0 ? (
        <div className="empty-state">Aún no hay datos suficientes.</div>
      ) : (
        <div className="chart-card">
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={datos.top_productos} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis type="number" allowDecimals={false} />
              <YAxis type="category" dataKey="nombre" width={140} />
              <Tooltip />
              <Bar dataKey="cantidad" fill="#16a34a" radius={[0, 6, 6, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      <h2>Demanda por mes</h2>
      {!datos.demanda_por_mes || datos.demanda_por_mes.length === 0 ? (
        <div className="empty-state">Aún no hay eventos suficientes para esta tabla.</div>
      ) : (
        <table className="data-table">
          <thead>
            <tr>
              <th>Mes</th>
              <th>Cantidad de eventos</th>
            </tr>
          </thead>
          <tbody>
            {datos.demanda_por_mes.map((fila) => (
              <tr key={fila.mes}>
                <td>{fila.mes}</td>
                <td>{fila.cantidad}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
