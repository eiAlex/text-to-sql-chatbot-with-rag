#!/usr/bin/env python3
"""
Script para criar o banco de dados SQLite da empresa XPTO teste.
Este script cria tabelas, dados de exemplo e metadados (comentários) para uma empresa fictícia.
"""
import sqlite3
import os

def create_xpto_database():
    """Cria o banco de dados da empresa XPTO com tabelas, dados e metadados."""
    
    # Criar diretório data se não existir
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Conectar ao banco de dados
    conn = sqlite3.connect('data/xpto_empresa.db')
    cursor = conn.cursor()
    
    # Criar tabelas de metadados primeiro
    create_metadata_tables(cursor)
    
    # Criar tabelas principais
    create_business_tables(cursor)
    
    # Inserir metadados (comentários)
    insert_table_comments(cursor)
    insert_column_comments(cursor)
    
    # Inserir dados de exemplo
    insert_sample_data(cursor)
    
    # Confirmar mudanças e fechar conexão
    conn.commit()
    conn.close()
    
    print("✅ Banco de dados da empresa XPTO criado com sucesso!")
    print("📍 Localização: data/xpto_empresa.db")
    print("📋 Inclui metadados completos (comentários de tabelas e colunas)")

def create_metadata_tables(cursor):
    """Cria as tabelas de metadados para comentários."""
    
    # Tabela para comentários de tabelas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS table_comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        table_name TEXT UNIQUE NOT NULL,
        comment TEXT NOT NULL,
        business_purpose TEXT,
        data_owner TEXT,
        created_date DATE DEFAULT CURRENT_DATE
    )
    ''')
    
    # Tabela para comentários de colunas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS column_comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        table_name TEXT NOT NULL,
        column_name TEXT NOT NULL,
        comment TEXT NOT NULL,
        business_meaning TEXT,
        data_type_description TEXT,
        constraints_description TEXT,
        example_values TEXT,
        UNIQUE(table_name, column_name)
    )
    ''')
    
    print("✅ Tabelas de metadados criadas!")

