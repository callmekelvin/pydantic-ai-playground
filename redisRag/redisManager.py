from redisvl.index import AsyncSearchIndex
from redis.asyncio import Redis
from redisvl.query import VectorQuery
from dataclasses import dataclass

import os

@dataclass
class GodotDocFile:
    parent_folder: str
    file_name: str
    file_contents: str
    user_embedding: bytes
    
class RedisManager:
    _instance = None
    _client = None
    _index = None

    def __init__(self):
        if RedisManager._instance is not None:
            return
        
        RedisManager._instance = self

    async def createRedisConnection(self):
        try:
            self._client = Redis.from_url("redis://localhost:6379")

            redisSchemaPath = os.path.join(os.getcwd(), 'schema.yaml')
            self._index = AsyncSearchIndex.from_yaml(redisSchemaPath, redis_client=self._client, validate_on_load=True)
            await self._index.create()
            return

        except Exception as e:
            print("RedisManager.createRedisConnection Error - Error creating connection/ index", str(e))
            raise e

    async def addKeys(self, data: list[GodotDocFile], id_field = None):
        try:
            await self._index.load(data, id_field=id_field)
            return
        
        except Exception as e:
            print("RedisManager.addKeys Error - Error loading Redis data", str(e))
            raise e


    async def query(self, vector, noResults, fieldsToReturn=["parent_folder", "file_name", "file_contents"]):
        try:
            query = VectorQuery(
                vector=vector,
                vector_field_name="user_embedding",
                return_fields=fieldsToReturn,
                num_results=noResults
            )

            results = await self._index.query(query)
            # print(results)

            return results

        except Exception as e:
            print("RedisManager.query Error - Error querying Redis VL", str(e))
            raise e

    async def cleanRedisVectorDatabase(self):
        try:
            index_exists = await self._index.exists()

            if (index_exists):
                await self._index.delete(drop=True)

        except Exception as e:
            print("RedisManager.cleanRedisVectorDatabase Error - Error clearing database", str(e))
            raise e
