DELIMITER $$
CREATE FUNCTION DocumentosEntregados(fecha_inicio DATE, fecha_fin DATE)
RETURNS INT DETERMINISTIC
BEGIN
    DECLARE cantidad INT;

    SELECT COUNT(*) INTO cantidad
    FROM entrega
    WHERE Fecha_entrega BETWEEN fecha_inicio AND fecha_fin;

    RETURN cantidad;
END$$
DELIMITER ;

-- Ejemplo de uso:
-- SELECT DocumentosEntregados('2023-01-01', '2023-12-31') AS Entregados;
