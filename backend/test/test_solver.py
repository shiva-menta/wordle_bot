from wordle_bot.src.wordle_solver import *


# expected_value tests
def test_ev_normal_1():
    assert expected_value(2,1) == 0.5

def test_ev_normal_2():
    assert expected_value(16,4) == 0.5

def test_ev_abnormal_1():
    assert round(expected_value(31,7), 2) == 0.48

def test_ev_abnormal_2():
    assert round(expected_value(143,3), 2) == 0.12

def test_ev_same_val():
    assert expected_value(2,2) == 0


# get_answer_template_tests
def test_gat_allgreens():
    assert get_answer_template('stars', 'stars') == 'ggggg'

def test_gat_nomatches():
    assert get_answer_template('shiva', 'teddy') == 'xxxxx'

def test_gat_allyellows():
    assert get_answer_template('basil', 'liasb') == 'yyyyy'

def test_gat_allyelloworgreen_1():
    assert get_answer_template('bisal', 'basil') == 'gygyg'

def test_gat_allyelloworgreen_2():
    assert get_answer_template('skart', 'stark') == 'gyggy'

def test_gat_mixedresults_1():
    assert get_answer_template('shots', 'sloth') == 'gyggx'

def test_gat_mixedresults_2():
    assert get_answer_template('light', 'sloth') == 'yxxyy'

def test_gat_mixedresults_3():
    assert get_answer_template('tsars', 'sstaa') == 'ygyxy'

def test_gat_doubleletter_1():
    assert get_answer_template('peeps', 'shear') == 'xxgxy'

def test_gat_doubleletter_2():
    assert get_answer_template('tones', 'toons') == 'ggyxg'

def test_gat_doubleletter_3():
    assert get_answer_template('ereaa', 'shear') == 'xyggx'


# word_matches_template_tests
def test_wmt_allgreens_true():
    assert word_matches_template('stars', 'stars', 'ggggg')

def test_wmt_allgreens_false():
    assert not word_matches_template('stars', 'stars', 'xygyg')

def test_wmt_nomatches_true():
    assert word_matches_template('shiva', 'teddy', 'xxxxx')

def test_wmt_nomatches_false():
    assert not word_matches_template('shiva', 'teddy', 'xxygx')

def test_wmt_allyellows_true():
    assert word_matches_template('basil', 'liasb', 'yyyyy')

def test_wmt_allyellows_false():
    assert not word_matches_template('basil', 'liasb', 'ygxgy')

def test_wmt_allyelloworgreen_1_true():
    assert word_matches_template('bisal', 'basil', 'gygyg')

def test_wmt_allyelloworgreen_1_false():
    assert not word_matches_template('bisal', 'basil', 'gxgxg')

def test_wmt_allyelloworgreen_2_true():
    assert word_matches_template('skart', 'stark', 'gyggy')

def test_wmt_allyelloworgreen_2_false():
    assert not word_matches_template('skart', 'stark', 'gxxgy')

def test_wmt_mixedresults_1_true():
    assert word_matches_template('sloth', 'shots', 'gyggx')

def test_wmt_mixedresults_1_false():
    assert not word_matches_template('sloth', 'shots', 'gyggg')

def test_wmt_mixedresults_2_true():
    assert word_matches_template('sloth', 'light', 'yxxyy')

def test_wmt_mixedresults_2_false():
    assert not word_matches_template('sloth', 'light', 'yxgyy')

def test_wmt_mixedresults_3_true():
    assert word_matches_template('sstaa', 'tsars', 'ygyxy')

def test_wmt_mixedresults_3_false():
    assert not word_matches_template('sstaa', 'tsars', 'ygyyg')

def test_wmt_doubleletter_1_true():
    assert word_matches_template('shear', 'peeps', 'xxgxy')

def test_wmt_doubleletter_1_false():
    assert not word_matches_template('shear', 'peeps', 'xygxy')

def test_wmt_doubleletter_2_true():
    assert word_matches_template('toons', 'tones', 'ggyxg')

def test_wmt_doubleletter_2_false():
    assert not word_matches_template('toons', 'tones', 'gggxg')

def test_wmt_doubleletter_3_true():
    assert word_matches_template('shear', 'ereaa', 'xyggx')

def test_wmt_doubleletter_3_false():
    assert not word_matches_template('shear', 'ereaa', 'xygxy')


# filter_words tests
def test_answer():
    assert filter_words('eeeee','xxxxx',['shiva', 'hello']) == ['shiva']

# generate_all_possible_template_types tests
def test_gatt_no_restrictions():
    assert len(get_all_possible_template_types('xxxxx')) == 243
    assert len(get_all_possible_template_types('xyxxx')) == 243

def test_gatt_one_letter_restriction():
    assert len(get_all_possible_template_types('xxgxx')) == 81

def test_gatt_four_letter_restriction():
    assert len(get_all_possible_template_types('gggxg')) == 3

def test_gatt_three_letter_restriction():
    assert len(get_all_possible_template_types('gggxy')) == 9

# return_highest_frequency_word tests
def test_hfw_singleton():
    assert return_highest_frequency_word(['hello']) == 'hello'

def test_hfw_two_words():
    assert return_highest_frequency_word(['hello', 'zweig']) == 'hello'

def test_hfw_three_words():
    assert return_highest_frequency_word(['hello', 'zweig', 'apple']) == 'apple'

# get_best_guess_data tests



