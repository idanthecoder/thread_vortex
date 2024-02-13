import asyncio
import time


async def brew_coffee():
    print("Start brew_coffee()")
    await asyncio.sleep(3)
    print("End brew_coffee()")
    return "Coffee ready"


async def toast_bagel():
    print("Start toast_bagel()")
    await asyncio.sleep(3)
    print("End toast_bagel()")
    return "Bagel toasted"


async def main():
    start_time = time.time()

    #batch = asyncio.gather(brew_coffee(), toast_bagel())
    #result_coffee, result_bagel = await batch

    coffee_task = asyncio.create_task(brew_coffee())
    toast_task = asyncio.create_task(toast_bagel())

    result_coffee = await coffee_task
    result_bagel = await toast_task

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Result of brew_coffee: {result_coffee}")
    print(f"Result of toast_bagel: {result_bagel}")
    print(f"Total execution time: {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main())
