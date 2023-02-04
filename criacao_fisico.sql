/* Cria as tabelas */

CREATE TABLE turma (
    codigo SERIAL UNIQUE NOT NULL PRIMARY KEY,
    fk_modalidade_codigo INTEGER NOT NULL
);

CREATE TABLE profissional (
    cargo VARCHAR(30) NOT NULL,
    foto BYTEA,
    cref VARCHAR(15) NOT NULL,
    cpf CHAR(11) UNIQUE NOT NULL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL
);

CREATE TABLE aluno (
    cpf CHAR(11) UNIQUE NOT NULL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    data_nascimento DATE NOT NULL,
    foto BYTEA,
    fk_plano_codigo INTEGER NOT NULL
);

CREATE TABLE unidade (
    codigo SERIAL UNIQUE NOT NULL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    endereco VARCHAR(150) NOT NULL
);

CREATE TABLE sala (
    codigo SERIAL UNIQUE NOT NULL PRIMARY KEY,
    numero INTEGER NOT NULL,
    fk_unidade_codigo INTEGER NOT NULL
);

CREATE TABLE equipamento (
    codigo SERIAL UNIQUE NOT NULL PRIMARY KEY,
    descricao VARCHAR(50) NOT NULL,
    data_aquisicao DATE NOT NULL,
    fk_sala_codigo INTEGER NOT NULL
);

CREATE TABLE plano (
    codigo SERIAL UNIQUE NOT NULL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    valor DECIMAL NOT NULL
);

CREATE TABLE ficha_treinamento (
    codigo SERIAL UNIQUE NOT NULL PRIMARY KEY,
    vencimento DATE NOT NULL,
    data_criacao DATE NOT NULL,
    fk_aluno_cpf CHAR(11) NOT NULL,
    fk_profissional_cpf CHAR(11) NOT NULL
);

CREATE TABLE exercicio_prescrito (
    num_repeticoes INTEGER NOT NULL,
    num_series INTEGER NOT NULL,
    tecnica VARCHAR(50),
    intervalo_descanso INTEGER NOT NULL,
    observacao VARCHAR(100),
    ritmo CHAR(4) NOT NULL,
    codigo SERIAL UNIQUE NOT NULL PRIMARY KEY,
    fk_tipo_exercicio_codigo INTEGER NOT NULL
);

CREATE TABLE modalidade (
    codigo SERIAL UNIQUE NOT NULL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    faixa_etaria VARCHAR(10) NOT NULL
);

CREATE TABLE tipo_exercicio (
    codigo SERIAL UNIQUE NOT NULL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    fk_equipamento_codigo INTEGER
);

CREATE TABLE e_composta (
    fk_exercicio_prescrito_codigo INTEGER NOT NULL,
    fk_ficha_treinamento_codigo INTEGER NOT NULL
);

CREATE TABLE utiliza (
    fk_sala_codigo INTEGER NOT NULL,
    fk_turma_codigo INTEGER NOT NULL,
    horario_inicio TIME NOT NULL,
    horario_fim TIME NOT NULL,
    dia_semana VARCHAR(10) NOT NULL
);

CREATE TABLE conduz (
    fk_profissional_cpf CHAR(11) NOT NULL,
    fk_turma_codigo INTEGER NOT NULL
);

CREATE TABLE esta_matriculado (
    fk_turma_codigo INTEGER NOT NULL,
    fk_aluno_cpf CHAR(11) NOT NULL
);

CREATE TABLE da_acesso (
    fk_plano_codigo INTEGER NOT NULL,
    fk_unidade_codigo INTEGER NOT NULL
);

CREATE TABLE compreende (
    fk_plano_codigo INTEGER NOT NULL,
    fk_modalidade_codigo INTEGER NOT NULL
);

CREATE TABLE trabalha_em (
    fk_profissional_cpf CHAR(11) NOT NULL,
    fk_unidade_codigo INTEGER NOT NULL,
    horario_inicio TIME NOT NULL,
    horario_fim TIME NOT NULL,
    dia_semana VARCHAR(10) NOT NULL
);
 
ALTER TABLE turma ADD CONSTRAINT FK_turma_2
    FOREIGN KEY (fk_modalidade_codigo)
    REFERENCES modalidade (codigo)
    ON DELETE CASCADE;
 
