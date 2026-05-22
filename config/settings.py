"""
Configurations Globais do Projeto NEopy
"""

# ========== JOGO DE MOTA ==========
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "NEopy - Motorcycle 3D Game"
SKY_COLOR = (0.5, 0.7, 1.0, 1.0)
WORLD_SIZE = 200

# Câmera
CAMERA_DISTANCE = 15
CAMERA_HEIGHT = 5
CAMERA_SMOOTHNESS = 0.1

# Física
GRAVITY = 9.8
FRICTION = 0.3
MAX_SPEED = 50
ACCELERATION = 20
BRAKE_FORCE = 30
TURN_SPEED = 180  # graus por segundo

# Debug
SHOW_FPS = True

# ========== BANCO DE DADOS ==========
DATABASE_NAME = 'neopy.db'
DATABASE_PATH = 'database/neopy.db'

# ========== CONFIGURAÇÕES DA APLICAÇÃO ==========
APP_TITLE = "NEopy - Sistema Integrado"
APP_WIDTH = 1000
APP_HEIGHT = 700
APP_THEME = "modern"

# ========== QUESTIONÁRIO ==========
QUIZ_TIME_PER_QUESTION = 30  # segundos
QUIZ_PASS_PERCENTAGE = 60  # % mínimo para passar

# ========== PASSE ==========
PASSE_TEMPLATE = "templates/passe_template.png"
PASSE_OUTPUT_DIR = "output/passes/"
EXCEL_OUTPUT_DIR = "output/excel/"
PDF_OUTPUT_DIR = "output/pdf/"
