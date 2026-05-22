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
        
        conn.commit()
        conn.close()
        print("✅ Banco de dados inicializado com sucesso!")
    
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
    
    def buscar_pessoa_cpf(self, cpf):
        """Busca pessoa por CPF"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM pessoas WHERE cpf = ? AND ativo = 1', (cpf,))
        pessoa = dict(cursor.fetchone() or {})
        
        conn.close()
        return pessoa
    
    # ========== OPERAÇÕES COM QUESTÕES ==========
    
    def adicionar_questao(self, pergunta, opcao_a, opcao_b, opcao_c, opcao_d, resposta_correta, dificuldade='medio'):
        """Adiciona uma nova questão"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO questoes (pergunta, opcao_a, opcao_b, opcao_c, opcao_d, resposta_correta, dificuldade)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (pergunta, opcao_a, opcao_b, opcao_c, opcao_d, resposta_correta, dificuldade))
        
        conn.commit()
        questao_id = cursor.lastrowid
        conn.close()
        
        return questao_id
    
    def obter_todas_questoes(self, dificuldade=None):
        """Retorna todas as questões"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if dificuldade:
            cursor.execute('SELECT * FROM questoes WHERE dificuldade = ?', (dificuldade,))
        else:
            cursor.execute('SELECT * FROM questoes')
        
        questoes = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return questoes
    
    def obter_questoes_aleatorias(self, quantidade=10, dificuldade=None):
        """Retorna questões aleatórias"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if dificuldade:
            cursor.execute('SELECT * FROM questoes WHERE dificuldade = ? ORDER BY RANDOM() LIMIT ?', 
                          (dificuldade, quantidade))
        else:
            cursor.execute('SELECT * FROM questoes ORDER BY RANDOM() LIMIT ?', (quantidade,))
        
        questoes = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return questoes
    
    # ========== OPERAÇÕES COM RESPOSTAS DO QUIZ ==========
    
    def salvar_resposta_quiz(self, pessoa_id, questao_id, resposta_dada, correta, tempo_gasto):
        """Salva resposta de uma questão"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO respostas_quiz (pessoa_id, questao_id, resposta_dada, correta, tempo_gasto)
            VALUES (?, ?, ?, ?, ?)
        ''', (pessoa_id, questao_id, resposta_dada, 1 if correta else 0, tempo_gasto))
        
        conn.commit()
        conn.close()
    
    def salvar_resultado_quiz(self, pessoa_id, total_questoes, acertos, erros, percentual_acerto, tempo_total, passou):
        """Salva resultado final do quiz"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO resultados_quiz (pessoa_id, total_questoes, acertos, erros, percentual_acerto, tempo_total, passou)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (pessoa_id, total_questoes, acertos, erros, percentual_acerto, tempo_total, 1 if passou else 0))
        
        conn.commit()
        resultado_id = cursor.lastrowid
        conn.close()
        
        return resultado_id
    
    def obter_resultados_pessoa(self, pessoa_id):
        """Retorna histórico de resultados de uma pessoa"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM resultados_quiz WHERE pessoa_id = ? ORDER BY data_conclusao DESC', (pessoa_id,))
        resultados = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return resultados
    
    def obter_estatisticas_geral(self):
        """Retorna estatísticas gerais"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) as total FROM pessoas WHERE ativo = 1')
        total_pessoas = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) as total FROM resultados_quiz WHERE passou = 1')
        total_aprovados = cursor.fetchone()[0]
        
        cursor.execute('SELECT AVG(percentual_acerto) as media FROM resultados_quiz')
        media_acertos = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            'total_pessoas': total_pessoas,
            'total_aprovados': total_aprovados,
            'media_acertos': round(media_acertos, 2)
        }


# Instância global do banco de dados
db = Database()