ALTER TABLE aluno ADD CONSTRAINT FK_aluno_2
    FOREIGN KEY (fk_plano_codigo)
    REFERENCES plano (codigo)
    ON DELETE CASCADE;
 
ALTER TABLE sala ADD CONSTRAINT FK_sala_2
    FOREIGN KEY (fk_unidade_codigo)
    REFERENCES unidade (codigo)
    ON DELETE RESTRICT;
 
ALTER TABLE equipamento ADD CONSTRAINT FK_equipamento_2
    FOREIGN KEY (fk_sala_codigo)
    REFERENCES sala (codigo)
    ON DELETE CASCADE;
 
ALTER TABLE ficha_treinamento ADD CONSTRAINT FK_ficha_treinamento_2
    FOREIGN KEY (fk_aluno_cpf)
    REFERENCES aluno (cpf)
    ON DELETE CASCADE;
 
ALTER TABLE ficha_treinamento ADD CONSTRAINT FK_ficha_treinamento_3
    FOREIGN KEY (fk_profissional_cpf)
    REFERENCES profissional (cpf)
    ON DELETE CASCADE;
 
ALTER TABLE exercicio_prescrito ADD CONSTRAINT FK_exercicio_prescrito_2
    FOREIGN KEY (fk_tipo_exercicio_codigo)
    REFERENCES tipo_exercicio (codigo)
    ON DELETE CASCADE;
 
ALTER TABLE tipo_exercicio ADD CONSTRAINT FK_tipo_exercicio_2
    FOREIGN KEY (fk_equipamento_codigo)
    REFERENCES equipamento (codigo)
    ON DELETE CASCADE;
 
ALTER TABLE e_composta ADD CONSTRAINT FK_e_composta_1
    FOREIGN KEY (fk_exercicio_prescrito_codigo)
    REFERENCES exercicio_prescrito (codigo)
    ON DELETE RESTRICT;
 
ALTER TABLE e_composta ADD CONSTRAINT FK_e_composta_2
    FOREIGN KEY (fk_ficha_treinamento_codigo)
    REFERENCES ficha_treinamento (codigo)
    ON DELETE SET NULL;
 
ALTER TABLE utiliza ADD CONSTRAINT FK_utiliza_1
    FOREIGN KEY (fk_sala_codigo)
    REFERENCES sala (codigo)
    ON DELETE RESTRICT;
 
ALTER TABLE utiliza ADD CONSTRAINT FK_utiliza_2
    FOREIGN KEY (fk_turma_codigo)
    REFERENCES turma (codigo)
    ON DELETE SET NULL;
 
ALTER TABLE conduz ADD CONSTRAINT FK_conduz_1
    FOREIGN KEY (fk_profissional_cpf)
    REFERENCES profissional (cpf)
    ON DELETE RESTRICT;
 
ALTER TABLE conduz ADD CONSTRAINT FK_conduz_2
    FOREIGN KEY (fk_turma_codigo)
    REFERENCES turma (codigo)
    ON DELETE SET NULL;
 
ALTER TABLE esta_matriculado ADD CONSTRAINT FK_esta_matriculado_1
    FOREIGN KEY (fk_turma_codigo)
    REFERENCES turma (codigo)
    ON DELETE SET NULL;
 
ALTER TABLE esta_matriculado ADD CONSTRAINT FK_esta_matriculado_2
    FOREIGN KEY (fk_aluno_cpf)
    REFERENCES aluno (cpf)
    ON DELETE SET NULL;
 
ALTER TABLE da_acesso ADD CONSTRAINT FK_da_acesso_1
    FOREIGN KEY (fk_plano_codigo)
    REFERENCES plano (codigo)
    ON DELETE RESTRICT;
 
ALTER TABLE da_acesso ADD CONSTRAINT FK_da_acesso_2
    FOREIGN KEY (fk_unidade_codigo)
    REFERENCES unidade (codigo)
    ON DELETE RESTRICT;
 
ALTER TABLE compreende ADD CONSTRAINT FK_compreende_1
    FOREIGN KEY (fk_plano_codigo)
    REFERENCES plano (codigo)
    ON DELETE RESTRICT;
 
ALTER TABLE compreende ADD CONSTRAINT FK_compreende_2
    FOREIGN KEY (fk_modalidade_codigo)
    REFERENCES modalidade (codigo)
    ON DELETE RESTRICT;
 