def create_business_tables(cursor):
    """Cria as tabelas principais do negócio."""
    
    # Tabela de Funcionários
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS funcionarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        cargo TEXT NOT NULL,
        departamento TEXT NOT NULL,
        salario DECIMAL(10,2) NOT NULL,
        data_admissao DATE NOT NULL,
        telefone TEXT,
        endereco TEXT,
        ativo BOOLEAN DEFAULT 1,
        supervisor_id INTEGER,
        FOREIGN KEY (supervisor_id) REFERENCES funcionarios (id)
    )
    ''')
    
    # Tabela de Departamentos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS departamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE NOT NULL,
        descricao TEXT,
        gerente_id INTEGER,
        orcamento DECIMAL(12,2),
        localizacao TEXT,
        centro_custo TEXT,
        FOREIGN KEY (gerente_id) REFERENCES funcionarios (id)
    )
    ''')
    
    # Tabela de Projetos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS projetos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        descricao TEXT,
        cliente_id INTEGER,
        departamento_id INTEGER,
        gerente_projeto_id INTEGER,
        data_inicio DATE NOT NULL,
        data_fim_prevista DATE,
        data_fim_real DATE,
        orcamento DECIMAL(12,2),
        custo_real DECIMAL(12,2),
        prioridade TEXT CHECK(prioridade IN ('Baixa', 'Média', 'Alta', 'Crítica')),
        status TEXT CHECK(status IN ('Planejamento', 'Em Andamento', 'Pausado', 'Concluído', 'Cancelado')),
        FOREIGN KEY (cliente_id) REFERENCES clientes (id),
        FOREIGN KEY (departamento_id) REFERENCES departamentos (id),
        FOREIGN KEY (gerente_projeto_id) REFERENCES funcionarios (id)
    )
    ''')
    
    # Tabela de Clientes
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        telefone TEXT,
        endereco TEXT,
        cidade TEXT,
        estado TEXT,
        cep TEXT,
        cnpj TEXT UNIQUE,
        inscricao_estadual TEXT,
        tipo_cliente TEXT CHECK(tipo_cliente IN ('Pessoa Física', 'Pessoa Jurídica')),
        segmento_mercado TEXT,
        data_cadastro DATE NOT NULL,
        limite_credito DECIMAL(10,2),
        ativo BOOLEAN DEFAULT 1
    )
    ''')
    
    # Tabela de Vendas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS vendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero_pedido TEXT UNIQUE NOT NULL,
        cliente_id INTEGER NOT NULL,
        funcionario_id INTEGER NOT NULL,
        data_venda DATE NOT NULL,
        data_entrega_prevista DATE,
        data_entrega_real DATE,
        valor_bruto DECIMAL(10,2) NOT NULL,
        desconto DECIMAL(5,2) DEFAULT 0,
        valor_total DECIMAL(10,2) NOT NULL,
        descricao TEXT,
        forma_pagamento TEXT,
        condicoes_pagamento TEXT,
        status TEXT CHECK(status IN ('Orçamento', 'Aprovado', 'Faturado', 'Entregue', 'Pago', 'Cancelado')),
        observacoes TEXT,
        FOREIGN KEY (cliente_id) REFERENCES clientes (id),
        FOREIGN KEY (funcionario_id) REFERENCES funcionarios (id)
    )
    ''')
    
    # Tabela de Produtos/Serviços
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo_produto TEXT UNIQUE NOT NULL,
        nome TEXT NOT NULL,
        descricao TEXT,
        categoria TEXT,
        subcategoria TEXT,
        preco_venda DECIMAL(10,2) NOT NULL,
        custo_unitario DECIMAL(10,2),
        margem_lucro DECIMAL(5,2),
        estoque_atual INTEGER DEFAULT 0,
        estoque_minimo INTEGER DEFAULT 0,
        estoque_maximo INTEGER,
        unidade_medida TEXT,
        fornecedor_principal TEXT,
        localizacao_estoque TEXT,
        ativo BOOLEAN DEFAULT 1
    )
    ''')
    
    # Tabela de Itens de Venda
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS itens_venda (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        venda_id INTEGER NOT NULL,
        produto_id INTEGER NOT NULL,
        quantidade INTEGER NOT NULL,
        preco_unitario DECIMAL(10,2) NOT NULL,
        desconto_item DECIMAL(5,2) DEFAULT 0,
        valor_total_item DECIMAL(10,2) NOT NULL,
        observacoes TEXT,
        FOREIGN KEY (venda_id) REFERENCES vendas (id),
        FOREIGN KEY (produto_id) REFERENCES produtos (id)
    )
    ''')
    
    # Tabela de Fornecedores
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS fornecedores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        razao_social TEXT,
        cnpj TEXT UNIQUE NOT NULL,
        inscricao_estadual TEXT,
        email TEXT,
        telefone TEXT,
        endereco TEXT,
        cidade TEXT,
        estado TEXT,
        cep TEXT,
        contato_principal TEXT,
        prazo_entrega_medio INTEGER,
        condicoes_pagamento TEXT,
        avaliacao DECIMAL(3,1),
        ativo BOOLEAN DEFAULT 1
    )
    ''')
    
    print("✅ Tabelas principais criadas!")

