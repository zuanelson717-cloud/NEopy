"""
Gerenciador do Mundo/Cenário
"""

from config.settings import *


class World:
    """Representa o mundo do jogo"""
    
    def __init__(self, show_base):
        """
        Inicializa o mundo
        show_base: referência ao ShowBase do Panda3D
        """
        self.show_base = show_base
        self.obstacles = []
        self.checkpoints = []
        self.particles = []
        
        # Criar ambiente
        self.create_terrain()
        self.create_sky()
        self.create_obstacles()
        self.create_checkpoints()
    
    def create_terrain(self):
        """Cria o terreno"""
        # Criar plano para o chão
        from panda3d.core import CardMaker
        
        cm = CardMaker("terrain")
        cm.setFrame(-WORLD_SIZE/2, WORLD_SIZE/2, -WORLD_SIZE/2, WORLD_SIZE/2)
        
        terrain = self.show_base.render.attachNewNode(cm.generate())
        terrain.setP(-90)  # Rotacionar para ficar horizontal
        terrain.setPos(0, -0.1, 0)
        terrain.setColor(0.2, 0.5, 0.2, 1)  # Verde grama
        
        self.terrain = terrain
    
    def create_sky(self):
        """Cria o céu"""
        # Criar dome do céu (usando uma esfera)
        self.show_base.sky = None
        # Simplificado - apenas usar cor de fundo que já foi configurada
    
    def create_obstacles(self):
        """Cria obstáculos no mundo"""
        # Alguns objetos para teste
        obstacle_positions = [
            (10, 0, 10),
            (-10, 0, 15),
            (20, 0, -5),
            (-15, 0, -20),
            (0, 0, 30),
            (25, 0, 25),
        ]
        
        for i, (x, y, z) in enumerate(obstacle_positions):
            self.add_obstacle(x, y, z, radius=2)
    
    def add_obstacle(self, x, y, z, radius=1):
        """
        Adiciona um obstáculo ao mundo
        """
        # Criar modelo do obstáculo
        obstacle_model = self.show_base.loader.loadModel("models/box")
        obstacle_model.setScale(radius * 2)
        obstacle_model.setPos(x, y, z)
        obstacle_model.setColor(0.8, 0.4, 0.1, 1)  # Laranja
        obstacle_model.reparentTo(self.show_base.render)
        
        # Registrar obstáculo
        obstacle_data = {
            'x': x,
            'y': y,
            'z': z,
            'radius': radius,
            'model': obstacle_model,
            'type': 'box'
        }
        
        self.obstacles.append(obstacle_data)
    
    def create_checkpoints(self):
        """Cria checkpoints para corrida"""
        checkpoint_positions = [
            (0, 0, 0),
            (0, 0, 50),
            (50, 0, 50),
            (50, 0, 0),
        ]
        
        for i, (x, y, z) in enumerate(checkpoint_positions):
            self.add_checkpoint(x, y, z, i)
    
    def add_checkpoint(self, x, y, z, checkpoint_id=0):
        """
        Adiciona um checkpoint
        """
        # Criar marcador visual
        marker = self.show_base.loader.loadModel("models/box")
        marker.setScale(5, 0.5, 5)
        marker.setPos(x, y - 0.5, z)
        marker.setColor(0.2, 0.2, 0.8, 0.3)  # Azul semi-transparente
        marker.reparentTo(self.show_base.render)
        
        checkpoint_data = {
            'id': checkpoint_id,
            'x': x,
            'y': y,
            'z': z,
            'radius': 5,
            'model': marker,
            'passed': False
        }
        
        self.checkpoints.append(checkpoint_data)
    
    def check_checkpoint(self, motorcycle):
        """
        Verifica se a mota passou por um checkpoint
        """
        for checkpoint in self.checkpoints:
            if checkpoint['passed']:
                continue
            
            distance = ((motorcycle.x - checkpoint['x'])**2 + 
                       (motorcycle.z - checkpoint['z'])**2)**0.5
            
            if distance < checkpoint['radius']:
                checkpoint['passed'] = True
                return checkpoint['id']
        
        return -1
    
    def reset_checkpoints(self):
        """Reseta todos os checkpoints"""
        for checkpoint in self.checkpoints:
            checkpoint['passed'] = False
    
    def spawn_particle(self, x, y, z, particle_type='dust'):
        """
        Cria uma partícula no mundo
        """
        particle_data = {
            'x': x,
            'y': y,
            'z': z,
            'type': particle_type,
            'lifetime': 0.5,
            'age': 0
        }
        
        self.particles.append(particle_data)
    
    def update_particles(self, delta_time):
        """Atualiza partículas"""
        dead_particles = []
        
        for particle in self.particles:
            particle['age'] += delta_time
            
            if particle['age'] > particle['lifetime']:
                dead_particles.append(particle)
        
        for particle in dead_particles:
            self.particles.remove(particle)
    
    def cleanup(self):
        """Limpa o mundo"""
        if self.terrain:
            self.terrain.removeNode()
        
        for obstacle in self.obstacles:
            if obstacle['model']:
                obstacle['model'].removeNode()
        
        for checkpoint in self.checkpoints:
            if checkpoint['model']:
                checkpoint['model'].removeNode()
