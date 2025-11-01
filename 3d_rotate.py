from ursina import *
import serial, time

# === Bluetooth setup (optional) ===
try:
    bluetooth = serial.Serial('COM7', 9600, timeout=0.1)  # Change COM port
    time.sleep(2)
    print("✅ Bluetooth Connected.")
except Exception as e:
    print("Bluetooth connection failed:", e)
    bluetooth = None

# === Ursina setup ===
app = Ursina()
window.title = "3D Cube Manual Rotation"
window.borderless = False
window.fullscreen = False
window.fps_counter.enabled = True

# Environment
Sky()
ground = Entity(model='plane', scale=50, texture='white_cube', texture_scale=(50,50),
                color=color.rgb(100,150,100), collider='box')
DirectionalLight(direction=(1,-1,-1), shadows=True)

# === Cube ===
cube = Entity(
    model='cube',
    scale=2,
    color=color.orange,   # Base color / visible
    position=(0,2,5),    # Moved further from the camera along Z
    collider='box'
)

# Camera setup
camera.position = (0, 5, -12)  # Camera stays in the same place
camera.rotation_x = 20

# Movement / rotation variables
move_speed = 5
rotate_speed = 60
jump_height = 0.35
is_jumping = False
velocity_y = 0
gravity = 0.02

# --- Movement & rotation function ---
def move_or_rotate(command):
    global is_jumping, velocity_y

    if command == "FORWARD":
        cube.z -= move_speed * time.dt
    elif command == "BACKWARD":
        cube.z += move_speed * time.dt
    elif command == "LEFT":
        cube.x -= move_speed * time.dt
    elif command == "RIGHT":
        cube.x += move_speed * time.dt
    elif command == "ROTATE_LEFT":
        cube.rotation_y += rotate_speed * time.dt
    elif command == "ROTATE_RIGHT":
        cube.rotation_y -= rotate_speed * time.dt
    elif command == "ROTATE_UP":
        cube.rotation_x += rotate_speed * time.dt
    elif command == "ROTATE_DOWN":
        cube.rotation_x -= rotate_speed * time.dt
    elif command == "ROLL_LEFT":
        cube.rotation_z += rotate_speed * time.dt
    elif command == "ROLL_RIGHT":
        cube.rotation_z -= rotate_speed * time.dt
    elif command == "JUMP" and not is_jumping:
        velocity_y = jump_height
        is_jumping = True

# --- Update loop ---
def update():
    global is_jumping, velocity_y

    # Bluetooth commands
    if bluetooth and bluetooth.in_waiting > 0:
        try:
            command = bluetooth.readline().decode().strip()
            if command:
                move_or_rotate(command)
        except:
            pass

    # Keyboard controls
    if held_keys['w']:
        move_or_rotate("ROTATE_UP")
    if held_keys['s']:
        move_or_rotate("ROTATE_DOWN")
    if held_keys['a']:
        move_or_rotate("ROTATE_LEFT")
    if held_keys['d']:
        move_or_rotate("ROTATE_RIGHT")
    if held_keys['q']:
        move_or_rotate("ROLL_LEFT")
    if held_keys['e']:
        move_or_rotate("ROLL_RIGHT")
    if held_keys['space']:
        move_or_rotate("JUMP")

    # Gravity / jump
    if is_jumping:
        cube.y += velocity_y
        velocity_y -= gravity
        if cube.y <= 2:  # Base position above ground
            cube.y = 2
            is_jumping = False
            velocity_y = 0

    camera.look_at(cube.position + Vec3(0,1,0))

app.run()