ALTER TABLE trabalha_em ADD CONSTRAINT FK_trabalha_em_1
    FOREIGN KEY (fk_profissional_cpf)
    REFERENCES profissional (cpf)
    ON DELETE RESTRICT;
 
ALTER TABLE trabalha_em ADD CONSTRAINT FK_trabalha_em_2
    FOREIGN KEY (fk_unidade_codigo)
    REFERENCES unidade (codigo)
    ON DELETE RESTRICT;

/* Popula as tabelas */

INSERT INTO 
    modalidade 
        (nome, faixa_etaria)
VALUES  
        ('Natação','Infantil'),
        ('Natação', 'Bebê'),
        ('Natação', 'Adulto'),
        ('Musculação', 'Adulto'),
        ('Ioga', 'Adulto'),
        ('Ballet', 'Infantil'),
        ('Ballet', 'Adulto'),
        ('Judô', 'Infantil'),
        ('Judô', 'Adulto'),
        ('Spinning', 'Adulto'),
        ('Abdominal', 'Adulto'),
        ('Corrida', 'Adulto'),
        ('Pilates', 'Adulto'),
        ('Circo', 'Infantil'),
        ('Hidroginástica', 'Adulto');

INSERT INTO
    turma
    (fk_modalidade_codigo)
VALUES
    (1),
    (4),
    (9),
    (10),
    (12);


INSERT INTO
    plano
        (nome, valor)
VALUES
        ('Acqua trimestral', 300.00),
        ('Acqua semestral', 250.00),
        ('Acqua anual', 210.00),
        ('Musculação trimestral', 250.00),
        ('Musculação semestral', 170.00),
        ('Musculação anual', 140.00),
        ('Platinum semestral', 450.00),
        ('Platinum anual', 399.00),
        ('Diamond semestral', 519.00),
        ('Diamond anual', 499.00);


INSERT INTO
    unidade
        (nome,endereco)
VALUES
        ('Asa Sul', 'Shopping Pier 21, Conjunto 32 - Asa Sul, Brasília - DF, 70200-002'),
        ('Asa Norte I', 'Quadra B, Asa Norte Entrequadra Norte 110/111 - Brasília, DF, 70753-400'),
        ('Asa Norte II', 'SGAN 911 Parte Academia - Asa Norte, Brasília - DF, 70790-110'),
        ('Lago Sul', 'SHIS QI 11 bloco f - Lago Sul, Brasília - DF, 71625-550'),
        ('Águas Claras', 'R. das Pitangueiras, 1 - Águas Claras, Brasília - DF, 71938-540');


INSERT INTO
    sala
        (numero,fk_unidade_codigo)
VALUES
        (1,1),
        (2,1),
        (3,1),
        (4,1),
        (5,1),
        (1,2),
        (2,2),
        (3,2),
        (1,3),
        (2,3),
        (3,3),
        (4,3),
        (5,3),
        (1,4),
        (2,4),
        (3,4),
        (1,5),
        (2,5),
        (3,5);


INSERT INTO
    equipamento
        (descricao, data_aquisicao, fk_sala_codigo)
VALUES
        ('Cadeira abdutora', '2019-09-14', 1),
        ('Cadeira adutora', '2019-09-14', 1),
        ('Cadeira extensora', '2019-09-14', 1),
        ('Cadeira flexora', '2019-09-14', 1),
        ('Leg Press', '2021-03-23', 1),
        ('Graviton', '2021-03-23', 2),
        ('Pack Deck', '2021-03-23', 2),
        ('Panturrilha sentada', '2021-03-23', 1), 
        ('Puxador', '2022-08-17', 2),
        ('Supino', '2022-08-17', 2),
        ('Bicicleta ergométrica', '2022-08-17', 3),  
        ('Esteira', '2022-08-17', 3),
        ('Elíptico', '2022-08-17', 3),
        ('Remo Indoor', '2022-08-17', 3),
        ('Simulador de escada', '2022-08-17', 3),
        ('Cadillac', '2022-08-17', 4),
        ('Step Chair', '2022-08-17', 4), 
        ('Ladder Barrel', '2022-08-17', 4);

INSERT INTO
    tipo_exercicio
        (nome, fk_equipamento_codigo)
