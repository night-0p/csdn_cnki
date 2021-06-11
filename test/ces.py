def get_file(file):
    f=file
    user_list=[]
    password_list=[]
    phone_list=[]
    for i in f.readlines():
        line=i.decode("gbk")
        user=line.split(',')[0]
        user_list.append(user)
        password=line.split(',')[1]
        password_list.append(password)
        phone=line.split(',')[2].replace('\n','')
        phone_list.append(phone)
    print(user_list)
