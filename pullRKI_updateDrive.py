# Set up path references and dependencies.
import os

# Import important helper libraries.
from datetime import datetime
import mimetypes

# Import modules created to serve the project.
from utils import DB_interface as DBI
from utils.Drive_interface import Drive
from utils import path_config as pc


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


print("now: ", datetime.now())
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
print("RKI data drive upload finished")
