
def load_api_kwargs():
    """ Fast API kwargs """
    kwargs = {
            "title": "LLM Apps Backend",
            "description": "A Backend Rest Api for LLM apps",
            "summary": """
                This is an application that provides a backend service for multiple LLM apps.
            """,
            "version": "0.0.1",
            "terms_of_service": "https://www.hifeyinc.com/terms/",
            "contact": {
                "name": "Temiloluwa Adeoti",
                "url": "https://temiloluwa.github.io/",
                "email": "temilolu74@gmail.com",
            },
            "license_info": {
                "name": "Apache 2.0",
                "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
            },
            "openapi_tags": [
                {
                    "name": "User",
                    "description": "Person learning a language using the Lingua trainer API",
                },
                {
                    "name": "Words",
                    "description": "Words that a user is learning or learnt",
                    "externalDocs": {
                        "description": "Words that guide a user's experience on the app",
                        "url": "https://fastapi.tiangolo.com/",
                    },
                },
                {
                    "name": "Challenges",
                    "description": "The challenges offered by the Lingua trainer help improve the user's language competence",
                },
            ],
        }
    
    return kwargs
