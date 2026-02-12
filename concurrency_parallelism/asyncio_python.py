import time

import asyncio
async def call_api(name,delay):
    print(f'calling the api {name} will take {delay}')
    await asyncio.sleep(delay)
    print(f' api {name}responded {delay}')
    return f'{name}_data'

async def main():
    start = time.perf_counter()
    background_job = asyncio.create_task(call_api('start', 10))
    results=await asyncio.gather(
         call_api('order', 2),
         call_api('user', 4),
         call_api('deliver', 6),
    )
    #result_1 = await background_job
    result_1 = ''
    return [results,  result_1]
if __name__ == '__main__':
    result = asyncio.run(main())
    print(result)
