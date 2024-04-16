# ICL-Benchmark
The 100 datapoints and the evaluation function.

The image files and json files of the same number is a pair. 
The json file contain: the question, a list of keys and a list with each element is an example output of the cooresponding key.

The evaluation function requires the llm output contain the key pattern such as: "Overal: " where 'overall' is a key.
The score is 0 if the key pattern is not found. Otherwise score is the Bertscore between the llm outputs and example outputs.
