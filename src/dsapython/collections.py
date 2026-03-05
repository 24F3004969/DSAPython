from collections import Counter


def do_done(li):
    dir_is = dict(Counter(li))
    return dir_is


my_di = do_done(
    [1006, 1008, 1009, 1008, 1007, 1005, 1008, 1001, 1003, 1009, 1006, 1003, 1004, 1002, 1008, 1005, 1004, 1007, 1006,
     1002, 1002, 1001, 1004, 1001, 1003, 1007, 1007, 1005, 1004, 1002])
sorted_di = dict(sorted(my_di.items(), key=lambda x: [x[1]], reverse=True))
map_list = {}
for i in sorted_di:
    if sorted_di[i] not in map_list:
        map_list[sorted_di[i]] = [i]
    else:
        map_list[sorted_di[i]].append(i)
lis=[]
for k in map_list.values():
    lis+=sorted(k)
print(lis)


