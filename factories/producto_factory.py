from models.tablas import Producto

class ProductoFactory:
    
    @staticmethod
    def crear(nombre, descripcion, precio, tipo):
        """
        Fábrica inteligente: Aplica reglas de negocio específicas 
        dependiendo del tipo de servicio de la empresa de eventos.
        """
        descripcion_procesada = descripcion

        # Reglas específicas por categoría
        if tipo == 'comida':
            # Ejemplo: Forzamos una etiqueta para el catering
            descripcion_procesada = f"[Alimentos/Bebidas] {descripcion}"
            
        elif tipo == 'maquinaria':
            # Ejemplo: Advertencia de manipulación para equipos
            descripcion_procesada = f"[Requiere instalación técnica] {descripcion}"
            
        elif tipo == 'animacion':
            # Ejemplo: Etiqueta para talento humano
            descripcion_procesada = f"[Personal/Talento] {descripcion}"

        # Creamos y retornamos la instancia configurada
        nuevo_producto = Producto(
            nombre=nombre,
            descripcion=descripcion_procesada,
            precio=precio,
            tipo=tipo
        )
        
        return nuevo_producto