def insert_table_comments(cursor):
    """Insere comentários das tabelas."""
    
    table_comments = [
        ('funcionarios', 'Cadastro completo dos colaboradores da empresa XPTO', 'Armazena informações pessoais, profissionais e organizacionais dos funcionários', 'RH'),
        ('departamentos', 'Estrutura organizacional da empresa', 'Define a hierarquia e organização departamental da empresa', 'RH'),
        ('projetos', 'Controle e acompanhamento de projetos', 'Gerencia todos os projetos executados pela empresa, incluindo cronogramas e orçamentos', 'PMO'),
        ('clientes', 'Base de clientes da empresa', 'Cadastro completo de clientes pessoa física e jurídica com informações comerciais', 'Vendas'),
        ('vendas', 'Registro de todas as transações comerciais', 'Controla o ciclo completo de vendas desde orçamento até pagamento', 'Vendas'),
        ('produtos', 'Catálogo de produtos e serviços', 'Cadastro completo de produtos e serviços oferecidos pela empresa', 'Comercial'),
        ('itens_venda', 'Detalhamento dos produtos/serviços vendidos', 'Relaciona produtos específicos a cada venda realizada', 'Vendas'),
        ('fornecedores', 'Cadastro de fornecedores e parceiros', 'Base de fornecedores com avaliações e condições comerciais', 'Compras'),
        ('table_comments', 'Metadados - Comentários das tabelas', 'Armazena descrições e propósitos de cada tabela do sistema', 'TI'),
        ('column_comments', 'Metadados - Comentários das colunas', 'Armazena descrições detalhadas de cada campo das tabelas', 'TI')
    ]
    
    cursor.executemany('''
        INSERT INTO table_comments (table_name, comment, business_purpose, data_owner)
        VALUES (?, ?, ?, ?)
    ''', table_comments)
    
    print("✅ Comentários das tabelas inseridos!")

