data = {'I am sad': ['Confusion', 'Calmness', 'Interest'], 'I am happy': ['Joy', 'Excitement']}
result_string = ""

for sentence, emotions in data.items():
    # Format the emotions list into a string
    emotions_str = ', '.join(emotions)
    # Construct the sentence with emotions in brackets
    sentence_with_emotions = f"[{emotions_str}] {sentence}\n"
    result_string += sentence_with_emotions

print(result_string)