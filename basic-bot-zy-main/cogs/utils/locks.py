import asyncio

class Locks:
    def __init__(self):
        self.locks = {}
        self.main_lock = asyncio.Lock()

    async def get_lock(self, user_id):
        async with self.main_lock:
            if not user_id in self.locks:
                self.locks[user_id] = asyncio.Lock()

            return self.locks[user_id]


lock_manager = Locks()
