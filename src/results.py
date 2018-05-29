import sys
import csv
import sqlite3


#DB_NAME = 'bigrams.db'
#DB_NAME = 'trigrams.db'
BASE_DIR = '/Users/ahounsel/git/censor-search/'


def count_new_domains(itr):
    "Count the amount of new censored domains found"

    conn = sqlite3.connect(BASE_DIR + DB_NAME)
    c = conn.cursor()

    rows = c.execute(('select distinct domain from urls where censored=1 ' +
                     'and iteration=?'), (itr,)).fetchall()
    itr_domains = [domain[0] for domain in rows]
    rows = c.execute(('select distinct domain from urls where censored=1 ' +
                     'and iteration<?'), (itr,)).fetchall()
    not_itr_domains = [domain[0] for domain in rows]
    diff = list(set(itr_domains) - set(not_itr_domains))
    str = 'New domains found on itr {0}: {1}'.format(itr, len(diff))
    print(str)
    conn.close()


def get_results(db, maxRows, allDomains):
    conn = sqlite3.connect(BASE_DIR + 'src/' + db)
    c = conn.cursor()

    rows = c.execute('select distinct domain from urls where censored=1 '
                     + 'and rowid <= ?', (maxRows,)).fetchall()
    itr_domains = [domain[0] for domain in rows]
    itr_domains = sorted(itr_domains)

    top_1000 = []
    i = 0
    with open (BASE_DIR + 'lists/top-1m.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in csvreader:
            if i < 1000:
                top_1000.append(row[1])
                i += 1
            else:
                break

    domain_count = 0
    results = []
    for domain in itr_domains:
        d = domain
        if d[:4] == 'www.':
            d = d[4:]
        contained = False
        if not allDomains:
            for top_domain in top_1000:
                if top_domain in d:
                    contained = True
                    break
        if not contained and d not in results:
            results.append(d)
    conn.close()
    return results


def get_unique_urls(maxRows):
    bigram_conn = sqlite3.connect(BASE_DIR + 'src/' + 'bigrams.db')
    trigram_conn = sqlite3.connect(BASE_DIR + 'src/' + 'trigrams.db')
    bigram_cursor = bigram_conn.cursor()
    trigram_cursor = trigram_conn.cursor()

    bigram_urls = bigram_cursor.execute('select url from urls where rowid <= ?',
                                        (maxRows,)).fetchall()
    trigram_urls = trigram_cursor.execute('select url from urls where rowid <= ?',
                                          (maxRows,)).fetchall()
    urls_in_common = set(bigram_urls) | set(trigram_urls)
    print(len(urls_in_common))


def compare_results(db, allDomains):
    my_results = set(get_results(db, 1000000, allDomains))
    with open(BASE_DIR + 'lists/filteredweb.txt', 'r') as f:
        filteredweb_results = set(f.read().splitlines())
    difference = sorted(my_results - filteredweb_results)
        
    print(db)
    print('# of censored domains found by CensorSearch:', len(my_results))
    print('# of censored domains found by FilteredWeb:', len(filteredweb_results))
    print('Length of the set difference:', len(difference))
    return my_results

     
if __name__ == "__main__":
    bigram_results = sorted(compare_results('bigrams.db', False))
    trigram_results = sorted(compare_results('trigrams.db', False))
    total_results = sorted(set(bigram_results) | set(trigram_results))
    print('Total # of censored domains discovered:', len(total_results))

    with open('bigram_list.txt', 'w') as blocklist:
        for domain in bigram_results:
            blocklist.write(domain + '\n')

    with open('trigram_list.txt', 'w') as blocklist:
        for domain in trigram_results:
            blocklist.write(domain + '\n')

    with open('total_list.txt', 'w') as blocklist:
        for domain in total_results:
            blocklist.write(domain + '\n')            
