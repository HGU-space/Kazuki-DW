###############################################
#リレーショナル　データベーすからPetOwnerオブジェクトの
#取り出しと格納
###############################################
from pysqlite2 import dbapi as sqlite
from petowner  import PetOwner

#このペットの飼い主のエントリを挿入：置換
def savePetOwner(petowner, cursor):
    #Dana Mooreのレコード探す場合のクエリの構築
    # SELECT people.id FROM people WHERE people.given_name = 'Dana' AND people.surname = 'Moore'
    q = "SELECT people.id FROM people \
                WHERE people.given_name = '%s' \
                AND people.surname = '%s'"%\
                (petowner.firstname, petowner.lastname)
    cursor.excute(q)
    data = cursor.fetchall()
    #必要なら新しいエントリを作る
    if(data(len)==0):
        #INSERT INTO people VALUES ('Dana', 'Moore', NULL)
        cursor.execute("INSERT INTO people VALUES \
                        ('%s', '%s', NULL)"%\
                        (petowner.firstname, petowner.lastname))
        cursor.execute("select max(id) FROM people") #idの割り当て
        data = cursor.fetchall()
    id = data[0][0]
    cursor.execute("DELETE FROM pets WHERE petowner_id = %d"%id)
    for p in petowner.pets:
        cursor.execute("INSERT INTO pets VALUES ('%s', '%d')"%(p, id))
    #存在するならペットの飼い主のレコードを取り出す
    def loadPetOwner(firstname, lastname, cursor):
        q = "SELECT people.given_name, people.surname, pets.name" + \
            "FROM people, pets" + \
            "WHERE people.id=pets.owner_id + " + \
                "AND people.given_name = '%s''"%firstname + \
                "AND people.surname = '%s''"%lastname
        cursor.execute(q)
        data = cursor.fetchall()
        if(len(data) == 0):
            return None
        firstname = data[0][0]
        lastname  = data[0][1]
        pets = []
        for d in data:
            pets.append(d[2])
        return PetOwner(firstname, lastname, pets)

#保存するコードテスト
if __name__ == "__main__":
    con = sqlite.connect("petsowners", isolataion_level=None)
        cursor = con.cursor
    dana = PetOwner("Dana", "Moore", \
                     ("Fluffy", "Pochie"))
    ray  = PetOwner("Ray", "Budd", ("Itchy", "Scratchy"))
    bill = PetOwner("Bill", "Wright", ("Snowball1", "Snowball2"))

    savePetOwner(dana, cursor)
    savePetOwner(ray, cursor)
    savePetOwner(bill, cursor)

    d = loadPetOwner("Dana", "Moore", cursor)
    print d

    cursor.close()
    con.close()

