#!/usr/bin/env python3
"""
Script para criar o banco de dados SQLite da empresa XPTO teste.
Este script cria tabelas e dados de exemplo para uma empresa fictícia.
"""
import sqlite3
import random
from datetime import datetime, timedelta
import os

def create_xpto_database():
    """Cria o banco de dados da empresa XPTO com tabelas e dados de exemplo."""
    
    # Criar diretório data se não existir
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Conectar ao banco de dados
    conn = sqlite3.connect('data/xpto_empresa.db')
    cursor = conn.cursor()
    
    # Criar tabelas
    create_tables(cursor)
    
    # Inserir dados de exemplo
    insert_sample_data(cursor)
    
    # Confirmar mudanças e fechar conexão
    conn.commit()
    conn.close()
    
    print("✅ Banco de dados da empresa XPTO criado com sucesso!")
    print("📍 Localização: data/xpto_empresa.db")

def create_tables(cursor):
    """Cria as tabelas do banco de dados."""
    
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
        ativo BOOLEAN DEFAULT 1
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
        data_inicio DATE NOT NULL,
        data_fim_prevista DATE,
        data_fim_real DATE,
        orcamento DECIMAL(12,2),
        status TEXT CHECK(status IN ('Planejamento', 'Em Andamento', 'Pausado', 'Concluído', 'Cancelado')),
        FOREIGN KEY (cliente_id) REFERENCES clientes (id),
        FOREIGN KEY (departamento_id) REFERENCES departamentos (id)
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
        tipo_cliente TEXT CHECK(tipo_cliente IN ('Pessoa Física', 'Pessoa Jurídica')),
        data_cadastro DATE NOT NULL,
        ativo BOOLEAN DEFAULT 1
    )
    ''')
    
    # Tabela de Vendas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS vendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        funcionario_id INTEGER NOT NULL,
        data_venda DATE NOT NULL,
        valor_total DECIMAL(10,2) NOT NULL,
        descricao TEXT,
        forma_pagamento TEXT,
        status TEXT CHECK(status IN ('Pendente', 'Pago', 'Cancelado')),
        FOREIGN KEY (cliente_id) REFERENCES clientes (id),
        FOREIGN KEY (funcionario_id) REFERENCES funcionarios (id)
    )
    ''')
    
    # Tabela de Produtos/Serviços
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        descricao TEXT,
        categoria TEXT,
        preco DECIMAL(10,2) NOT NULL,
        custo DECIMAL(10,2),
        estoque_atual INTEGER DEFAULT 0,
        estoque_minimo INTEGER DEFAULT 0,
        fornecedor TEXT,
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
        desconto DECIMAL(5,2) DEFAULT 0,
        FOREIGN KEY (venda_id) REFERENCES vendas (id),
        FOREIGN KEY (produto_id) REFERENCES produtos (id)
    )
    ''')
    
    print("✅ Tabelas criadas com sucesso!")

def insert_sample_data(cursor):
    """Insere dados de exemplo nas tabelas."""
    
    # Dados de Departamentos
    departamentos_data = [
        ('Tecnologia da Informação', 'Desenvolvimento de software e infraestrutura', None, 500000.00, 'São Paulo - SP'),
        ('Recursos Humanos', 'Gestão de pessoas e recrutamento', None, 200000.00, 'São Paulo - SP'),
        ('Vendas', 'Comercialização de produtos e serviços', None, 800000.00, 'São Paulo - SP'),
        ('Marketing', 'Promoção da marca e produtos', None, 300000.00, 'Rio de Janeiro - RJ'),
        ('Financeiro', 'Gestão financeira e contábil', None, 150000.00, 'São Paulo - SP'),
        ('Operações', 'Logística e operações', None, 600000.00, 'Belo Horizonte - MG')
    ]
    
    cursor.executemany('''
    INSERT INTO departamentos (nome, descricao, gerente_id, orcamento, localizacao)
    VALUES (?, ?, ?, ?, ?)
    ''', departamentos_data)
    
    # Dados de Funcionários
    funcionarios_data = [
        ('Maria Silva Santos', 'maria.silva@xpto.com.br', 'Diretora de TI', 'Tecnologia da Informação', 15000.00, '2020-01-15', '(11) 99999-1001', 'Rua das Flores, 123, São Paulo - SP', 1),
        ('João Pedro Oliveira', 'joao.oliveira@xpto.com.br', 'Gerente de RH', 'Recursos Humanos', 8000.00, '2019-03-10', '(11) 99999-1002', 'Av. Paulista, 456, São Paulo - SP', 1),
        ('Ana Carolina Costa', 'ana.costa@xpto.com.br', 'Diretora de Vendas', 'Vendas', 12000.00, '2018-06-20', '(11) 99999-1003', 'Rua Augusta, 789, São Paulo - SP', 1),
        ('Carlos Eduardo Lima', 'carlos.lima@xpto.com.br', 'Desenvolvedor Senior', 'Tecnologia da Informação', 7500.00, '2021-02-01', '(11) 99999-1004', 'Rua da Consolação, 321, São Paulo - SP', 1),
        ('Fernanda Almeida', 'fernanda.almeida@xpto.com.br', 'Analista de Marketing', 'Marketing', 5500.00, '2022-04-15', '(21) 99999-2001', 'Av. Copacabana, 654, Rio de Janeiro - RJ', 1),
        ('Roberto Santos', 'roberto.santos@xpto.com.br', 'Contador', 'Financeiro', 6000.00, '2020-08-30', '(11) 99999-1005', 'Rua do Comércio, 987, São Paulo - SP', 1),
        ('Luciana Ferreira', 'luciana.ferreira@xpto.com.br', 'Vendedora', 'Vendas', 4500.00, '2023-01-10', '(11) 99999-1006', 'Rua XV de Novembro, 147, São Paulo - SP', 1),
        ('Pedro Henrique Silva', 'pedro.silva@xpto.com.br', 'Desenvolvedor Junior', 'Tecnologia da Informação', 4000.00, '2023-07-01', '(11) 99999-1007', 'Rua Bela Vista, 258, São Paulo - SP', 1),
        ('Juliana Rodrigues', 'juliana.rodrigues@xpto.com.br', 'Supervisora de Operações', 'Operações', 7000.00, '2021-11-15', '(31) 99999-3001', 'Av. Afonso Pena, 369, Belo Horizonte - MG', 1),
        ('Ricardo Moura', 'ricardo.moura@xpto.com.br', 'Analista Financeiro', 'Financeiro', 5000.00, '2022-09-20', '(11) 99999-1008', 'Rua José Bonifácio, 741, São Paulo - SP', 1)
    ]
    
    cursor.executemany('''
    INSERT INTO funcionarios (nome, email, cargo, departamento, salario, data_admissao, telefone, endereco, ativo)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', funcionarios_data)
    
    # Dados de Clientes
    clientes_data = [
        ('TechCorp Ltda', 'contato@techcorp.com.br', '(11) 3333-1001', 'Av. Faria Lima, 1000', 'São Paulo', 'SP', '01451-000', '12.345.678/0001-90', 'Pessoa Jurídica', '2022-01-15', 1),
        ('InnovaSoft', 'vendas@innovasoft.com.br', '(11) 3333-1002', 'Rua Oscar Freire, 500', 'São Paulo', 'SP', '01426-001', '23.456.789/0001-01', 'Pessoa Jurídica', '2022-03-20', 1),
        ('Maria José da Silva', 'mariajose@gmail.com', '(11) 99999-5001', 'Rua das Palmeiras, 123', 'São Paulo', 'SP', '04567-890', '123.456.789-00', 'Pessoa Física', '2022-06-10', 1),
        ('Comércio ABC S/A', 'financeiro@comercioabc.com.br', '(21) 3333-2001', 'Av. Rio Branco, 200', 'Rio de Janeiro', 'RJ', '20040-020', '34.567.890/0001-12', 'Pessoa Jurídica', '2021-12-05', 1),
        ('João Carlos Pereira', 'joaocarlos@hotmail.com', '(11) 99999-5002', 'Rua Sete de Setembro, 456', 'São Paulo', 'SP', '01234-567', '234.567.890-11', 'Pessoa Física', '2023-02-28', 1),
        ('LogiMax Transportes', 'contato@logimax.com.br', '(31) 3333-3001', 'Av. Amazonas, 800', 'Belo Horizonte', 'MG', '30112-000', '45.678.901/0001-23', 'Pessoa Jurídica', '2022-08-15', 1),
        ('SuperMercado Estrela', 'compras@superestrela.com.br', '(11) 3333-1003', 'Rua do Mercado, 750', 'São Paulo', 'SP', '03456-789', '56.789.012/0001-34', 'Pessoa Jurídica', '2021-11-30', 1),
        ('Ana Beatriz Souza', 'anabeatriz@yahoo.com', '(21) 99999-6001', 'Rua Ipanema, 321', 'Rio de Janeiro', 'RJ', '22071-900', '345.678.901-22', 'Pessoa Física', '2023-05-12', 1)
    ]
    
    cursor.executemany('''
    INSERT INTO clientes (nome, email, telefone, endereco, cidade, estado, cep, cnpj, tipo_cliente, data_cadastro, ativo)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', clientes_data)
    
    # Dados de Produtos/Serviços
    produtos_data = [
        ('Sistema de Gestão ERP', 'Sistema completo de gestão empresarial', 'Software', 25000.00, 15000.00, 5, 2, 'XPTO Desenvolvimento', 1),
        ('Consultoria em TI', 'Consultoria especializada em tecnologia', 'Serviços', 150.00, 100.00, 0, 0, 'XPTO Consultoria', 1),
        ('Desenvolvimento de Website', 'Criação de sites responsivos', 'Serviços', 5000.00, 3000.00, 0, 0, 'XPTO Design', 1),
        ('Suporte Técnico Mensal', 'Suporte técnico especializado', 'Serviços', 800.00, 400.00, 0, 0, 'XPTO Suporte', 1),
        ('Licença de Software Básico', 'Licença anual de software', 'Software', 1200.00, 800.00, 50, 10, 'XPTO Licenças', 1),
        ('Treinamento Corporativo', 'Treinamento para equipes', 'Serviços', 2000.00, 1200.00, 0, 0, 'XPTO Educação', 1),
        ('Backup em Nuvem', 'Serviço de backup automatizado', 'Serviços', 300.00, 150.00, 0, 0, 'XPTO Cloud', 1),
        ('App Mobile Personalizado', 'Desenvolvimento de aplicativo mobile', 'Software', 15000.00, 10000.00, 3, 1, 'XPTO Mobile', 1)
    ]
    
    cursor.executemany('''
    INSERT INTO produtos (nome, descricao, categoria, preco, custo, estoque_atual, estoque_minimo, fornecedor, ativo)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', produtos_data)
    
    # Dados de Projetos
    projetos_data = [
        ('Sistema ERP TechCorp', 'Implementação completa do sistema ERP', 1, 1, '2023-01-15', '2023-12-31', None, 180000.00, 'Em Andamento'),
        ('Website InnovaSoft', 'Desenvolvimento do novo website corporativo', 2, 1, '2023-03-01', '2023-06-30', '2023-06-25', 35000.00, 'Concluído'),
        ('App Mobile ComércioABC', 'Aplicativo de vendas para dispositivos móveis', 4, 1, '2023-05-15', '2024-02-28', None, 120000.00, 'Em Andamento'),
        ('Consultoria LogiMax', 'Otimização de processos logísticos', 6, 6, '2023-07-01', '2023-11-30', None, 45000.00, 'Em Andamento'),
        ('Suporte SuperMercado Estrela', 'Suporte técnico mensal continuado', 7, 1, '2022-12-01', '2023-12-31', None, 24000.00, 'Em Andamento')
    ]
    
    cursor.executemany('''
    INSERT INTO projetos (nome, descricao, cliente_id, departamento_id, data_inicio, data_fim_prevista, data_fim_real, orcamento, status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', projetos_data)
    
    # Gerar dados de vendas (mais realistas)
    vendas_data = []
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 11, 8)
    
    for i in range(50):  # 50 vendas de exemplo
        random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        cliente_id = random.randint(1, 8)
        funcionario_vendas = [3, 7]  # IDs dos funcionários de vendas
        funcionario_id = random.choice(funcionario_vendas)
        valor = round(random.uniform(500, 50000), 2)
        formas_pagamento = ['À vista', 'Cartão de Crédito', 'Boleto', 'Transferência', 'PIX']
        status_opcoes = ['Pago', 'Pago', 'Pago', 'Pendente']  # Mais vendas pagas
        
        vendas_data.append((
            cliente_id,
            funcionario_id,
            random_date.strftime('%Y-%m-%d'),
            valor,
            f'Venda de produtos/serviços XPTO #{i+1}',
            random.choice(formas_pagamento),
            random.choice(status_opcoes)
        ))
    
    cursor.executemany('''
    INSERT INTO vendas (cliente_id, funcionario_id, data_venda, valor_total, descricao, forma_pagamento, status)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', vendas_data)
    
    # Gerar itens de venda para algumas vendas
    for venda_id in range(1, 21):  # Primeiras 20 vendas
        num_itens = random.randint(1, 4)
        for _ in range(num_itens):
            produto_id = random.randint(1, 8)
            quantidade = random.randint(1, 5)
            # Buscar preço do produto
            cursor.execute('SELECT preco FROM produtos WHERE id = ?', (produto_id,))
            preco_base = cursor.fetchone()[0]
            preco_unitario = round(preco_base * random.uniform(0.8, 1.2), 2)  # Variação de ±20%
            desconto = round(random.uniform(0, 15), 2) if random.random() > 0.7 else 0
            
            cursor.execute('''
            INSERT INTO itens_venda (venda_id, produto_id, quantidade, preco_unitario, desconto)
            VALUES (?, ?, ?, ?, ?)
            ''', (venda_id, produto_id, quantidade, preco_unitario, desconto))
    
    print("✅ Dados de exemplo inseridos com sucesso!")

if __name__ == "__main__":
    create_xpto_database()