mydict = {
    "key": {
        "key": {
            "key": {
                "key": "potato"
            }
        }
    }
}

level = 0
subobject = mydict

while True:
    print(f"level={level}")
    print(f"subobject={subobject}")

    if isinstance(subobject, dict):
        firstkey = list(subobject.keys())[0]
        subobject = subobject[firstkey]
    else:
        print("Got " + subobject + "!")
        break

    level += 1

print("done!")
