import translator

input = "test tes2 test5"
output = []
buffer = ""
word = ""


for x in input:
    if x == " ":
        output.append(word)
        word = ""
    else:
        word = word + x
output.append(word)

print(output)