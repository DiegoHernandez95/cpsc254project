import os
import time

# simple file information retrieval using os
class FileInfoRetriever:
    @staticmethod
    def get_file_info(file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        creation_time = os.path.getctime(file_path)
        formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(creation_time))
        
        return {
            "name": file_name,
            "size_kb": file_size / 1024,
            "formatted_time": formatted_time
        }
