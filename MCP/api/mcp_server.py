import os
import subprocess
from mcp.server.fastmcp import FastMCP

mpc = FastMCP("AssistantCodeReader",port =8000)

@mcp.tool()
def read_file(file_path:str) -> str:
    """ Read the content of a file given its path using a system command('cat').

    Args:
        file_path (str): The path to the file to be read.

    Returns:
        str: The content of the file or an error message.
    """
    if not os.path.isfile(file_path):
        return f"Error: {file_path} is not a valid path."
    
    try:
        result = subprocess.run(["cat", file_path], capture_output=True, text=True, check=True)
        return result.stdout
    except Exception as e:
        return f"Error reading file:{str(e)}"
    
    