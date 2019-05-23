from django.shortcuts import render, HttpResponse, redirect, reverse
import datetime
import time

# Create your views here.
from app01.models import Module, Course_to_Module, Course, User, Attendance_Record
import numpy as np
import cv2
import pickle
import os
import hashlib
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from PIL import Image


def login(request):
    hl = hashlib.md5()
    if request.method == 'GET':
        s_id = request.session.get('s_id')
        role = request.session.get('role')
        # print(user.name)
        if s_id is not None and role is "student":
            return redirect(reverse('exist_photo'))
        elif s_id is not None:
            return redirect(reverse('home'))
    else:
        s_id = request.POST.get('s_id')
        password = request.POST.get('password')
        hl.update(password.encode(encoding='utf-8'))
        password = hl.hexdigest()
        if User.objects.filter(s_id=s_id, password=password).exists():
            user = User.objects.get(s_id=s_id, password=password)
            request.session['s_id'] = s_id
            request.session['name'] = user.name
            request.session['role'] = user.role
            request.session['c_id_id'] = user.c_id.id
            request.session['id'] = user.id
            remember = request.POST.get("remember")
            # print(remember)
            if remember != 'remember':
                request.session.set_expiry(0)
            if user.role == "student":
                return redirect(reverse('exist_photo'))
            else:
                return redirect(reverse('home'))

        else:
            render(request, 'login.html', {"title": "login", "meg": "id or password incorrect"})

        # try:
        #     user = User.objects.get(s_id=s_id, password=password)
        # except:
        #     render(request, 'login.html', {"title": "login", "meg": "id or password incorrect"})
        #     print("fuck")
        # else:
        #     # remember = request.POST.get("remember")
        #     # if remember == 'remember':
        #     request.session['s_id'] = s_id
        #     return redirect(reverse('home'))

    return render(request, 'login.html', {"title": "login"})


def logout(request):
    request.session.flush()  # 键和值一起清空
    return render(request, 'login.html', {"title": "login"})


def home(request):
    s_id = request.session.get('s_id')  # 登入用的 id
    id = request.session.get('id')  # 唯一的id
    role = request.session.get('role')
    c_id_id = request.session.get('c_id_id')

    print(role)

    if s_id is None:
        return redirect(reverse('login'))
    today = time.strftime('%Y-%m-%d', time.localtime(time.time()))

    now_time = time.strftime('%H:%M:%S', time.localtime(time.time()))

    week_day = time.strftime('%w', time.localtime(time.time()))
    week_day = int(week_day)

    print(today, now_time, week_day)

    try:
        if role == "teacher":
            course_module = \
                Course_to_Module.objects.select_related("c_id", "m_id", "s_id").get(start_date__lte=today,
                                                                                    end_date__gte=today,
                                                                                    start_time__lte=now_time,
                                                                                    end_time__gte=now_time, s_id_id=id,
                                                                                    weekday=week_day, )  # 教師的首頁
        else:
            course_module = \
                Course_to_Module.objects.select_related("c_id", "m_id", "s_id").get(start_date__lte=today,
                                                                                    end_date__gte=today,
                                                                                    start_time__lte=now_time,
                                                                                    end_time__gte=now_time,
                                                                                    c_id_id=c_id_id,
                                                                                    weekday=week_day, )  # 學生的首頁
    except:

        context = {
            "course_module": {"m_id": {"name": "no course at this time"}}
        }
        return render(request, 'home.html', context=context)
    else:
        today = datetime.date.today()
        today = today.strftime('%Y-%m-%d')
        user_list = User.objects.filter(c_id_id=course_module.c_id.id, role="student")  # 拿到該課程學生的列表

        attendance_record = Attendance_Record.objects.filter(
            c_to_m_id_id=course_module.id, today_date=today)

        request.session['c_to_m_id_id'] = course_module.id

        for user in user_list:
            if not Attendance_Record.objects.filter(c_to_m_id_id=course_module.id, today_date=today,
                                                    s_id_id=user.id).exists():
                Attendance_Record.objects.create(today_date=today, arrive_time="00:00:00",
                                                 is_late=0, is_abs=1, c_to_m_id_id=course_module.id,
                                                 s_id_id=user.id)

        context = {
            "title": home,
            "course_module": course_module,
            # "module": module,
            # "course": course,
            "user_list": user_list,
            "attendance_record": attendance_record

        }

        return render(request, 'home.html', context=context)

    # course_module = Course_to_Module.objects.all()
    # for c_m in course_module:
    #
    #     print(c_m.start_date, c_m.end_date, c_m.start_time, c_m.end_time, week_day)

    # module = Module.objects.filter(id=course_module.m_id_id)[0]
    # course = Course.objects.filter(id=course_module.c_id_id)[0]


