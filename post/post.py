from anytree import Node


class Post(Node):
    def __init__(self, name, step, parent=None, children=None, owner=None, message='', type_agent='', 
                 news=None, post_template=None, reply_template=None, instructions_template=None, **kwargs):

        super().__init__(name, parent, children, **kwargs)
        self.step = step
        self.owner = owner if type(owner) == int else owner
        self.message = message
        self.type_agent = type_agent
        self.post_template = post_template
        self.reply_template = reply_template
        self.news = news
        self.instructions_template = instructions_template
        self.parent = parent

        for attribute in kwargs:
            self.__dict__[attribute] = kwargs[attribute]
        
    def saludar(self):
        print("Version modificada")


    def get_prompt(self, language, min_caract, max_caract, user_description):
        need_reply = True
        #parent_node = self.search_to_reply()

        if self.name == 0:
            need_reply = False
            raise ValueError("The root node should't request prompt")
            
        if need_reply:
            instructions, post = self.create_reply(language, min_caract, max_caract, user_description)
        else:
            instructions, post = self.create_post(language, min_caract, max_caract, user_description)
        return instructions, post

    def search_to_reply(self):
        if self.name == 0:
            return self
        if not self.repost:
            return self
        return self.parent.search_to_reply()
    
    def search_to_reply_message(self):
        return self.search_to_reply().message
    

    def search_to_reply_uid(self):
        return self.search_to_reply().cause
    
    
    def create_reply(self, language, min_caract, max_caract,
                     user_description='Average Social Media User'):
        to_reply = self.parent.search_to_reply_message()
        stance = self.stance
        cause = self.cause
        if stance == 'against':
            stance = 'are against'
        elif stance == 'agree':
            stance = 'are in favor'
        else:
            stance = 'are neutral'
        response = self.response
        features = ['casual', 'informal', 'conversational']
        included = ['statistics', 'personal experience', 'fun facts']
        instructions = self.instructions_template.format(language=language,
                                           stance=stance, response=response,
                                           feature1=features[0], feature2=features[1], feature3=features[2],
                                           included1=included[0], included2=included[1], included3=included[2],
                                           user_description=user_description)
        
        post = self.reply_template.format(news=self.news, to_reply=to_reply, cause=cause, stance= stance, response=response, min_caract=min_caract, max_caract=max_caract)
        return instructions, post
    
    def create_post(self, language, min_caract, max_caract,
                    user_description='Average Social Media User'):
        stance = self.stance
        if stance == 'against':
            stance = 'are against'
        elif stance == 'agree':
            stance = 'are in favor'
        else:
            stance = 'are neutral'
        response = self.response
        features = ['casual', 'informative', 'conversational']
        included = ['statistics', 'personal experience', 'fun facts']
        instructions = self.instructions_template.format(language=language,
                                           stance=stance, response=response,
                                           feature1=features[0], feature2=features[1], feature3=features[2],
                                           included1=included[0], included2=included[1], included3=included[2],
                                           user_description=user_description)
        post = self.post_template.format(news=self.news, min_caract=min_caract, max_caract=max_caract)
        return instructions, post

    def set_message(self, message):
        self.message = message
