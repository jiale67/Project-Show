from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import fitz
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
SOURCE = Path('D:/大论文仓库/ren_latex')
ASSETS = ROOT / 'figures'
ASSETS.mkdir(parents=True, exist_ok=True)
FIGURES = {
    'lio': '激光惯性里程计系统架构.pdf',
    'map_localization': '预建地图定位框架.pdf',
    'icp': '两阶段ICP初始对齐.pdf',
    'loc_trajectory': '实验_轨迹对比图.pdf',
    'loc_accuracy': '实验_定位精度对比图.pdf',
    'clustering': '聚类效果对比示意图.pdf',
    'detector': '检测器检测示意图.png',
    'valid_points': '去除无效点云示意图.pdf',
    'planner': '学习增强MPC局部规划架构图.pdf',
    'envelope': '包络约束与点级表示对比图.pdf',
    'encoder': '点级神经网络编码结构.pdf',
    'rolling': '学习增强MPC滚动优化流程图.pdf',
    's1_trajectory': 'ch05_traj_S1_p1.pdf',
    's2_trajectory': 'ch05_traj_S2_p2.pdf',
    'planning_time': 'ch05_plan_time_box.pdf',
    'robot': 'ch05_v550_robot_model.pdf',
}

manifest = {'source_root': str(SOURCE), 'source_hashes': {}, 'figures': {}}
for file in [SOURCE / 'main-thesis.tex', *[SOURCE / 'chapter' / f'chap0{n}.tex' for n in (3,4,5)], *[SOURCE / 'pic' / name for name in FIGURES.values()]]:
    manifest['source_hashes'][str(file)] = hashlib.sha256(file.read_bytes()).hexdigest()

poppler = shutil.which('pdftoppm')
for key, name in FIGURES.items():
    source = SOURCE / 'pic' / name
    target = ASSETS / f'{key}.png'
    if source.suffix == '.pdf':
        doc = fitz.open(source)
        assert len(doc) == 1, name
        subprocess.run([poppler, '-singlefile', '-r', '180', '-png', str(source), str(target.with_suffix(''))], check=True, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
    else:
        shutil.copy2(source, target)
    with Image.open(target) as im:
        size = im.size
    manifest['figures'][key] = {'source': str(source), 'file': str(target), 'size': size}
    print(f'{key}: {size[0]}x{size[1]}')
(ROOT / 'sources.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')

font = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 18)
thumb_w, thumb_h = 620, 360
sheet = Image.new('RGB', (thumb_w*4, thumb_h*4), '#e5eaf0')
draw = ImageDraw.Draw(sheet)
for i, (key, meta) in enumerate(manifest['figures'].items()):
    x, y = (i%4)*thumb_w, (i//4)*thumb_h
    img = Image.open(meta['file']).convert('RGB')
    img.thumbnail((thumb_w-24, thumb_h-54))
    sheet.paste(img, (x+(thumb_w-img.width)//2, y+12+(thumb_h-54-img.height)//2))
    draw.text((x+14, y+thumb_h-35), key + ' | ' + Path(meta['source']).name, font=font, fill='#16304f')
sheet.save(ROOT / 'source_figures_contact.png')