def t_history(request):
    print("hehe")

    if request.method == 'GET':
        course_id = request.GET.get('course_id')
        print(course_id)
        module_id = request.GET.get('module_id')
        date = request.GET.get('date')
        time = request.GET.get('time')
        s_id = request.session.get('s_id')
        id = request.session.get('id')
        # print(user.name)
        data = []
        page = request.GET.get('page')
        if s_id is None:
            return redirect(reverse('login'))
        elif time is not None:
            course_module = \
                Course_to_Module.objects.filter(c_id_id=course_id,
                                                m_id_id=module_id, s_id_id=id,
                                                start_time=time, )

            attendance_record = Attendance_Record.objects.select_related("s_id").filter(today_date=date,
                                                                                        c_to_m_id__in=course_module)

            paginator = Paginator(attendance_record, 10)  # 每页显示2条
            try:
                attendance_record_p = paginator.page(page)
            except PageNotAnInteger:
                # 如果请求的页数不是整数，返回第一页。
                attendance_record_p = paginator.page(1)
            except EmptyPage:
                # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
                attendance_record_p = paginator.page(paginator.num_pages)

            for a_r in attendance_record_p:
                d = {'id': a_r.s_id.id, 's_id': a_r.s_id.s_id, 'name': a_r.s_id.name, 'role': a_r.s_id.role,
                     'arrive_time': a_r.arrive_time.strftime('%H:%M:%S'), 'is_late': a_r.is_late, 'is_abs': a_r.is_abs,
                     'a_r_id': a_r.id, }
                print(d)
                data.append(d)

            print(data)
            data1 = {
                'num_pages': paginator.num_pages, 'current_page': page,
                'has_previous': attendance_record_p.has_previous(), 'has_next': attendance_record_p.has_next(),
                'data': data
            }
            return JsonResponse(data1, safe=False)
        elif date is not None:
            course_module = \
                Course_to_Module.objects.select_related("c_id", "m_id", "s_id").filter(
                    c_id_id=course_id,
                    m_id_id=module_id, s_id_id=id,
                ).values('start_time').distinct()
            # attendance_record = Attendance_Record.objects.filter(today_date=date, c_to_m_id__in=course_module).values(
            #     'today_date').distinct()

            for c_m in course_module:
                print(c_m)
                d = {'start_time': c_m['start_time'].strftime('%H:%M:%S')}
                print(d)
                data.append(d)
            return JsonResponse(data, safe=False)

        elif module_id is not None:
            course_module = \
                Course_to_Module.objects.filter(c_id_id=course_id, m_id_id=module_id, s_id_id=id)

            attendance_record = Attendance_Record.objects.order_by("-today_date").filter(
                c_to_m_id__in=course_module).values(
                'today_date').distinct()
            # today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            # for c_m in course_module:
            #     getEveryDay(c_m.start_date, today)

            print(attendance_record)
            for a_r in attendance_record:
                print(a_r)
                d = {'today_date': a_r['today_date'].strftime('%Y-%m-%d')}
                print(d)
                data.append(d)
            return JsonResponse(data, safe=False)

        elif course_id is not None:
            course_module = \
                Course_to_Module.objects.select_related("c_id", "m_id", "s_id").filter(c_id_id=course_id,
                                                                                       s_id_id=id).distinct()
            for c_m in course_module:
                d = {"id": c_m.m_id.id, "m_id": c_m.m_id.m_id, "name": c_m.m_id.name}
                data.append(d)
            print(data)
            return JsonResponse(data, safe=False)
        else:
            course_module = \
                Course_to_Module.objects.select_related("c_id", "m_id", "s_id").filter(s_id_id=id).distinct()
            # print(s_id)
            # print(course_module)
            context = {

                "course_module": course_module,

            }
    else:
        is_abs = request.POST.get('is_abs')

        time1 = request.POST.get('time')
        # s_id = request.POST.get('s_id')
        a_r_id = request.POST.get('a_r_id')
        data = {}
        attendance_record = Attendance_Record.objects.select_related("c_to_m_id").get(id=a_r_id)
        if is_abs == "false":
            is_abs = False
            data['is_abs'] = False
        else:
            data['is_abs'] = True
            data['is_late'] = False
            attendance_record.is_abs = True
            attendance_record.is_late = False
            attendance_record.save()
            return JsonResponse(data, safe=False)

        attendance_record.is_abs = is_abs
        ptime = datetime.datetime.strptime(time1, '%H:%M')  # string to datetime.datetime
        s_start_time = attendance_record.c_to_m_id.start_time.strftime('%H:%M:%S')  # datetime.time to string
        s_start_time = datetime.datetime.strptime(s_start_time, '%H:%M:%S')  # string to datetime.datetime

        # ptime=ptime.time().isoformat()
        # ptime = datetime.time.strptime(time,"%H:%M")
        ptime1 = datetime.datetime.strptime(time1, '%H:%M').time()  # string to datetime.time
        # print(ptime)
        # print(s_start_time)
        # print(attendance_record.is_late)
        # print(attendance_record.arrive_time)
        # print(type(attendance_record.arrive_time))
        # print(ptime1)
        # print(type(ptime1))
        # print(attendance_record)
        if (ptime - s_start_time).seconds <= 600:
            print((ptime - s_start_time).seconds)
            attendance_record.is_late = False
            data['is_late'] = False
        elif (s_start_time - ptime).seconds <= 300:
            print((s_start_time - ptime).seconds)
            attendance_record.is_late = False
            data['is_late'] = False
        else:
            attendance_record.is_late = True
            data['is_late'] = True
        attendance_record.arrive_time = ptime1
        attendance_record.save()
        return JsonResponse(data, safe=False)

    return render(request, 't_history.html', context=context)


