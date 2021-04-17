word = 'geeks for geeks'

# returns first occurrence of Substring
result = word.find('geeks')
print("Substring 'geeks' found at index:", result)

result = word.find('')
print("Substring '' found at index:", result)

# How to use find()
if (word.find('') != -1):
    print("Contains given substring ")
else:
    print("Doesn't contains given substring")