VALUES
        ('Adução de quadril', 2 ),
        ('Abdução de quadril', 1),
        ('Extensão de joelho', 3),
        ('Extensão de joelho', 5),
        ('Flexão de joelho', 4),
        ('Abdominal', 6),
        ('Extensão de cotovelo', 10),
        ('Corrida', 12),
        ('Corrida', 13),
        ('Caminhada', 12),
        ('Remada', 14),
        ('Pedala', 11);


/* TO DO inserir foto como bytea */

INSERT INTO
    aluno
        (cpf, nome, data_nascimento, fk_plano_codigo)
VALUES
        ('12043814982', 'Alberto Silva Franco', '2022-03-11', 1),
        ('08932475252', 'Júlia Nunes Alves', '1989-09-14', 6),
        ('09287454235', 'João da Silva Antunes', '1995-01-12', 8),
        ('25843758345', 'Fábio Lima Algures', '2010-12-03', 2),
        ('75983752955', 'Natália Rodrigues da Cunha', '1978-04-15', 9);

/* TO DO inserir foto como bytea */

INSERT INTO
    profissional
        (cargo, cref, cpf, nome)
VALUES
        ('Instrutor', '1248DF', '09821374012', 'Marcos Pereira Romero'),
        ('Instrutor', '89183GO', '92648927643', 'Jane Costa Ribeiro'),
        ('Instrutor', '102848SP', '24375782902', 'Flávio Assunção Oliveira'),
        ('Coordenador', '190348MG', '12948742392', 'Pamela Borges Ramos'),
        ('Coordenador', '923784DF', '23470174091', 'Rafael Ribeiro Pereira');

INSERT INTO
    ficha_treinamento
        (vencimento, data_criacao, fk_aluno_cpf, fk_profissional_cpf)
VALUES
        ('2023-01-29', '2022-11-29','12043814982','09821374012'),
        ('2023-02-02', '2022-12-02','08932475252','92648927643'),
        ('2023-02-09', '2022-12-09','08932475252','92648927643'),
        ('2023-02-14', '2022-12-14','75983752955','92648927643'),
        ('2023-03-01', '2023-01-01','75983752955','92648927643');

INSERT INTO
    exercicio_prescrito
        (num_repeticoes, num_series, tecnica, intervalo_descanso, observacao, ritmo, fk_tipo_exercicio_codigo)
VALUES
		(10,3, '-', 120, '-', '3030', 3),
        (15,2,'pausa e descanso',90,'-', '2121',4),
        (10,3,'isometria',120,'apoiar coluna com almofada','3232',1),
        (8,2,'biset',120,'-','2020',2),
        (8,2,'biset',120,'combinar com abdução', '3131',5);

INSERT INTO
    e_composta
        (fk_exercicio_prescrito_codigo, fk_ficha_treinamento_codigo)
VALUES
        (1,1),
        (2,1),
        (3,1),
        (4,2),
        (5,2);

INSERT INTO
    esta_matriculado
        (fk_turma_codigo, fk_aluno_cpf)
VALUES
        (2,'12043814982'),
        (3,'08932475252'),
        (4,'09287454235'),
        (1,'25843758345'),
        (2,'75983752955');

INSERT INTO
    conduz
        (fk_profissional_cpf,fk_turma_codigo)
VALUES
        ('92648927643',1),
        ('09821374012',1),
        ('24375782902',2),
        ('12948742392',3), 
        ('23470174091',3);

INSERT INTO
    utiliza
        (fk_sala_codigo, fk_turma_codigo, horario_inicio, horario_fim, dia_semana)
VALUES
        (1,2,'08:00:00','20:00:00','segunda'),
        (1,2,'08:00:00','20:00:00','quarta'),
        (1,2,'08:00:00','18:00:00','sexta'),
        (2,1,'16:00:00','17:00:00','terça'),
        (2,1,'16:00:00','17:00:00','quinta');

INSERT INTO
    trabalha_em
        (fk_profissional_cpf, fk_unidade_codigo, horario_inicio, horario_fim, dia_semana)
VALUES
        ('09821374012',1,'08:00:00','12:00:00','terça'),
        ('09821374012',1,'08:00:00','12:00:00','quinta'),
        ('92648927643',2,'10:00:00','14:00:00','segunda'),
        ('92648927643',2,'10:00:00','14:00:00','quarta'),
        ('92648927643',2,'10:00:00','14:00:00','sexta');

