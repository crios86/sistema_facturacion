-- Crear la tabla roles
CREATE TABLE IF NOT EXISTS `roles` (
  `id` TINYINT(1) UNSIGNED NOT NULL AUTO_INCREMENT,
  `role_name` VARCHAR(20) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
);

-- Insertar los roles en la tabla roles
INSERT INTO `roles` (`id`, `role_name`) VALUES
  (1, 'master'),
  (2, 'administrador'),
  (3, 'operador');

-- Crear la tabla user con el campo role_id por defecto 1 y status
CREATE TABLE IF NOT EXISTS `user` (
  `user_id` SMALLINT(3) UNSIGNED NOT NULL AUTO_INCREMENT, -- Cambiado a user_id
  `username` VARCHAR(20) COLLATE utf8_unicode_ci NOT NULL,
  `password` CHAR(128) COLLATE utf8_unicode_ci NOT NULL,
  `fullname` VARCHAR(50) COLLATE utf8_unicode_ci NOT NULL,
  `email` VARCHAR(100) COLLATE utf8_unicode_ci NOT NULL,
  `document_type` VARCHAR(50) COLLATE utf8_unicode_ci NOT NULL,
  `identity_number` VARCHAR(50) COLLATE utf8_unicode_ci NOT NULL,
  `role_id` TINYINT(1) UNSIGNED NOT NULL DEFAULT 1,  -- Campo para el rol con valor por defecto 1
  `status` TINYINT(1) NOT NULL DEFAULT 1,  -- Campo status, por defecto 1 (activo)
  PRIMARY KEY (`user_id`),  -- Clave primaria user_id
  FOREIGN KEY (`role_id`) REFERENCES `roles`(`id`) ON DELETE SET DEFAULT
);
