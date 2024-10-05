import subprocess
import time
import os
import sys

job_id = sys.argv[1]

def get_requested_walltime(job_id):
    print(job_id)
    command = f'qstat -f {job_id} | grep "Resource_List.walltime"'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    walltime_str = result.stdout.strip().split('=')[-1].strip()
    print(walltime_str)
    h, m, s = map(int, walltime_str.split(':'))
    return h * 3600 + m * 60 + s

def send_email_alert(job_id, user_email="mt1210236@iitd.ac.in"):
    subject = f"Low GPU Utilization Alert for Job {job_id}"
    body = f"The GPU utilization for your job {job_id} has been under 25% for too long. The job is being monitored."
    
    command = f'echo "{body}" | mailx -s "{subject}" {user_email}'
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Alert email sent to {user_email} regarding job {job_id}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to send email: {e}")

def get_gpu_utilization():
    command = 'nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    gpu_util = int(result.stdout.strip())
    return gpu_util

def kill_job(job_id):
    print(f"Killing job {job_id} due to GPU underutilization.")
    subprocess.run(f"qdel {job_id}", shell=True)

def monitor_gpu(job_id, interval=5):
    walltime_seconds = get_requested_walltime(job_id)
    max_underutilization_time = walltime_seconds * 0.20
    underutilized_time = 0
    total_runtime = 0

    print(f"Monitoring GPU usage for job {job_id}...")

    while total_runtime < walltime_seconds:
        gpu_util = get_gpu_utilization()
        print(f"GPU Utilization: {gpu_util}%")

        if gpu_util < 25:
            underutilized_time += interval
        else:
            underutilized_time = 0

        if underutilized_time > max_underutilization_time:
            print("Ending Job")
            # kill_job(job_id) # uncomment to actually use this script to end jobs
            break

        total_runtime += interval
        time.sleep(interval)

    print(f"Job {job_id} finished or walltime expired.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python gpu_util.py <job_id>")
        sys.exit(1)

    monitor_gpu(job_id)
