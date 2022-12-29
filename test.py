count=10
page=0
o=0
lst=[0,1,2,3,4,5,6,7,8,9,10]
while True:
    if page > 1 and page<count:
        a=input(f"back:'<'\nnext:'>' --:")
        if a == '>':
            page+=1
            print(lst[o:page])
            o=page
        elif a == '<':
            page-=1
            print(lst[page:o])
            o=page
    elif page <= 1:
        a=input(f"{page} next:'>' --:")
        page+=1
        print(lst[o:page])
        o=page
    elif page>=count:
        a=input(f"{page}back:'<':")
        page-=1
        print(lst[page:o])
        o=page