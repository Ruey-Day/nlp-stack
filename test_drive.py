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
        print("MOBILE ROBOT TELEOP")
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
        print("\n" + "="*60)
        print("INCREMENTAL CONTROLS:")
        print("="*60)
        print("""
    W : +Forward
    S : -Forward
    A : +Turn Left
    D : -Turn Left (Turn Right)

    Q : +Forward  +Left
    E : +Forward  -Left
    Z : -Forward  +Left
    C : -Forward  -Left

    Space : STOP
    Ctrl+C: Exit
        """)
        print("="*60)

        # velocity state
        self.vx = 0.0
        self.vy = 0.0
        self.wz = 0.0

        step_lin = 0.1
        step_ang = 0.1

        self.settings = termios.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin.fileno())

        try:
            while True:
                key = self.get_key()
                if not key:
                    continue

                # FORWARD / BACKWARD
                if key.lower() == 'w':
                    self.vx += step_lin

                elif key.lower() == 's':
                    self.vx -= step_lin

                # TURNING (left positive)
                elif key.lower() == 'a':
                    self.wz += step_ang

                elif key.lower() == 'd':
                    self.wz -= step_ang

                # COMBINED
                elif key.lower() == 'q':
                    self.vx += step_lin
                    self.wz += step_ang

                elif key.lower() == 'e':
                    self.vx += step_lin
                    self.wz -= step_ang

                elif key.lower() == 'z':
                    self.vx -= step_lin
                    self.wz += step_ang

                elif key.lower() == 'c':
                    self.vx -= step_lin
                    self.wz -= step_ang

                # STOP
                elif key == ' ':
                    self.vx = self.vy = self.wz = 0.0
                
                # clamp for safety
                self.vx = max(-2.0, min(2.0, self.vx))
                self.wz = max(-3.0, min(3.0, self.wz))

                # send command
                self.send_velocity(
                    linear_x=self.vx,
                    linear_y=self.vy,
                    angular_z=self.wz
                )

                print(
                    f"\rVx: {self.vx:+.2f} m/s | Wz: {self.wz:+.2f} rad/s     ",
                    end='', flush=True
                )

                time.sleep(0.01)

        except KeyboardInterrupt:
            print("\n\nCtrl+C detected — stopping robot")

        finally:
            self.stop()
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
            print("✓ Robot stopped cleanly\n")

def main():
    print("\n" + "="*60)
    print("GAZEBO MOBILE ROBOT TELEOP")
    print("="*60)
    print()
    
    print("✓ Starting teleop (skipping Gazebo check)...")
    print("  Make sure Gazebo is running with the robot spawned!\n")
    
    # Run teleop
    teleop = RobotTeleop()
    teleop.run()


if __name__ == '__main__':
    main()