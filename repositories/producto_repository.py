from models.tablas import db, Producto

class ProductoRepository:
    
    @staticmethod
    def obtener_todos():
        """Devuelve todo el catálogo de servicios e inventario"""
        return Producto.query.all()

    @staticmethod
    def obtener_por_id(producto_id):
        """Busca un producto específico"""
        return Producto.query.get_or_404(producto_id)

    @staticmethod
    def guardar(producto):
        """Guarda un nuevo producto en la base de datos"""
        db.session.add(producto)
        db.session.commit()

    @staticmethod
    def eliminar(producto):
        """Elimina un producto del catálogo"""
        db.session.delete(producto)
        db.session.commit()