def s_history(request):
    context = {}

    if request.method == 'GET':

        module_id = request.GET.get('module_id')

        s_id = request.session.get('s_id')
        id = request.session.get('id')
        # print(user.name)
        data = []
        page = request.GET.get('page')

        if s_id is None:
            return redirect(reverse('login'))
        elif module_id is not None:
            course_module = \
                Course_to_Module.objects.filter(m_id_id=module_id)
            attendance_record = Attendance_Record.objects.order_by("-today_date").select_related("c_to_m_id").filter(
                s_id_id=id,
                c_to_m_id__in=course_module)

            paginator = Paginator(attendance_record, 10)  # 每页显示2条
            # print(attendance_record)
            # for today_date in attendance_record:
            #     print(today_date.today_date)

            attendance_time = 0
            total_time = 0
            for a_r in attendance_record:
                s_start_time = a_r.c_to_m_id.start_time.strftime('%H:%M:%S')  # datetime.time to string
                s_start_time = datetime.datetime.strptime(s_start_time, '%H:%M:%S')  # string to datetime.datetime
                s_end_time = a_r.c_to_m_id.end_time.strftime('%H:%M:%S')  # datetime.time to string
                s_end_time = datetime.datetime.strptime(s_end_time, '%H:%M:%S')  # string to datetime.datetime
                s_arrive_time = a_r.arrive_time.strftime('%H:%M:%S')  # datetime.time to string
                s_arrive_time = datetime.datetime.strptime(s_arrive_time, '%H:%M:%S')  # string to datetime.datetime

                total_time += (s_end_time - s_start_time).seconds
                if not a_r.is_abs:
                    attendance_time += (s_end_time - s_arrive_time).seconds
                else:
                    attendance_time += 0

            try:
                attendance_record_p = paginator.page(page)
            except PageNotAnInteger:
                # 如果请求的页数不是整数，返回第一页。
                attendance_record_p = paginator.page(1)
            except EmptyPage:
                # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
                attendance_record_p = paginator.page(paginator.num_pages)

            # attendance_time = 0
            # total_time = 0

            for a_r in attendance_record_p:
                d = {'id': a_r.id, 'today_date': a_r.today_date.strftime('%Y-%m-%d'),
                     'start_time': a_r.c_to_m_id.start_time.strftime('%H:%M:%S'),
                     'end_time': a_r.c_to_m_id.end_time.strftime('%H:%M:%S'), 'class_room': a_r.c_to_m_id.class_room,
                     'arrive_time': a_r.arrive_time.strftime('%H:%M:%S'), 'is_late': a_r.is_late, 'is_abs': a_r.is_abs,
                     }
                data.append(d)
            if attendance_time == 0:
                attendance_rate = 0
            else:
                attendance_rate = (attendance_time / total_time) * 100

            data1 = {
                'num_pages': paginator.num_pages, 'current_page': page,
                'has_previous': attendance_record_p.has_previous(), 'has_next': attendance_record_p.has_next(),
                'attendance_rate': attendance_rate,
                'data': data
            }
            return JsonResponse(data1, safe=False)



        else:
            m_id_id = Attendance_Record.objects.filter(s_id_id=id, ).values('c_to_m_id').distinct()
            course_to_module = Course_to_Module.objects.select_related("m_id").filter(id__in=m_id_id)
            print(course_to_module)

            # print(s_id)
            # print(course_module)
            context = {

                "course_to_module": course_to_module,

            }

        return render(request, 's_history.html', context=context)


