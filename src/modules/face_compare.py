import os
import cv2
import base64
import logging
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkfrs.v2.region.frs_region import FrsRegion
from huaweicloudsdkfrs.v2 import *

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 华为云配置
AK = os.getenv("HUAWEICLOUD_SDK_AK","your_access_key_here").strip()  # 替换为您的Access Key
SK = os.getenv("HUAWEICLOUD_SDK_SK","your_secret_key_here").strip()  # 替换为您的Secret Key
PROJECT_ID = "your_project_id_here"  # 替换为您的项目ID
REGION = "your_region_here"  # 替换为您的区域

credentials = BasicCredentials(AK, SK).with_project_id(PROJECT_ID)


def validate_face_image(image_path):
    """验证图片是否包含有效人脸"""
    try:
        # 首先检查文件是否存在
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"图片文件不存在: {image_path}")
        
        # 检查文件是否为空
        if os.path.getsize(image_path) == 0:
            raise ValueError(f"图片文件为空: {image_path}")
        
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"无效的图片文件: {image_path}")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        
        # 调整检测参数，提高检测阈值，减少误检测
        faces = face_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.3,  # 增加缩放因子，减少误检测
            minNeighbors=6,   # 增加最小邻居数，提高检测精度
            minSize=(100, 100),  # 设置最小人脸尺寸
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        if len(faces) == 0:
            raise ValueError("未检测到人脸")
        
        # 只保留最大的人脸（过滤误检测的小面积人脸）
        max_area = 0
        max_face = None
        for (x, y, w, h) in faces:
            area = w * h
            if area > max_area:
                max_area = area
                max_face = (x, y, w, h)
        
        # 如果最大人脸面积小于图片面积的10%，可能是误检测
        img_area = img.shape[0] * img.shape[1]
        if max_face and (max_face[2] * max_face[3]) < img_area * 0.1:
            raise ValueError("未检测到有效人脸")

        return True
    except Exception as e:
        logger.error(f"图片验证失败: {str(e)}")
        # 重新抛出异常，让调用者能够处理
        raise


def compare_face(face1_path, face2_path):
    """人脸比对函数"""
    try:
        # 验证文件存在
        if not all(map(os.path.isfile, [face1_path, face2_path])):
            # 提供更详细的错误信息，指出哪个文件不存在
            missing_files = [path for path in [face1_path, face2_path] if not os.path.isfile(path)]
            raise FileNotFoundError(f"人脸图片文件不存在: {', '.join(missing_files)}")

        # 验证图片有效性
        validate_face_image(face1_path)
        validate_face_image(face2_path)

        # 初始化客户端
        client = FrsClient.new_builder() \
            .with_credentials(credentials) \
            .with_region(FrsRegion.value_of(REGION)) \
            .build()

        # 读取并编码图片
        def read_image(path):
            try:
                with open(path, "rb") as f:
                    return base64.b64encode(f.read()).decode()
            except Exception as e:
                raise IOError(f"读取图片失败: {str(e)}")

        img1 = read_image(face1_path)
        img2 = read_image(face2_path)

        # 构建请求
        request = CompareFaceByBase64Request()
        request.body = FaceCompareBase64Req(
            image1_base64=img1,
            image2_base64=img2
        )

        # 发送请求
        response = client.compare_face_by_base64(request)
        result = response.to_dict()

        # 解析结果
        similarity = result.get("similarity", 0)
        logger.info(f"人脸比对相似度: {similarity}")

        return similarity >= 0.85

    except exceptions.ClientRequestException as e:
        logger.error(f"华为云API错误: {e.error_code} - {e.error_msg}")
        raise Exception(f"服务暂时不可用（错误码：{e.error_code}）")
    except Exception as e:
        logger.error(f"人脸比对失败: {str(e)}")
        # 重新抛出异常，让调用者处理
        raise