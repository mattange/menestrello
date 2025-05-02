def response_format() -> dict:
    """
    Sets up the response format for the chatbot.
    """
    # Define the response format for the chatbot
    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "story_section",
            "schema": {
                "type": "object",
                "properties": {
                    "introduction": {
                        "type": "string",
                        "description": "The introduction by the chatbot."
                    },
                    "title": {
                        "type": "string",
                        "description": "The title of the section."
                    },
                    "fragment": {
                        "type": "string",
                        "description": "The content of the story section."
                    },
                    "question": {
                        "type": "string",
                        "description": "The question for the."
                    },
                    "options": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "option": {
                                    "type": "integer",
                                    "description": "The option number."
                                },
                                "description": {
                                    "type": "string",
                                    "description": "The description of the option."
                                }
                            },
                            "required": ["option", "description"]
                        }
                    }
                },
                "required": ["title", "fragment"]
            }
        }
    }
    return response_format