def open_camera(request):
    BASE_DIR = os.path.dirname(os.path.os.path.abspath(__file__))
    # print(BASE_DIR)
    face_cascade = cv2.CascadeClassifier(BASE_DIR + '/static/src/cascades/data/haarcascade_frontalface_alt2.xml')
    # eye_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_eye.xml')
    # smile_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_smile.xml')

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(BASE_DIR + "/static/src/recognizers/face-trainner.yml")

    labels = {"person_name": 1}
    with open(BASE_DIR + "/static/src/pickles/face-labels.pickle", 'rb') as f:
        og_labels = pickle.load(f)
        labels = {v: k for k, v in og_labels.items()}  # {'0':'wong','1':'chan'}

    cap = cv2.VideoCapture(0)

    while (True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        for (x, y, w, h) in faces:
            # print(x,y,w,h)
            roi_gray = gray[y:y + h, x:x + w]  # (ycord_start, ycord_end)
            roi_color = frame[y:y + h, x:x + w]

            # recognize? deep learned model predict keras tensorflow pytorch scikit learn
            id_, conf = recognizer.predict(roi_gray)
            if conf >= 45 and conf <= 85:
                # print(5: #id_)
                # print(labels[id_])
                color = (0, 255, 0)  # BGR 0-255
                stroke = 2
                end_cord_x = x + w
                end_cord_y = y + h
                cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)

                font = cv2.FONT_HERSHEY_SIMPLEX

                s_id, name = labels[id_].split("-")

                color = (255, 255, 255)
                stroke = 2
                cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)
                attendance_record(request, s_id)
            else:

                color = (0, 0, 255)  # BGR 0-255
                stroke = 2
                end_cord_x = x + w
                end_cord_y = y + h
                cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
        # subitems = smile_cascade.detectMultiScale(roi_gray)
        # for (ex,ey,ew,eh) in subitems:
        #	cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        # Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


def attendance_record(request, s_id):
    c_to_m_id_id = request.session.get('c_to_m_id_id')
    user = User.objects.get(s_id=s_id)
    today = datetime.date.today()
    today = today.strftime('%Y-%m-%d')
    now_time = datetime.datetime.now().strftime("%H:%M:%S")
    # now_time = time.time()
    # now_time = now_time.strftime('%H:%M:%S')
    a_r = Attendance_Record.objects.select_related("c_to_m_id").filter(today_date=today,
                                                                       c_to_m_id_id=c_to_m_id_id, s_id_id=user.id)

    if not a_r:
        return JsonResponse({"status": 0, "msg": "no data update"}, safe=False)

    if (a_r[0].arrive_time.strftime("%H:%M:%S") == "00:00:00"):
        s_start_time = a_r[0].c_to_m_id.start_time.strftime('%H:%M:%S')  # datetime.time to string
        s_start_time = datetime.datetime.strptime(s_start_time, '%H:%M:%S')  # string to datetime.datetime
        s_arrive_time = datetime.datetime.strptime(now_time, '%H:%M:%S')  # string to datetime.datetime
        if (s_start_time - s_arrive_time).seconds <= 300:
            print("early: " + (s_start_time - s_arrive_time).seconds)
            late = False
        elif (s_arrive_time - s_start_time).seconds <= 600:
            late = False
            print("late: " + (s_arrive_time - s_start_time).seconds)
        else:
            print("real late")
            late = True
        Attendance_Record.objects.filter(today_date=today,
                                         c_to_m_id_id=c_to_m_id_id, s_id_id=user.id).update(
            arrive_time=now_time, is_abs=False, is_late=late)
        return JsonResponse({"status": 1, "s_id": s_id, "msg": "table need to update"}, safe=False)
    return JsonResponse({"status": 0, "msg": "no data update"}, safe=False)


