import json

f = open("changeAttendancePK.json", "r")

s = f.read()

x = json.loads(s)

q = 1968

for a in x:
	# print(a['pk'])
	a['pk'] = q
	q = q+1

# print()

ff = open("changeAttendancePK2.json", "w")
ff.write(json.dumps(x, indent=2));


f.close()