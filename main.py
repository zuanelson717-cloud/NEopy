#!/usr/bin/env python3
"""
Motorcycle 3D Game - NEopy
Um jogo de mota em 3D feito com Panda3D
"""

import sys
import math
from panda3d.core import Point3, Vec3, TransformState
from direct.showbase.ShowBase import ShowBase
from direct.task import Task

# Importar módulos do jogo
from config.settings import *
from game.motorcycle import Motorcycle
from game.physics import PhysicsEngine
from game.world import World


class MotorcycleGame(ShowBase):
    """Classe principal do jogo"""
    
    def __init__(self):
        """Inicializa o jogo"""
        ShowBase.__init__(self)
        
        # Configurações da janela
        self.win.setSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.set_background_color(*SKY_COLOR)
        self.windowProperties.setTitle(WINDOW_TITLE)
        
        # Iluminação
        self.setup_lights()
        
        # Criar objetos do jogo
        self.motorcycle = Motorcycle(0, 2, 0)
        self.physics_engine = PhysicsEngine()
        self.world = World(self)
        
        # Criar modelo da mota (primitivo)
        self.create_motorcycle_model()
        
        # Câmera
        self.camera_distance = CAMERA_DISTANCE
        self.camera_height = CAMERA_HEIGHT
        
        # Controles
        self.keys = {}
        self.setup_controls()
        
        # FPS
        self.fps_counter = 0
        
        # Task para atualizar o jogo
        self.taskMgr.add(self.update_game, "update_game")
        
        print("🏍️  Motorcycle 3D Game - NEopy iniciado!")
        print("Controles: W/A/S/D - Mover | SPACE - Pular | ESC - Sair")
    
    def setup_lights(self):
        """Configura a iluminação da cena"""
        from panda3d.core import AmbientLight, DirectionalLight
        
        # Luz ambiente
        ambient_light = AmbientLight("ambient_light")
        ambient_light.setColor((0.8, 0.8, 0.8, 1))
        self.render.attachNewNode(ambient_light)
        self.render.setLight(self.render.attachNewNode(ambient_light))
        
        # Luz direcional (sol)
        directional_light = DirectionalLight("directional_light")
        directional_light.setColor((1, 1, 1, 1))
        dir_light_np = self.render.attachNewNode(directional_light)
        dir_light_np.setPos(10, 10, 10)
        self.render.setLight(dir_light_np)
    
    def create_motorcycle_model(self):
        """Cria um modelo primitivo da mota"""
        # Usar modelo box para prototipagem rápida
        self.motorcycle.model = self.loader.loadModel("models/box")
        self.motorcycle.model.setScale(1, 0.5, 2)  # Comprido e fino (como uma mota)
        self.motorcycle.model.setColor(0.8, 0.1, 0.1, 1)  # Vermelho
        self.motorcycle.model.reparentTo(self.render)
        self.motorcycle.model.setPos(self.motorcycle.x, self.motorcycle.y, self.motorcycle.z)
    
    def setup_controls(self):
        """Configura os controles do jogo"""
        # Detectar teclas pressionadas
        self.accept('w', self.set_key, ['w', True])
        self.accept('w-up', self.set_key, ['w', False])
        
        self.accept('s', self.set_key, ['s', True])
        self.accept('s-up', self.set_key, ['s', False])
        
        self.accept('a', self.set_key, ['a', True])
        self.accept('a-up', self.set_key, ['a', False])
        
        self.accept('d', self.set_key, ['d', True])
        self.accept('d-up', self.set_key, ['d', False])
        
        self.accept('space', self.set_key, ['space', True])
        self.accept('space-up', self.set_key, ['space', False])
        
        self.accept('escape', self.quit_game)
        
        # Inicializar dicionário de teclas
        self.keys = {'w': False, 's': False, 'a': False, 'd': False, 'space': False}
    
    def set_key(self, key, value):
        """Registra estado de uma tecla"""
        self.keys[key] = value
    
    def update_game(self, task):
        """Atualiza a lógica do jogo a cada frame"""
        delta_time = globalClock.getDt()
        
        # Limitar delta_time para estabilidade
        if delta_time > 0.016:  # > 60 FPS
            delta_time = 0.016
        
        # Processar entrada
        self.handle_input(delta_time)
        
        # Aplicar física
        self.physics_engine.apply_physics(self.motorcycle, delta_time)
        
        # Atualizar posição do modelo
        self.motorcycle.update_speed()
        self.motorcycle.model.setPos(
            self.motorcycle.x,
            self.motorcycle.y,
            self.motorcycle.z
        )
        
        # Atualizar rotação
        self.motorcycle.model.setHpr(
            self.motorcycle.rotation_y,
            self.motorcycle.rotation_x,
            self.motorcycle.rotation_z
        )
        
        # Atualizar câmera para seguir a mota
        self.update_camera()
        
        # Debug info
        if SHOW_FPS:
            self.show_debug_info()
        
        return Task.cont
    
    def handle_input(self, delta_time):
        """Processa entrada do usuário"""
        # Aceleração
        if self.keys.get('w', False):
            self.physics_engine.apply_acceleration(self.motorcycle, 1)
        
        # Frenagem/Marcha ré
        if self.keys.get('s', False):
            self.physics_engine.apply_brake(self.motorcycle)
        
        # Virada esquerda
        if self.keys.get('a', False):
            self.motorcycle.turn(-1, delta_time)
        
        # Virada direita
        if self.keys.get('d', False):
            self.motorcycle.turn(1, delta_time)
        
        # Pulo (só no chão)
        if self.keys.get('space', False) and self.motorcycle.on_ground:
            self.motorcycle.velocity_y = 15
            self.keys['space'] = False  # Consumir pulo
    
    def update_camera(self):
        """Atualiza posição da câmera para seguir a mota"""
        # Câmera atrás e acima da mota
        angle_rad = math.radians(self.motorcycle.rotation_y)
        
        camera_x = self.motorcycle.x - math.sin(angle_rad) * self.camera_distance
        camera_y = self.motorcycle.y + self.camera_height
        camera_z = self.motorcycle.z - math.cos(angle_rad) * self.camera_distance
        
        # Suavizar movimento da câmera
        current_pos = self.camera.getPos()
        smooth_pos = Point3(
            current_pos.x + (camera_x - current_pos.x) * CAMERA_SMOOTHNESS,
            current_pos.y + (camera_y - current_pos.y) * CAMERA_SMOOTHNESS,
            current_pos.z + (camera_z - current_pos.z) * CAMERA_SMOOTHNESS
        )
        
        self.camera.setPos(smooth_pos)
        
        # Olhar para a mota (um pouco à frente dela)
        look_ahead = 5
        look_x = self.motorcycle.x + math.sin(angle_rad) * look_ahead
        look_z = self.motorcycle.z + math.cos(angle_rad) * look_ahead
        look_y = self.motorcycle.y + 1
        
        self.camera.lookAt(Point3(look_x, look_y, look_z))
    
    def show_debug_info(self):
        """Mostra informações de debug na tela"""
        fps = globalClock.getAverageFrameRate()
        speed = self.motorcycle.speed
        pos = self.motorcycle.get_position()
        
        info = f"""
FPS: {fps:.1f}
Velocidade: {speed:.1f} m/s
Posição: ({pos[0]:.1f}, {pos[1]:.1f}, {pos[2]:.1f})
Rotação: {self.motorcycle.rotation_y:.1f}°
No chão: {'Sim' if self.motorcycle.on_ground else 'Não'}
        """
        
        # Limpar info anterior
        if hasattr(self, 'debug_text'):
            self.debug_text.destroy()
        
        # Mostrar nova info
        from direct.gui.OnscreenText import OnscreenText
        self.debug_text = OnscreenText(
            text=info,
            pos=(-1.3, 0.9),
            scale=0.05,
            fg=(1, 1, 1, 1),
            shadow=(0, 0, 0, 0.5)
        )
    
    def quit_game(self):
        """Sai do jogo"""
        print("Saindo do jogo...")
        self.taskMgr.remove("update_game")
        self.world.cleanup()
        sys.exit()


def main():
    """Função principal"""
    game = MotorcycleGame()
    game.run()


if __name__ == "__main__":
    main()
