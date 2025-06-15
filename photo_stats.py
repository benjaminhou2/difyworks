import os
from datetime import datetime
from PIL import Image
import piexif
from pathlib import Path
from collections import defaultdict
import shutil
from PIL.ExifTags import TAGS
import hashlib

def calculate_image_hash(file_path):
    """计算图片的哈希值，用于检测重复照片"""
    try:
        with Image.open(file_path) as img:
            # 将图片转换为小尺寸的灰度图
            img = img.convert('L').resize((8, 8))
            # 计算像素平均值
            pixels = list(img.getdata())
            avg = sum(pixels) / len(pixels)
            # 生成哈希值
            bits = ''.join('1' if pixel > avg else '0' for pixel in pixels)
            return int(bits, 2)
    except Exception as e:
        print(f"计算图片哈希值时出错 {file_path}: {str(e)}")
        return None

def get_exif_info(file_path):
    """获取详细的EXIF信息"""
    try:
        exif_dict = piexif.load(file_path)
        exif_info = {}
        
        # 获取拍摄时间
        if piexif.ImageIFD.DateTime in exif_dict["0th"]:
            exif_info["拍摄时间"] = exif_dict["0th"][piexif.ImageIFD.DateTime].decode('utf-8')
        
        # 获取相机信息
        if piexif.ImageIFD.Make in exif_dict["0th"]:
            exif_info["相机品牌"] = exif_dict["0th"][piexif.ImageIFD.Make].decode('utf-8')
        if piexif.ImageIFD.Model in exif_dict["0th"]:
            exif_info["相机型号"] = exif_dict["0th"][piexif.ImageIFD.Model].decode('utf-8')
            
        # 获取拍摄参数
        if piexif.ExifIFD.ExposureTime in exif_dict["Exif"]:
            exif_info["曝光时间"] = str(exif_dict["Exif"][piexif.ExifIFD.ExposureTime])
        if piexif.ExifIFD.FNumber in exif_dict["Exif"]:
            f_number = exif_dict["Exif"][piexif.ExifIFD.FNumber]
            exif_info["光圈值"] = f"f/{f_number[0]/f_number[1]:.1f}"
        if piexif.ExifIFD.ISOSpeedRatings in exif_dict["Exif"]:
            exif_info["ISO"] = str(exif_dict["Exif"][piexif.ExifIFD.ISOSpeedRatings])
        if piexif.ExifIFD.FocalLength in exif_dict["Exif"]:
            focal_length = exif_dict["Exif"][piexif.ExifIFD.FocalLength]
            exif_info["焦距"] = f"{focal_length[0]/focal_length[1]:.1f}mm"
            
        return exif_info
    except:
        return {}

def get_photo_info(file_path):
    """获取照片的详细信息"""
    try:
        # 获取文件基本信息
        file_stat = os.stat(file_path)
        file_size = file_stat.st_size / (1024 * 1024)  # 转换为MB
        created_time = datetime.fromtimestamp(file_stat.st_ctime)
        modified_time = datetime.fromtimestamp(file_stat.st_mtime)
        
        # 获取图片尺寸
        with Image.open(file_path) as img:
            width, height = img.size
            
        # 获取EXIF信息
        exif_info = get_exif_info(file_path)
        
        # 计算图片哈希值
        image_hash = calculate_image_hash(file_path)
            
        return {
            "文件名": os.path.basename(file_path),
            "文件大小": f"{file_size:.2f}MB",
            "创建时间": created_time.strftime("%Y-%m-%d %H:%M:%S"),
            "修改时间": modified_time.strftime("%Y-%m-%d %H:%M:%S"),
            "分辨率": f"{width}x{height}",
            "文件路径": str(file_path),
            "图片哈希值": str(image_hash),
            **exif_info  # 添加EXIF信息
        }
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {str(e)}")
        return None

