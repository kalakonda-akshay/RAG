"""
System Hardware Monitoring Module (CPU, RAM).
"""
import psutil


def get_system_stats() -> dict:
    """
    Returns CPU percentage, RAM percentage, and RAM available in GB.
    """
    try:
        cpu_percent = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory()
        return {
            "cpu_percent": cpu_percent,
            "ram_percent": mem.percent,
            "ram_used_gb": round((mem.total - mem.available) / (1024 ** 3), 2),
            "ram_total_gb": round(mem.total / (1024 ** 3), 2),
        }
    except Exception:
        return {
            "cpu_percent": 0.0,
            "ram_percent": 0.0,
            "ram_used_gb": 0.0,
            "ram_total_gb": 0.0,
        }
