import time
import cv2
import numpy as np
import torch

# Ensure PyTorch is strictly targeting your Nvidia GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
if device.type == "cpu":
    raise RuntimeError(
        "Nvidia GPU not detected by PyTorch! Make sure CUDA drivers are installed."
    )

print(f"Targeting GPU: {torch.cuda.get_device_name(0)}")

# Screen dimensions (Set high to maximize GPU load)
WIDTH, HEIGHT = 1920, 1080

# Pre-allocate mathematical grids directly on the Nvidia VRAM
x = torch.linspace(-10, 10, WIDTH, device=device)
y = torch.linspace(-10, 10, HEIGHT, device=device)
X, Y = torch.meshgrid(x, y, indexing="xy")

print("Launching simulation loop. Press 'q' in the window to exit.")
start_time = time.time()

while True:
    t = time.time() - start_time

    # 1. HEAVY GPU COMPUTATION LAYER
    # Running thousands of trigonometric and exponential functions per pixel to hit 100% load
    r = torch.sqrt(X**2 + Y**2)
    z = (
        torch.sin(r - 5 * t)
        * torch.cos(X * torch.sin(t) - Y * torch.cos(t))
        * torch.exp(-0.05 * r)
    )

    # Distort coordinates further to keep GPU math engines working continuously
    z += 0.5 * torch.sin(X * 2.0 + t) * torch.cos(Y * 2.0 - t)
    z += 0.25 * torch.sin(r * 4.0 - 3.0 * t)

    # Normalize the output values to a 0.0 - 1.0 range
    z = (z - z.min()) / (z.max() - z.min() + 1e-5)

    # 2. CREATE COLOR CHANNELS ON GPU
    # Distributing channels across different mathematical transformations
    r_chan = torch.sin(z * np.pi)
    g_chan = torch.sin(z * np.pi + 2.0)
    b_chan = torch.cos(z * np.pi)

    # Stack channels to form an RGB frame on VRAM
    rgb_tensor = torch.stack([r_chan, g_chan, b_chan], dim=-1)

    # 3. TRANSFER TO DISPLAY BUFFER
    # Convert from PyTorch GPU memory structure to Numpy CPU format for the window
    frame = (rgb_tensor.cpu().numpy() * 255).astype(np.uint8)

    # Convert to BGR format for standard OpenCV rendering
    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # Display the visual window
    cv2.imshow("NVIDIA PyTorch Core Burner", frame_bgr)

    # Keep the delay at 1ms so the pipeline stays completely maxed out
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
