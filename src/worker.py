from arq.connections import RedisSettings


REDIS_SETTINGS = RedisSettings("redis")


async def startup(ctx):
    pass


async def shutdown(ctx):
    pass


async def test(ctx):
    print("test")


class WorkerSettings:
    functions = [test]
    on_startup = startup
    on_shutdown = shutdown
    redis_settings = REDIS_SETTINGS
