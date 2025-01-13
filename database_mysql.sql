CREATE TABLE `Telewizor`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `przekatna_cal` INT NOT NULL,
    `typ_wyswietlacza` VARCHAR(255) NOT NULL,
    `rozdzielczosc` BIGINT NOT NULL,
    `smart_TV` BOOLEAN NOT NULL
);
CREATE TABLE `Komputer`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `procesor` BIGINT UNSIGNED NOT NULL,
    `pamiec_RAM` BIGINT UNSIGNED UNSIGNED NOT NULL,
    `pojemnosc_dysku` INT NOT NULL
);
CREATE TABLE `Monitor`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `przekatna_cal` INT NOT NULL,
    `odswiezanie_Hz` INT NOT NULL,
    `rozdzielczość` BIGINT NOT NULL,
    `typ_wyswietlacza` VARCHAR(255) NOT NULL,
    `glosniki_` BOOLEAN NOT NULL,
    `proporcje_ekranu` VARCHAR(255) NOT NULL
);
CREATE TABLE `Procesor`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `liczba_rdzeni` BIGINT NOT NULL,
    `taktowanie` BIGINT NOT NULL,
    `rodzaj_gniazda` VARCHAR(255) NOT NULL
);
CREATE TABLE `RAM`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `typ_pamieci` VARCHAR(255) NOT NULL,
    `pojemnosc_GB` INT NOT NULL,
    `taktowanie_MHz` BIGINT NOT NULL
);
CREATE TABLE `Listaproduktow`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `kategoria` VARCHAR(255) NOT NULL,
    `marka` VARCHAR(255) NOT NULL,
    `model` VARCHAR(255) NOT NULL
);
CREATE TABLE `Listasklepow`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `id_produktu` BIGINT UNSIGNED NOT NULL,
    `nazwa` VARCHAR(255) NOT NULL
);
CREATE TABLE `Listaopinii`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `id_produktu` BIGINT UNSIGNED UNSIGNED NOT NULL,
    `opinia` VARCHAR(255) NOT NULL,
    `data` DATETIME NOT NULL
);
CREATE TABLE `Historiacen`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `id_sklepu_z_danym_produktem` BIGINT UNSIGNED NOT NULL,
    `cena` DECIMAL(8, 2) NOT NULL,
    `data` DATE NOT NULL
);
ALTER TABLE
    `Komputer` ADD CONSTRAINT `komputer_id_foreign` FOREIGN KEY(`id`) REFERENCES `Listaproduktow`(`id`);
ALTER TABLE
    `Monitor` ADD CONSTRAINT `monitor_id_foreign` FOREIGN KEY(`id`) REFERENCES `Listaproduktow`(`id`);
ALTER TABLE
    `Telewizor` ADD CONSTRAINT `telewizor_id_foreign` FOREIGN KEY(`id`) REFERENCES `Listaproduktow`(`id`);
ALTER TABLE
    `Procesor` ADD CONSTRAINT `procesor_id_foreign` FOREIGN KEY(`id`) REFERENCES `Listaproduktow`(`id`);
ALTER TABLE
    `RAM` ADD CONSTRAINT `ram_id_foreign` FOREIGN KEY(`id`) REFERENCES `Listaproduktow`(`id`);


ALTER TABLE
    `Komputer` ADD CONSTRAINT `komputer_pamiec_ram_foreign` FOREIGN KEY(`pamiec_RAM`) REFERENCES `RAM`(`id`);
ALTER TABLE
    `Komputer` ADD CONSTRAINT `komputer_procesor_foreign` FOREIGN KEY(`procesor`) REFERENCES `Procesor`(`id`);
ALTER TABLE
    `Historiacen` ADD CONSTRAINT `historia_cen_id_sklepu_z_danym_produktem_foreign` FOREIGN KEY(`id_sklepu_z_danym_produktem`) REFERENCES `Listasklepow`(`id`);
ALTER TABLE
    `Listaopinii` ADD CONSTRAINT `lista_opinii_id_produktu_foreign` FOREIGN KEY(`id_produktu`) REFERENCES `Listaproduktow`(`id`);
ALTER TABLE
    `Listasklepow` ADD CONSTRAINT `lista_sklepow_id_produktu_foreign` FOREIGN KEY(`id_produktu`) REFERENCES `Listaproduktow`(`id`);
