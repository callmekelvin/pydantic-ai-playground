## Pydantic + Redis Vector Database as RAG

## Instructions to Run

1. Start Redis Docker Containers - `docker compose up -d`
2. Start Llama.cpp Embedding Server
    - Embedding Server: `llama-server -m "<EMBEDDING_GGUF_FILE_NAME_AND_PATH>" --port 9090 --embedding`
3. Update `schema.yml` to the Number of Embedding Demnsions supported by the Embedding Model
    ```
    # Note: Vector Embedding Dimensions depends on Embedding Model
    # Ex. Qwen3-Embedding-0.6B = 1024 Dimensions
    - name: user_embedding
      type: vector
      attrs:
        algorithm: flat
        dims: 1024
        distance_metric: cosine
        datatype: float32
    ```
4. Install `uv` Python Package Manager Framework
5. To retrieve the Godot Documentation and to build the Redis VL, run: `uv run prepareRAGStore.py`
    - Embedding takes a long time, on an AMD RX-6700XT GPU, it takes 45 minutes for embedding to complete
7. Start Llama.cpp Chat Model Server
    - Chat Model Server: `llama-server -m "<CHAT_MODEL_GGUF_FILE_NAME_AND_PATH>" --port 8080`
8. Run the Chat Agent: `uv run godotChat.py`

<hr>

## Redis Backups

As embedding takes a long time, it makes sense to save a copy of the Redis VL state when embeddings are populated to prevent having to re-embed documents each time.

Saving Redis Snapshot (RDB File) from Docker to Local Directory
1. `docker exec -it redis_container redis-cli SAVE` or `docker exec -it redis_container redis-cli --rdb /data/dump.rdb`
2. `docker cp redis_container:/data/dump.rdb ./dump.rdb`

<br>

Currently, the Redis VL Database features a docker volume bind mount with the `redis_data` folder
- Hence, on termination of session, it will overwrite and save Redis Snapshot in this `redis_data` folder
- A Backup RDB File has been saved under `redis_db_dump_with_embeddings.rdb`, which can be renamed and copied into `redis_data` as `dump.rdb` to restore the existing Embedded Documents

<br>

To start from a fresh Redis DB Instance, run the following in a Python Script:
```
async def cleanDatabase():
    redis = RedisManager()
    await redis.createRedisConnection()
    await redis.cleanRedisVectorDatabase()

asyncio.run(cleanDatabase())
```

<hr>

## Resources

- https://pydantic.dev/docs/ai/examples/data-analytics/rag/
- https://pydantic.dev/docs/ai/guides/embeddings/#_top
- https://redis.io/docs/latest/develop/ai/redisvl/

<hr>

## Retrieval Augmented Generation (RAG) Steps:
1. Prepare raw documents (Ex. Text, Files, Images, etc)
    - Collect , clean, normalise data/ documents and add metadata, etc
2. Chunking you raw documents (Optional for Small Documents)
    - Chunking is the process of partitioning large documents into smaller chunks, which would be then be vector embedded
    - Chunking allows for higher precision matches/ retrieval when vector embedded, allowing for better partial matching within documents
3. Select Embedding Model
    - Choose Embedding Model depending on your use case (Ex. Text, Files, Images, etc)
4. Create Vector Embedding Database
5. Populate the Vector Embedding Database with Vector Embedding Entries
    - This database will contain vector embeddings of chunks/ raw documents
6. In order to query the Vector Embedding Database, you will need to vector embed your Text Query
    - You will then be returned the closest documents/ chunks to the vector embedded Text Query in the vector space
    - You can also build a Vector Index (ANN Data Structures) to speed up Vector Embed Queries

<hr>