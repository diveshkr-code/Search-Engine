

#var-to crawl: is the list of pages left to crawl
#var-crawled: collest all the links which have already been crawled

# PART 1: Given a url collect all links in the url
#Given a url this code will find all the links in that url by
#1.Extract source code using get_page
#2.Using get_all_links
def get_page(url):
        import requests
        return requests.get(url).text


def get_next_target(page):
    start_link = page.find('<a href=')

    if start_link == -1 :
        return None, 0

    star_quote = page.find('"', start_link)
    end_quote = page.find('"', star_quote + 1)
    url = page[star_quote + 1 : end_quote ]
    return url, end_quote


def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else :
            break
    return links
#   END OF PART 1


# PART 2: Crawl the web from a seed page and collect all links and index it in a list

#   union: Takes 2 lists and makes list1 the union of those lists
def union(list1, list2):
    for i in list2:
        if i not in list1:
            list1.append(i)

#   crawl_web: Given a seed page as input will output list of all the links below it as you browse deeper.
def crawl_web(seed):
    to_crawl = [seed]
    crawled = []
    index={}
    graph = {}
    i=0
    while to_crawl:
        current = to_crawl.pop()
        if current not in crawled and current[0:4]=='http' and i<=100 :   #i<100: to reduce time to get results
            #current[0:4]: prevents schema error from requests package
            #https://stackoverflow.com/questions/30770213/no-schema-supplied-and-other-errors-with-using-requests-get
            content=get_page(current)
            add_page_to_index(index,current,content)
            oulinks = get_all_links(content)
            graph[current] =  oulinks
            union(to_crawl, oulinks)
            crawled.append(current)
        i+=1

    return index, graph


# add_page_to_index: split the content(source code) into words(keyword) and add them into the index
def add_page_to_index(index,url,content):
    words=content.split()
    for entry in words:
        add_to_index(index,entry,url)
    return index


def add_to_index(index,keyword,url):
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword]=[url]



# PART 3: Responding to search queries
#Respond to queries if any url contains the keyword given that will be returned
def lookup(index,keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None


#string.split() doesn't work perfectly it seperates on whitespace only hence the punctuation marks
#like ',' remain at seperated word
def split_string(source,splitlist):
    output=[]
    atsplit=True
    for char in source:
        if char in splitlist:
            atsplit=True
        else:
            if atsplit:
                output.append(char)
                atsplit=False
            else:
                output[-1]=output[-1]+char
    return output


#PART 4: Create a hash table

#Hash function:
def hash(string,buckets):
    hash_val = 0
    for ch in string:
        hash_val+=ord(ch)

    return hash_val%buckets

def make_hash_tables(no_buckets):
    hash_table=[]
    for i in range(0,no_buckets):
        hash_table.append([])

    return hash_table


#hashtable_get_bucket: Take the kekyword hash it and return the bucket that might contains that keyword
def hashtable_get_bucket(hash_table,keyword):
    bucket_no = hash(keyword,len(hash_table))
    return hash_table[bucket_no]


def hashtable_lookup(hash_table,word):
    bucket=hashtable_get_bucket(hash_table,word)
    for entry in bucket:
        if entry[0] == word:
            return entry[1]

    return None

def hashtable_update(hash_table,word,value):
    bucket=hashtable_get_bucket(hash_table,word)
    for entry in bucket:
        if entry[0]==word:
            entry[1]=value
            return

    bucket.append([word,value])


#Compute popularity ranks of web pages using RELAXATION ALGORITHM
def compute_ranks(graph):
    d=0.8 #dampoing coefficient
    num_loops=10
    ranks={}
    new_ranks={}
    no_pages=len(graph)
    for page in graph:
        ranks[page]=1.0/no_pages

    for i in range(0,num_loops):
        new_ranks={}
        for page in graph:
            new_ranks[page]= (1-d)/no_pages
            for node in graph:
                if page in graph[node]:
                    new_ranks[page]+= d * ranks[node] / len(graph[node])

        ranks=new_ranks

    return ranks



print(get_all_links(get_page('http://stackexchange.com')))
##
"""
    print(add_page_to_index([],'http://titan.dcs.bbk.ac.uk/~kikpef01/testpage.html',
    get_page('http://titan.dcs.bbk.ac.uk/~kikpef01/testpage.html')))
"""
##

index=[]
print(crawl_web('http://titan.dcs.bbk.ac.uk/~kikpef01/testpage.html'))
print(hash('au',12))

index, graph = crawl_web('http://google.com')
print(compute_ranks(graph))
