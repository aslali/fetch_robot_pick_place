import asyncio
from kasa import SmartBulb
import time

# bulb = SmartBulb("129.97.71.104")

IP = "129.97.71.118"
async def get_bulb():
    bulb = SmartBulb(IP)
    return bulb

async def set_bulb():
    res = get_bulb()
    bulb = await res
    await bulb.update()
    assert bulb.is_bulb
    await bulb.turn_on()
    cur_hsv = [0, 0, 100]
    with open("lamp_stat.txt", "w") as f:
        for s in cur_hsv:
            f.write(str(s) + "\n")
    await bulb.set_hsv(cur_hsv[0], cur_hsv[1], cur_hsv[2])
    time.sleep(3)
    while True:

        try:
            with open("lamp_stat.txt", "r") as f:
                tmp_hsv = []
                for line in f:
                    tmp_hsv.append(int(line.strip()))
        except:
            print(tmp_hsv)
            tmp_hsv = cur_hsv

        if (tmp_hsv != cur_hsv) and (len(tmp_hsv) == 3):
            cur_hsv = tmp_hsv
            await bulb.set_hsv(cur_hsv[0], cur_hsv[1], cur_hsv[2])
            await bulb.update()
    await bulb.turn_off()

if __name__ == '__main__':
    asyncio.run(set_bulb())