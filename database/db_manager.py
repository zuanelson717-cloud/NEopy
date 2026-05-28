"""
Módulo de Banco de Dados - NEopy
Gerencia todas as operações com SQLite
"""

import sqlite3
import os
from datetime import datetime
from config.settings import DATABASE_PATH


class Database:
    """Classe para gerenciar operações com banco de dados"""
    
    def __init__(self):
        """Inicializa conexão com banco de dados"""
        self.db_path = DATABASE_PATH
        self.ensure_db_dir()
        self.init_db()
    
    def ensure_db_dir(self):
        """Garante que o diretório existe"""
        db_dir = os.path.dirname(self.db_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
    
    def get_connection(self):
        """Retorna conexão com banco de dados"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        """Inicializa tabelas do banco"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabela de Pessoas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pessoas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT UNIQUE NOT NULL,
                email TEXT,
                telefone TEXT,
                data_nascimento TEXT,
                empresa TEXT,
                cargo TEXT,
                foto_path TEXT,
                data_cadastro TEXT DEFAULT CURRENT_TIMESTAMP,
                ativo INTEGER DEFAULT 1
            )
        ''')
        
        # Tabela de Questões (Quiz)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS questoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pergunta TEXT NOT NULL,
                opcao_a TEXT NOT NULL,
                opcao_b TEXT NOT NULL,
                opcao_c TEXT NOT NULL,
                opcao_d TEXT NOT NULL,
                resposta_correta TEXT NOT NULL,
                dificuldade TEXT DEFAULT 'medio',
                categoria TEXT DEFAULT 'matematica'
            )
        ''')
        
        # Tabela de Respostas (Histórico do Quiz)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS respostas_quiz (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pessoa_id INTEGER,
                questao_id INTEGER,
                resposta_dada TEXT,
                correta INTEGER,
                data_resposta TEXT DEFAULT CURRENT_TIMESTAMP,
                tempo_gasto INTEGER,
                FOREIGN KEY (pessoa_id) REFERENCES pessoas(id),
                FOREIGN KEY (questao_id) REFERENCES questoes(id)
            )
        ''')
        
        # Tabela de Resultados (Score do Quiz)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS resultados_quiz (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pessoa_id INTEGER,
                total_questoes INTEGER,
                acertos INTEGER,
                erros INTEGER,
                percentual_acerto REAL,
                tempo_total INTEGER,
                data_conclusao TEXT DEFAULT CURRENT_TIMESTAMP,
                passou INTEGER,
                FOREIGN KEY (pessoa_id) REFERENCES pessoas(id)
            )
        ''')
        
        # Tabela de Matérias de Informática (Entrada/Saída)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS materiais_informatica (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descricao TEXT NOT NULL,
                categoria TEXT NOT NULL,
                numero_serie TEXT UNIQUE,
                valor_unitario REAL,
                quantidade_total INTEGER,
                quantidade_disponivel INTEGER,
                data_entrada TEXT,
                fornecedor TEXT,
                localizacao TEXT,
                status TEXT DEFAULT 'ativo',
                observacoes TEXT,
                data_cadastro TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de Movimentação de Matérias (Entrada/Saída)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS movimentacao_materiais (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                material_id INTEGER NOT NULL,
                tipo_movimentacao TEXT NOT NULL,
                quantidade INTEGER,
                data_movimentacao TEXT DEFAULT CURRENT_TIMESTAMP,
                usuario_id INTEGER,
                responsavel TEXT,
                motivo TEXT,
                observacoes TEXT,
                FOREIGN KEY (material_id) REFERENCES materiais_informatica(id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print("\u2705 Banco de dados inicializado com sucesso!")
    
    # ========== OPERAÇÕES COM PESSOAS ==========
    
    def adicionar_pessoa(self, nome, cpf, email, telefone, data_nascimento, empresa, cargo, foto_path=None):
        """Adiciona uma nova pessoa ao banco"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO pessoas (nome, cpf, email, telefone, data_nascimento, empresa, cargo, foto_path)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (nome, cpf, email, telefone, data_nascimento, empresa, cargo, foto_path))
            
            conn.commit()
            pessoa_id = cursor.lastrowid
            conn.close()
            
            return pessoa_id
        except sqlite3.IntegrityError:
            return None
    
    def obter_todas_pessoas(self):
        """Retorna todas as pessoas cadastradas"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM pessoas WHERE ativo = 1 ORDER BY data_cadastro DESC')
        pessoas = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return pessoas
    
    def obter_pessoa(self, pessoa_id):
        """Retorna dados de uma pessoa específica"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM pessoas WHERE id = ? AND ativo = 1', (pessoa_id,))
        pessoa = dict(cursor.fetchone() or {})
        
        conn.close()
        return pessoa
    
    def atualizar_pessoa(self, pessoa_id, **kwargs):
        """Atualiza dados de uma pessoa"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        campos = ', '.join([f"{k} = ?" for k in kwargs.keys()])
        valores = list(kwargs.values()) + [pessoa_id]
        
        cursor.execute(f'UPDATE pessoas SET {campos} WHERE id = ?', valores)
        
        conn.commit()
        conn.close()
        
        return True
    
    def deletar_pessoa(self, pessoa_id):
        """Deleta (marca como inativo) uma pessoa"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('UPDATE pessoas SET ativo = 0 WHERE id = ?', (pessoa_id,))
        
        conn.commit()
        conn.close()
        
        return True
    
    # ========== OPERAÇÕES COM MATÉRIAS DE INFORMÁTICA ==========
    
    def adicionar_material(self, descricao, categoria, numero_serie, valor_unitario, quantidade_total, 
                          data_entrada, fornecedor, localizacao, observacoes=''):
        """Adiciona um novo material de informática"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO materiais_informatica 
                (descricao, categoria, numero_serie, valor_unitario, quantidade_total, 
                 quantidade_disponivel, data_entrada, fornecedor, localizacao, observacoes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (descricao, categoria, numero_serie, valor_unitario, quantidade_total, 
                  quantidade_total, data_entrada, fornecedor, localizacao, observacoes))
            
            conn.commit()
            material_id = cursor.lastrowid
            conn.close()
            
            return material_id
        except sqlite3.IntegrityError:
            return None
    
    def obter_todos_materiais(self):
        """Retorna todos os materiais cadastrados"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM materiais_informatica WHERE status = "ativo" ORDER BY data_cadastro DESC')
        materiais = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return materiais
    
    def obter_material(self, material_id):
        """Retorna dados de um material específico"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM materiais_informatica WHERE id = ? AND status = "ativo"', (material_id,))
        material = dict(cursor.fetchone() or {})
        
        conn.close()
        return material
    
    def registrar_movimentacao(self, material_id, tipo_movimentacao, quantidade, responsavel, motivo='', observacoes=''):
        """Registra entrada ou saída de material"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Registrar movimentação
            cursor.execute('''
                INSERT INTO movimentacao_materiais 
                (material_id, tipo_movimentacao, quantidade, responsavel, motivo, observacoes)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (material_id, tipo_movimentacao, quantidade, responsavel, motivo, observacoes))
            
            # Atualizar quantidade disponível
            if tipo_movimentacao.lower() == 'entrada':
                cursor.execute('UPDATE materiais_informatica SET quantidade_disponivel = quantidade_disponivel + ? WHERE id = ?',
                             (quantidade, material_id))
            elif tipo_movimentacao.lower() == 'saida':
                cursor.execute('UPDATE materiais_informatica SET quantidade_disponivel = quantidade_disponivel - ? WHERE id = ?',
                             (quantidade, material_id))
            
            conn.commit()
            movimentacao_id = cursor.lastrowid
            conn.close()
            
            return movimentacao_id
        except Exception as e:
            conn.close()
            print(f"Erro ao registrar movimentação: {e}")
            return None
    
    def obter_movimentacoes_material(self, material_id):
        """Retorna histórico de movimentações de um material"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM movimentacao_materiais 
            WHERE material_id = ? 
            ORDER BY data_movimentacao DESC
        ''', (material_id,))
        
        movimentacoes = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return movimentacoes
    
    def obter_todas_movimentacoes(self):
        """Retorna todas as movimentações de materiais"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT mm.*, mi.descricao FROM movimentacao_materiais mm
            JOIN materiais_informatica mi ON mm.material_id = mi.id
            ORDER BY mm.data_movimentacao DESC
        ''')
        
        movimentacoes = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return movimentacoes
    
    def obter_relatorio_materiais(self):
        """Gera relatório de todos os materiais com movimentações"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                mi.*,
                COUNT(mm.id) as total_movimentacoes,
                SUM(CASE WHEN mm.tipo_movimentacao = 'entrada' THEN mm.quantidade ELSE 0 END) as total_entradas,
                SUM(CASE WHEN mm.tipo_movimentacao = 'saida' THEN mm.quantidade ELSE 0 END) as total_saidas
            FROM materiais_informatica mi
            LEFT JOIN movimentacao_materiais mm ON mi.id = mm.material_id
            WHERE mi.status = 'ativo'
            GROUP BY mi.id
            ORDER BY mi.data_cadastro DESC
        ''')
        
        relatorio = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return relatorio


# Instância global do banco de dados
db = Database()
