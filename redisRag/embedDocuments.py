import threading
import os
import shutil

import numpy as np
from dataclasses import asdict
import asyncio

from redisManager import RedisManager, GodotDocFile
from llamaCppEmbeddingModel import embedder

from chunkDocuments import getThreadPartitionSizes

godot_chunked_folder_name = "godot-docs-chunked"

def embedDocuments():
    """
    Embed documents in parallel using multiple threads
    """

    # Obtain files to embed
    filesToEmbed = prepareToEmbedDocuments()

    numOfDocuments = len(filesToEmbed)
    noThreads = 4
    threadPartitions = getThreadPartitionSizes(numOfDocuments, noThreads)

    threads = []
    threadNo = 0
    for partitions in threadPartitions:
        t = threading.Thread(target=embedDocumentsChildThread, 
                             kwargs={ "workList": filesToEmbed[partitions[0]: partitions[1]], "threadNo": threadNo }
                            )
        threads.append(t)
        threadNo += 1

    # Start each thread
    for t in threads:
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    return

def prepareToEmbedDocuments():
    """
    Retrieve List of File Names which contents need to be embedded
    """

    current_working_dir = os.getcwd()
    godot_chunked_folder_path = os.path.join(current_working_dir, godot_chunked_folder_name)

    filesToEmbed = []
    for root, dir, files in os.walk(godot_chunked_folder_path):
        for file in files:
            filesToEmbed.append(os.path.join(root, file))

    # print(filesToEmbed)
    return filesToEmbed

async def embedDocumentUnitOfWork(redis, work):
    """
    Open a file, read its contents, embed the text using a model, and store the embeddings in Redis
    """

    # Open and Read File Contents
    file_contents = ""
    with open(work, 'r') as file:
        file_contents = file.read()

    file.close()

    # Embed Documents
    # Bottleneck: Depends on how fast LLama Embedding Model Server can respond
    embedResult = await embedder.embed_documents(
        [file_contents]
    )

    # print(embedResult)
    # print(embedResult[0])

    embeddedDoc = asdict(
        GodotDocFile(
                parent_folder = os.path.dirname(work),
                file_name = os.path.basename(work),
                file_contents = file_contents,
                user_embedding = np.array(embedResult[0], dtype=np.float32).tobytes()
            )
        )
    
    # print(embeddedDoc)

    # Save Embedded Document to Redis
    await redis.addKeys([embeddedDoc], id_field="file_name")

    return

async def embedDocumentsChildTask(workList):
    # Create Redis Connection for each Thread to prevent connection bottleneck
    redis = RedisManager()
    await redis.createRedisConnection()

    for work in workList:
        await embedDocumentUnitOfWork(redis, work)

    return

def embedDocumentsChildThread(workList, threadNo):
    asyncio.run(embedDocumentsChildTask(workList))

    print(f"Thread {threadNo}: Work Complete")
    return

# embedDocuments()