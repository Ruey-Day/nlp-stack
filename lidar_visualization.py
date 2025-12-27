import subprocess
import threading
import numpy as np
import matplotlib.pyplot as plt
import time

LIDAR_TOPIC = "/model/mobile_robot/scan"
NUM_SAMPLES = 640

ranges = np.zeros(NUM_SAMPLES)
lock = threading.Lock()


def read_lidar():
    """
    Read ranges from gz.msgs.LaserScan in text mode.
    """
    global ranges
    cmd = ["gz", "topic", "-e", "-t", LIDAR_TOPIC]

    print(f"[DEBUG] Starting subprocess with command: {' '.join(cmd)}")
    
    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        print("[DEBUG] Subprocess started successfully")
    except Exception as e:
        print(f"[ERROR] Failed to start subprocess: {e}")
        return

    range_values = []
    message_count = 0
    
    print("[DEBUG] Starting to read lines from subprocess...")
    
    for line in proc.stdout:
        line = line.strip()
        
        # Look for lines that start with "ranges:"
        if line.startswith("ranges:"):
            # Extract the value after "ranges: "
            value_str = line.split("ranges:", 1)[1].strip()
            
            try:
                value = float(value_str)
                range_values.append(value)
                
                # When we have collected NUM_SAMPLES ranges, update the array
                if len(range_values) == NUM_SAMPLES:
                    message_count += 1
                    
                    with lock:
                        ranges[:] = np.array(range_values, dtype=np.float32)
                        # Replace inf with 0
                        ranges[np.isinf(ranges)] = 0.0
                        ranges[np.isnan(ranges)] = 0.0
                        
                        valid_count = np.sum((ranges > 0.1) & (ranges < 10.0))
                        
                        if message_count <= 5 or message_count % 10 == 0:
                            print(f"[DEBUG] Message {message_count}: {valid_count} valid points, "
                                  f"min: {ranges[ranges > 0].min():.3f}, "
                                  f"max: {ranges[ranges < 10].max():.3f}, "
                                  f"mean: {ranges[ranges > 0].mean():.3f}")
                    
                    # Reset for next message
                    range_values = []
                    
            except ValueError:
                # Handle 'inf' or 'nan' strings
                if value_str == "inf":
                    range_values.append(float('inf'))
                elif value_str == "nan":
                    range_values.append(float('nan'))
                else:
                    print(f"[WARNING] Could not parse: {value_str}")
    
    print("[DEBUG] Subprocess stdout closed")


def main():
    print("[MAIN] Starting LiDAR reader thread...")
    threading.Thread(target=read_lidar, daemon=True).start()
    
    # Give thread time to get first data
    print("[MAIN] Waiting 2 seconds for initial data...")
    time.sleep(2)

    # Angles for your URDF lidar: -3.14 to 3.14 with 640 samples
    angles = np.linspace(-np.pi, np.pi, NUM_SAMPLES)
    print(f"[MAIN] Angles array created: {len(angles)} angles from {angles[0]:.3f} to {angles[-1]:.3f}")

    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 10))
    sc = ax.scatter([], [], s=2, c='blue')
    ax.set_aspect("equal")
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_title("2D LiDAR View (Top-Down)")
    ax.set_xlabel("X [m]")
    ax.set_ylabel("Y [m]")
    ax.grid(True, alpha=0.3)
    
    # Add a small red dot at the origin to show robot position
    ax.plot(0, 0, 'ro', markersize=8, label='Robot')
    ax.legend()
    
    print("[MAIN] Plot window created, starting visualization loop...")

    loop_count = 0
    last_update_time = time.time()
    
    while True:
        loop_count += 1
        
        with lock:
            r = ranges.copy()

        # Filter valid ranges
        valid = (r > 0.1) & (r < 10.0) & ~np.isnan(r) & ~np.isinf(r)
        valid_count = np.sum(valid)
        
        current_time = time.time()
        if current_time - last_update_time > 2.0:  # Print every 2 seconds
            print(f"[MAIN] Loop {loop_count}: {valid_count} valid points out of {NUM_SAMPLES}")
            if valid_count > 0:
                print(f"[MAIN] Valid range stats - min: {r[valid].min():.3f}, max: {r[valid].max():.3f}")
            last_update_time = current_time
        
        if np.any(valid):
            x = r[valid] * np.cos(angles[valid])
            y = r[valid] * np.sin(angles[valid])
            sc.set_offsets(np.c_[x, y])

        plt.draw()
        plt.pause(0.05)


if __name__ == "__main__":
    print("="*60)
    print("LiDAR Viewer - Gazebo Topic Echo Mode")
    print("="*60)
    try:
        main()
    except KeyboardInterrupt:
        print("\n[MAIN] LiDAR viewer closed by user.")
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()