########## integrating data ##########
test150824 = pd.DataFrame( [ ] )
##########

folder = './file/' # not set yet
f_list = ['A.xlsx', 'B.xlsx', 'C.xlsx', 'D.xlsx']

for frame in f_list:
    fpath = folder + frame
    temp = pd.read_excel(fpath)
    test150824 = test150824.append(temp)

test150824.columns = ['content', 'tag', 'date', 'place']


# removing repeated data
test150824.drop_duplicates(subset = [ "content"] , inplace = True)
test150824.to_excel('./file/test150824.xlsx', index = False)
