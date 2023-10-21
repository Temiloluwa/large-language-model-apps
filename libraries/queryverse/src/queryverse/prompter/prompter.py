class BasePrompter:
    def __init__(self, template=""):
        self.template = template

    def generate_dictionary(self, role, content):
        return {"role": role, "content": content}

    def receive_content(self, role, content):
        return self.generate_dictionary(role, content)

    def format(self, **variables):
        content = self.template
        if variables:
            for variable, value in variables.items():
                content = content.replace(f"{{{variable}}}", str(value))

        return content
 
    def __repr__(self):
        return self.template

    def __call__(self, **variables):
        content = self.format(**variables)
        return self.receive_content(self.role, content)
        

class SystemPrompter(BasePrompter):
    def __init__(self, template=""):
        super().__init__(template)
        self.role = "system"

class UserPrompter(BasePrompter):
    def __init__(self, template=""):
        super().__init__(template)
        self.role="user"

class AssistantPrompter(BasePrompter):
    def __init__(self, template=""):
        super().__init__(template)
        self.role="assistant"

