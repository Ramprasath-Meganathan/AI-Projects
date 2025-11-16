def load_agent(client,model,logger):
    tools = client.get_tools()
    tool_names = [tool.name for tool in tools]
    logger.info(f"Available tools from MCP: {tool_names}")

    if not tools:
        logger.warning("No tools rerieved from MCP server. Agent capabilities might be limited.")

    agent_executor = create_react_agent(model,tools)
    logger.info("ReAct agent created")
    return agent_executor

def create_full_query(user_query, agent_base_prompt, working_directory, logger):
    context_prefix = ""
    if working_directory:
        if not os.path.isdir(working_directory):
                logger.warning(f"Working directory '{working_directory}' set in context does not exist on the API server.")
                context_prefix = f"Context: The current working directory is set to '{working_directory}' (Note: This path may not be valid on the server). Please consider this path when referring to project files.\n\n"
        else:
                context_prefix = f"Context: The current working directory is set to '{working_directory}'. Please consider this path when referring to project files.\n\n"

    full_query = f"{context_prefix}{agent_base_prompt}\n\nUser Question:\n{user_query}"
    return full_query

@app.post("/generate", response_model=GenerateResponse)
async def generate_response_api(request: QueryRequest):
    """
    API endpoint to generate a response based on the user query,
    using the currently set working directory context.
    """
    global current_working_directory
    logger.info(f"Received /generate request. Query: '{request.query[:100]}...'. Current WD: '{current_working_directory}'")

    if not request.query or not request.query.strip():
         raise HTTPException(status_code=400, detail="Query cannot be empty.")

    try:
        final_answer = await run_agent(request.query, current_working_directory)
        logger.info(f"Sending response: {final_answer[:100]}...")
        return GenerateResponse(response=final_answer)
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.exception(f"Unexpected error in /generate endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected internal server error occurred: {str(e)}")

@app.post("/set_working_directory", response_model=SetDirectoryResponse)
async def set_working_directory_api(request: SetDirectoryRequest):
    """
    Sets the working directory path that will be added to the agent's context.
    """
    global current_working_directory
    path_to_set = request.path.strip()
    if not path_to_set:
        raise HTTPException(status_code=400, detail="Path cannot be empty.")

    current_working_directory = path_to_set
    logger.info(f"Working directory set to: {current_working_directory}")
    return SetDirectoryResponse(
        message="Working directory successfully set.",
        current_path=current_working_directory
    )