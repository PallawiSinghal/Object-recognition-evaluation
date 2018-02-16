import cv2

#boxn = [xmin,ymin,xmax,ymax]
boxA = [249,114,452,316]
boxB = [249,114,452,316]
# boxB = [299,164,502,366]#+50 TO ORIGINAL
imgA = "/Users/pallawi/Desktop/test.jpg"
imgB = "/Users/pallawi/Desktop/test.jpg"
def convert(size, box):
    dw = 1./size[0]
    print "pixel width --- dw", dw
    dh = 1./size[1]
    print "pixel height --- dh", dh
    x = (box[0] + box[1])/2.0
    x_draw = x
    print "x wise center coordinate --- x",x
    y = (box[2] + box[3])/2.0
    y_draw = y
    print "y wise center coordinate --- y",y
    w = box[1] - box[0]
    print "bounding box width --- w", w
    h = box[3] - box[2]
    print "bounding box height --- h", h
    x = x*dw
    print "new x = x*dw",x
    w = w*dw
    print "new w = w*dw",w
    y = y*dh
    print "new y = y*dw",y
    h = h*dh
    print "new h = h*dw",h
    return x,y,w,h,y_draw,x_draw

def train_data(img,box):
    image = cv2.imread(img)
    label_image = cv2.rectangle(image,(box[0],box[1]),(box[2],box[3]),(0,255,0),3)
    width_image = int(image.shape[1])
    height_image = int(image.shape[0])
    size = (width_image, height_image)
    print "Image Dimension - width,height",size
    box = (float(box[0]), float(box[2]), float(box[1]), float(box[3]))
    print "box",box
    x,y,w,h,y_draw,x_draw = convert(size, box)
    y_draw = int(y_draw)
    x_draw = int(x_draw)
    print x_draw
    label_image = cv2.rectangle(image,(x_draw,y_draw),(x_draw,y_draw),(0,255,0),3)
    outA = label_image
    return label_image

def test_data(img,box):
    image = cv2.imread(img)
    label_image = cv2.rectangle(image,(box[0],box[1]),(box[2],box[3]),(0,255,0),3)
    width_image = int(image.shape[1])
    height_image = int(image.shape[0])
    size = (width_image, height_image)
    print "Image Dimension - width,height",size
    box = (float(box[0]), float(box[2]), float(box[1]), float(box[3]))
    print "box",box
    x,y,w,h,y_draw,x_draw = convert(size, box)
    y_draw = int(y_draw)
    x_draw = int(x_draw)
    print x_draw
    label_image = cv2.rectangle(image,(x_draw,y_draw),(x_draw,y_draw),(0,255,0),3)
    outB = label_image
    return outB

def bb_intersection_over_union(boxA, boxB):
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
    # compute the area of intersection rectangle
    interArea = (xB - xA + 1) * (yB - yA + 1)
    print "interArea", interArea
    # compute the area of both the prediction and ground-truth
    # rectangles
    boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
    print "boxAArea", boxAArea
    boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
    print "boxBArea", boxBArea
    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = interArea / float(boxAArea + boxBArea - interArea)
    # return the intersection over union value
    return iou

outA = train_data(imgA,boxA)
outB = test_data(imgB,boxB)
iou = bb_intersection_over_union(boxA, boxB)
print "IOU",iou
cv2.imshow("Bounding box tain",outA)
cv2.imshow("Bounding box test",outB)
cv2.waitKey(0)





# Detection("/Users/pallawi/Desktop/test.jpg", [39, 63, 203, 112], [54, 66, 198, 114])
