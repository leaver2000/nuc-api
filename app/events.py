
import datetime
import re

from requests import Session

from .extract import ApacheDir


class NotAvaliable(Exception):
    ...

PATH = "nccf/com/{model}/prod/"

def get_557ww(ragr:ApacheDir, target_day:int)->bool:
    latests_run_saved=False
    for path in ragr.navto(PATH.format(model="557ww")).iterdir():
        date = datetime.datetime.strptime(
            re.search(r"\d+/$", path.url).group(), "%Y%m%d/"
        )
        if date.day == target_day:
            latests_run_saved=True

            for file in path.iterfiles():
                url = file.url
                # filename = url.rsplit("/", maxsplit=1)[-1]
                time_delta = datetime.timedelta(hours=int(url[-4:]))
                valid_time = date + time_delta
                # save_to = Path('ragr-test')  # '/media/external/data/'
                # save_to.mkdir(exist_ok=True)
                if valid_time.day == target_day:
                    ...
                    print("557ww")

    return latests_run_saved


def get_hrrr(ragr:ApacheDir, target_day:int):

    
    def file_condition(url:str):
        return (
            url.endswith("grib2") 
            and "sfc" in url 
            and int(re.search(r"(?<=t)\d{2}(?=z)",url).group()) == 0 
            and int(re.search(r"\d{2}(?=.grib2)", url).group()) < 24
        )
    latests_run_saved=False
    for path in ragr.navto(PATH.format(model="hrrr")).iterdir():
        date = datetime.datetime.strptime(
            re.search(r"\d+/$", path.url).group(), "%Y%m%d/"
        )
        if date.day == target_day:
            latests_run_saved=True
            path = path.navto("conus")

            for file in path.iterfiles(file_condition):
                print(file)
                # url = file.url
                # print(re.search(r"(?<=t)\d{2}(?=z)",url).group())
                # print(url)
                # filename = url.rsplit("/", maxsplit=1)[-1]
                # # time_delta = datetime.timedelta(hours=int(url[-4:]))
                # # valid_time = date + time_delta
                # # # save_to = Path('ragr-test')  # '/media/external/data/'
                # # # save_to.mkdir(exist_ok=True)
                # # if valid_time.day == target_day:
                # #     ...
                # #     print("hrrr")

    return latests_run_saved
def daily_download(
    target_day=int,
) -> None:

    with Session() as session:
        ragr = ApacheDir(session, url="https://nomads.ncep.noaa.gov/pub/data")

        return {
            "557ww":get_557ww(ragr, target_day),
            "hrrr":get_hrrr(ragr, target_day)
            }



if __name__ == "__main__":
    x= daily_download(target_day=datetime.datetime.utcnow().day)
    print(x)

