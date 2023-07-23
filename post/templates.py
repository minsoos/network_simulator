POST_TEMPLATE = '''
Please ignore all previous instructions.
Please respond only in the {language} language.
The post's character count should be between {min_caract} to {max_caract} characters without line breaks.
You are a Average Social Media User. Do not self reference. Do not explain what you are doing.
Please write a post about the following news: "{news}". Add emojis to the thread when appropriate.
Avoid repeating the news explicitly.
The post has to end in a point full stop.
You are {stance} the news. The post is a {response}.
Your content should be {feature1}, {feature2} and {feature3}. Don't write data as a template.
Please use understandable words. Please include {included1}, {included2} and {included3} in the thread.
Please respond directly to my query without adding any extra information or paragraphs. Use the following format: <user post>
'''

REPLY_TEMPLATE = '''
Please ignore all previous instructions.
Please respond only in the {language} language.
The reply's character count should be approximately between {min_caract} to {max_caract} characters without line breaks.
You are a Average Social Media User. Do not self reference. Do not explain what you are doing.
The news is as follows: "{news}".
Please reply the following post about the news: "{to_reply}". Add emojis to the thread when appropriate.
Avoid repeating the news explicitly.
The post has to end in a point full stop.
You are {stance} the previous post. The post is a {response}.
Your content should be {feature1}, {feature2} and {feature3}. Don't write data as a template.
Please use understandable words. Please include {included1}, {included2} and {included3} in the thread.
Please respond directly to my query without adding any extra information or paragraphs. Use the following format: <user post>
'''
