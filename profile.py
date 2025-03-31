import pandas as pd

path = 'Data_base/profile.csv'

class Profile():
    def __init__(self, name, nik, work_schendule = None,dohod = None):
        self.name = name
        self.nik = nik
        self.work_schendule = work_schendule
        self.dohod = dohod
        self.friends = None


def add_profile(profile:Profile):
    df = pd.read_csv(path)
    new_row = {"name":profile.name,"nik": profile.nik,
              "work_schendule": profile.work_schendule,"dohod":profile.dohod,
               "friends":profile.friends}
    df = pd.concat([df,pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(path,index=False)

def has_profile(nik):
    df = pd.read_csv(path)
    result = df[df["nik"] == nik]
    if result.empty:
        return False
    return result

# my_profile = Profile("Evgen","Microgboss","5/2",50000)
# add_profile(my_profile)

df = pd.read_csv(path)
print(has_profile("Microgboss"))