# Dvigatel klassi - avtomobilning dvigateli(motori) haqida ma'lumot beradi. ishlab_chiqaruvchi,ot_kuchi,dvigatel_turi maydonlari mavjud.
class Dvigatel:
    def __init__(self,ishlab_chiqaruvchi,ot_kuchi,dvigatel_turi):
        self.ishlab_chiqaruvchi = ishlab_chiqaruvchi
        self.ot_kuchi = ot_kuchi
        self.dvigatel_turi = dvigatel_turi
    def __repr__(self):
        return f"Dvigatelni ishlab chiquvchi: {self.ishlab_chiqaruvchi}\nDvigatel kuchi: {self.ot_kuchi} ot kuchi\nDvigatel turi: {self.dvigatel_turi}"

# Avtobil klassi - avtomobilning xususiyatlari haqida ma'lumot berish uchun.
# Avtobil dvigateli xarakteristikasi haqidagi ma'lumotni Dvigatel klassiga tegishli obyekt orqali chiqaramiz
class Avtomobil:
    def __init__(self,model,rang,yil,dvigatel):
        self.model = model
        self.rang = rang
        self.yil = yil
        self.dvigatel = dvigatel

    def __repr__(self):
        return f"Avtomobil modeli: {self.model}\nRangi: {self.rang}\nIshlab chiqarilgan yili: {self.yil}\nDvigateli: {self.dvigatel}"
dvigatel1=Dvigatel("GM",210,'Gibrid')
avto1=Avtomobil("Kia",'Qora',2025,dvigatel1)
print(avto1)