import qrcode, os
from PIL import Image, ImageDraw, ImageFont


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


i = 1
for eve in os.listdir("./base/symbol_1"):
    if eve.endswith(".png"):
        temp_base_pic = Image.new('RGBA', (1200, 2200), (255, 255, 255))
        temp_pic = Image.open("./base/symbol_1/%s" % eve).convert("RGBA").resize((1200, 1800), Image.ANTIALIAS)
        temp_base_pic.paste(temp_pic, (0, 0), temp_pic)
        url = "http://greetingcard.0duzhan.com/"
        temp_base_pic.paste(get_qrcode(url), (475, 1800), get_qrcode(url))
        draw = ImageDraw.Draw(temp_base_pic)
        draw.text((455, 2100), "长按扫码制作贺卡", (0, 0, 0), font=ImageFont.truetype('./base/font/字体管家乔乔体.ttf', 40))
        temp_base_pic.resize((960, 1760), Image.ANTIALIAS)
        temp_base_pic.save("./base/symbol/%d.png" % i)
        i = i + 1
