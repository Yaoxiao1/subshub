
OPENAI_API = "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"
PROMPT_MSG = '''
you are a professional interpreter to translate a subtitle into Chinese, The user will offer the lines of the subtitles, 
and you will just need to translate the lines into Chinese, you should keep the line number and the time indicator (which has a format like HOUR:MIN:SEC,MS --> HOUR:MIN:SEC,MS)
'''

MODEL = "gpt-3.5-turbo"
MESSAGES = []
THREAD_COUNT = 3
CHUNK_SIZE = 4
BATCH_SIZE = 5