import cv2
import dlib
import base64
import json
import uuid


def return_msg(error, msg):
    return_data = {
        "uuid": str(uuid.uuid1()),
        "error": error,
        "message": msg
    }
    print(return_data)
    return return_data


def addHat(img, hat_img):
    print("分离rgba通道，合成rgb三通道帽子图，a通道后面做mask用")
    r, g, b, a = cv2.split(hat_img)
    rgbHat = cv2.merge((r, g, b))

    print("dlib人脸关键点检测器,正脸检测")
    predictorPath = "shape_predictor_5_face_landmarks.dat"
    predictor = dlib.shape_predictor(predictorPath)
    detector = dlib.get_frontal_face_detector()
    dets = detector(img, 1)

    print("如果检测到人脸")
    if len(dets) > 0:
        for d in dets:
            x, y, w, h = d.left(), d.top(), d.right() - d.left(), d.bottom() - d.top()

            print("关键点检测，5个关键点")
            shape = predictor(img, d)

            print("选取左右眼眼角的点")
            point1 = shape.part(0)
            point2 = shape.part(2)

            print("求两点中心")
            eyes_center = ((point1.x + point2.x) // 2, (point1.y + point2.y) // 2)

            print("根据人脸大小调整帽子大小")
            factor = 1.5
            resizedHatH = int(round(rgbHat.shape[0] * w / rgbHat.shape[1] * factor))
            resizedHatW = int(round(rgbHat.shape[1] * w / rgbHat.shape[1] * factor))

            if resizedHatH > y:
                resizedHatH = y - 1

            print("根据人脸大小调整帽子大小")
            resizedHat = cv2.resize(rgbHat, (resizedHatW, resizedHatH))

            print("用alpha通道作为mask")
            mask = cv2.resize(a, (resizedHatW, resizedHatH))
            maskInv = cv2.bitwise_not(mask)

            print("帽子相对与人脸框上线的偏移量")
            dh = 0
            bgRoi = img[y + dh - resizedHatH:y + dh,
                    (eyes_center[0] - resizedHatW // 3):(eyes_center[0] + resizedHatW // 3 * 2)]

            print("原图ROI中提取放帽子的区域")
            bgRoi = bgRoi.astype(float)
            maskInv = cv2.merge((maskInv, maskInv, maskInv))
            alpha = maskInv.astype(float) / 255

            print("相乘之前保证两者大小一致（可能会由于四舍五入原因不一致）")
            alpha = cv2.resize(alpha, (bgRoi.shape[1], bgRoi.shape[0]))
            bg = cv2.multiply(alpha, bgRoi)
            bg = bg.astype('uint8')

            print("提取帽子区域")
            hat = cv2.bitwise_and(resizedHat, cv2.bitwise_not(maskInv))

            print("相加之前保证两者大小一致（可能会由于四舍五入原因不一致）")
            hat = cv2.resize(hat, (bgRoi.shape[1], bgRoi.shape[0]))
            print("两个ROI区域相加")
            addHat = cv2.add(bg, hat)

            print("把添加好帽子的区域放回原图")
            img[y + dh - resizedHatH:y + dh,
            (eyes_center[0] - resizedHatW // 3):(eyes_center[0] + resizedHatW // 3 * 2)] = addHat

            return img


def main_handler(event, context):
    try:
        try:
            print("将接收到的base64图像转为pic")
            imgData = base64.b64decode(json.loads(event["body"])["pic"])
            with open('/tmp/picture.png', 'wb') as f:
                f.write(imgData)
        except Exception as e:
            return return_msg(True, "未能成功获取到头像，请检查pic参数是否为base64编码。")

        try:
            print("读取帽子素材以及用户头像")
            hatImg = cv2.imread("hat.png", -1)
            userImg = cv2.imread("/tmp/picture.png")

            output = addHat(userImg, hatImg)
            cv2.imwrite("/tmp/output.jpg", output)
        except Exception as e:
            return return_msg(True, "图像添加圣诞帽失败，请检查图片中是否有圣诞帽或者图片是否可读。")

        print("读取头像进行返回给用户，以Base64返回")
        with open("/tmp/output.jpg", "rb") as f:
            base64Data = str(base64.b64encode(f.read()), encoding='utf-8')

        return return_msg(False, {"picture": base64Data})
    except Exception as e:
        return return_msg(True, str(e))


def test():
    with open("test.png", 'rb') as f:
        image = f.read()
        image_base64 = str(base64.b64encode(image), encoding='utf-8')
    event = {
        "requestContext": {
            "serviceId": "service-f94sy04v",
            "path": "/test/{path}",
            "httpMethod": "POST",
            "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
            "identity": {
                "secretId": "abdcdxxxxxxxsdfs"
            },
            "sourceIp": "14.17.22.34",
            "stage": "release"
        },
        "headers": {
            "Accept-Language": "en-US,en,cn",
            "Accept": "text/html,application/xml,application/json",
            "Host": "service-3ei3tii4-251000691.ap-guangzhou.apigateway.myqloud.com",
            "User-Agent": "User Agent String"
        },
        "body": "{\"pic\":\"%s\", \"base\":\"1\"}" % image_base64,
        "pathParameters": {
            "path": "value"
        },
        "queryStringParameters": {
            "foo": "bar"
        },
        "headerParameters": {
            "Refer": "10.0.2.14"
        },
        "stageVariables": {
            "stage": "release"
        },
        "path": "/test/value",
        "queryString": {
            "foo": "bar",
            "bob": "alice"
        },
        "httpMethod": "POST"
    }
    print(main_handler(event, None))


if __name__ == "__main__":
    test()
