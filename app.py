########################################################################################
######################          Import packages      ###################################
########################################################################################
from flask import Blueprint, render_template, flash, request
from werkzeug.wrappers import AcceptMixin
from flask_login import login_required, current_user
from __init__ import create_app, db

import base64
import requests
from models import Prediction

import numpy as np
import cv2
from PIL import Image

from tensorflow import keras
import tensorflow as tf
import base64
import cv2


import json

import flask_monitoringdashboard as dashboard

########################################################################################
# our main blueprint
main = Blueprint('main', __name__)


def convert_one_channel(img):
    #some images have 3 channels , although they are grayscale image
    if len(img.shape)>2:
        img=img[:,:,0]
        return img
    else:
        return img



@main.route('/') # home page that return 'index'
def index():
    return render_template('index.html')

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():

    x_image = ''
    y_image = ''


    if request.method == 'POST':

        img = request.files['image']

        x_image = base64.b64encode(img.read()).decode("utf-8")
        
        payload = json.dumps({"base64str": x_image,})

        try:
            response = requests.put("https://dentalsegmentationapicontainer.azurewebsites.net/predict", data = payload)

            y_image = response.json()

            img = Image.open(img)
            x_image = np.array(img)
            
            x_image = cv2.imencode('.jpg', x_image)[1].tobytes()
            x_image = base64.b64encode(x_image).decode("utf-8")
            x_image = 'data:image/jpg;base64, ' + x_image

            #####################################SAVE TO DATABASE################################################################
            new_prediction = Prediction(dr_email = current_user.email, base64_x= x_image, base64_y = y_image[1])
            ## add the new prediction to the database
            db.session.add(new_prediction)
            db.session.commit()
            print("Saved to db")


            return render_template('profile.html', name=current_user.name, x_image=x_image, segmented_image=y_image[1] ,y_image=y_image[0], state="Version du modèle: 0.2")


        except Exception as e:

            print(e)
            return render_template('profile.html', name=current_user.name, x_image=x_image, y_image=y_image, state="Le modèle de segmentation n'est pas connecté :(")


    return render_template('profile.html', name=current_user.name, x_image=x_image, y_image=y_image, state="")   

        ################################################################################################################


@main.route('/predictions') # define predictions path
@login_required
def predictions(): 
    
    user_predictions = Prediction.query.filter_by(dr_email=current_user.email).all()

    return render_template('predictions.html', predictions=user_predictions, dr_email=current_user.email)



app = create_app() # we initialize our flask app using the __init__.py function
dashboard.bind(app)
if __name__ == '__main__':
    db.create_all(app=create_app()) # create the SQLite database
    app.run(debug=True) # run the flask app on debug mode
