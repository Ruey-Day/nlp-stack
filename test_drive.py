#!/usr/bin/env python3
"""
Teleop for mobile_robot using Gazebo topics
Control the robot with WASD keys
"""

import subprocess
import time
import sys
import termios
import tty
import select

class RobotTeleop:
    def __init__(self):
        self.topic = "/model/mobile_robot/cmd_vel"
        self.linear_speed = 0.5
        self.angular_speed = 1.0
        self.settings = None
        
        print("\n" + "="*60)
        print("🎮 MOBILE ROBOT TELEOP")
        print("="*60)
        print(f"\nControl topic: {self.topic}")
        print(f"Initial speed - Linear: {self.linear_speed} m/s, Angular: {self.angular_speed} rad/s")
        
    def send_velocity(self, linear_x=0.0, linear_y=0.0, angular_z=0.0):
        """Send velocity command via Gazebo topic"""
        cmd = [
            "gz", "topic",
            "-t", self.topic,
            "-m", "gz.msgs.Twist",
            "-p", f"linear: {{x: {linear_x}, y: {linear_y}, z: 0.0}}, angular: {{x: 0.0, y: 0.0, z: {angular_z}}}"
        ]
        # Fixed: use stdout and stderr separately, not capture_output
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    def stop(self):
        """Stop the robot"""
        self.send_velocity(0.0, 0.0, 0.0)
    
    def get_key(self):
        """Get single keypress without blocking"""
        if select.select([sys.stdin], [], [], 0.01) == ([sys.stdin], [], []):
            return sys.stdin.read(1)
        return None
    
    def run(self):
        """Main teleop loop"""
        print("\n" + "="*60)
        print("CONTROLS:")
        print("="*60)
        print("""
  Movement:
    W : Forward          Q : Forward + Turn Left
    S : Backward         E : Forward + Turn Right  
    A : Turn Left        Z : Backward + Turn Left
    D : Turn Right       C : Backward + Turn Right
    
  Speed Control:
    + : Increase speed
    - : Decrease speed
    
  Other:
    Space : Emergency STOP
    X     : Exit
        """)
        print("="*60)
        print("\nReady! Press keys to drive...\n")
        
        # Set terminal to raw mode
        self.settings = termios.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin.fileno())
        
        last_key = None
        
        try:
            while True:
                key = self.get_key()
                
                if key and key != last_key:
                    last_key = key
                    
                    # Forward/Backward
                    if key.lower() == 'w':
                        print(f"\r⬆️  FORWARD {self.linear_speed:.1f} m/s         ", end='', flush=True)
                        self.send_velocity(linear_x=self.linear_speed)
                        
                    elif key.lower() == 's':
                        print(f"\r⬇️  BACKWARD {self.linear_speed:.1f} m/s        ", end='', flush=True)
                        self.send_velocity(linear_x=-self.linear_speed)
                        
                    # Turning
                    elif key.lower() == 'a':
                        print(f"\r↪️  TURN LEFT {self.angular_speed:.1f} rad/s    ", end='', flush=True)
                        self.send_velocity(angular_z=self.angular_speed)
                        
                    elif key.lower() == 'd':
                        print(f"\r↩️  TURN RIGHT {self.angular_speed:.1f} rad/s   ", end='', flush=True)
                        self.send_velocity(angular_z=-self.angular_speed)
                        
                    # Combined movements
                    elif key.lower() == 'q':
                        print(f"\r↖️  FORWARD LEFT                ", end='', flush=True)
                        self.send_velocity(linear_x=self.linear_speed, angular_z=self.angular_speed)
                        
                    elif key.lower() == 'e':
                        print(f"\r↗️  FORWARD RIGHT               ", end='', flush=True)
                        self.send_velocity(linear_x=self.linear_speed, angular_z=-self.angular_speed)
                        
                    elif key.lower() == 'z':
                        print(f"\r↙️  BACKWARD LEFT               ", end='', flush=True)
                        self.send_velocity(linear_x=-self.linear_speed, angular_z=self.angular_speed)
                        
                    elif key.lower() == 'c':
                        print(f"\r↘️  BACKWARD RIGHT              ", end='', flush=True)
                        self.send_velocity(linear_x=-self.linear_speed, angular_z=-self.angular_speed)
                        
                    # Stop
                    elif key == ' ':
                        print(f"\r🛑 STOP                         ", end='', flush=True)
                        self.stop()
                        
                    # Speed control
                    elif key == '+' or key == '=':
                        self.linear_speed = min(2.0, self.linear_speed + 0.1)
                        self.angular_speed = min(3.0, self.angular_speed + 0.1)
                        print(f"\r⚡ SPEED UP - Linear: {self.linear_speed:.1f}, Angular: {self.angular_speed:.1f}   ", end='', flush=True)
                        
                    elif key == '-' or key == '_':
                        self.linear_speed = max(0.1, self.linear_speed - 0.1)
                        self.angular_speed = max(0.1, self.angular_speed - 0.1)
                        print(f"\r🐌 SPEED DOWN - Linear: {self.linear_speed:.1f}, Angular: {self.angular_speed:.1f}   ", end='', flush=True)
                        
                    # Exit
                    elif key.lower() == 'x':
                        print("\r🏁 EXITING...                   ")
                        self.stop()
                        break
                        
                    elif key == '\x03':  # Ctrl+C
                        break
                
                time.sleep(0.01)
                
        except Exception as e:
            print(f"\n❌ Error: {e}")
            
        finally:
            self.stop()
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
            print("\n\n✓ Robot stopped. Goodbye!\n")


def main():
    print("\n" + "="*60)
    print("🤖 GAZEBO MOBILE ROBOT TELEOP")
    print("="*60)
    print()
    
    print("✓ Starting teleop (skipping Gazebo check)...")
    print("  Make sure Gazebo is running with the robot spawned!\n")
    
    # Run teleop
    teleop = RobotTeleop()
    teleop.run()


if __name__ == '__main__':
    main()