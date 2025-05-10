#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
import math
import time

class PositionCommandPublisher(Node):
    def __init__(self):
        super().__init__('position_command_publisher')
        
        # Crea un publisher para enviar comandos de posición
        self.publisher_ = self.create_publisher(
            Float64MultiArray, 
            '/position_controller/commands', 
            10)
        
        # Timer para publicar comandos periódicamente (cada 0.1 segundos)
        self.timer = self.create_timer(0.1, self.timer_callback)
        
        # Variables para seguimiento
        self.start_time = time.time()

    def timer_callback(self):
        """Función que se llama periódicamente para publicar nuevos comandos"""
        elapsed = time.time() - self.start_time
        
        # Crea un patrón de movimiento (por ejemplo, un movimiento sinusoidal)
        pos1 = 1.0 * math.sin(0.5 * elapsed)  # Movimiento sinusoidal para joint1
        pos2 = 0.5 * math.sin(0.7 * elapsed)  # Movimiento sinusoidal para joint2
        
        # Crea el mensaje
        msg = Float64MultiArray()
        msg.data = [pos1, pos2]
        
        # Publica el mensaje
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publicando: [{pos1:.2f}, {pos2:.2f}]')

def main():
    rclpy.init()
    
    publisher = PositionCommandPublisher()
    
    try:
        rclpy.spin(publisher)
    except KeyboardInterrupt:
        publisher.get_logger().info('Detenido mediante teclado')
    finally:
        # Detener el robot al finalizar enviando posición 0
        stop_msg = Float64MultiArray()
        stop_msg.data = [0.0, 0.0]
        publisher.publisher_.publish(stop_msg)
        
        # Limpieza
        publisher.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
