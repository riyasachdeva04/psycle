from transformers import DistilBertTokenizer, DistilBertForQuestionAnswering
import re
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_model():
    # Load pre-trained DistilBERT model and tokenizer
    model_name = "distilbert-base-cased-distilled-squad"
    tokenizer = DistilBertTokenizer.from_pretrained(model_name)
    model = DistilBertForQuestionAnswering.from_pretrained(model_name)
    return model, tokenizer


def answer_question(page_contents, question):
    # Initialize variables to store the best answer and its confidence score
    best_answer = None
    best_score = float('-inf')

    for page_content in page_contents:
        # Clean the text
        cleaned_text = re.sub(r'\s+', ' ', page_content.replace('\n', ' '))
        
        # Tokenize input document and question
        inputs = tokenizer(question, cleaned_text, return_tensors="pt")

        # Get model's predicted answer
        outputs = model(**inputs)
        start_logits = outputs.start_logits
        end_logits = outputs.end_logits

        start_idx = start_logits.argmax().item()
        end_idx = end_logits.argmax().item() + 1

        # Decode the answer from the tokenized input
        answer = tokenizer.decode(inputs["input_ids"][0][start_idx:end_idx])

        # Calculate confidence score (you may want to fine-tune this)
        confidence_score = start_logits.max().item() + end_logits.max().item()

        # Update best answer if the current one has a higher confidence score
        if confidence_score > best_score:
            best_answer = {'answer': answer, 'metadata': {}}
            best_score = confidence_score

    return best_answer


if __name__ == "__main__":
    # Load model
    model, tokenizer = load_model()

    loader = PyPDFLoader("books/6-Parent-and-Teacher-Guidebook-for-Autism-2nd-edition.pdf")
    pages = loader.load_and_split()

    # splits
    text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    separators='n\n',
    chunk_size = 1000,
    chunk_overlap  = 20,
    length_function = len,
    is_separator_regex = True,
)

    # Split
    docs = text_splitter.split_documents(pages)
    page_contents = [doc.page_content for doc in docs]

    # Example question
    question = "what is autism?"

    # Answer question with the most compatible answer
    best_answer = answer_question(page_contents, question)

    # Print the best answer
    print(f"Best Answer: {best_answer['answer']}")
    print(f"Metadata: {best_answer['metadata']}")