INSERT INTO
    compreende
        (fk_plano_codigo, fk_modalidade_codigo)
VALUES
        (1,1),
        (1,2),
        (1,3),
        (6,4),
        (9,4);

INSERT INTO
    da_acesso
        (fk_plano_codigo,fk_unidade_codigo)
VALUES
        (1,3),
        (6,1),
        (6,2),
        (9,1),
        (9,2);


/* ############################

Cria view nome_aluno_modalidade_unidade, que permite visualizar
em uma única relação, a partir dos nomes, as conexões entre
alunos, turmas, modalidades e unidades.

#############################*/

CREATE VIEW nome_aluno_modalidade_unidade as
	SELECT tb5.aluno as aluno, tb5.turma_codigo as turma_codigo, tb5.modalidade as modalidade, unidade.nome as unidade_nome, tb5.cpf
	FROM unidade
	INNER JOIN
		(SELECT tb4.aluno as aluno, tb4.modalidade as modalidade, tb4.turma_codigo as turma_codigo, tb4.cpf, sala.fk_unidade_codigo as unidade_codigo
		FROM sala
		INNER JOIN
			(SELECT DISTINCT tb3.aluno as aluno, tb3.modalidade as modalidade, tb3.turma_codigo as turma_codigo, tb3.cpf, utiliza.fk_sala_codigo as sala_codigo
			FROM utiliza
			INNER JOIN
				(SELECT tb2.nome as aluno, modalidade.nome as modalidade, tb2.cpf, tb2.turma_codigo as turma_codigo
				FROM modalidade
				INNER JOIN
					(SELECT tb1.nome, tb1.cpf, turma.fk_modalidade_codigo, tb1.fk_turma_codigo as turma_codigo
					FROM turma
					INNER JOIN
						(SELECT aluno.nome, aluno.cpf, fk_turma_codigo
						FROM aluno 
						INNER JOIN esta_matriculado 
						ON fk_aluno_cpf = aluno.cpf) as tb1
					ON fk_turma_codigo = turma.codigo) as tb2
				ON fk_modalidade_codigo = modalidade.codigo) as tb3
			ON tb3.turma_codigo = utiliza.fk_turma_codigo) as tb4
		ON tb4.sala_codigo = sala.codigo) as tb5
	ON tb5.unidade_codigo = unidade.codigo
	ORDER BY turma_codigo;

/* ############################

Cria procedure criar_turma, que simultaneamente inserir dados
nas tabelas turma, utiliza e conduz.

#############################*/



CREATE PROCEDURE criar_turma(
	fk_modalidade_codigo INTEGER,
	fk_profissional_cpf CHAR(11),
	fk_sala_codigo INTEGER,
	horario_inicio TIME,
	horario_fim TIME,
	dia_semana VARCHAR(10))	
LANGUAGE plpgsql
AS $$
DECLARE
	turma_codigo INTEGER;
BEGIN
	INSERT INTO
		turma
		(fk_modalidade_codigo)
	VALUES
		(fk_modalidade_codigo)
	RETURNING
		turma.codigo INTO turma_codigo;
	
	INSERT INTO
		conduz
		(fk_profissional_cpf, fk_turma_codigo)
	VALUES
		(fk_profissional_cpf, turma_codigo);
		
	INSERT INTO
		utiliza
		(fk_sala_codigo, fk_turma_codigo, horario_inicio, horario_fim, dia_semana)
	VALUES
		(fk_sala_codigo, turma_codigo, horario_inicio, horario_fim, dia_semana);
END;$$


/* ############################

Chama a procedure criar_turma, como exemplo.

#############################*/

CALL criar_turma(1, '09821374012', 1, '09:00:00', '10:00:00','quinta');



/*############################# importar bytea 
File file = new File("C:\Users\andmi\Downloads\young-bearded-man-with-striped-shirt.jpg");
FileInputStream fis = new FileInputStream(file);
PreparedStatement ps = conn.prepareStatement("INSERT INTO aluno VALUES (?, ?, ?, ?, ?)");
ps.setBinaryStream(4, fis, file.length());
ps.executeUpdate();
ps.close();
fis.close();

"C:\Users\andmi\Downloads\young-bearded-man-with-striped-shirt.jpg"

*/
       

    

