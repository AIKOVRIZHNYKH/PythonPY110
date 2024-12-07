import base64
import json

with open('D:\_test_script\Photo_Artem_Kovrizhnykh.png', 'rb') as file:
    data = file.read()

encoded_data = base64.b64encode(data)
#print(encoded_data)
#print(data.decode('utf-8'))

# print(len(encoded_data))
count_parts = len(encoded_data) // 30000 + 1
# print(count_parts)

future_json = {}
start = 0
end = 30000         # НЕ ВКЛЮЧИТЕЛЬНО

for i in range(count_parts):
    part_name = f"part_{i}"
    part_data = encoded_data[start:end]
    future_json[part_name] = str(part_data)
    start += 30000
    end += 30000

#print(future_json)
#print(json.dumps(future_json, indent=4))

with open('D:\_test_script\Photo_Artem_Kovrizhnykh.json', 'w') as f2:
    json.dump(future_json, f2)
