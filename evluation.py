from evaluate import load
import re

bertscore = load("bertscore")

def find_and_output_between(text, first_group, second_group):
    # Escape special characters in word groups and build regex pattern
    pattern = re.escape(first_group) + r'(.*?)' + re.escape(second_group)
    
    # Use re.search to find the pattern in the text
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)

    # If a match is found, output the text between the word groups
    if match:
        between_text = match.group(1).strip()
        return between_text
    
def get_words_after_pattern(text, pattern):
    # This regex pattern looks for the specified pattern and then captures
    # all characters after it until the end of the string.
    match = re.search(pattern + r'(.*)', text)
    if match:
        # Extract the part after the pattern
        after_pattern = match.group(1)
        # Split the string into words and return them
        return after_pattern
    
def evaluation_metric(llm_outputs, data_examples):    

    #first input is a list of outputs to be evaluated
    #the second input is the a list of data_example with each data point is a dictionary with key:'keywords' and 'example_outputs'
    #score is in the range 0-5 with score 0 means the format is not followed
    #score 1-5 means the format is followed and measures the degree of matchness

    def find_leftmost_empty(lst):
        for index, element in enumerate(lst):
            if element == -1:
                return index

    num_of_keys = []
    sentences_llm = []
    sentences_example = []

    scores_out = [-1]*len(llm_outputs) #Initialize the scores with -1
    
    for i in range(len(llm_outputs)):
        keys = data_examples[i]['keys']

        keyword_positions = []

        for key in keys:
            keyword_positions.append(llm_outputs[i].find(key))

        if -1 not in keyword_positions:
            num_of_keys.append(len(keys))
            sentences_example += data_examples[i]['example_outputs']
            for n_k in range(len(keys)-1):
                sentence = find_and_output_between(llm_outputs[i], keys[n_k], keys[n_k+1])
                sentences_llm.append(sentence)
            sentence = get_words_after_pattern(llm_outputs[i], keys[-1])
            sentences_llm.append(sentence)
        else:
            scores_out[i] = 0 #This data point not follows the format

    #print(sentences_llm)
    #print(sentences_example)
    sentence_scores = bertscore.compute(predictions=sentences_llm, references=sentences_example, lang="en")['recall']

    starting_index = 0

    print(sentence_scores)
    for i in range(len(num_of_keys)):
        #get score per sample by averaging scores of its sentences
        score = sum(sentence_scores[starting_index:starting_index+num_of_keys[i]])/num_of_keys[i]
        starting_index += num_of_keys[i]
        index = find_leftmost_empty(scores_out)
        scores_out[index] = score*5 # normalize score to the range 0-5

    return scores_out