def insert_column_comments(cursor):
    """Insere comentários das colunas."""
    
    column_comments = [
        # Funcionários
        ('funcionarios', 'id', 'Identificador único do funcionário', 'Chave primária auto-incrementável', 'Número inteiro sequencial', 'Único, não nulo', '1, 2, 3...'),
        ('funcionarios', 'nome', 'Nome completo do colaborador', 'Identificação pessoal oficial', 'Texto até 255 caracteres', 'Obrigatório', 'João Silva Santos'),
        ('funcionarios', 'email', 'Endereço de email corporativo', 'Email para comunicação oficial', 'Texto formato email', 'Único, obrigatório', 'joao.silva@xpto.com.br'),
        ('funcionarios', 'cargo', 'Função/posição na empresa', 'Define responsabilidades e hierarquia', 'Texto até 100 caracteres', 'Obrigatório', 'Analista, Gerente, Diretor'),
        ('funcionarios', 'departamento', 'Setor de alocação do funcionário', 'Divisão organizacional', 'Texto até 100 caracteres', 'Obrigatório', 'TI, Vendas, RH'),
        ('funcionarios', 'salario', 'Remuneração mensal bruta', 'Valor em reais da remuneração', 'Decimal (10,2)', 'Obrigatório, > 0', '5000.00, 8500.50'),
        ('funcionarios', 'data_admissao', 'Data de contratação', 'Início do vínculo empregatício', 'Data no formato YYYY-MM-DD', 'Obrigatório', '2023-01-15'),
        ('funcionarios', 'telefone', 'Número de telefone de contato', 'Comunicação direta com funcionário', 'Texto formato telefone', 'Opcional', '(11) 99999-1234'),
        ('funcionarios', 'endereco', 'Endereço residencial completo', 'Informação para correspondência', 'Texto até 200 caracteres', 'Opcional', 'Rua A, 123 - São Paulo'),
        ('funcionarios', 'ativo', 'Status do funcionário na empresa', 'Indica se funcionário está ativo', 'Booleano (0/1)', 'Padrão: 1 (ativo)', '1=ativo, 0=inativo'),
        ('funcionarios', 'supervisor_id', 'Referência ao supervisor direto', 'Hierarquia organizacional', 'Referência a funcionarios.id', 'Opcional', '5, 12, NULL'),
        
        # Departamentos
        ('departamentos', 'id', 'Identificador único do departamento', 'Chave primária auto-incrementável', 'Número inteiro sequencial', 'Único, não nulo', '1, 2, 3...'),
        ('departamentos', 'nome', 'Nome oficial do departamento', 'Denominação organizacional', 'Texto até 100 caracteres', 'Único, obrigatório', 'Recursos Humanos'),
        ('departamentos', 'descricao', 'Descrição das atividades', 'Função e responsabilidades', 'Texto até 500 caracteres', 'Opcional', 'Gestão de pessoas...'),
        ('departamentos', 'gerente_id', 'Funcionário responsável pelo depto', 'Liderança departamental', 'Referência a funcionarios.id', 'Opcional', '3, 7, NULL'),
        ('departamentos', 'orcamento', 'Orçamento anual do departamento', 'Verba disponível em reais', 'Decimal (12,2)', 'Opcional, >= 0', '500000.00'),
        ('departamentos', 'localizacao', 'Localização física do depto', 'Endereço ou andar do escritório', 'Texto até 200 caracteres', 'Opcional', '2º andar - Bloco A'),
        ('departamentos', 'centro_custo', 'Código do centro de custo', 'Controle financeiro contábil', 'Texto até 20 caracteres', 'Opcional', 'CC-001, CC-RH'),
        
        # Projetos  
        ('projetos', 'id', 'Identificador único do projeto', 'Chave primária auto-incrementável', 'Número inteiro sequencial', 'Único, não nulo', '1, 2, 3...'),
        ('projetos', 'nome', 'Nome identificador do projeto', 'Título do projeto', 'Texto até 150 caracteres', 'Obrigatório', 'Sistema ERP Cliente X'),
        ('projetos', 'descricao', 'Descrição detalhada do escopo', 'Objetivos e entregáveis', 'Texto até 1000 caracteres', 'Opcional', 'Implementação completa...'),
        ('projetos', 'cliente_id', 'Cliente proprietário do projeto', 'Relacionamento comercial', 'Referência a clientes.id', 'Opcional', '1, 5, NULL'),
        ('projetos', 'departamento_id', 'Departamento executor', 'Responsabilidade organizacional', 'Referência a departamentos.id', 'Opcional', '1, 3'),
        ('projetos', 'gerente_projeto_id', 'Gerente responsável', 'Liderança do projeto', 'Referência a funcionarios.id', 'Opcional', '2, 8'),
        ('projetos', 'data_inicio', 'Data de início do projeto', 'Marco inicial', 'Data no formato YYYY-MM-DD', 'Obrigatório', '2023-01-15'),
        ('projetos', 'data_fim_prevista', 'Prazo planejado de conclusão', 'Meta de entrega', 'Data no formato YYYY-MM-DD', 'Opcional', '2023-12-31'),
        ('projetos', 'data_fim_real', 'Data efetiva de conclusão', 'Entrega real', 'Data no formato YYYY-MM-DD', 'Opcional', '2024-01-10'),
        ('projetos', 'orcamento', 'Orçamento aprovado em reais', 'Valor planejado', 'Decimal (12,2)', 'Opcional, >= 0', '150000.00'),
        ('projetos', 'custo_real', 'Custo efetivamente gasto', 'Valor realizado', 'Decimal (12,2)', 'Opcional, >= 0', '148500.75'),
        ('projetos', 'prioridade', 'Nível de prioridade do projeto', 'Classificação de importância', 'Texto controlado', 'Baixa/Média/Alta/Crítica', 'Alta, Crítica'),
        ('projetos', 'status', 'Situação atual do projeto', 'Estado do ciclo de vida', 'Texto controlado', 'Status predefinidos', 'Em Andamento'),
        
        # Clientes
        ('clientes', 'id', 'Identificador único do cliente', 'Chave primária auto-incrementável', 'Número inteiro sequencial', 'Único, não nulo', '1, 2, 3...'),
        ('clientes', 'nome', 'Nome ou razão social', 'Identificação do cliente', 'Texto até 200 caracteres', 'Obrigatório', 'TechCorp Ltda'),
        ('clientes', 'email', 'Email principal de contato', 'Comunicação comercial', 'Texto formato email', 'Único, obrigatório', 'contato@techcorp.com'),
        ('clientes', 'telefone', 'Telefone de contato', 'Comunicação direta', 'Texto formato telefone', 'Opcional', '(11) 3333-1001'),
        ('clientes', 'endereco', 'Endereço completo', 'Localização física', 'Texto até 300 caracteres', 'Opcional', 'Av. Paulista, 1000'),
        ('clientes', 'cidade', 'Cidade do cliente', 'Localização municipal', 'Texto até 100 caracteres', 'Opcional', 'São Paulo'),
        ('clientes', 'estado', 'Estado/UF do cliente', 'Localização estadual', 'Texto 2 caracteres', 'Opcional', 'SP, RJ, MG'),
        ('clientes', 'cep', 'Código de endereçamento postal', 'Localização por CEP', 'Texto formato CEP', 'Opcional', '01451-000'),
        ('clientes', 'cnpj', 'CNPJ ou CPF do cliente', 'Documento de identificação', 'Texto formato documento', 'Único, opcional', '12.345.678/0001-90'),
        ('clientes', 'inscricao_estadual', 'Inscrição estadual', 'Documento estadual PJ', 'Texto até 20 caracteres', 'Opcional', '123.456.789.012'),
        ('clientes', 'tipo_cliente', 'Classificação pessoa física/jurídica', 'Tipo de documento', 'Texto controlado', 'PF ou PJ apenas', 'Pessoa Jurídica'),
        ('clientes', 'segmento_mercado', 'Setor de atuação do cliente', 'Classificação comercial', 'Texto até 100 caracteres', 'Opcional', 'Tecnologia, Varejo'),
        ('clientes', 'data_cadastro', 'Data de registro do cliente', 'Histórico do relacionamento', 'Data no formato YYYY-MM-DD', 'Obrigatório', '2023-01-15'),
        ('clientes', 'limite_credito', 'Limite de crédito em reais', 'Valor máximo para vendas', 'Decimal (10,2)', 'Opcional, >= 0', '50000.00'),
        ('clientes', 'ativo', 'Status ativo/inativo', 'Indica se cliente está ativo', 'Booleano (0/1)', 'Padrão: 1 (ativo)', '1=ativo, 0=inativo'),
        
        # Produtos
        ('produtos', 'codigo_produto', 'Código único do produto', 'Identificador SKU interno', 'Texto até 50 caracteres', 'Único, obrigatório', 'PROD-001, SRV-045'),
        ('produtos', 'preco_venda', 'Preço de venda ao cliente', 'Valor comercial em reais', 'Decimal (10,2)', 'Obrigatório, > 0', '1500.00, 25000.00'),
        ('produtos', 'margem_lucro', 'Percentual de margem de lucro', 'Margem sobre o custo', 'Decimal (5,2)', 'Opcional, 0-100', '30.5, 45.0'),
        ('produtos', 'unidade_medida', 'Unidade de medida do produto', 'Como é comercializado', 'Texto até 20 caracteres', 'Opcional', 'UN, KG, M2, HR')
    ]
    
    cursor.executemany('''
        INSERT INTO column_comments (table_name, column_name, comment, business_meaning, data_type_description, constraints_description, example_values)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', column_comments)
    
    print("✅ Comentários das colunas inseridos!")

def insert_sample_data(cursor):
    """Insere dados de exemplo nas tabelas."""
    
    # Dados de Departamentos
    departamentos_data = [
        ('Tecnologia da Informação', 'Desenvolvimento de software e infraestrutura de TI', None, 500000.00, 'São Paulo - SP', 'CC-TI-001'),
        ('Recursos Humanos', 'Gestão de pessoas, recrutamento e desenvolvimento', None, 200000.00, 'São Paulo - SP', 'CC-RH-001'),
        ('Vendas', 'Comercialização de produtos e serviços', None, 800000.00, 'São Paulo - SP', 'CC-VD-001'),
        ('Marketing', 'Promoção da marca e marketing digital', None, 300000.00, 'Rio de Janeiro - RJ', 'CC-MK-001'),
        ('Financeiro', 'Gestão financeira, contábil e controladoria', None, 150000.00, 'São Paulo - SP', 'CC-FN-001'),
        ('Operações', 'Logística, operações e qualidade', None, 600000.00, 'Belo Horizonte - MG', 'CC-OP-001')
    ]
    
    cursor.executemany('''
    INSERT INTO departamentos (nome, descricao, gerente_id, orcamento, localizacao, centro_custo)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', departamentos_data)
    
    # Dados de Funcionários
    funcionarios_data = [
        ('Maria Silva Santos', 'maria.silva@xpto.com.br', 'Diretora de TI', 'Tecnologia da Informação', 15000.00, '2020-01-15', '(11) 99999-1001', 'Rua das Flores, 123, São Paulo - SP', 1, None),
        ('João Pedro Oliveira', 'joao.oliveira@xpto.com.br', 'Gerente de RH', 'Recursos Humanos', 8000.00, '2019-03-10', '(11) 99999-1002', 'Av. Paulista, 456, São Paulo - SP', 1, None),
        ('Ana Carolina Costa', 'ana.costa@xpto.com.br', 'Diretora de Vendas', 'Vendas', 12000.00, '2018-06-20', '(11) 99999-1003', 'Rua Augusta, 789, São Paulo - SP', 1, None),
        ('Carlos Eduardo Lima', 'carlos.lima@xpto.com.br', 'Desenvolvedor Senior', 'Tecnologia da Informação', 7500.00, '2021-02-01', '(11) 99999-1004', 'Rua da Consolação, 321, São Paulo - SP', 1, 1),
        ('Fernanda Almeida', 'fernanda.almeida@xpto.com.br', 'Analista de Marketing', 'Marketing', 5500.00, '2022-04-15', '(21) 99999-2001', 'Av. Copacabana, 654, Rio de Janeiro - RJ', 1, None),
        ('Roberto Santos', 'roberto.santos@xpto.com.br', 'Contador', 'Financeiro', 6000.00, '2020-08-30', '(11) 99999-1005', 'Rua do Comércio, 987, São Paulo - SP', 1, None),
        ('Luciana Ferreira', 'luciana.ferreira@xpto.com.br', 'Consultora de Vendas', 'Vendas', 4500.00, '2023-01-10', '(11) 99999-1006', 'Rua XV de Novembro, 147, São Paulo - SP', 1, 3),
        ('Pedro Henrique Silva', 'pedro.silva@xpto.com.br', 'Desenvolvedor Junior', 'Tecnologia da Informação', 4000.00, '2023-07-01', '(11) 99999-1007', 'Rua Bela Vista, 258, São Paulo - SP', 1, 4),
        ('Juliana Rodrigues', 'juliana.rodrigues@xpto.com.br', 'Supervisora de Operações', 'Operações', 7000.00, '2021-11-15', '(31) 99999-3001', 'Av. Afonso Pena, 369, Belo Horizonte - MG', 1, None),
        ('Ricardo Moura', 'ricardo.moura@xpto.com.br', 'Analista Financeiro', 'Financeiro', 5000.00, '2022-09-20', '(11) 99999-1008', 'Rua José Bonifácio, 741, São Paulo - SP', 1, 6)
    ]
    
    cursor.executemany('''
    INSERT INTO funcionarios (nome, email, cargo, departamento, salario, data_admissao, telefone, endereco, ativo, supervisor_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', funcionarios_data)
    
    # Dados de Fornecedores
    fornecedores_data = [
        ('TechSupply Brasil Ltda', 'TechSupply Brasil Ltda', '11.222.333/0001-44', '123.456.789', 'compras@techsupply.com.br', '(11) 3000-1001', 'Av. Industrial, 500', 'São Paulo', 'SP', '04000-000', 'Carlos Fornecedor', 15, '30 dias', 4.5, 1),
        ('SoftwareCorp', 'Software Corporation do Brasil', '22.333.444/0001-55', '234.567.890', 'vendas@softwarecorp.com.br', '(11) 3000-1002', 'Rua Software, 200', 'São Paulo', 'SP', '04001-000', 'Ana Licenças', 7, '60 dias', 4.8, 1),
        ('EquipTech Solutions', 'EquipTech Solutions Ltda', '33.444.555/0001-66', '345.678.901', 'atendimento@equiptech.com.br', '(21) 3000-2001', 'Av. Tecnologia, 800', 'Rio de Janeiro', 'RJ', '20000-000', 'João Equipamentos', 20, '45 dias', 4.2, 1)
    ]
    
    cursor.executemany('''
    INSERT INTO fornecedores (nome, razao_social, cnpj, inscricao_estadual, email, telefone, endereco, cidade, estado, cep, contato_principal, prazo_entrega_medio, condicoes_pagamento, avaliacao, ativo)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', fornecedores_data)
    
    # Dados de Clientes (atualizados com novos campos)
    clientes_data = [
        ('TechCorp Ltda', 'contato@techcorp.com.br', '(11) 3333-1001', 'Av. Faria Lima, 1000', 'São Paulo', 'SP', '01451-000', '12.345.678/0001-90', '123.456.789.012', 'Pessoa Jurídica', 'Tecnologia', '2022-01-15', 100000.00, 1),
        ('InnovaSoft', 'vendas@innovasoft.com.br', '(11) 3333-1002', 'Rua Oscar Freire, 500', 'São Paulo', 'SP', '01426-001', '23.456.789/0001-01', '234.567.890.123', 'Pessoa Jurídica', 'Software', '2022-03-20', 75000.00, 1),
        ('Maria José da Silva', 'mariajose@gmail.com', '(11) 99999-5001', 'Rua das Palmeiras, 123', 'São Paulo', 'SP', '04567-890', '123.456.789-00', None, 'Pessoa Física', 'Consultoria', '2022-06-10', 15000.00, 1),
        ('Comércio ABC S/A', 'financeiro@comercioabc.com.br', '(21) 3333-2001', 'Av. Rio Branco, 200', 'Rio de Janeiro', 'RJ', '20040-020', '34.567.890/0001-12', '345.678.901.234', 'Pessoa Jurídica', 'Varejo', '2021-12-05', 50000.00, 1),
        ('João Carlos Pereira', 'joaocarlos@hotmail.com', '(11) 99999-5002', 'Rua Sete de Setembro, 456', 'São Paulo', 'SP', '01234-567', '234.567.890-11', None, 'Pessoa Física', 'Serviços', '2023-02-28', 10000.00, 1)
    ]
    
    cursor.executemany('''
    INSERT INTO clientes (nome, email, telefone, endereco, cidade, estado, cep, cnpj, inscricao_estadual, tipo_cliente, segmento_mercado, data_cadastro, limite_credito, ativo)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', clientes_data)
    
    # Dados de Produtos/Serviços (atualizados)
    produtos_data = [
        ('ERP-001', 'Sistema de Gestão ERP', 'Sistema completo de gestão empresarial integrado', 'Software', 'ERP', 25000.00, 15000.00, 40.0, 5, 2, 10, 'UN', 'XPTO Desenvolvimento', 'Estoque TI', 1),
        ('CONS-001', 'Consultoria em TI', 'Consultoria especializada em tecnologia da informação', 'Serviços', 'Consultoria', 150.00, 100.00, 33.3, 0, 0, 0, 'HR', 'XPTO Consultoria', 'N/A', 1),
        ('WEB-001', 'Desenvolvimento de Website', 'Criação de sites responsivos e modernos', 'Serviços', 'Desenvolvimento', 5000.00, 3000.00, 40.0, 0, 0, 0, 'UN', 'XPTO Design', 'N/A', 1),
        ('SUP-001', 'Suporte Técnico Mensal', 'Suporte técnico especializado continuado', 'Serviços', 'Suporte', 800.00, 400.00, 50.0, 0, 0, 0, 'MES', 'XPTO Suporte', 'N/A', 1),
        ('LIC-001', 'Licença de Software Básico', 'Licença anual de software básico', 'Software', 'Licenciamento', 1200.00, 800.00, 33.3, 50, 10, 100, 'UN', 'XPTO Licenças', 'Estoque TI', 1)
    ]
    
    cursor.executemany('''
    INSERT INTO produtos (codigo_produto, nome, descricao, categoria, subcategoria, preco_venda, custo_unitario, margem_lucro, estoque_atual, estoque_minimo, estoque_maximo, unidade_medida, fornecedor_principal, localizacao_estoque, ativo)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', produtos_data)
    
    # Dados de Projetos (atualizados)
    projetos_data = [
        ('Sistema ERP TechCorp', 'Implementação completa do sistema ERP para gestão integrada', 1, 1, 1, '2023-01-15', '2023-12-31', None, 180000.00, None, 'Alta', 'Em Andamento'),
        ('Website InnovaSoft', 'Desenvolvimento do novo website corporativo responsivo', 2, 1, 4, '2023-03-01', '2023-06-30', '2023-06-25', 35000.00, 34500.00, 'Média', 'Concluído'),
        ('Consultoria ComércioABC', 'Consultoria para otimização de processos de TI', 4, 1, 1, '2023-05-15', '2024-02-28', None, 45000.00, None, 'Alta', 'Em Andamento')
    ]
    
    cursor.executemany('''
    INSERT INTO projetos (nome, descricao, cliente_id, departamento_id, gerente_projeto_id, data_inicio, data_fim_prevista, data_fim_real, orcamento, custo_real, prioridade, status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', projetos_data)
    
    # Gerar algumas vendas de exemplo
    vendas_data = [
        ('PED-2023-001', 1, 3, '2023-08-15', '2023-09-15', '2023-09-10', 25000.00, 5.0, 23750.00, 'Venda sistema ERP', 'Boleto', '30 dias', 'Pago', 'Cliente muito satisfeito'),
        ('PED-2023-002', 2, 7, '2023-09-20', '2023-10-20', '2023-10-18', 5000.00, 0.0, 5000.00, 'Desenvolvimento website', 'PIX', 'À vista', 'Pago', None),
        ('PED-2023-003', 3, 3, '2023-10-05', '2023-11-05', None, 1200.00, 10.0, 1080.00, 'Licenças software', 'Cartão', '2x sem juros', 'Faturado', 'Aguardando entrega')
    ]
    
    cursor.executemany('''
    INSERT INTO vendas (numero_pedido, cliente_id, funcionario_id, data_venda, data_entrega_prevista, data_entrega_real, valor_bruto, desconto, valor_total, descricao, forma_pagamento, condicoes_pagamento, status, observacoes)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', vendas_data)
    
    # Itens das vendas
    itens_vendas_data = [
        (1, 1, 1, 25000.00, 5.0, 23750.00, 'Sistema ERP completo'),
        (2, 3, 1, 5000.00, 0.0, 5000.00, 'Website responsivo'),  
        (3, 5, 1, 1200.00, 10.0, 1080.00, 'Licença anual básica')
    ]
    
    cursor.executemany('''
    INSERT INTO itens_venda (venda_id, produto_id, quantidade, preco_unitario, desconto_item, valor_total_item, observacoes)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', itens_vendas_data)
    
    print("✅ Dados de exemplo inseridos com sucesso!")

def get_metadata_info(db_path):
    """Função para consultar metadados do banco."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("\n" + "="*60)
    print("📋 METADADOS DO BANCO DE DADOS XPTO")
    print("="*60)
    
    # Comentários de tabelas
    print("\n🏢 COMENTÁRIOS DAS TABELAS:")
    cursor.execute("SELECT table_name, comment, data_owner FROM table_comments ORDER BY table_name")
    for row in cursor.fetchall():
        print(f"  📊 {row[0]}: {row[1]} (Owner: {row[2]})")
    
    # Exemplos de comentários de colunas
    print("\n📝 COMENTÁRIOS DE COLUNAS (amostra):")
    cursor.execute("""
        SELECT table_name, column_name, comment, example_values 
        FROM column_comments 
        WHERE table_name = 'funcionarios'
        ORDER BY column_name
        LIMIT 5
    """)
    for row in cursor.fetchall():
        print(f"  🔸 {row[0]}.{row[1]}: {row[2]}")
        print(f"      Exemplos: {row[3]}")
    
    conn.close()

if __name__ == "__main__":
    create_xpto_database()
    get_metadata_info('data/xpto_empresa.db')