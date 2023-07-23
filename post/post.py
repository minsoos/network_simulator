from anytree import Node


class Post(Node):
    def __init__(self, name, parent=None, children=None, owner=None, message='', response=None,
                 stance=None, repost=False, cause=None, method=None, post_template=None,
                 reply_template=None, news=None, **kwargs):

        super().__init__(name, parent, children, **kwargs)
        self.owner = owner
        self.message = message
        self.stance = stance
        self.response = response
        self.repost = repost
        self.cause = cause
        self.method = method
        self.post_template = post_template
        self.reply_template = reply_template
        self.news = news

    def get_prompt(self, language, min_caract, max_caract):
        need_reply = True
        if self.name == 0:
            need_reply = False
        else:
            if self.parent.name == 0:
                need_reply = False
        if need_reply:
            prompt = self.create_reply(language, min_caract, max_caract)
        else:
            prompt = self.create_post(language, min_caract, max_caract)
        return prompt

    def search_to_reply(self):
        if not self.repost:
            return self.message
        return self.parent.search_to_reply()

    def create_reply(self, language, min_caract, max_caract):
        to_reply = self.parent.search_to_reply()
        stance = self.stance
        response = self.response
        features = ['casual', 'informative', 'conversational']
        included = ['statistics', 'personal experience', 'fun facts']
        post = self.reply_template.format(language=language,
                                           news=self.news, to_reply=to_reply, stance=stance, response=response,
                                           min_caract=min_caract, max_caract=max_caract,
                                           feature1=features[0], feature2=features[1], feature3=features[2],
                                           included1=included[0], included2=included[1], included3=included[2])
        return post

    def create_post(self, language, min_caract, max_caract):
        stance = self.stance
        response = self.response
        features = ['casual', 'informative', 'conversational']
        included = ['statistics', 'personal experience', 'fun facts']
        post = self.post_template.format(language=language,
                                           news=self.news, stance=stance, response=response,
                                           min_caract=min_caract, max_caract=max_caract,
                                           feature1=features[0], feature2=features[1], feature3=features[2],
                                           included1=included[0], included2=included[1], included3=included[2])
        return post

    def set_message(self, message):
        self.message = message
