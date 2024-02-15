import psutil
from functools import partial
import time


class ProcessMonitor:


    def status(self, env_dir: str):

        status = []

        fun = partial(ProcessMonitor.filter_by_exe, env_dir)


        for p in filter(fun, psutil.process_iter()):

            process_info = {
                "status": p.status(),
                "name": p.name(),
                "pid": p.pid,
                "exec": p.exe(),
                "cmd": p.cmdline(),
            }
            status.append(process_info)

        return status

    def terminate(self, env_dir: str):
        terminated = []
        fun = partial(ProcessMonitor.filter_by_exe, env_dir)
        for p in filter(fun, psutil.process_iter()):
            p.terminate()
            terminated.append(f"{p.pid} - {p.name()}")
        
        return terminated
    

    def kill(self, env_dir: str):
        terminated = []
        fun = partial(ProcessMonitor.filter_by_exe, env_dir)
        running = False
        for p in filter(fun, psutil.process_iter()):
            if p.is_running():
                running = True

        if running:
            time.sleep(3)

        for p in filter(fun, psutil.process_iter()):
            p.kill()
            terminated.append(f"{p.pid} - {p.name()}")

        return terminated


    @classmethod
    def filter_by_exe(cls, env_dir, p):
        try:
            if p.exe().startswith(env_dir):
                return True
        except:
            pass
        return False
