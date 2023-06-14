import csv
import re
import time
import psutil

def load_dictionary(filename):
    dictionary = {}
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            english_word, french_word = row
            dictionary[english_word.lower()] = french_word
    return dictionary

def load_word_list(filename):
    word_list = set()
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            word_list.add(line.strip())
    return word_list

def replace_words(text, word_list, dictionary):
    frequency = {}
    translated_text = text
    for word in word_list:
        if word.lower() in dictionary:
            french_word = dictionary[word.lower()]
            pattern = r"\b{}\b".format(re.escape(word))
            translated_text = re.sub(pattern, french_word, translated_text, flags=re.IGNORECASE)
            frequency[word] = translated_text.lower().count(french_word.lower())
    return translated_text, frequency

def save_output(translated_text, frequency, time_taken, memory_used):
    with open('t8.shakespeare.translated.txt', 'w', encoding='utf-8') as file:
        file.write(translated_text)
    
    with open('frequency.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['English word', 'French word', 'Frequency'])
        for english_word, french_word in frequency.items():
            frequency_count = frequency[english_word]
            writer.writerow([english_word, french_word, frequency_count])
    
    with open('performance.txt', 'w', encoding='utf-8') as file:
        file.write(f"Time to process: {time_taken} seconds\n")
        file.write(f"Memory used: {memory_used} MB\n")

def main():
    start_time = time.time()
    
    # Load input files
    dictionary = load_dictionary('french_dictionary.csv')
    word_list = load_word_list('find_words.txt')
    
    # Read the input text file
    with open('t8.shakespeare.txt', 'r', encoding='utf-8') as file:
        text = file.read()
    
    # Replace words and get frequency
    translated_text, frequency = replace_words(text, word_list, dictionary)
    
    # Save output files
    save_output(translated_text, frequency, round(time.time() - start_time, 2), psutil.Process().memory_info().rss / 1024 / 1024)
    
    print("Processing completed successfully.")

if __name__ == '__main__':
    main()