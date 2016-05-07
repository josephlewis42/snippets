import random

def euclidian_distance(x, y):
	# calculates the euclidian distance between vectors x and y
	
	inner = map(lambda tup: (tup[0] - tup[1])**2, zip(x,y))
	dist  = sum(inner) ** .5  # sqrt
	
	return dist


def calculate_centroid(vectors):
	# calculates a new centroid based on vectors
	pairs = zip(*vectors)
	n = float(len(vectors))
	
	return [sum(pair) / n for pair in pairs]


def nearest_k(x, k):
	# returns the index of the vector in k that is nearest to x
	distances = [euclidian_distance(x, i) for i in k]
	return distances.index(min(distances))
		

rounds = 0
def k_means(data, k, last_assignments=None):
	global rounds
	# choose our initial vectors
	if not isinstance(k, list):
		k = random.sample(data, k)
	
	# setup our last assignmetns if not already done
	if last_assignments == None:
		last_assignments = [-1] * len(data)
	
	# Assignment step
	assignments = [nearest_k(x,k) for x in data]

	# Update step
	new_k = [-1] * len(k)
	for i, vec in enumerate(k):
		group = filter(lambda x: x[0] == i, zip(assignments, data))
		group = map(lambda x: x[1], group)
		new_k[i] = calculate_centroid(group)
	
	rounds += 1
	if assignments == last_assignments:
		return assignments
	return k_means(data, new_k, assignments)

wordlist = ["hot","chocolate","cocoa","beans","ghana","africa","butter",
"truffles","sweet","sugar","cane","brazil","beet","cake","icing",
"black","forest", "harvest"]

docs = []

def add_document(words):
	words = words.strip().split(" ")
	doc = [w in words for w in wordlist]
	doc = map(float, doc)
	docs.append(doc)

add_document("hot chocolate cocoa beans")
add_document("cocoa ghana africa")
add_document("beans harvest ghana")
add_document("cocoa butter")
add_document("butter truffles")
add_document("sweet chocolate")
add_document("sweet sugar")
add_document("sugar cane brazil")
add_document("sweet sugar beet")
add_document("sweet cake icing")
add_document("cake black forest")


print k_means(docs, 5)
print rounds
