# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 20:30:36 2019

@author: Agata
"""

"""
this code finds the topics in a collection of tweets using Latenet Dirchelet Allocation
"""

from sklearn.decomposition import LatentDirichletAllocation
lda=LatentDirichletAllocation(n_topics=3, learning_method="batch", max_iter=25, random_state=0)
tematy1=lda.fit_transform(R1)
tematy0=lda.fit(R1)

lda.components_.shape
tematy0.components_.shape
#sorting
sorting=np.argsort(lda.components_,axis=1)[:, ::-1]
#feature names
feature_names=np.array(vect.get_feature_names())
#print out the topics
def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Temat %d:" % (topic_idx+1))
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-no_top_words - 1:-1]]))

no_top_words = 15
display_topics(tematy0, feature_names, no_top_words)

# Log Likelyhood: Higher the better
print("Log Likelihood: ", lda.score(R1))

# Perplexity: Lower the better. Perplexity = exp(-1. * log-likelihood per word)
print("Perplexity: ", lda.perplexity(R1))

# See model parameters
print(lda.get_params())

#comaprison of models with differnet number of topics
topics=[3, 5, 10, 15, 20, 25]
data=[R1, R2, R3, R4]
def wybor(topics, data):
    for data in data:
        loglikelihood=[]
        perplexity=[]
        for topics in topics:
            lda=LatentDirichletAllocation(n_topics=topics, learning_method="batch", max_iter=25, random_state=0)
            loglikelihood.append(lda.score(data)) 
            perplexity.append(lda.perplexity(data))  



from sklearn.model_selection import GridSearchCV
# Define Search Param
search_params = {'n_components': [3, 5, 10, 15, 20, 25]}

# Init the Model
lda = LatentDirichletAllocation()
# Init Grid Search Class
model = GridSearchCV(lda, param_grid=search_params)
# Do the Grid Search
model.fit(R1)
# Best Model
best_lda_model = model.best_estimator_
# Model Parameters
print("Best Model's Params: ", model.best_params_)
# Log Likelihood Score
print("Best Log Likelihood Score: ", model.best_score_)
# Perplexity
print("Model Perplexity: ", best_lda_model.perplexity(R1))
# Get Log Likelyhoods from Grid Search Output
model.grid_scores_
n_topics = [3, 5, 10, 15, 20, 25]
log_likelyhoods_5 = [round(gscore.mean_validation_score) for gscore in model.grid_scores_ if gscore.parameters['learning_decay']==0.5]
log_likelyhoods_7 = [round(gscore.mean_validation_score) for gscore in model.grid_scores_ if gscore.parameters['learning_decay']==0.7]
log_likelyhoods_9 = [round(gscore.mean_validation_score) for gscore in model.grid_scores_ if gscore.parameters['learning_decay']==0.9]

log_likelyhoods = [round(gscore.mean_validation_score) for gscore in model.grid_scores_ ]
# Show the results on a graph
plt.figure(figsize=(12, 8))
plt.plot(n_topics, log_likelyhoods)
plt.plot(n_topics, log_likelyhoods_7, label='0.7')
plt.plot(n_topics, log_likelyhoods_9, label='0.9')
plt.title("Comparison of LDA models")
plt.xlabel("Number of topics")
plt.ylabel("Log Likelyhood Scores")
plt.legend(title='Learning decay', loc='best')
plt.show()

