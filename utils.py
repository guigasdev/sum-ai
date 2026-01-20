import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient, AbstractiveSummaryAction, ExtractiveSummaryAction
from azure.ai.translation.text import TextTranslationClient
from azure.ai.translation.text.models import InputTextItem
import requests # Fallback or specific utility if needed

load_dotenv()

# Translator Configuration
TRANSLATOR_ENDPOINT = os.getenv("AZURE_TRANSLATOR_ENDPOINT")
TRANSLATOR_KEY = os.getenv("AZURE_TRANSLATOR_KEY")
TRANSLATOR_REGION = os.getenv("AZURE_TRANSLATOR_REGION")

# Language Service Configuration
LANGUAGE_ENDPOINT = os.getenv("AZURE_LANGUAGE_ENDPOINT")
LANGUAGE_KEY = os.getenv("AZURE_LANGUAGE_KEY")

def get_translation(text, target_language, source_language=None):
    """
    Translates text using Azure Translator SDK.
    """
    if not TRANSLATOR_KEY or not TRANSLATOR_REGION:
        return "Error: Translator keys not configured. Please check your .env file."

    try:
        credential = AzureKeyCredential(TRANSLATOR_KEY)
        
        client = TextTranslationClient(endpoint=TRANSLATOR_ENDPOINT, credential=credential, region=TRANSLATOR_REGION)

        input_text_elements = [InputTextItem(text=text)]
        
        # Prepare arguments
        kwargs = {"body": input_text_elements, "to_language": [target_language]}
        if source_language:
            kwargs["from_language"] = source_language
            
        response = client.translate(**kwargs)
        
        if response:
            return response[0].translations[0].text
        return "Error: No translation returned."

    except Exception as e:
        return f"Error during translation: {str(e)}"

def get_summary(text, summary_type="Extractive"):
    """
    Summarizes text using Azure AI Language Service.
    """
    if not LANGUAGE_KEY or not LANGUAGE_ENDPOINT:
        return "Error: Language Service keys not configured. Please check your .env file."

    try:
        client = TextAnalyticsClient(
            endpoint=LANGUAGE_ENDPOINT, 
            credential=AzureKeyCredential(LANGUAGE_KEY)
        )
        
        poller = None
        # Adjust sentence count based on text length roughly (optional but helpful)
        # For very short texts, 1 or 2 sentences is enough.
        target_sentence_count = 3
        if len(text) < 500:
            target_sentence_count = 1
        elif len(text) < 1000:
            target_sentence_count = 2

        if summary_type == "Extractive":
            poller = client.begin_analyze_actions(
                documents=[text],
                actions=[ExtractiveSummaryAction(max_sentence_count=target_sentence_count)]
            )
        else: # Abstractive
            poller = client.begin_analyze_actions(
                documents=[text],
                actions=[AbstractiveSummaryAction(sentence_count=target_sentence_count)]
            )
            
        document_results = poller.result()
        
        summary_result = ""
        for result in document_results:
            action_result = result[0]  # First action result
            
            if action_result.is_error:
                return f"Error: {action_result.code} - {action_result.message}"
                
            if summary_type == "Extractive":
                for sentence in action_result.sentences:
                    summary_result += sentence.text + " "
            else: # Abstractive
                for summary in action_result.summaries:
                    summary_result += summary.text + "\n"
                    
        return summary_result.strip()
    except Exception as e:
        return f"Error during summarization: {str(e)}"
