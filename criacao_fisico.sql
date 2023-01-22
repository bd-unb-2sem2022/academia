/* dr_logico: */

CREATE TABLE turma (
    codigo INTEGER PRIMARY KEY,
    fk_modalidade_codigo INTEGER
);

CREATE TABLE profissional (
    cargo INTEGER,
    foto BYTEA,
    cref INTEGER,
    cpf CHAR(11) PRIMARY KEY
);

CREATE TABLE aluno (
    cpf INTEGER PRIMARY KEY,
    nome VARCHAR(50),
    data_nascimento DATE,
    foto BYTEA,
    fk_plano_codigo INTEGER
);

CREATE TABLE unidade (
    codigo INTEGER PRIMARY KEY,
    nome VARCHAR(50),
    endereco VARCHAR(150)
);

CREATE TABLE sala (
    codigo INTEGER PRIMARY KEY,
    numero INTEGER,
    fk_unidade_codigo INTEGER
);

CREATE TABLE equipamento (
    codigo INTEGER PRIMARY KEY,
    descricao VARCHAR(50),
    data_aquisicao DATE,
    fk_sala_codigo INTEGER
);

CREATE TABLE plano (
    codigo INTEGER PRIMARY KEY,
    nome VARCHAR(50),
    valor DECIMAL
);

CREATE TABLE ficha_treinamento (
    codigo INTEGER PRIMARY KEY,
    vencimento DATE,
    data_criacao DATE,
    fk_aluno_cpf INTEGER,
    fk_profissional_cpf CHAR(11)
);

CREATE TABLE exercicio_prescrito (
    num_repeticoes INTEGER,
    num_series INTEGER,
    tecnica VARCHAR(50),
    intervalo_descanso INTEGER,
    observacao VARCHAR(100),
    ritmo CHAR(4),
    codigo INTEGER PRIMARY KEY,
    fk_tipo_exercicio_codigo INTEGER
);

CREATE TABLE modalidade (
    codigo INTEGER PRIMARY KEY,
    nome VARCHAR(50),
    faixa_etaria VARCHAR(10)
);

CREATE TABLE tipo_exercicio (
    codigo INTEGER PRIMARY KEY,
    nome VARCHAR(50),
    fk_equipamento_codigo INTEGER
);

CREATE TABLE e_composta (
    fk_exercicio_prescrito_codigo INTEGER,
    fk_ficha_treinamento_codigo INTEGER
);

CREATE TABLE utiliza (
    fk_sala_codigo INTEGER,
    fk_turma_codigo INTEGER,
    horario_inicio TIMESTAMP,
    horario_fim TIMESTAMP,
    dia_semana VARCHAR(10)
);

CREATE TABLE conduz (
    fk_profissional_cpf CHAR(11),
    fk_turma_codigo INTEGER
);

CREATE TABLE esta_matriculado (
    fk_turma_codigo INTEGER,
    fk_aluno_cpf INTEGER
);

CREATE TABLE da_acesso (
    fk_plano_codigo INTEGER,
    fk_unidade_codigo INTEGER
);

CREATE TABLE compreende (
    fk_plano_codigo INTEGER,
    fk_modalidade_codigo INTEGER
);

CREATE TABLE trabalha_em (
    fk_profissional_cpf CHAR(11),
    fk_unidade_codigo INTEGER,
    horario_inicio TIMESTAMP,
    horario_fim TIMESTAMP,
    dia_semana VARCHAR(10)
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