def create_thumbnail(image_path, thumbnail_path, size=(200, 200)):
    """创建缩略图"""
    try:
        with Image.open(image_path) as img:
            img.thumbnail(size)
            img.save(thumbnail_path, "JPEG")
        return True
    except Exception as e:
        print(f"创建缩略图失败 {image_path}: {str(e)}")
        return False

def main():
    # 目标目录
    target_dir = r"C:\Users\PC-320\Pictures\iCloud Photos\Photos"
    
    # 支持的图片格式
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    
    # 统计信息
    total_photos = 0
    photo_info_list = []
    photos_by_year = defaultdict(list)
    photos_by_type = defaultdict(list)
    duplicate_photos = defaultdict(list)
    
    # 创建缩略图目录
    thumbnail_dir = "thumbnails"
    os.makedirs(thumbnail_dir, exist_ok=True)
    
    # 遍历目录
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if Path(file).suffix.lower() in image_extensions:
                total_photos += 1
                file_path = os.path.join(root, file)
                info = get_photo_info(file_path)
                
                if info:
                    # 按年份分类
                    year = info.get("拍摄时间", info["创建时间"])[:4]
                    photos_by_year[year].append(info)
                    
                    # 按文件类型分类
                    file_type = Path(file).suffix.lower()
                    photos_by_type[file_type].append(info)
                    
                    # 检测重复照片
                    if info["图片哈希值"]:
                        duplicate_photos[info["图片哈希值"]].append(info)
                    
                    # 创建缩略图
                    thumbnail_path = os.path.join(thumbnail_dir, f"thumb_{total_photos}.jpg")
                    if create_thumbnail(file_path, thumbnail_path):
                        info["缩略图"] = thumbnail_path
                    
                    photo_info_list.append(info)
    
    # 生成Markdown报告
    with open('photo_report.md', 'w', encoding='utf-8') as f:
        f.write("# 照片统计报告\n\n")
        f.write(f"## 统计概览\n\n")
        f.write(f"- 总照片数量：{total_photos}张\n")
        f.write(f"- 统计时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # 按年份统计
        f.write("## 按年份统计\n\n")
        for year in sorted(photos_by_year.keys(), reverse=True):
            f.write(f"### {year}年\n")
            f.write(f"- 照片数量：{len(photos_by_year[year])}张\n\n")
        
        # 按文件类型统计
        f.write("## 按文件类型统计\n\n")
        for file_type, photos in photos_by_type.items():
            f.write(f"### {file_type}格式\n")
            f.write(f"- 照片数量：{len(photos)}张\n")
            f.write(f"- 总大小：{sum(float(p['文件大小'].replace('MB', '')) for p in photos):.2f}MB\n\n")
        
        # 重复照片检测
        f.write("## 重复照片检测\n\n")
        duplicate_count = 0
        for hash_value, photos in duplicate_photos.items():
            if len(photos) > 1:
                duplicate_count += len(photos) - 1
                f.write(f"### 重复照片组 {duplicate_count}\n")
                for photo in photos:
                    f.write(f"- {photo['文件名']}\n")
                f.write("\n")
        
        f.write(f"### 重复照片统计\n")
        f.write(f"- 重复照片总数：{duplicate_count}张\n\n")
        
        # 照片详细信息
        f.write("## 照片详细信息\n\n")
        for info in photo_info_list:
            f.write("### " + info["文件名"] + "\n\n")
            if "缩略图" in info:
                f.write(f"![缩略图]({info['缩略图']})\n\n")
            for key, value in info.items():
                if key not in ["文件名", "缩略图"]:
                    f.write(f"- {key}：{value}\n")
            f.write("\n")
    
    print(f"统计完成！共发现{total_photos}张照片。详细报告已保存到 photo_report.md")
    print(f"重复照片数量：{duplicate_count}张")
    print(f"缩略图已保存到 {thumbnail_dir} 目录")

if __name__ == "__main__":
    main() 