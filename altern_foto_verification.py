import dlib
from skimage import io
from scipy.spatial import distance
import os
import pickle

sp = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
facerec = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')
detector = dlib.get_frontal_face_detector()

with open("comp_facedescriptors.pickle", "rb") as f:
    fc_dsks = pickle.load(f)

rec_mins = dict.fromkeys(list(fc_dsks.keys()), 0)
rec_avs = dict.fromkeys(list(fc_dsks.keys()), 0)

def get_name(url):
    # Загружаем первую фотографию

    img = io.imread(url)
    dets = detector(img, 1)

    for k, d in enumerate(dets):
        shape = sp(img, d)
    try:
        face_descriptor1 = facerec.compute_face_descriptor(img, shape)
    except:
        return "noname"
    
    for comp in fc_dsks.keys():
        for face in fc_dsks[comp]:
            a = distance.euclidean(face_descriptor1, face)
            rec_avs[comp] += a
            rec_mins[comp] = a if rec_mins[comp] == 0 else min(rec_mins[comp], a)
    
    min_comps = []
    for comp in rec_mins.keys():
        if rec_mins[comp] < 0.6:
            min_comps.append(comp)
    
    len_min_comps = len(min_comps)
    ret = "noname"
    if len_min_comps > 1:
        avs = list(rec_avs.values())
        keys = list(rec_mins.keys())
        avs = [i/3.0 for i in avs]
        minval = min(avs)
        ret = keys[avs.index(minval)]
    elif len_min_comps == 1:
        ret = min_comps[0]

    if ret == "borodin":
        ret = "Бородин"
    elif ret == "brams":
        ret = "Брамс"
    elif ret == "mozart":
        ret = "Моцарт"
    elif ret == "gaidn":
        ret = "Гайдн"
    elif ret == "glinka":
        ret = "Глинка"
    elif ret == "chaikovskiy":
        ret = "Чайковский"
    elif ret == "rachmaninov":
        ret = "Рахманинов"
    
    return ret

if __name__ == "__main__":
    url = "https://pp.userapi.com/c851132/v851132402/42a26/dCKwCsVQibs.jpg"
    print(get_name(url))
    
    """ls = os.listdir("smpls2")
    counter = 0
    total = len(ls)
    for url in ls:
        name = get_name("smpls2/" + url)
        print(str(url) + ": " + str(name))
        if name == "Бородин":
            counter += 1

    print(counter / total)"""