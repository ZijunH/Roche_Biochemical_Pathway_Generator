import os
import urllib.request
import shutil
import workerpool
from PIL import Image


url = "http://mapserver1.biochemical-pathways.com"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
maps = {"map1": (54, 38), "map2": (45, 38)}
features = ("grid", "background",  "regulatoryEffects", "higherPlants",
            "unicellularOrganisms", "coenzymes", "substrates", "enzymes")
X_SIZE = 1024
Y_SIZE = 1024


class DownloadJob(workerpool.Job):
    def __init__(self, loc_url, save_to):
        self.loc_url = loc_url
        self.save_to = save_to

    def run(self):
        req = urllib.request.Request(url=self.loc_url, headers=headers)
        with urllib.request.urlopen(req) as response, open(self.save_to, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)


class MergerJob(workerpool.Job):
    def __init__(self, map_name, i, j):
        self.map_name = map_name
        self.i = i
        self.j = j

    def run(self):
        with Image.new('RGBA', (X_SIZE, Y_SIZE), "white") as local_canvas:
            for feature in features:
                make_dir(self.map_name, "merged")
                store_loc = store_location_maker(
                    self.map_name, feature, self.i, self.j)
                with Image.open(store_loc).convert("RGBA") as canvas:
                    if canvas.size[0] != X_SIZE or canvas.size[1] != Y_SIZE:
                        canvas.resize((X_SIZE, Y_SIZE))
                    local_canvas.paste(canvas, (0, 0), white2alpha(canvas))
            make_dir(self.map_name, "merged", self.i)
            store_loc = store_location_maker(
                self.map_name, "merged", self.i, self.j)
            local_canvas.save(store_loc)


def url_maker(map_name, feature, i, j):
    return ("%s/%s/%s/6/%d/%d.png" % (url, map_name, feature, i, j))


def store_location_maker(map_name, feature, i, j):
    return ("%s/%s/%d/%d.png" % (map_name, feature, i, j))


def white2alpha(img):
    pixdata = img.load()
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pixdata[x, y] == (255, 255, 255, 255):
                pixdata[x, y] = (255, 255, 255, 0)
    return img


def make_dir(*args):
    args = map(lambda x: str(x), args)
    dir_name = "/".join(args)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def save_imgs():
    pool = workerpool.WorkerPool(size=10)
    for map_name in maps:
        i_range = maps[map_name][0]
        j_range = maps[map_name][1]
        make_dir(map_name)
        for feature in features:
            make_dir(map_name, feature)
            for i in range(i_range):
                make_dir(map_name, feature, i)
                for j in range(j_range):
                    loc_url = url_maker(map_name, feature, i, j)
                    save_to = store_location_maker(map_name, feature, i, j)
                    job = DownloadJob(loc_url, save_to)
                    pool.put(job)
    pool.shutdown()
    pool.wait()
    # proofread
    pool = workerpool.WorkerPool(size=10)
    for map_name in maps:
        i_range = maps[map_name][0]
        j_range = maps[map_name][1]
        make_dir(map_name)
        for feature in features:
            make_dir(map_name, feature)
            for i in range(i_range):
                make_dir(map_name, feature, i)
                for j in range(j_range):
                    loc_url = url_maker(map_name, feature, i, j)
                    save_to = store_location_maker(map_name, feature, i, j)
                    if not os.path.exists(save_to):
                        job = DownloadJob(loc_url, save_to)
                        pool.put(job)
    pool.shutdown()
    pool.wait()


def get_layers():
    pool = workerpool.WorkerPool(size=10)
    for map_name in maps:
        i_range = maps[map_name][0]
        j_range = maps[map_name][1]
        # (0, 24, 28, 37, 45)
        for i in range(i_range):
            for j in range(j_range):
                job = MergerJob(map_name, i, j)
                pool.put(job)
    pool.shutdown()
    pool.wait()
    # proofread due to exceptions in concurrency
    pool = workerpool.WorkerPool(size=10)
    for map_name in maps:
        i_range = maps[map_name][0]
        j_range = maps[map_name][1]
        for i in range(i_range):
            for j in range(j_range):
                store_loc = store_location_maker(map_name, "merged", i, j)
                if not os.path.exists(store_loc):
                    job = MergerJob(map_name, i, j)
                    pool.put(job)
    pool.shutdown()
    pool.wait()


def merge_layers():
    for map_name in maps:
        i_range = maps[map_name][0]
        j_range = maps[map_name][1]
        x_dim = X_SIZE * i_range
        y_dim = Y_SIZE * j_range
        with Image.new('RGBA', (x_dim, y_dim), (255, 255, 255, 0)) as feature_canvas:
            for i in range(i_range):
                for j in range(j_range):
                    store_loc = store_location_maker(map_name, "merged", i, j)
                    with Image.open(store_loc) as canvas:
                        feature_canvas.paste(canvas, (i * X_SIZE, j * Y_SIZE))
            feature_canvas.save(map_name + ".png")


print("Process Begins")
save_imgs()
get_layers()
merge_layers()
print("Process Ends")
