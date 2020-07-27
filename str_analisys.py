from itertools import combinations
from collections import Counter
import pandas as pd


def extract_n_kw_combo_frequency_df(raw_dataframe, n_word_combo=2):
    # All headlines to lowercase
    raw_dataframe['Headline'] = [headline.lower() for headline in raw_dataframe['Headline']]
    # Create new colum by splitting headlines into unique words
    raw_dataframe['headline_words'] = [headline.split() for headline in raw_dataframe.Headline]
    # Removing unwanted characters  and whitespaces from splitted words
    raw_dataframe['headline_words'] = [[word.strip(',') for word in sublist] for sublist in
                                       raw_dataframe['headline_words']]
    raw_dataframe['headline_words'] = [[word.strip(':') for word in sublist] for sublist in
                                       raw_dataframe['headline_words']]
    raw_dataframe['headline_words'] = [[word.strip('""') for word in sublist] for sublist in
                                       raw_dataframe['headline_words']]
    raw_dataframe['headline_words'] = [[word.strip('') for word in sublist] for sublist in
                                       raw_dataframe['headline_words']]
    # Creating column with filtered words not in blacklist
    raw_dataframe['hd_words_filt'] = [[word for word in sublist if word not in words_bl] for sublist in
                                      raw_dataframe['headline_words']]
    # Gettin the frequcney of the combination of words
    kw_word_combo_freq = word_combo_freq(raw_dataframe['hd_words_filt'], n_word_combo)
    # Creating DataFrame with results
    df = pd.DataFrame.from_dict(kw_word_combo_freq, orient='index').reset_index()
    df.rename(columns={'index': 'kws_combo', 0: 'freq'}, inplace=True)
    df = df.sort_values('freq', ascending=False).reset_index(drop=True)
    return df


def word_combo_freq(lines, n_word_combo=2):
    pair_counter = Counter()
    for line in lines:
        unique_tokens = sorted(set(line))  # exclude duplicates in same line and sort to ensure one word is always before other
        combos = combinations(unique_tokens, n_word_combo)
        pair_counter += Counter(combos)
    return pair_counter


words_bl = ('a', 'ante', 'bajo', 'cabe', 'con', 'día', 'contra', 'me', 'después', 'dijo',
                'habló', 'sus', 'le', 'de', 'qué', 'desde', 'durante', 'en', 'entre', 'hacia',
                'hasta', 'mediante', 'para', 'por', 'según', 'sin', 'so', 'sobre', 'tras',
                'versus', 'vía', 'la', 'el', 'que', 'los', 'del', 'y', 'un', 'las', 'se',
                'su', 'una', 'al', 'como', 'no', 'es', 'o', 'lo', 'pero', 'fue', 'mas',
                'más', 'muy', 'esta', 'este', 'ha', 'está', 'cómo', 'hoy', 'así', 'ex', 'uno',
                'dos', 'tres', 'ya', 'ser', 'mil', 'mayo', 'quiénes', 'dice', 'ni')