import os
import argparse
import re
import string


def load_stopwords(filename):
    with open(filename, 'r') as file:
        stop_words = set(word.strip().lower() for word in file)
    return stop_words


def remove_stopwords_and_punctuations(text, stop_words):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation.replace('\'', '')))
    words = text.split()
    words = [word for word in words if word not in stop_words]
    text = ' '.join(words)
    return text


def linear_search(query, document_type):
    search_folder = 'collection_original' if document_type == 'original' else 'collection_no_stopwords'
    for file_name in os.listdir(search_folder):
        with open(os.path.join(search_folder, file_name), 'r') as file:
            if query in file.read().lower():
                print(file_name)


def split_fables(file_name):
    with open(file_name, 'r') as file:
        content = file.read()
    content = content.split('\n', 306)[-1]
    fables = re.split('\n\n\n\n', content)
    output_folder = 'collection_original'
    output_folder_no_stopwords = 'collection_no_stopwords'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    if not os.path.exists(output_folder_no_stopwords):
        os.makedirs(output_folder_no_stopwords)
    for index, fable in enumerate(fables, start=1):
        lines = fable.strip().split('\n')
        title = lines[0].strip()
        text = '\n'.join(lines[2:]).strip()
        fable_number = str(index).zfill(2)
        fable_name = re.sub(r'[_,\']+', '', title.lower().strip()).replace(' ', '_')
        file_name = "{}_{}.txt".format(fable_number, fable_name)
        with open(os.path.join(output_folder, file_name), 'w') as f:
            f.write(f"{title}\n\n{text}\n\n")
        text = remove_stopwords_and_punctuations(text, stop_words)
        with open(os.path.join(output_folder_no_stopwords, file_name), 'w') as f:
            f.write(f"{title}\n\n{text}\n\n")


if __name__ == '__main__':
    # Define and parse command line arguments
    parser = argparse.ArgumentParser(description="A basic information retrieval system.")
    parser.add_argument('--extract-collection', type=str, help="Document to be split into fables")
    parser.add_argument('--query', type=str, help="User query")
    parser.add_argument('--model', type=str, default='bool', choices=['bool'], help="Retrieval model (default: bool)")
    parser.add_argument('--search-mode', type=str, default='linear', choices=['linear'], help="Search mode (default: linear)")
    parser.add_argument('--documents', type=str, default='original', choices=['original', 'no_stopwords'], help="Source documents for search (default: original)")
    args = parser.parse_args()

    # Load stop words from 'englishST.txt'
    stop_words = load_stopwords('englishST.txt')

    # Extract collection if specified
    if args.extract_collection:
        split_fables(args.extract_collection)

    # Perform linear search if specified
    if args.query and args.model == 'bool' and args.search_mode == 'linear':
        linear_search(args.query, args.documents)
