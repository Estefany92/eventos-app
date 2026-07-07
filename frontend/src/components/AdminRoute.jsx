import { Navigate } from "react-router-dom";

export default function AdminRoute({ user, children }) {
  if (user.rol !== "admin") {
    return <Navigate to="/" replace />;
  }
  return children;
}
