from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import numpy as np

import matplotlib.pyplot as plt
import matplotlib

# matplotlib.use('Agg')

average_drop_rate = 0

lr_model = LogisticRegression()


def startup():
    global lr_model

    users_array = np.genfromtxt('previsions.csv', delimiter=',')
    average_drop_rate = (np.mean([i[0] for i in users_array]) * 100)

    X_train, X_test, y_train, y_test = train_test_split([i[1:] for i in users_array], [i[0] for i in users_array],
                                                        test_size=0.4, random_state=42)

    lr_model.fit(X_train, y_train)


def test_new_client(data):
    cd_sex, mt_rev, nb_enf, age_ad, cd_tmt_0, cd_tmt_2, cd_tmt_4, cd_tmt_6, cd_sit_fam_A, cd_sit_fam_B, cd_sit_fam_C, \
    cd_sit_fam_D, cd_sit_fam_E, cd_sit_fam_F, cd_sit_fam_G, cd_sit_fam_M, cd_sit_fam_P, cd_sit_fam_S, cd_sit_fam_U, \
    cd_sit_fam_V, cd_tmt_0, cd_tmt_2, cd_tmt_4, cd_tmt_6, cd_cat_cl_10, cd_cat_cl_21, cd_cat_cl_22, cd_cat_cl_23, \
    cd_cat_cl_24, cd_cat_cl_25, cd_cat_cl_32, cd_cat_cl_40, cd_cat_cl_50, cd_cat_cl_61, cd_cat_cl_82, cd_cat_cl_98 = data

    new_client = [[cd_sex, mt_rev, nb_enf, age_ad, cd_tmt_0, cd_tmt_2, cd_tmt_4, cd_tmt_6, cd_sit_fam_A, cd_sit_fam_B,
                   cd_sit_fam_C,
                   cd_sit_fam_D, cd_sit_fam_E, cd_sit_fam_F, cd_sit_fam_G, cd_sit_fam_M, cd_sit_fam_P, cd_sit_fam_S,
                   cd_sit_fam_U,
                   cd_sit_fam_V, cd_tmt_0, cd_tmt_2, cd_tmt_4, cd_tmt_6, cd_cat_cl_10, cd_cat_cl_21, cd_cat_cl_22,
                   cd_cat_cl_23,
                   cd_cat_cl_24, cd_cat_cl_25, cd_cat_cl_32, cd_cat_cl_40, cd_cat_cl_50, cd_cat_cl_61, cd_cat_cl_82,
                   cd_cat_cl_98]]
    Y_pred = lr_model.predict_proba(new_client)
    drop_probability = Y_pred[0][1] * 100

    fig = plt.figure()
    objects = ('Average Drop Rate', 'New Client')
    y_pos = np.arange(len(objects))
    performance = [average_drop_rate,
                   drop_probability]

    ax = fig.add_subplot(111)
    colors = ['gray', 'blue']
    plt.bar(y_pos, performance, align='center', color=colors, alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.axhline(average_drop_rate, color="r")
    plt.ylim([0, 100])
    plt.ylabel('Drop Probability')
    plt.title('New client drop rate probability \n ' +
              str(round(drop_probability, 2)) + '% ')

    plt.show()


if __name__ == '__main__':
    startup()

    clients = [
        (2, 0, 0, 85, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (1, 0, 0, 74, 1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0),
        (2, 0, 0, 85, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (2, 0, 0, 55, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (2, 0, 0, 41, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (2, 0, 0, 30, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (1, 0, 0, 30, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (1, 0, 0, 80, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    ]

    for cl in clients:
        test_new_client(cl)
