import os,sys
import shutil

from PIL import Image
from progressbar import Percentage, ProgressBar,Bar,ETA

root_path = "/home/crb/datasets/engineer_car/traingPhoto-output/"
server_path = "/data1/datasets/wajueji/images/"
start_count = 745
test_num = 100
train_num = 644
box_num = 817


if __name__ == "__main__" :
    txt_input_dir = root_path + "label/"
    img_input_dir = root_path + "image/"
    txt_output_dir = root_path + "labels/"
    img_output_dir = root_path + "images/"

    if not os.path.exists(img_output_dir):
        os.makedirs(img_output_dir)
    if not os.path.exists(txt_output_dir):
        os.makedirs(txt_output_dir)

    train_txt_path = root_path + "train.txt"
    test_txt_path = root_path + "test.txt"

    txt_input_list = os.listdir(txt_input_dir)
    count = start_count

    train_file = open(train_txt_path, 'w')
    test_file = open(test_txt_path, 'w')

    test_count = 0
    for i in range(1, start_count, 1):

        if i%3 == 0 and test_count < 100:
            test_count += 1
            test_file.write(server_path + "%05d" % i + '.jpg\n')
        else:
            train_file.write(server_path + "%05d" % i + '.jpg\n')


    if count % 10 == 0:

        train_num += 1

    bar = ProgressBar(widgets=[Bar('>', '[', ']'), ' ', Percentage(), ' ', ETA()], maxval=len(txt_input_list))

    #for txt_input_path in bar(txt_input_list):
    for txt_input_path in txt_input_list:
        #print(txt_input_path)
        if not os.path.isfile(txt_input_dir + txt_input_path) or (os.path.splitext(txt_input_path)[-1] != '.txt'):
            continue
        file_name = os.path.splitext(txt_input_path)[-2]
        img_input_path = file_name + ".jpg"

        try:
            image = Image.open(img_input_dir + img_input_path)
            width, height = image.size
        except:
            print(txt_input_path)
            print("no img file!")
            continue

        with open(txt_input_dir + txt_input_path, 'r') as txt_f1:
            txt_lines = txt_f1.readlines()
            #print(txt_lines)
            if len(txt_lines) == 0:
                print(txt_input_path)
                print("label empty!")
                continue

            label_list = []
            for txt_line in txt_lines:

                txt_list = txt_line.split()
                if(len(txt_list) != 5):
                    print(txt_input_path)
                    print(txt_list)
                    print("txt list len error")
                    continue
                class_id = int(txt_list[0])
                x1 = int(txt_list[1])
                y1 = int(txt_list[2])
                x2 = int(txt_list[3])
                y2 = int(txt_list[4])
                if((x1 == 0 and x2 == 0 and y1 == 0 and y2 == 0)
                    or x2 <= x1 or y2 <= y1):
                    print(txt_input_path)
                    print(txt_list)
                    print("label error!")
                    continue

                if (x1 < 0): x1 = 1;
                if (y1 < 0): y1 = 1;
                if (x2 > width): x2 = width - 2;
                if (y2 > height): y2 = height - 2;
                x = (x1 + x2) / 2.0 / width
                y = (y1 + y2) / 2.0 / width
                w = (x2 - x1 - 1) / width
                h = (y2 - y1 - 1) / height
                #print(class_id, x, y, w, h)
                label = [class_id, x, y, w, h]
                label_list.append(label)
            if len(label_list) == 0:
                continue

            img_output_path = "%05d" % count + ".jpg"
            txt_output_path = "%05d" % count + ".txt"
            count += 1

            shutil.copyfile(img_input_dir + img_input_path, img_output_dir + img_output_path)
            #image.save(img_output_dir + img_output_path)
            with open(txt_output_dir + txt_output_path, 'w') as txt_f2:
                for label in label_list:
                    label_txt = "%s %s %s %s %s\n" % (label[0], label[1], label[2], label[3], label[4])
                    #print(label_txt)
                    txt_f2.write(label_txt)
                    box_num += 1

            if count % 20 != 0:
                train_file.write(server_path + img_output_path + '\n')
                train_num += 1
            if count % 10 == 0:
                test_file.write(server_path + img_output_path + '\n')
                test_num += 1

        if count % 100 == 0:
            print(count)

    print("total num")
    print("images: ", count)
    print("train: ", train_num)
    print("test: ", test_num)
    print("box: ", box_num)

    train_file.close()
    test_file.close()
