from concurrent.futures import ThreadPoolExecutor, as_completed, wait
from tqdm import tqdm 

class Parallel:
    def __init__(self, max_workers=32):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.jobs = []
    def add(self, f):
        future = self.executor.submit(f)
        self.jobs.append(future)
    def wait(self):
        pbar = tqdm(range(len(self.jobs)))
        for _ in as_completed(self.jobs):
            pbar.update()
        # wait(self.jobs)
        self.jobs = []
