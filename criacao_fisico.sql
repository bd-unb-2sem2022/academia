

CREATE TABLE turma (
    codigo SERIAL UNIQUE NOT NULL PRIMARY KEY,
    fk_modalidade_codigo INTEGER NOT NULL
);

CREATE TABLE profissional (
    cargo INTEGER NOT NULL,
    foto BYTEA,
    cref VARCHAR(15) NOT NULL,
    cpf CHAR(11) UNIQUE NOT NULL PRIMARY KEY
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
    fk_aluno_cpf INTEGER NOT NULL,
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
    fk_equipamento_codigo INTEGER NOT NULL
);

CREATE TABLE e_composta (
    fk_exercicio_prescrito_codigo INTEGER NOT NULL,
    fk_ficha_treinamento_codigo INTEGER NOT NULL
);

CREATE TABLE utiliza (
    fk_sala_codigo INTEGER NOT NULL,
    fk_turma_codigo INTEGER NOT NULL,
    horario_inicio TIMESTAMP NOT NULL,
    horario_fim TIMESTAMP NOT NULL,
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
    horario_inicio TIMESTAMP NOT NULL,
    horario_fim TIMESTAMP NOT NULL,
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