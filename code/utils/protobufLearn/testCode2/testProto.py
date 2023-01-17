import person_pb2
# import testProto.p


def setInfo(a_info):
    a_info.id = 1
    a_person = a_info.people
    a_person.age = 88
    a_person.name = "first_name"
    score1 = a_person.score.add()
    score1.object = "python"
    score1.score = 90
    score2= a_person.score.add()
    score2.object = "c++"
    score2.score = 88
    phone = a_person.number
    phone.phone = 400100
    phone.type = 2
    # print(a_info)
    return a_info

first_info = person_pb2.one()
one_info = setInfo(first_info)
print(one_info)
proto_info = one_info.SerializeToString()
print(proto_info)

def getInfo(wanted_info):
    wanted_id = wanted_info.id
    print("info id:", wanted_id)
    print("his age: ", wanted_info.people.age)
    for sco in wanted_info.people.score:
        print("his scores:",sco)
    print("his phoneType:", wanted_info.people.number.type)
    if wanted_info.people.number.type == wanted_info.people.PhoneType.HOME:
        print("his phonetype: HOME")

first_parsed = person_pb2.one()
first_parsed.ParseFromString(proto_info)
# print(first_parsed)
getInfo(first_parsed)