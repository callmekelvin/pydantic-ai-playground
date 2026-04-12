import threading
import os
import shutil

godot_folder_name = "godot-docs-html-stable"
godot_chunked_folder_name = "godot-docs-chunked"

def chunkDocuments():
    """
    Chunk documents in parallel using multiple threads
    """

    sourceFolderToChunkedFolderFileLst = prepareDirForChunking()

    numOfDocuments = len(sourceFolderToChunkedFolderFileLst)
    noThreads = 4
    threadPartitions = getThreadPartitionSizes(numOfDocuments, noThreads)

    threads = []
    threadNo = 0
    for partitions in threadPartitions:
        t = threading.Thread(target=chunkingChildThread, 
                             kwargs={ "workList": sourceFolderToChunkedFolderFileLst[partitions[0]: partitions[1]], "threadNo": threadNo }
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

def prepareDirForChunking():
    """
    Prepares source and chunked directories for document chunking
    
    Returns:
        List of (source_path, chunked_path) tuples for each file.
    """

    current_working_dir = os.getcwd()
    godot_folder_path = os.path.join(current_working_dir, godot_folder_name)
    godot_sources_folder_path = os.path.join(godot_folder_path, "_sources")
    godot_chunked_folder_path = os.path.join(current_working_dir, godot_chunked_folder_name)

    if not (os.path.isdir(godot_folder_path) and os.path.isdir(godot_sources_folder_path)):
        print("Missing Godot Documentation - Please Retrieve Godot Documentation First")

    # Ensure Clean Directory for Chunked Godot Docs
    if os.path.isdir(godot_chunked_folder_path):
        shutil.rmtree(godot_chunked_folder_path)
    
    os.mkdir(godot_chunked_folder_path)

    # TXT Files in _sources Folder contain raw Godot Documentation content, which is suitable for vectorisation
    sourcesFolderDict = {}
    for root, dir, files in os.walk(godot_sources_folder_path):
        sourcesFolderDict[root] = files
        # print(f"Directory Name: {root}\nFiles List: {files}\n")


    # Create List Map of Godot Documentation Files to Chunk
    # To prepare for chunking and threading work, create new directory for chunked Godot Documentation
    sourceFolderToChunkedFolderFileLst = []
    for dir, files in sourcesFolderDict.items():
        # Get Directory's Relative Path from Godot Source Folder Dir
        relDirPath = os.path.relpath(dir, godot_sources_folder_path)

        # Generate New Godot Chunked Folder Dir
        chunkedDirPath = os.path.join(godot_chunked_folder_path, relDirPath)

        if not os.path.isdir(chunkedDirPath):
            os.makedirs(chunkedDirPath)

        for file in files:
            sourceFilePath = os.path.join(dir, file)
            chunkedFilePath = os.path.join(chunkedDirPath, file)

            sourceFolderToChunkedFolderFileLst.append((sourceFilePath, chunkedFilePath))

    return sourceFolderToChunkedFolderFileLst

def getThreadPartitionSizes(numOfDocuments, noThreads = 4):
    """
    Divides document list into partitions for threading.
    
    Returns:
        List of (start, end) tuples for each partition.
    """

    noPartitions = numOfDocuments // noThreads
    remainder = numOfDocuments % noThreads

    partitions = []
    start = 0

    for i in range(noThreads):
        size = noPartitions + (1 if i < remainder else 0)
        end = start + size
        partitions.append((start, end))

        start = end

    return partitions

def getOverlappingChunks(numOfLines, chunkSize, overlap):
    """
    Generates overlapping chunks for a given number of file lines
    
    Returns:
        List of (start, end) tuples for each chunk.
    """

    if numOfLines < chunkSize:
        return [(0, numOfLines)]
    
    # Initial Step of 200, Effective Subsequent Step Increments of 180
    numOfChunks = int(((numOfLines - chunkSize) // overlap) + 1)

    chunks = []
    for chunkNo in range(numOfChunks):
        start = chunkNo * overlap
        end = start + chunkSize
        chunks.append((int(start), int(end)))
    
    return chunks    

def chunkDocumentUnitOfWork(sourcePath, resultPath):
    """
    Splits a document into overlapping chunks of 200 lines with 10% overlap.
    Each chunk is saved as a separate file in the specified result path.
    """

    resultDirName = os.path.dirname(resultPath)
    resultChunkBaseName = os.path.basename(resultPath)

    # Open Source File
    with open(sourcePath, "r", encoding="utf-8") as sourceFile:

        # Perform Chunking based on Num Of Lines in File
        sourceFileLines = sourceFile.readlines()
        numOfLines = len(sourceFileLines)

        # Fixed Chunking Based Off Lines - 200 Lines
        # Overlap Chunking - 10% Line Overlap to ensure Context is lost between chunks
        chunkSize = 200
        overlap = 0.9 * 200
        chunkList = getOverlappingChunks(numOfLines, chunkSize, overlap)
        # print(chunkList)

        chunkNo = 0
        for chunk in chunkList:
            resultChunkedFileName = f"chunk-{chunkNo}-{resultChunkBaseName}"
            resultChunkedFilePath = os.path.join(resultDirName, resultChunkedFileName)

            # Write chunks to each file
            with open(resultChunkedFilePath, "w", encoding="utf-8") as destFile:
                destFile.writelines(sourceFileLines[chunk[0] : chunk[1]])
                chunkNo += 1
            
            destFile.close()

    sourceFile.close()

    return

def chunkingChildThread(workList, threadNo):
    """
    Processes a list of (source_path, result_path) pairs by chunking each document.
    """

    for work in workList:
        chunkDocumentUnitOfWork(work[0], work[1])

    print(f"Thread {threadNo}: Work Complete")
    return

# chunkDocuments()