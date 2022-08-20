import asyncio
from kasa import SmartBulb
import time

# bulb = SmartBulb("129.97.71.104")

IP = "192.168.0.170"
async def get_bulb():
    bulb = SmartBulb(IP)
    return bulb

async def set_bulb():
    res = get_bulb()
    bulb = await res
    await bulb.update()
    assert bulb.is_bulb
    await bulb.turn_off()
    time.sleep(3)
    for i in range (6):
        await bulb.set_hsv(180, 100, 80)
        await bulb.update()
        time.sleep(1)
        # for j in range(500000):
        #     print('hello')
        # await bulb.turn_off()
        await bulb.set_hsv(0, 100, 80)
        time.sleep(1)

        await bulb.set_hsv(0, 0, 100)
        time.sleep(1)
        await bulb.update()
    await bulb.turn_off()

if __name__ == '__main__':
    asyncio.run(set_bulb())
