import pandas as pd
import re
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', None)

df = pd.read_csv('jeopardy.csv')
# print(df.head(50))
# print(df.columns)       # mis-formatted column name

df = df.rename(columns = lambda column_name: column_name[1:] if column_name != 'Show Number' else column_name)
# print(df.columns)       # fixed column name format
# change air date from string to datetime
df['Air Date'] = pd.to_datetime(df['Air Date'])
# change values from string to float
df['Value'] = df.Value.apply(lambda x: float(x[1:].replace(',', '')) if x != 'None' else 0)
# remove hyperlinks
df['Question'] = df.Question.replace('(\(?<.*>\.?\)?)', '', regex = True)


count_nan = len(df) - df.count()    # output 2 nan values on answer column
df = df.fillna(value = {'Answer': 'Null'})      #fixed nan into string
count_nan = len(df) - df.count()
# print(count_nan)        # check for nan values again

# function to filter dataset
def filter_questions_data(data, words):
    def filter_word_list(question, words):
        words_in_question = True
        question = question.lower()
        for word in words:
            if (word.lower() in question) == False:
                words_in_question = False
        return words_in_question
    filter = lambda x: filter_word_list(x, words)
    return data.loc[data['Question'].apply(filter)]

test = filter_questions_data(df, ['king', 'england'])
# print(test)

# function to filter, more precise without anything before/after
def regex_filter_questions_data(data, words):
    def filter_word_list(question, words):
        words_in_question = True
        question = question.lower()
        for word in words:
            word = word.lower()
            word = re.compile(r'(\A|\s|\'|"|\( re.IGNORECASE)' + word + r"([,]|\.|\'|\"|\)|s|\s|\Z|\W, re.IGNORECASE)")
            if re.search(word, question) == None:
                words_in_question = False
        return words_in_question
    filter = lambda question: filter_word_list(question, words)
    return data[data['Question'].apply(filter)]

test2 = regex_filter_questions_data(df, ['king', 'england'])
# print(test2)

# function to return unique answer count
def unique_answers(word_list):
    data = regex_filter_questions_data(df, word_list)
    return data.Answer.value_counts()

print(unique_answers(['King']))
print(df.head(50))