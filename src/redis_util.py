import redis.asyncio as red

# Async redis acces 

async def get_redis():
    return await red.from_url("redis://localhost:6379", decode_responses=True)


async def update_context(user_id: str | int, user_content: str, ai_content: str):
    redis = await get_redis()
    history_key = f'user:{user_id}:context'
    await redis.rpush(history_key, user_content, ai_content) 
    await redis.ltrim(history_key, -20, -1) #limit 20 last msg


async def get_context(user_id: str | int):
    redis = await get_redis()
    history_key = f'user:{user_id}:context'
    messages = await redis.lrange(history_key, 0, -1)  # all msgs in memory
    # to deepseek
    formatted_messages = [{"role": "user", "content": msg} if i % 2 == 0 else {"role": "assistant", "content": msg}
                          for i, msg in enumerate(messages)]
    
    return formatted_messages

    
    
