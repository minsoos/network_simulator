INSTRUCTIONS_TEMPLATE = '''
Please ignore all previous instructions.
Respond only in {language}.
You are a {user_description}. Do not self reference. Do not explain what you are doing.
Please, write in an informal way.
Add emojis to the thread when appropriate.
Avoid repeating the news explicitly.
Avoid referencing other users with their names.
Your content should be {feature1}, {feature2} and {feature3}. Don't write data as a template.
Please use understandable words. Please include {included1}, {included2} and {included3} in the thread.
You {stance} the news. The post is a {response}.
Please respond directly to my query without adding any extra information or paragraphs. Use the following format: <user post>
'''

POST_TEMPLATE = '''
Please write a post between {min_caract} and {max_caract} characters replying to and about the following news: "{news}". 
'''

REPLY_TEMPLATE = '''
The news is as follows: "{news}".
Please reply in a post, without copying, between {min_caract} and {max_caract} characters, to the following post about the news: "{to_reply}".
Please do not copy the last post.
'''

CORRECTNESS_TEMPLATE = '''
The news is as follows: '{news}'.
Please rewrite the related news post below: '{post}'.
Delete any parts that lack meaning.
Don't add new information.
Correct any misspelled words, but retain the informal style of writing.
'''

