def create_chat_configs(initial_message, agent_workflow, default_config=None):
    """
    Create chat configurations by prepending default_config to each agent config.
    
    Args:
        initial_message: Message for the first agent
        agent_workflow: List of dictionaries containing agent sender/recipient pairs
        default_config: Default configuration to prepend to each agent (defaults to None)
    
    Returns:
        List of chat configurations ready for initiate_chats
    """
    if default_config is None:
        default_config = {
            "message": "Use context from the previous agent.",
            "silent": False,
            "summary_method": "last_msg",
        }
    
    chat_configs = []
    
    for i, agent_config in enumerate(agent_workflow):
        config = {**default_config, **agent_config}
        
        # Add initial message only to the first agent
        if i == 0:
            config["message"] = initial_message
            
        chat_configs.append(config)
    
    return chat_configs 