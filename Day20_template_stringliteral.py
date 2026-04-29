variety = 'silicon'
template = t'Try some {variety}!'
print(type(template))
print(list(template))

from compression import zstd
import math

data = str(math.pi).encode() * 20
compressed = zstd.compress(data)
ratio = len(compressed) / len(data)
print(f"Achieved compression ratio of {ratio}")



import asyncio

async def play_track(track):
    await asyncio.sleep(5)
    print(f'🎵 Finished: {track}')

async def play_album(name, tracks):
    async with asyncio.TaskGroup() as tg:
        for track in tracks:
            tg.create_task(play_track(track), name=track)

async def main():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(
          play_album('Sundowning', ['TNDNBTG', 'Levitate']),
          name='Sundowning')
        tg.create_task(
          play_album('TMBTE', ['DYWTYLM', 'Aqua Regia']),
          name='TMBTE')

if __name__ == '__main__':
    asyncio.run(main())

