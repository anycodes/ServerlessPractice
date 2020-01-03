# -*- coding: utf8 -*-

import qrcode, uuid, json, base64
from PIL import Image, ImageDraw, ImageFont


def return_msg(error, msg):
    return_data = {
        "uuid": str(uuid.uuid1()),
        "error": error,
        "message": msg
    }
    print(return_data)
    return return_data


def get_qrcode(url):
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=8,
        border=1,
    )

    # 传入数据
    qr.add_data(url)
    qr.make(fit=True)
    # 生成二维码
    img = qr.make_image()
    # 保存二维码
    img.save('/tmp/qrcode.png')
    return Image.open('/tmp/qrcode.png').convert("RGBA")


def get_input_str(input_str, font, draw, need_height=False):
    length = 0
    new_str = ""
    max_height = []
    for eve in input_str:
        width, height = draw.textsize(eve, font)
        max_height.append(height)
        length = length + width
        if length > 804 and eve != "\n":
            length = width
            new_str = new_str + "\n" + eve
        else:
            new_str = new_str + eve
    if need_height:
        if len(new_str.split("\n")) > 10:
            return False
        return (new_str, max(max_height) * len(new_str.split("\n")) if "\n" in new_str else max(max_height))
    else:
        return new_str


def do_watermark(temp_watermark_pic, watermark_pic_new_x, watermark_pic_new_y):
    for i in range(watermark_pic_new_x):
        for k in range(watermark_pic_new_y):
            color = temp_watermark_pic.getpixel((i, k))
            if color != (255, 255, 255, 0):
                color = color[:-1] + (40,)
                temp_watermark_pic.putpixel((i, k), color)
    return temp_watermark_pic


def main_handler(event, context):
    try:
        json_data = json.loads(event["body"])
        frame_file = "./base/frame/%s.png" % (json_data["frame"])
        title_file = "./base/word/%s.png" % (json_data["title"])
        watermark_file = "./base/others/%s.png" % (json_data["watermark"])
        font = ImageFont.truetype('./base/font/%s.ttf' % (json_data["font"]), 40)
        input_str = json_data["text"]
        from_str = json_data["from"]
        to_str = json_data["to"]
        symbol_file = "http://greetingcard.0duzhan.com/fu.html?id=%s" % (json_data["symbol"])
    except Exception as e:
        print(e)
        return return_msg(True, "参数获取失败")

    if len(from_str) > 20:
        return return_msg(True, "落款昵称不可超过20字符")
    if len(to_str) > 20:
        return return_msg(True, "被赠与人昵称不可超过20字符")
    if len(input_str) > 200:
        return return_msg(True, "祝福内容不可以超过200字")

    try:
        temp_base_pic = Image.new('RGBA', (954, 1348), (255, 255, 255))
        frame_pic = Image.open(frame_file).convert("RGBA").resize((954, 1348), Image.ANTIALIAS)
        title_pic = Image.open(title_file).convert("RGBA")
        watermark_pic = Image.open(watermark_file).convert("RGBA")
        title_pic_x, title_pic_y = title_pic.size
        title_pic_new_x = 310
        title_pic_new_y = int(title_pic_y * title_pic_new_x / title_pic_x)
        title_pic = title_pic.resize((title_pic_new_x, title_pic_new_y), Image.ANTIALIAS)
        watermark_pic_x, watermark_pic_y = watermark_pic.size
        watermark_pic_new_x = 800
        watermark_pic_new_y = int(watermark_pic_y * watermark_pic_new_x / watermark_pic_x)
        watermark_pic = watermark_pic.resize((watermark_pic_new_x, watermark_pic_new_y), Image.ANTIALIAS)
        temp_watermark_pic = Image.new('RGBA', (watermark_pic_new_x, watermark_pic_new_y), (255, 255, 255, 0))
        temp_watermark_pic.paste(watermark_pic, (0, 0), watermark_pic)
        temp_watermark_pic = do_watermark(temp_watermark_pic, watermark_pic_new_x, watermark_pic_new_y)
        temp_base_pic.paste(frame_pic, (0, 0), frame_pic)
        temp_base_pic.paste(title_pic, (320, 30), title_pic)
        temp_base_pic.paste(temp_watermark_pic, (77, int((1348 - int(watermark_pic_new_y)) / 2)), temp_watermark_pic)
        temp_base_pic.paste(get_qrcode(symbol_file),  (355, 970), get_qrcode(symbol_file))
        draw = ImageDraw.Draw(temp_base_pic)
        draw.text((75, 300), get_input_str(to_str + ":", font, draw), (0, 0, 0), font=font)
        temp_data = get_input_str(input_str, font, draw, True)
        if not temp_data:
            return return_msg(True, "不要有太多的换行哦")
        input_str, content_height = temp_data
        draw.text((75, 400), input_str, (0, 0, 0), font=font)
        length_data = 850
        for eve_ap in from_str:
            width, height = draw.textsize(eve_ap, font)
            length_data = length_data - width
        draw.text((length_data, content_height + 400), get_input_str(from_str, font, draw), (0, 0, 0), font=font)
        draw.text((415, 1240), get_input_str("扫码抽取新年福", font, draw), (0, 0, 0),
                  font=ImageFont.truetype('./base/font/01.ttf', 20))
        temp_base_pic.save("/tmp/test_output.png")
        with open("/tmp/test_output.png", "rb") as f:
            base64Data = str(base64.b64encode(f.read()), encoding='utf-8')
        return return_msg(False, {"picture": base64Data})
    except Exception as e:
        print(e)
        return return_msg(True, "贺卡生成失败")


def test():
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
        "body": json.dumps({
            "frame": "18",
            "title": "1",
            "watermark": "5",
            "font": "字体管家乔乔体",
            "text": "祝您在新的一年身体健康，万事如意，天天开心，工作顺利！祝您在新的一年身体健康，万事如意，天天开心，工作顺利！祝您在新的一年身体健康，万事如意，天天开心，工作顺利！祝您在新的一年身体健康，万事如意，天天开心，工作顺利！祝您在新的一年身体健康，万事如意，天天开心，工作顺利！祝您在新的一年身体健康，万事如意，天天开心，工作顺利！",
            "symbol": "945a0cc6430f6ef661bc14773e122f98",
            "from": "dfounderliu",
            "to": "anycodes"
        }),
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