# return render(request, 'home.html')


def exist_photo(request):
    arr = []
    BASE_DIR = os.path.dirname(os.path.os.path.abspath(__file__))
    file_dir = BASE_DIR + '/static/src/images/'
    for dirs in os.listdir(file_dir):
        print(dirs)  # 当前路径下所有子目录
        arr.append(dirs)
    print(arr)
    if request.session.get('s_id') + "-" + request.session.get('name') in arr:
        return redirect(reverse('home'))
    else:
        return render(request, 'take_photo.html')


def take_photo(request):
    BASE_DIR = os.path.dirname(os.path.os.path.abspath(__file__))
    savePath = BASE_DIR + '/static/src/images/' + request.session.get('s_id') + "-" + request.session.get('name')
    cam_id = 0
    face_size = (47, 62)
    # monitor_winSize = (640, 480)

    face_cascade = cv2.CascadeClassifier(BASE_DIR + '/static/src/cascades/data/haarcascade_frontalface_alt2.xml')
    # face_cascade = cv2.CascadeClassifier('objects\\lbpcascade_frontalface.xml')

    if not os.path.exists(savePath):
        os.makedirs(savePath)

    camera = cv2.VideoCapture(0)
    i = 0
    while True:
        (grabbed, img) = camera.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=10,
            minSize=face_size,
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        font = cv2.FONT_HERSHEY_SIMPLEX
        color = (255, 255, 255)
        stroke = 2
        for (x, y, w, h) in faces:

            if (w > face_size[0] and h > face_size[1]):
                roi_color = img[y:y + h, x:x + w]
                now = datetime.datetime.now()
                if (i < 100):
                    faceName = '%s_%s_%s_%s_%s_%s_%s.jpg' % (
                        now.year, now.month, now.day, now.hour, now.minute, now.second, i)
                    cv2.imwrite(savePath + "\\" + faceName, roi_color)
                    i += 1
                else:
                    cv2.putText(img, "finish, press 'q' to close camera", (x, y), font, 1, color, stroke,
                                cv2.LINE_AA)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)

        cv2.imshow("Frame", img)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

            # When everything done, release the capture
    camera.release()
    cv2.destroyAllWindows()
    image_dir = BASE_DIR + "/static/src/images/"
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    current_id = 0
    label_ids = {}  # {'wong':0,'chan':1}
    y_labels = []
    x_train = []
    for root, dirs, files in os.walk(image_dir):
        for file in files:
            if file.endswith("png") or file.endswith("jpg"):
                path = os.path.join(root, file)
                print('root', root)
                print('path', path)
                # arr = os.path.basename(root).split("-")
                # label = arr[1].replace(" ", "-").lower()
                label = os.path.basename(root)
                print(label)
                # print(label, path)
                if not label in label_ids:
                    label_ids[label] = current_id
                    current_id += 1
                id_ = label_ids[label]
                # print(label_ids)
                # y_labels.append(label) # some number
                # x_train.append(path) # verify this image, turn into a NUMPY arrray, GRAY
                pil_image = Image.open(path).convert("L")  # grayscale
                size = (550, 550)

                final_image = pil_image.resize(size, Image.ANTIALIAS)
                image_array = np.array(final_image, "uint8")  # 轉換所有圖像為 numpy array
                # print(image_array)
                # faces = face_cascade.detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=5)
                # print(image_array)

                # for (x, y, w, h) in faces:
                #     roi = image_array[y:y + h, x:x + w]
                #     x_train.append(roi)
                #     y_labels.append(id_)
                x_train.append(image_array)
                y_labels.append(id_)

    # print(y_labels)
    # print(x_train)

    with open(BASE_DIR + "/static/src/pickles/face-labels.pickle", 'wb') as f:
        pickle.dump(label_ids, f)

    recognizer.train(x_train, np.array(y_labels))  # x_train存圖片, y_labels存標籤
    recognizer.save(BASE_DIR + "/static/src/recognizers/face-trainner.yml")

    return JsonResponse({"msg": "train photo success"}, safe=False)
