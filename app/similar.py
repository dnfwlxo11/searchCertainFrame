from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.applications.inception_v3 import preprocess_input
from tensorflow.keras.applications.efficientnet import EfficientNetB0
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model
from numpy import dot
from numpy.linalg import norm
from pathlib import Path
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import os
import tensorflow as tf

# 특징 추출할때 사용할 모델 선택
def setModel(model):
    if (model == 'VGG16'):
        model = VGG16(weights='imagenet')
        model = Model(inputs=model.input, outputs=model.get_layer('fc1').output)
    elif (model == 'InceptionV3'):
        model = InceptionV3(weights='imagenet')
        model = Model(inputs=model.input, outputs=model.get_layer('avg_pool').output)
    elif (model == 'EfficientNet-B0'):
        model = EfficientNetB0(weights='imagenet')
        model = Model(inputs=model.input, outputs=model.get_layer('avg_pool').output)
    elif (model == 'ResNet50'):
        model = ResNet50(weights='imagenet')
        model = Model(inputs=model.input, outputs=model.get_layer('avg_pool').output)
    else:
        print('{} 모델은 없거나 지원하지 않습니다.'.format(model))
    
# 이미지에서 특성 추출
def feature_extractor(model, img):
    img = Image.open(img)
    img = img.resize((model.input.shape[1], model.input.shape[2]))
    img = img.convert('RGB')
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    feature = model.predict(x)[0]
    return feature / np.linalg.norm(feature)

# 특정 디렉토리 내의 이미지들 경로를 추출
def getImageDB_li(dirName):
    imageDB_li = os.listdir('static/{}/{}/'.format(dirName, dirName))
    imageDB_li = ['static/{}/{}/'.format(dirName, dirName) + image for image in imageDB_li]
    
    return imageDB_li

# 이미지 데이터베이스에서 특징을 추출하여 *.npy 형식으로 추출
def setImageDB(imageDB_li, dirName):
    if not os.path.exists(dirName + '_npy'):
        os.mkdir('static/{}/{}_npy'.format(dirName, dirName))
    for img in sorted(imageDB_li):
        feature = feature_extractor(model, img)

        feature_path = 'static/{}/{}_npy/'.format(dirName, dirName) + img.split('/')[-1].split('.')[0] + '.npy'
        np.save(feature_path, feature)

# 코사인 유사도
def cos_sim(a, b):
    return dot(a, b)/(norm(a)*norm(b))

# 유클리디언 유사도
def euclidean(features, query):
    return np.linalg.norm(features - query, axis=1)

def speedMode(dirName, src, len):
    print('스피드 모드')
    query = np.sum(feature_extractor(model, src))

    features = []
    img_path = []
    for img_npy in Path('static/{}/{}_npy/'.format(dirName, dirName)).glob('*.npy'):
        features.append(np.load(img_npy))
        img_path.append(os.path.join('static/{}/{}/'.format(dirName, dirName), img_npy.stem + '.jpg'))

    features_dict = {}
    cnt = 0
    for item in features:
        features_dict[cnt] = abs(np.sum(item) - query)
        cnt+=1

    features_dict = sorted(features_dict.items(), key=(lambda x:x[1]))

    speed_features = []
    speed_imgPath = []
    keys_ = list(dict(features_dict).keys())

    for index in keys_:
        speed_features.append(features[index])
        speed_imgPath.append(img_path[index])

    print(speed_features, speed_imgPath)
    return speed_features[:int(len)], speed_imgPath[:int(len)]

def getFeatureAndPath(dirName):
    print('일반 모드')

    features = []
    img_path = []
    for img_npy in Path('static/{}/{}_npy/'.format(dirName, dirName)).glob('*.npy'):
        features.append(np.load(img_npy))
        img_path.append(os.path.join('static/{}/{}/'.format(dirName, dirName), img_npy.stem + '.jpg'))
        
    return features, img_path
        
# 유클리디언 유사도 계산
def calc_euclienan(features, img_path, src):
    query = feature_extractor(model, src)
    result = euclidean(features, query)
    
    ids = np.argsort(result)
    scores = [(result[id], img_path[id]) for id in ids]

    return scores

# 코사인 유사도 계산
def calc_cossim(features, img_path, src):
    query = feature_extractor(model, src)
    result = []
    for feature in features:
        result.append(cos_sim(feature, query))

    ids = np.argsort(result)
    print(len(ids))
    scores = [(result[id], img_path[id]) for id in ids]
    
    return scores
    
# 그래프를 그림
def draw_graph(result, scores, title):
    axes=[]
    fig=plt.figure(figsize=(24,24))
    plt.title(title)

    for a in range(len(scores)):
        score = scores[a]
        axes.append(fig.add_subplot(9, 3, a+1))
        subplot_title=str(score[0])
        axes[-1].set_title(subplot_title)  
        plt.axis('off')
        img = Image.open(score[1])
        plt.imshow(img)

    fig.tight_layout()
    plt.show()

os.environ["CUDA_VISIBLE_DEVICES"]= '0, 1'

physical_devices = tf.config.list_physical_devices('GPU')
try:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
    tf.config.experimental.set_memory_growth(physical_devices[1], True)
except:
    pass

model = VGG16(weights='imagenet')
model = Model(inputs=model.input, outputs=model.get_layer('fc1').output)