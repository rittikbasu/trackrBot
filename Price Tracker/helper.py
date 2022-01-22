# HELPER FUNCTIONS ---------------------------------------------

def next_available_col(worksheet):
    col  = len(worksheet.row_values(1)) + 1
    return col

def next_available_row(worksheet):
    row  = len(worksheet.col_values(1)) + 1
    return row

def get_country_code(url):
    cc = url[19:].split('/')[0]
    if len(cc) == 3:
        cc = 'us'
    else:
        cc = cc[-2:]
    return cc

def scraper_cc(url):
    cc_list = ['us','uk','ca','de','fr','es','br','mx','in','jp','cn','au']
    cc = url[19:].split('/')[0]
    if len(cc) == 3:
        cc = 'us'
    else:
        cc = cc[-2:]
        if cc not in cc_list:
            cc = 'us'
    return cc

def string_to_list_and_back(string,new_val):
    list_ = string.split(',')
    if new_val in list_:
        increment = 0
    else:
        list_.append(new_val)
        increment = 1
    new_string = ','.join(map(str, list_))
    return new_string, increment

# -----------------------------------------------------------------
