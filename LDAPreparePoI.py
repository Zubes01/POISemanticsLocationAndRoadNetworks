from gensim import models
from gensim.test.utils import datapath

from LDALearner import places_reviews

import os, csv
import CONSTANTS

import nltk



def main():
    folder_name = "LDA_Model_" + str(CONSTANTS.CATEGORY_NUM)
    city = "WDC"

    if os.path.exists(folder_name + "/" + city + "CleanedText.csv"):
        print("Start Loading Cleaned Text...")

        with open(folder_name + "/" + city + "CleanedText.csv", 'r') as rhandle:
            rfile = csv.reader(rhandle, delimiter='|')

            reviews = {}

            for each_row in rfile:
                reviews[each_row[0]] = reviews.get(each_row[0], []) + [each_row[1]]
    else:
        reviews = places_reviews("TripAdvisorCrawler/attraction" + city + "TripAdvisor.csv")

        with open(folder_name + "/" + city + "CleanedText.csv", 'a', newline='') as whandle:
            spamwriter = csv.writer(whandle, delimiter='|')

            for k, v in reviews.items():
                for each_review in v:
                    spamwriter.writerow([k, each_review])

    print("----------------------------------------")

    if not os.path.exists(folder_name + "/" + city + "DivVector.csv"):
        print("Start Generating Div Vector...")

        counter = [0] * CONSTANTS.CATEGORY_NUM

        model_file = datapath(os.getcwd() + "/" + folder_name + "/ldaTrainedModel")
        trained_model = models.LdaModel.load(model_file)
        dict_word = trained_model.id2word

        with open(folder_name + "/" + city + "DivVector.csv", 'a', newline='') as whandle:
            spamwriter = csv.writer(whandle)

            for k, v in reviews.items():
                corpus = dict_word.doc2bow((" ".join(v)).split())
                lda_score = [x[1] for x in trained_model[corpus]]

                category_idx = lda_score.index(max(lda_score))
                counter[category_idx] += 1

                spamwriter.writerow([k] + lda_score)

        print("Num of PoIs in each category: ", counter)


if __name__ == "__main__":
    main()