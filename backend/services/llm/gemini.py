
from operator import contains
from google import genai
from config.settings import settings
from models import NewsArticle

api_key = settings.GEMINI_API_KEY
SYSTEM_PROMPT='Summarize the following article, use bullet points only if it must be. Focus on key facts and ignore ads. Keep it concise. Maximum 100 words. Foramt'

'''
Input format:
 {
    SYSTEM_PROMPT: "",
    articles: [
        'article_1': {
            'title':...,
            'content': ...
        },
        'article_2': {
            'title':...,
            'content': ...
        },
        ...
    ]
}

Summary output expected:
 {
    'article_1': summary of article_1,
    'article_2': summary of article_2,
    ...
 }

'''


class GeminiLLM:
    def __init__(*arg, **kwarg):
        MAX_CONTEXT_LENGTH = 1_000_000
        context = ''
        
        pass

    def summarize():
        """ Build request and send to Gemini API to get summarization"""
        pass
    
    def check_context():
        """ Check current context length """
        pass

    def add_article(article: NewsArticle):
        """
        Calculate context length and decide to add or not
        Return:
        - True: add
        - False: nope
        """
        pass



