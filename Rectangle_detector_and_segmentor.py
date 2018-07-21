import cv2
import os
import numpy as np
import datetime
image_folder_path = "/Users/pallawi/dev/AI/Data/"
output_folder = "/Users/pallawi/dev/AI/Results/"

def morphology(Cannyedges):
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7))
    dilation = cv2.dilate(Cannyedges,kernel,iterations = 1)
    # cv2.imshow("dilation",dilation)
    # cv2.waitKey(0)
    return dilation

def takeSecond(elem):
    return elem[1]

def rotateimage(warp,output_folder):
    (h, w) = warp.shape[:2]
    center= (w / 2, h / 2)
    scale = 1.0
    date_and_time = datetime.datetime.now()
    d_t = date_and_time.isoformat()
    d_t = str(d_t)
    d_t = d_t.replace(".", "")
    d_t = d_t.replace(":", "")
    d_t = d_t.replace("-", "")
    while(1):
        cv2.imshow("Input to rotate",warp)
        key = cv2.waitKey(5000) & 0xFF
        if key == ord("1"):
            angle180 = 180
            M = cv2.getRotationMatrix2D(center, angle180, scale)
            rotated180 = cv2.warpAffine(warp, M, (w, h))
            cv2.imshow('saving image',rotated180)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            image_name = output_folder + "rotated_visiting_card_detected"+"_"+d_t + ".jpg"
            cv2.imwrite(image_name,rotated180)
            break
        elif key == ord("0"):
            break
        elif key == ord("2"):
            cv2.imshow('Saving image',warp)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            image_name = output_folder + "not_rotated_visiting_card_detected"+"_"+d_t + ".jpg"
            cv2.imwrite(image_name,warp)
            break



def find_Contours_manger(image_rez,ratio,orig,output_folder):
    gray = cv2.cvtColor(image_rez, cv2.COLOR_BGR2GRAY) #Convert image to graysacle
    blurred = cv2.GaussianBlur(gray, (5, 5), 0) #removed noise GaussianBlur
    bilateralFilter_image = cv2.bilateralFilter(blurred,7,10,10)#preserve edge and filter noise
    Cannyedges = cv2.Canny(bilateralFilter_image,10,120)#detect the edges using canny
    # cv2.imshow("Cannyedges",Cannyedges)
    # cv2.waitKey(0)
    dilation = morphology(Cannyedges)
    im2, contours, hierarchy = cv2.findContours(dilation,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    count = 0
    for c in contours:
        count = count + 1

        perimeter = cv2.arcLength(c,True)
        # print "perimeter",perimeter
        approx = cv2.approxPolyDP(c, 0.04 * perimeter, True)
        if len(approx) == 4:
            cv2.drawContours(image_rez,[c],-1,(0,0,255),1)
            # cv2.imshow("drawContours",image_rez)
            # cv2.waitKey(0)
            cv2.destroyAllWindows()
            Roi_coord_points = approx.reshape(4, 2)#reshape to work easier
            rect = np.zeros((4, 2), dtype = "float32")
            distance = [0]*4
            sum_coord = Roi_coord_points.sum(axis = 1)
            rect[0] = Roi_coord_points[np.argmin(sum_coord)]#top left
            distance[0] = np.sqrt(((rect[0][0]- Roi_coord_points[0][0])**2)+((rect[0][1]- Roi_coord_points[0][1])**2))
            distance[1] = np.sqrt(((rect[0][0]- Roi_coord_points[1][0])**2)+((rect[0][1]- Roi_coord_points[1][1])**2))
            distance[2] = np.sqrt(((rect[0][0]- Roi_coord_points[2][0])**2)+((rect[0][1]- Roi_coord_points[2][1])**2))
            distance[3] = np.sqrt(((rect[0][0]- Roi_coord_points[3][0])**2)+((rect[0][1]- Roi_coord_points[3][1])**2))
            sorted_distance = enumerate(distance)

            sorted_distance = sorted(sorted_distance,key = takeSecond, reverse = True)

            bottom_right_index = sorted_distance[0][0]
            bottom_right = Roi_coord_points[bottom_right_index]
            rect[2] = bottom_right
            top_right_index = sorted_distance[1][0]
            top_right = Roi_coord_points[top_right_index]
            rect[1] = top_right
            bottom_left_index = sorted_distance[2][0]
            bottom_left  = Roi_coord_points[bottom_left_index]
            rect[3]=bottom_left

            rect *= ratio
            (tl, tr, br, bl) = rect
            # print "----------------",(tl, tr, br, bl)
            widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
            widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))

            heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
            heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))

            maxWidth = max(int(widthA), int(widthB))
            maxHeight = max(int(heightA), int(heightB))

            dst = np.array([
	           [0, 0],
	           [maxWidth - 1, 0],
	           [maxWidth - 1, maxHeight - 1],
	           [0, maxHeight - 1]], dtype = "float32")
            M = cv2.getPerspectiveTransform(rect, dst)
            # print M
            warp = cv2.warpPerspective(orig, M, (maxWidth, maxHeight))
            rotateimage(warp,output_folder)

            print "---------------------------approx---start-----------------------"
            # print "count",count
            print 'approx',approx
            # print "ROI CORD",Roi_coord_points
            print "sum",sum_coord
            print "distance",distance
            print "sorted_distance",sorted_distance
            # print "diff",diff
            print "rectangel_proper",rect
            # print "widthA",widthA
            # print "widthB",widthB
            # print "heightA",heightA
            # print "heightB",heightB
            print "---------------------------approx---stop-----------------------"



if __name__ == '__main__':
    for filename in os.listdir(image_folder_path):
    	image_full_path = image_folder_path + filename
    	print "image_full_path",image_full_path
    	image = cv2.imread(image_full_path,1)#read image data
        ratio = image.shape[0] / 560.0
        orig = image.copy()
        # image_rez = image
        image_rez = cv2.resize(image, (560, 560))#resize image
        find_Contours_manger(image_rez,ratio,orig,output_folder)
