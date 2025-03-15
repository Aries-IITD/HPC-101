import torch
import time
import sys

#samajhdaar ko variable names hee kaafi hai

def keep_gpu_busy(device="cuda", tensor_size=8192 * 4, sleep_time=0.01):
    if not torch.cuda.is_available():
        print("CUDA is not available. Exiting.")
        return
    
    device = torch.device(device)
    print(f"Using device: {device}")

    torch.ones((tensor_size, tensor_size), device=device).mm(torch.ones((tensor_size, tensor_size), device=device))
    torch.cuda.synchronize()

    print("Starting dummy computations to keep GPU utilization high...")

    try:
        while True:
            A = torch.randn((tensor_size, tensor_size), device=device)
            B = torch.randn((tensor_size, tensor_size), device=device)
            C = A @ B
            torch.cuda.synchronize()
            time.sleep(sleep_time)

    except KeyboardInterrupt:
        print("Stopping GPU workload.")

if __name__ == "__main__":
    try:
        gpu_id = int(sys.argv[1])
    except:
        gpu_id = 0
    keep_gpu_busy()
