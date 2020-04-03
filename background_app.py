# Set up path references and dependencies.
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
sys.path.append(os.path.join(parentdir, "utils"))

# Import important helper libraries.
from flask import Flask, render_template
from waitress import serve
from datetime import datetime
import time
import mimetypes
from multiprocessing import Process


# Import modules created to serve the project.
from utils import DB_interface as DBI
from utils.Drive_interface import Drive
from utils import path_config as pc


app = Flask(__name__)
# Global variable
#DAYS = 500

@app.route('/')
def index():
    return render_template("index.html")



@app.route('/start_bckgrnd_update')
def start_bckgrnd_update():
    p = Process(target=bckgrnd_update, name="background_update")
    p.start()
    #p.join()
    now = datetime.now()
    user = {'username': 'MSE!'}
    posts = [
        {
            'author': {'username': 'Paul'},
            'body': 'Henrik has the update just been started?'
        },
        {
            'author': {'username': 'Henrik'},
            'body': 'You bet your sweet ass it has!'
        },
        {
            'author': {'username': 'Paul'},
            'body': 'So what time was is when it started?'
        },
        {
            'author': {'username': 'Henrik'},
            'body': 'It was exactly %s !' % now
        }

    ]
    return render_template("index.html", title="home", user = user, posts=posts)

def bckgrnd_update():
    drive = Drive()
    path = pc.get_RKI_landkreise_file()
    filename = path.name


    RKI = pc.get_RKI_file()
    RKI_name = RKI.name
    RKI_landkreise = pc.get_RKI_landkreise_file()
    RKI_landkreiseName = RKI_landkreise.name
    drive = Drive()

    drive.download_latest_file(RKI_landkreiseName, RKI_landkreise)
    drive.download_latest_file(RKI_name, RKI)

    updating = True
    while updating:
        print(datetime.now())
        # get str of today's date yyyy-mm-dd
        day = datetime.today()
        day_str = day.__str__()[:10]
        # cut filename and extension
        RKI_landkreiseName_no_ext, RKI_landkreise_ext = os.path.splitext(RKI_landkreiseName)
        RKI_Name_no_ext, RKI_ext = os.path.splitext(RKI_name)
        # construct filename with date
        RKI_landkreiseName_w_date = RKI_landkreiseName_no_ext + "_" + day_str + RKI_landkreise_ext
        RKI_Name_w_date = RKI_Name_no_ext + "_" + day_str + RKI_ext
        print("updating RKI DBs now")
        DB = DBI.DB_interface()
        DB.update_RKI_csv()
        DB.update_RKI_landkreise_csv()
        print("files updated")
        #guess mimetype
        mimetype_RKI, encoding_RKI = mimetypes.guess_type(RKI)
        mimetype_RKI_landkreise, encoding_RKI_landkreise = mimetypes.guess_type(RKI_landkreise)

        #upload files to drive
        drive.upload_file(RKI, RKI_Name_w_date, mimetype_RKI)
        drive.upload_file(RKI_landkreise, RKI_landkreiseName_w_date, mimetype_RKI_landkreise)
        day = 24 * 3600
        time.sleep(day)

if __name__ == "__main__":
    serve(app)
