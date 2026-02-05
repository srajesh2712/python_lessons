import time

import asyncio
async def call_api(name,delay):
    print(f'calling the api {name} will take {delay}')
    await asyncio.sleep(delay)
    print(f' api {name}responded {delay}')
    return f'{name}_data'

if __name__ == '__main__':
    start = time.perf_counter()
    call_api('order',2)
    call_api('user',4)
    call_api('deliver',6)