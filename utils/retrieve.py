from setup.setup_vector import turn_video_and_script_files_into_vectordb


vector_store = turn_video_and_script_files_into_vectordb("data")
retriever = vector_store.as_retriever()
