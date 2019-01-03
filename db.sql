CREATE TABLE tb_userdata (
	id_userdata INT NULL DEFAULT unique_rowid(),
	first_name STRING NULL,
	last_name STRING NULL,
	location STRING NULL,
	email STRING NULL,
	created_at TIMESTAMP WITH TIME ZONE NULL,
	CONSTRAINT tb_userdata_pk PRIMARY KEY (id_userdata ASC),
	UNIQUE INDEX tb_userdata_un (email ASC),
	FAMILY "primary" (id_userdata, first_name, last_name, location, email, created_at)
);

CREATE TABLE tb_project_app (
	id_project_app INT NOT NULL DEFAULT unique_rowid(),
	nm_project_app STRING NULL,
	nm_project_port STRING NULL,
	id_userdata INT NULL,
	CONSTRAINT tb_project_app_pk PRIMARY KEY (id_project_app ASC),
	CONSTRAINT tb_project_app_tb_userdata_fk FOREIGN KEY (id_userdata) REFERENCES tb_userdata (id_userdata) ON DELETE CASCADE ON UPDATE CASCADE,
	INDEX tb_project_app_auto_index_tb_project_app_tb_userdata_fk (id_userdata ASC),
	FAMILY "primary" (id_project_app, nm_project_app, nm_project_port, id_userdata)
);

CREATE TABLE tb_user (
	id_user INT NOT NULL DEFAULT unique_rowid(),
	id_userdata INT NOT NULL,
	username STRING NULL,
	password STRING NULL,
	CONSTRAINT tb_user_pk PRIMARY KEY (id_user ASC),
	UNIQUE INDEX tb_user_un (username ASC),
	CONSTRAINT tb_user_tb_userdata_fk FOREIGN KEY (id_userdata) REFERENCES tb_userdata (id_userdata) ON DELETE CASCADE ON UPDATE CASCADE,
	INDEX tb_user_auto_index_tb_user_tb_userdata_fk (id_userdata ASC),
	FAMILY "primary" (id_user, id_userdata, username, password)
);

INSERT INTO tb_userdata (id_userdata, first_name, last_name, location, email, created_at) VALUES
	(414218411381424129, 'mongkey', 'king', 'alamat', 'meongbego@gmail.com', NULL);

INSERT INTO tb_project_app (id_project_app, nm_project_app, nm_project_port, id_userdata) VALUES
	(414299650840035329, 'bless', '6969', 414218411381424129);

INSERT INTO tb_user (id_user, id_userdata, username, password) VALUES
	(414218746653540353, 414218411381424129, 'mongkey', '$pbkdf2-sha256$29000$e./d21trbQ2hlPI.h/C.Fw$L612tSbsa1pDyrrmKpEBnG0whsK4TZ.uVh7D9Z/U4.M');
