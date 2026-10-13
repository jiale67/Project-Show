from pathlib import Path
import base64
import html
import json

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / '_work'
SKILL = Path(r'C:\Users\19514\.codex\skills\html-ppt')
REFERENCE = Path(r'C:\Users\19514\Desktop\简历补充\项目展示')
SOURCES = json.loads((WORK / 'sources.json').read_text(encoding='utf-8-sig'))

def fig(key, caption, style='', cls='grow'):
    item = SOURCES['figures'][key]
    data = base64.b64encode(Path(item['file']).read_bytes()).decode()
    name = Path(item['source']).name
    return f'''<div class="figure {cls}" style="{style}">
      <figure class="img-frame contain"><img src="data:image/png;base64,{data}" alt="{html.escape(caption)}" data-origin="pic/{html.escape(name)}" tabindex="0" role="button" aria-label="放大：{html.escape(caption)}"></figure>
      <p class="img-cap">{caption} <span class="original-label">论文原图</span></p></div>'''

def table(headers, rows, cls='', focus=None):
    head = ''.join(f'<th scope="col">{x}</th>' for x in headers)
    body = ''
    for i, row in enumerate(rows):
        body += f'<tr{chr(32)+chr(99)+chr(108)+chr(97)+chr(115)+chr(115)+chr(61)+chr(34)+"ours"+chr(34) if i == focus else ""}>'
        body += ''.join(f'<td>{x}</td>' for x in row) + '</tr>'
    return f'<div class="table-box"><table class="{cls}"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'

def panel(title, content, cls='', style=''):
    return f'<div class="panel {cls}" style="{style}"><h3 class="panel-title">{title}</h3>{content}</div>'

def step(i, title, text):
    return f'<div class="step"><span class="index">{i:02}</span><div><h4>{title}</h4><p>{text}</p></div></div>'

def node(title, text, cls='', eyebrow=''):
    return f'<div class="flow-node {cls}"><p class="eyebrow">{eyebrow}</p><h3>{title}</h3><p>{text}</p></div>'

slides = []
def slide(chapter, kicker, title, body, source, notes, hero=False):
    n = len(slides) + 1
    header = f'<div class="page-head"><p class="kicker">{kicker}</p><h2 class="h2">{title}</h2></div>' if not hero else ''
    slides.append(f'''<section class="slide{' is-active' if n == 1 else ''}" data-title="{html.escape(title)}" data-chapter="{chapter}" data-page="{n}">
      {header}<div class="slide-main">{body}</div>
      <div class="deck-footer"><span class="page-source">{source}</span><span class="page-index">{n:02} / 10</span></div>
      <aside class="notes"><h3>{title}</h3><p>{notes}</p><p>来源：{source}</p></aside></section>''')

# 01 — cover + architecture, adapted from tech-sharing / arch-diagram.
slide('overview', 'RESEARCH / 核心算法', '复杂动态环境下机器人导航系统设计与应用', '''
  <div class="hero-top"><div><p class="kicker">MASTER'S THESIS / 核心算法成果</p>
    <h1 class="h1">复杂动态环境下<br><span class="accent">机器人导航系统设计与应用</span></h1>
    <div class="hero-meta"><strong>任佳乐</strong><span>杭州电子科技大学 · 控制工程硕士</span></div></div>
    <div class="hero-stamp"><b>定位 → 感知 → 规划</b><br>激光惯性定位<br>动静态障碍感知<br>神经距离编码与模型预测避障</div></div>
  <div class="flow system-flow">
    <div class="flow-node blue"><span class="node-no">CHAPTER 03 / LOCALIZATION</span><h3>地图约束定位</h3><p>FAST-LIO2 + 预建地图<br>初始位姿对齐 / 在线滤波</p><div class="tagline">输出：地图系位姿</div></div>
    <div class="flow-node green"><span class="node-no">CHAPTER 04 / PERCEPTION</span><h3>障碍检测与跟踪</h3><p>U深度图 + DBSCAN<br>匈牙利关联 / 恒加速度滤波</p><div class="tagline">输出：障碍边界与运动状态</div></div>
    <div class="flow-node amber"><span class="node-no">CHAPTER 05 / PLANNING</span><h3>学习增强MPC</h3><p>点级几何编码 / 动态预测点流<br>滚动优化 / 速度指令执行</p><div class="tagline">输出：可执行局部控制量</div></div>
  </div>
  <div class="interface-line"><span class="back">↶</span><strong>闭环接口</strong><span>位姿与传感器观测 → 环境表达 → 规划控制 → 机器人运动 → 新观测</span></div>
  <div class="hero-bottom"><div class="mini"><b>0.043–0.071 m</b><span>三场景混合建图定位 ATE-RMSE</span></div><div class="mini"><b>72.5% <small>（29/40）</small></b><span>S2复杂动态环境 · 本文规划成功率</span></div><div class="mini"><b>16.39 ms</b><span>S2本文方法 · 平均单周期规划计算耗时</span></div></div>
''', '内容来源：论文第3–5章 · 架构为按原文章节整理的接口示意',
'''展示范围限于第3、4、5章。总体接口连接定位、感知与规划；第5章当前仿真使用Gazebo真值速度并令障碍加速度为零，尚未验证第4章跟踪误差向规划传播。定位数值来自三场景ATE表；72.5%为S2本文方法29/40成功；16.39 ms为S2已记录规划计算周期均值。三项指标来自各章独立实验，不能解释为统一端到端实验。''', hero=True)

# 02 — map localization.
slide('3', 'CHAPTER 03 / 定位方法', '将FAST-LIO2接入预建地图，约束全局漂移',
  '<div class="split wide"><div class="col">' +
  fig('map_localization', '基于预建地图的FAST-LIO2定位框架') +
  '<div class="flow flow-tight">' + node('IMU传播', '状态预测 / 点云去畸变') + node('点到平面', '局部地图几何残差') + node('IESKF更新', 'ikd-Tree近邻检索') + '</div></div><div class="col">' +
  panel('启动与任务重启：两阶段对齐', '<div class="steps">' +
    step(1, '加载PCD地图', '建立预建地图索引，接收近似初始位姿。') +
    step(2, '粗对齐 → ICP精对齐', '先将当前点云变换至近似位置，再迭代配准。') +
    step(3, '写入滤波初始状态', '将对齐结果用于后续地图约束定位。') + '</div>') +
  panel('运行模式', table(['模式', '地图维护'], [
    ['纯定位', '固定预建地图，不增量写入'],
    ['混合建图', '前80帧稳定后，开启增量更新'],
    ['纯里程计', '在线建图，作为精度对照']
  ], 'no-mono compact')) +
  '<div class="callout"><strong>适用条件：</strong>启动重定位需要近似初值，初值质量影响ICP收敛可靠性。</div></div></div>',
  '第3章 §3.3–3.4 · 原图：预建地图定位框架.pdf',
  '''FAST-LIO2为基础里程计框架，本文扩展预建地图加载、近似初值和ICP对齐、地图约束在线更新以及纯定位/混合建图两种模式。两阶段初始对齐并非无先验全局重定位。纯定位固定地图；混合建图在前80帧后增量补充局部结构。''')

# 03 — localization evidence.
slide('3', 'CHAPTER 03 / 定位验证', '三类场景下，地图约束降低轨迹误差',
  '<div class="split"><div class="col">' +
  fig('loc_accuracy', 'APE时间序列与ATE分布对比') +
  panel('混合建图单帧计算', table(['场景', '平均耗时', '可达处理帧率'], [
    ['走廊', '18.5 ms', '54 Hz'], ['迷宫', '24.3 ms', '41 Hz'], ['圆柱体林', '20.1 ms', '50 Hz']
  ], 'compact') + '<p class="table-note">MID360实际输入10 Hz，IMU 100 Hz；i7-11800H / 16 GB。</p>') +
  '</div><div class="col">' +
  panel('ATE-RMSE / m', table(['场景', '纯定位', '混合建图', '纯里程计'], [
    ['走廊', '0.082', '<strong>0.071</strong>', '0.410'],
    ['迷宫', '0.046', '<strong>0.043</strong>', '0.190'],
    ['圆柱体林', '0.061', '<strong>0.058</strong>', '0.280']
  ], 'compact')) +
  panel('ICP初始对齐 / 迷宫场景', table(['初值扰动（m / °）', '成功率', '配准RMSE'], [
    ['&lt;1 / &lt;20', '99.5%', '2.1 cm'],
    ['1–2 / 20–30', '88.3%', '3.2 cm'],
    ['&gt;2 / &gt;30', '51.7%', '4.6 cm']
  ], 'compact') + '<p class="table-note">近似位姿越准确，初始配准越可靠。</p>') +
  '<div class="callout"><strong>混合建图相对纯里程计：</strong>三场景ATE-RMSE分别降低82.7%、77.4%、79.3%。</div>' +
  '</div></div>',
  '第3章 §3.5 · ATE统计表 / ICP初始对齐性能表 / 混合建图耗时表',
  '''ATE表只摘取原文RMSE列，未改变数值。降幅明确针对混合建图相对纯里程计。ICP表省略平均迭代次数，原文良好/中等/较差初值分别为25/52/78次。处理帧率为由单帧耗时得到的可达处理能力，雷达实际输入仍为10 Hz。实验采用Gazebo 11与ROS Noetic。''')

# 04 — detection.
slide('4', 'CHAPTER 04 / 障碍检测', '双路非学习检测，用空间一致性融合包围盒',
  '<div class="split equal"><div class="col">' +
  fig('detector', '深度图、U深度图与障碍物包围盒', 'flex:1.6') +
  fig('clustering', '聚类效果对比示意图', 'flex:.7') +
  '</div><div class="col"><div class="two-path">' +
  '<div class="path"><h4>深度图通路</h4><div class="part">按列统计深度直方图</div><div class="down">↓</div><div class="part">U深度图线段分组</div><div class="down">↓</div><div class="part">深度连续性搜索 → AABB</div></div>' +
  '<div class="path"><h4>点云通路</h4><div class="part">深度反投影 / 激光点云</div><div class="down">↓</div><div class="part">裁剪 / 降采样 / 离群过滤</div><div class="down">↓</div><div class="part">DBSCAN聚类 → AABB</div></div></div>' +
  '<div class="down">↓ 两路检测结果</div><div class="merge"><h3>双向最大IoU校验</h3><p class="small">互为最佳匹配，且双向IoU均达到阈值</p></div>' +
  table(['匹配结果', '保守处理规则'], [
    ['通过匹配', '中心取平均；各方向尺寸取较大值'],
    ['未通过匹配', '保留原始包围盒，交由跨帧跟踪判断']
  ], 'no-mono compact') +
  '<div class="callout"><strong>传感器接口：</strong>深度图可形成双路检测；激光输入经裁剪滤波后进入DBSCAN通路。</div>' +
  '</div></div>',
  '第4章 §4.2–4.3.1 · 原图：检测器检测示意图.png / 聚类效果对比示意图.pdf',
  '''检测器均为非学习式方法。U深度图基于按列深度统计、线段分组和原深度连续性搜索；DBSCAN对深度反投影或激光点云进行聚类。融合需双向IoU通过阈值且互为最佳。未通过匹配的结果继续保留，不能将图解为单路检测即被删除。本章无定量精度或感知耗时实验表，展示方法与示意图。''')

# 05 — tracking + map.
slide('4', 'CHAPTER 04 / 跟踪与环境表达', '关联运动状态，输出规划可用的局部环境',
  '<div class="flow flow-tight">' +
  node('归一化特征', '中心p / 尺寸d<br>点数n / 坐标标准差σ', 'green') +
  node('匈牙利关联', '相似度 s = exp(−‖fᵢ−fⱼ‖²)<br>全局一一匹配 + 阈值筛选', 'green') +
  node('恒加速度卡尔曼滤波', '状态 [x, y, vₓ, vᵧ, aₓ, aᵧ]ᵀ<br>有限漏检期间保留预测', 'green') + '</div>' +
  '<div class="split equal"><div class="col">' +
  panel('动态识别：包围盒速度 + 有效点投票', '<div class="condition"><div><b>目标速度门限</b><span>‖v<sub>box</sub>‖ ≥ v<sub>box_th</sub></span></div><div><b>有效点投票门限</b><span>动态投票比例 ≥ vote<sub>th</sub></span></div></div><p class="table-note">点级投票：v<sub>p</sub>·v<sub>box</sub> ≥ 0，且‖v<sub>p</sub>‖ &gt; v<sub>pc_th</sub>；仅统计跨帧有效对应点。</p>') +
  fig('valid_points', '剔除新入视场等无效对应点，减少伪运动投票') +
  '</div><div class="col">' +
  panel('局部占用地图更新', '''
    <div class="map-step"><span class="index">01</span><div><strong>同步位姿与观测</strong><span>将点云统一变换至地图坐标系</span></div></div>
    <div class="map-step"><span class="index">02</span><div><strong>Bresenham射线遍历</strong><span>沿途栅格更新为空闲，端点更新为占用</span></div></div>
    <div class="map-step"><span class="index">03</span><div><strong>截断log-odds累加</strong><span>融合连续观测，限制置信度上下界</span></div></div>
    <div class="map-step"><span class="index">04</span><div><strong>占用阈值 + 形态学膨胀</strong><span>形成可通行空间和机器人安全缓冲</span></div></div>''', style='flex:1') +
  '<div class="callout">短时失配仅预测，超过最大丢失帧数删除轨迹；动态标签采用有限保持。</div></div></div>' +
  '<div class="interface-line"><strong>规划接口</strong><span>① 障碍边界点 / AABB</span><span>② 动态位置 / 速度 / 加速度</span><span>③ 占用与膨胀地图</span></div>',
  '第4章 §4.3.2–4.4 · 原图：去除无效点云示意图.pdf',
  '''匹配代价为1−s，匹配后用恒加速度卡尔曼滤波更新目标状态。动态判别同时满足包围盒速度和有效对应点投票两类条件；新入视场点不参与投票。局部地图通过Bresenham射线、截断log-odds、阈值与膨胀形成环境表达。第5章本轮仿真用真值速度替代跟踪输入，因此接口设计与本轮规划实验输入需要区分。''')

# 06 — planner architecture.
slide('5', 'CHAPTER 05 / 规划总体方法', '用点级几何描述障碍，以MPC生成控制',
  '<div class="split wide"><div class="col">' +
  fig('planner', '神经距离编码MPC局部规划器总体架构') +
  '<div class="formula"><div class="formula-label">恒加速度预测点流</div>p<sub>k|t</sub> = p<sub>t</sub> + kΔt · v<sub>t</sub> + ½(kΔt)² · a<sub>t</sub></div>' +
  '<p class="chart-note">速度与加速度用于外部点流预测；网络接收各预测时刻的机器人局部二维障碍点。</p>' +
  '</div><div class="col">' +
  fig('envelope', '包络约束与点级障碍表示对比', 'flex:none;height:225px') +
  panel('输入与职责', table(['模块', '接口'], [
    ['上层参考路径', '有序二维位置序列，可按弧长采样；末点为目标'],
    ['几何编码器', '障碍点 → 距离相关量与分离方向'],
    ['MPC优化层', '结合运动模型、避障约束与参考路径求控制']
  ], 'no-mono compact')) +
  '<div class="callout"><strong>当前执行：</strong>取首项最优控制，经地图系→机体系旋转后直接下发速度指令。</div>' +
  '<p class="micro">原架构图中的“跟踪控制”为通用表示；本章实现直接输出cmd_vel。仿真实验统一采用起终点直线参考路径。</p>' +
  '</div></div>',
  '第5章 §5.2–5.3.3 · 原图：学习增强MPC局部规划架构图.pdf / 包络约束与点级表示对比图.pdf',
  '''本文借鉴NeuPAN/ObsPointNet/DUNE中的点级几何编码思路，采用神经距离编码结合MPC的局部规划器，不能等同于完整NeuPAN端到端框架。网络预测几何潜在特征，控制量由MPC求解。上层可用A*、RRT或直线，局部层承担避障与运动约束。恒加速度预测模型在本轮仿真中取a=0，速度用Gazebo真值差分。原图保持完整，旁注说明当前直接速度下发的实现边界。''')

# 07 — neural encoder and training.
network = '<div class="network"><div class="net-node"><div class="width">2</div><div class="act">局部二维点</div></div>'
for i in range(5):
    network += '<span class="net-arrow">→</span><div class="net-node"><div class="width">32</div><div class="act">' + ('LN + Tanh' if i % 2 == 0 else 'ReLU') + '</div></div>'
network += '<span class="net-arrow">→</span><div class="net-node"><div class="width">4</div><div class="act">ReLU / 非负μ</div></div></div>'
slide('5', 'CHAPTER 05 / 神经距离编码', '共享点级网络，离线学习机器人轮廓几何',
  fig('encoder', '点级编码器结构与特征生成流程；原图为通用示意，本文输入2维、输出4维', 'flex:none;height:260px') +
  network + '<div class="training-grid"><div class="col">' +
  panel('监督数据与训练配置', table(['配置项', '本文设置'], [
    ['机器人轮廓', '矩形 0.260 × 0.2446 m；n<sub>e</sub> = 4'],
    ['几何样本', '±4 m范围均匀采样；100,000点'],
    ['标签 / 划分', 'CVXPY / ECOS；训练80% / 验证20%'],
    ['优化 / 训练', 'Adam；batch 256；5000轮；CPU'],
    ['学习率', '5 × 10⁻⁵，每1500轮乘0.5']
  ], 'no-mono tiny-table')) + '</div><div class="col">' +
  panel('第5000轮损失 / MSE', table(['损失项', '训练集', '验证集'], [
    ['潜在特征μ', '7.62 × 10⁻⁵', '7.42 × 10⁻⁵'],
    ['距离', '6.29 × 10⁻⁷', '6.04 × 10⁻⁷'],
    ['方向系数', '9.85 × 10⁻⁶', '9.69 × 10⁻⁶'],
    ['偏置', '2.88 × 10⁻⁶', '2.10 × 10⁻⁶']
  ], 'tiny-table')) +
  '<div class="callout" style="font-size:18px">在线固定参数、仅前向推理。独立测试的距离误差、方向角误差与推理耗时，原文列为待实际日志补齐。</div>' + '</div></div>',
  '第5章 §5.3.4–5.3.5 · 编码器结构表 / 监督数据配置表 / 编码器训练损失表',
  '''五个32维隐藏层，第1/3/5层使用LayerNorm+Tanh，第2/4层ReLU，输出ReLU保证非负。所有障碍点、所有预测时刻共享参数。局部坐标尺度Dr=I。训练权重衰减10⁻⁴，5000轮归档CPU checkpoint。表仅摘取终轮训练与验证MSE，不将训练损失表解释为独立测试结果或规划安全证明。编码前≤100点，按估计距离筛选后进入优化≤10点。''')

# 08 — MPC and execution.
slide('5', 'CHAPTER 05 / 滚动优化与执行', '几何约束逐次更新，首项控制闭环执行',
  '<div class="split wide"><div class="col">' +
  fig('rolling', '学习增强MPC滚动优化流程') +
  '<div class="flow flow-tight">' + node('首项控制u₀*', '地图系平移速度 / 角速度', 'amber') +
  node('平面旋转', '转换为机体系速度', 'amber') + node('速度下发', '执行 → 新观测 → 再规划', 'amber') + '</div>' +
  '<p class="micro">到达目标输出零速；近距风险、超时或不可行时减速停车，多周期失败请求重规划。</p>' +
  '</div><div class="col">' +
  '<div class="runtime-metrics"><div class="metric"><div class="value">5<span class="unit">步</span></div><div class="label">预测步长0.3 s</div></div><div class="metric"><div class="value">0.1<span class="unit">s</span></div><div class="label">控制周期</div></div><div class="metric"><div class="value">2<span class="unit">次</span></div><div class="label">耦合迭代上限</div></div></div>' +
  panel('运动模型与优化约束', table(['项目', '表达 / 设置'], [
    ['全向运动学', 's<sub>k+1</sub> = s<sub>k</sub> + Δt · u<sub>k</sub>'],
    ['平移速度 / 增量', '二阶锥范数约束；1 m/s、1 m/s²'],
    ['角速度 / 增量', '独立箱约束；1 rad/s、2 rad/s²'],
    ['点级安全', '补偿距离一阶近似 + 非负松弛'],
    ['障碍点管理', '编码前 ≤100点；优化层 ≤10点'],
    ['目标函数', '状态 / 沿路径速度 / 控制平滑 / 安全裕度；横向权重κ=0.2']
  ], 'no-mono compact')) +
  '<div class="formula sm">d̂<sup>safe</sup> = d̂ − ε<sub>d</sub></div>' +
  '<p class="micro">ε<sub>d</sub>按独立测试集距离高估正部的高分位确定；原文未给出实测数值。线性化与松弛用于在线求解，不构成形式化安全证明。</p></div></div>',
  '第5章 §5.3.6–5.3.7 · MPC目标与约束 / 在线求解流程 · §5.4实验配置',
  '''状态为[x,y,θ]，控制为地图系[vx,vy,ω]；离散模型A=I、B=ΔtI。每轮固定几何编码及雅可比，求解后更新名义轨迹。预测时域1.5 s，控制周期0.1 s。平移速度用模长约束，角速度独立设定。首项控制转为机体系后直接发布cmd_vel，无独立轨迹跟踪/朝向控制环。机体系下发指令差分与世界系优化约束统计含义不同，不能据此声称急停阶段也始终满足加速度约束。''')

# 09 — task-level results with paired comparison.
slide('results', 'CHAPTER 05 / 仿真实验', '180次统一协议试验，对比任务完成性与轨迹质量',
  '<div class="protocol"><span class="pill blue">V550麦克纳姆底盘 / N10P雷达</span><span class="pill">Gazebo 11.15.1 + ROS Noetic</span><span class="pill">3种方法 ×（S1 20次 + S2 40次）</span></div>' +
  '<div class="split narrow-left"><div class="col">' +
  fig('s2_trajectory', 'S2第2组代表性轨迹；不同方法样本种子可能不同') +
  '<div class="evaluation"><div><b>S1 / 静态环境</b>40个凸障碍<br>每方法4组 × 5次</div><div><b>S2 / 复杂动态环境</b>22个静态 + 11个动态障碍<br>每方法4组 × 10次</div></div>' +
  '</div><div class="col">' +
  panel('全部试验：成功率与事件统计', table(['指标', '本文方法', 'AABB-MPC', 'DWA'], [
    ['S1 成功率', '100% (20/20)', '100% (20/20)', '100% (20/20)'],
    ['S2 成功率', '<strong>72.5% (29/40)</strong>', '72.5% (29/40)', '30.0% (12/40)'],
    ['S2 碰撞事件总数 / 次', '<strong>11</strong>', '14', '53'],
    ['S2 急停事件总数 / 次', '<strong>30</strong>', '56', '148']
  ], 'compact') + '<p class="table-note">成功 = 到达且全程无碰撞；事件数可能在一次试验中累积，不能视作失败试验数。</p>') +
  panel('S2共同成功的9组：同起终点、同种子配对', table(['指标（均值±标准差）', '本文方法', 'AABB-MPC', 'DWA'], [
    ['任务时间 T / s', '28.75±7.72', '31.30±9.07', '27.08±4.36'],
    ['路径长度 L / m', '8.14±1.29', '8.30±1.07', '8.03±1.15'],
    ['平移平滑 J<sub>v</sub> / (m/s)²', '0.244±0.110', '0.380±0.190', '0.287±0.104'],
    ['角速度平滑 J<sub>ω</sub> / (rad/s)²', '3.590±1.524', '5.093±3.025', '1.531±0.620']
  ], 'compact paired') + '<p class="table-note">仅在这9组共同成功集合中，本文相对AABB-MPC的时间与两项平滑代价更低。</p>') +
  '<div class="callout">S2两种MPC成功率相当；DWA的配对任务时间与角速度平滑代价较低，本文的平移平滑代价最低。</div>' +
  '</div></div>',
  '第5章 §5.4 · S1 / S2统计结果表 / 三种方法共同成功试验的配对比较表',
  '''全部试验每次重启Gazebo，统一种子和出发相位。S1三种方法均成功且无碰撞。S2碰撞/急停为事件总数。代表轨迹仅示运行现象，不能作为同相位配对证据。配对表仅针对三种方法共同成功的9组，Jv/Jω为控制变化累计代价，单位不同、分别比较，不能合并为一个平滑指标，也不能将9组结论推广到全部S2任务。S1本文平移平滑代价0.172±0.071，AABB-MPC 0.291±0.158，DWA 0.393±0.057。''')

# 10 — runtime and limits.
slide('results', 'CHAPTER 05 / 计算性能与验证范围', '规划计算满足已记录周期预算，保留实验适用范围',
  '<div class="split equal"><div class="col">' +
  fig('planning_time', 'S1与S2单周期规划耗时分布；红线为100 ms控制周期', 'flex:1') +
  panel('局部规划计算耗时 / ms', table(['场景 / 方法', '平均', 'P95', '最大', '&gt;100 ms'], [
    ['S1 本文方法', '15.92', '20.34', '36.55', '0.00%'],
    ['S1 AABB-MPC', '17.62', '22.60', '150.85', '0.08%'],
    ['S1 DWA', '2.05', '3.05', '4.69', '0.00%'],
    ['S2 本文方法', '16.39', '20.91', '84.97', '0.00%'],
    ['S2 AABB-MPC', '18.93', '24.24', '165.24', '0.15%'],
    ['S2 DWA', '1.63', '3.01', '5.17', '0.00%']
  ], 'tiny-table') + '<p class="table-note">汇总全部试验（含失败）的已记录计算周期；Ryzen 9 7940H，MPC使用PyTorch CPU / 8线程。</p>') +
  '</div><div class="col">' +
  '<div class="runtime-metrics"><div class="metric"><div class="value">16.39</div><div class="label">S2平均耗时 / ms</div></div><div class="metric"><div class="value">20.91</div><div class="label">S2 P95 / ms</div></div><div class="metric"><div class="value">0<span class="unit">%</span></div><div class="label">S2已记录超周期</div></div></div>' +
  panel('本轮实验支持的结果', '<div class="steps">' +
    step(1, '地图约束抑制定位漂移', '三场景中，纯定位与混合建图ATE均低于纯里程计。') +
    step(2, '动态场景任务完成性', 'S2本文与AABB-MPC均29/40成功，高于DWA的12/40。') +
    step(3, '计算耗时与轨迹质量', '本文已记录规划周期均低于100 ms；配对质量比较限定共同成功集合。') + '</div>') +
  panel('实验条件与结论范围', '''<div class="scope-line"><b>动态输入</b><span>Gazebo真值速度、a=0恒速外推；跟踪误差传播尚未验证。</span></div>
    <div class="scope-line"><b>几何与归因</b><span>未设独立非凸窄通道工况与模块消融；不归因于编码器单独贡献。</span></div>
    <div class="scope-line"><b>计时范围</b><span>局部计算口径，未覆盖传感器等待、通信等端到端链路。</span></div>''', 'soft') +
  '</div></div>',
  '第3章 §3.5 · 第5章 §5.4.4–5.5 · 单周期规划耗时分布 / 仿真实时性表',
  '''规划耗时对全部试验的已记录周期汇总。两种MPC包含求解，AABB-MPC另外包含聚类和包围盒边界采样，均不含仿真辅助真值速度关联；DWA仅为C++ compute()调用，非端到端。14次S1 DWA记录存在约0.51–0.93 s间隔，低compute耗时和零超周期不等于完整10 Hz链路连续。S2本文/AABB/DWA的RTF分别0.987/0.985/0.890。缺少计算环节分解、模块消融、独立非凸窄通道工况与跟踪误差传播实验，因此不声称全面最优或将差异归因于单一模块。''')

custom_js = r'''
(() => {
  const ready = () => {
    const slides = [...document.querySelectorAll('.deck > .slide')];
    const select = document.querySelector('#slide-select');
    slides.forEach((s,i) => select.add(new Option(`${String(i+1).padStart(2,'0')}  ${s.dataset.title}`, i+1)));
    const current = () => Math.max(0,slides.findIndex(s=>s.classList.contains('is-active')));
    const goto = n => {location.hash = '#/' + Math.max(1,Math.min(slides.length,n));};
    const sync = () => {
      const i=current(); select.value=i+1;
      document.querySelector('#slide-position').textContent=`${i+1} / ${slides.length}`;
      document.querySelector('#prev-slide').disabled=i===0;
      document.querySelector('#next-slide').disabled=i===slides.length-1;
      document.querySelectorAll('.chapter-nav a').forEach(a=>a.classList.toggle('active',a.dataset.chapter===slides[i].dataset.chapter));
    };
    new MutationObserver(sync).observe(document.querySelector('.deck'), {subtree:true,attributes:true,attributeFilter:['class']});
    sync(); select.addEventListener('change',()=>goto(+select.value));
    document.querySelector('#prev-slide').onclick=()=>goto(current());
    document.querySelector('#next-slide').onclick=()=>goto(current()+2);
    document.querySelectorAll('[data-key]').forEach(b=>b.onclick=()=>document.dispatchEvent(new KeyboardEvent('keydown',{key:b.dataset.key,bubbles:true})));
    const zoom=document.querySelector('#zoom-modal'), source=document.querySelector('#source-modal');
    let focusReturn=null;
    const show = modal => { focusReturn=document.activeElement; modal.classList.add('open'); modal.querySelector('.close-modal').focus(); };
    const close = () => {document.querySelectorAll('.modal.open').forEach(m=>m.classList.remove('open')); focusReturn?.focus();};
    document.querySelectorAll('.close-modal').forEach(b=>b.onclick=close);
    document.querySelectorAll('.modal').forEach(m=>m.addEventListener('click',e=>{if(e.target===m)close();}));
    document.querySelector('#show-source').onclick=()=> {
      const s=slides[current()];
      document.querySelector('#source-content').innerHTML=s.querySelector('.notes').innerHTML;
      const origins=[...s.querySelectorAll('[data-origin]')].map(img=>img.dataset.origin);
      document.querySelector('#source-files').textContent=origins.length?origins.join('\n'):'chapter/chap03.tex\nchapter/chap04.tex\nchapter/chap05.tex';
      show(source);
    };
    document.querySelectorAll('.slide .img-frame img').forEach(img=>{
      const open=()=>{
        const large=zoom.querySelector('img');large.src=img.src;large.alt=img.alt;large.classList.remove('enlarged');
        zoom.querySelector('.caption').textContent=img.alt+' · '+img.dataset.origin+' · 点击切换原始尺寸 / Esc关闭';
        show(zoom);
      };
      img.onclick=open;img.onkeydown=e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();e.stopPropagation();open();}};
    });
    zoom.querySelector('img').onclick=e=>e.target.classList.toggle('enlarged');
    document.addEventListener('keydown',e=>{
      const modal=document.querySelector('.modal.open');
      if(modal){
        if(e.key==='Escape')close();
        if(e.key==='Tab') {e.preventDefault();modal.querySelector('.close-modal').focus();}
        e.stopImmediatePropagation();return;
      }
      if(e.key==='t'||e.key==='T') {e.stopImmediatePropagation();return;}
      if(e.target.closest('select,button,a,input,textarea') && ['Enter',' ','ArrowDown','ArrowUp','ArrowLeft','ArrowRight','Backspace','Home','End'].includes(e.key))e.stopImmediatePropagation();
    },true);
  };
  document.addEventListener('DOMContentLoaded', ready);
})();
'''

extra_css = '''
/* Palette and typography are copied from the user's project portfolio. */
:root{--paper:var(--surface);--nav-bg:var(--bg);--blue-soft:#e8effb;--green-soft:#eff6f9;--amber-soft:#f8f2e8}
.slide{--chapter-color:var(--accent);padding:65px 96px 82px}
.slide[data-chapter="4"]{--chapter-color:var(--accent-2)}
.slide[data-chapter="5"]{--chapter-color:var(--accent)}
.slide[data-chapter="results"]{--chapter-color:var(--accent)}
.deck-header{top:29px;right:96px;left:96px;justify-content:space-between}
.deck-brand{display:flex;align-items:center;gap:12px;font-size:17px;color:var(--text-2);font-weight:500}
.monogram{display:grid;place-items:center;width:31px;height:31px;background:var(--accent);color:var(--accent-ink);font:600 13px var(--font-mono);border-radius:var(--radius-sm)}
.page-head{height:117px;padding-top:33px;padding-right:0}
.kicker{font-family:var(--font-mono);color:var(--accent);font-size:17px;letter-spacing:.08em}
.h1{font-size:64px;line-height:1.3}.h2{font-size:45px;line-height:1.27}
.accent{color:var(--accent)}
.slide-main{gap:20px}.hero-top{min-height:290px;padding-top:40px}
.hero-stamp{line-height:1.9}.hero-stamp b{color:var(--accent)}
.flow-node.blue{border-top-color:var(--accent)}.flow-node.green{border-top-color:var(--accent-2)}.flow-node.amber{border-top-color:var(--accent-3)}
.flow-node{background:var(--bg-soft)}.system-flow .flow-node{min-height:240px}
.hero-bottom small{font:20px var(--font-sans)}
.original-label{font-size:14px;border:1px solid var(--border);border-radius:5px;padding:1px 6px;float:right;color:var(--text-3)}
.deck-footer{left:96px;right:96px;bottom:26px}.page-index{margin-right:0}
.page-source{max-width:1510px;font-size:15px}
.metric .value,.ours{color:var(--accent)}
.net-node{padding:9px 8px}.network{gap:11px;padding:12px 16px}.net-node .width{font-size:27px}.net-node .act{font-size:15px}
.protocol{display:flex;align-items:center;gap:15px;flex:none}
.paired td{font-size:19px;white-space:nowrap}.paired th{font-size:18px}.paired td:first-child{font-family:var(--font-sans);font-size:18px}
.scope-line{display:grid;grid-template-columns:114px 1fr;gap:16px;font-size:19px;line-height:1.55;padding:11px 0;border-bottom:1px solid var(--border);color:var(--text-2)}
.scope-line:first-of-type{padding-top:0}.scope-line:last-child{border:0;padding-bottom:0}.scope-line b{color:var(--text-1)}
.slide[data-chapter="results"] .callout{font-size:19px}
.slide[data-page="2"] .step{padding:13px 16px}
.slide[data-page="2"] .steps{gap:10px}
.slide[data-page="2"] .panel{padding:20px 22px}
.slide[data-page="2"] .panel-title{margin-bottom:12px}
.slide[data-page="7"] .panel{padding:18px 22px}
.slide[data-page="7"] .panel-title{margin-bottom:12px}
.slide[data-page="7"] .tiny-table td,.slide[data-page="7"] .tiny-table th{padding:7px 10px}
.slide[data-page="7"] .col{gap:12px}
.slide[data-page="7"] .callout{padding:12px 18px}
.slide[data-page="8"] .panel{padding:20px 22px}
.slide[data-page="8"] .compact td,.slide[data-page="8"] .compact th{font-size:19px;padding:9px 11px}
.slide[data-page="9"] .panel{padding:16px 20px}
.slide[data-page="9"] .panel-title{margin-bottom:12px;font-size:22px}
.slide[data-page="9"] .compact td{font-size:20px;padding:8px 11px;line-height:1.32}
.slide[data-page="9"] .compact th{font-size:18px;padding:8px 11px}
.slide[data-page="9"] .paired td,.slide[data-page="9"] .paired td:first-child{font-size:18px}
.slide[data-page="9"] .table-note{font-size:16px;margin-top:10px}
.slide[data-page="9"] .col{gap:14px}
.slide[data-page="9"] .callout{font-size:18px;padding:12px 18px}
body:not([data-preview="1"]){padding-bottom:62px}
.deck-tools{position:fixed;left:0;right:0;bottom:0;height:62px;display:flex;align-items:center;justify-content:space-between;gap:14px;padding:11px 24px;background:var(--surface);border-top:1px solid var(--border);z-index:25;font-size:13px;color:var(--text-2)}
.tool-group{display:flex;gap:8px;align-items:center}
.deck-tools button,.deck-tools select{font:inherit;color:var(--text-2);border:1px solid var(--border);background:var(--surface);border-radius:var(--radius-sm);padding:7px 12px;cursor:pointer}
.deck-tools button:hover{background:var(--surface-2);color:var(--accent)}.deck-tools button:disabled{opacity:.4;cursor:default}
.deck-tools select{max-width:350px;min-width:150px;color:var(--text-1)}
.progress-bar{height:3px}.progress-bar>span{background:var(--accent)}
.notes-overlay{background:var(--surface);color:var(--text-1);border-color:var(--border);font-size:19px;box-shadow:var(--shadow-lg);padding-bottom:80px}
.notes-overlay h3{font-size:24px}.notes-overlay p{margin:12px 0}.notes-overlay strong{color:var(--accent)}
.source-box h3{font-size:24px}.source-box p{margin:12px 0}
[data-preview="1"] .deck-tools,[data-preview="1"] .deck-header{display:none}
@media(max-width:850px){.deck-tools select{max-width:250px}.keyhint{display:none}.overview.open{grid-template-columns:repeat(2,1fr);padding:22px;gap:14px}}
@media(max-width:600px){body:not([data-preview="1"]){padding-bottom:98px}.deck-tools{display:grid;grid-template-columns:1fr;height:98px;padding:8px 10px;gap:7px}.tool-group:first-child{display:grid;grid-template-columns:30px minmax(0,1fr) 30px auto}.tool-group:last-child{justify-content:flex-end}.deck-tools button{padding:6px 8px;white-space:nowrap;font-size:12px}.deck-tools select{max-width:none;min-width:0;width:100%;font-size:12px}.extra-tool{display:none}.modal{padding:12px}.modal .caption{font-size:12px}.source-box{font-size:15px;padding:22px}.overview.open{grid-template-columns:1fr;padding:18px}}
@media print{body{padding-bottom:0!important}.deck-tools{display:none!important}.slide{padding:65px 96px 82px}.deck-header{display:none!important}}
'''

css = (SKILL/'assets/base.css').read_text(encoding='utf-8-sig') + '\n' + (WORK/'deck.css').read_text(encoding='utf-8-sig') + '\n' + (REFERENCE/'assets/engineering.css').read_text(encoding='utf-8-sig') + '\n' + extra_css
runtime = (SKILL/'assets/runtime.js').read_text(encoding='utf-8-sig').replace('</script', '<\\/script')
runtime = runtime.replace('const scale = Math.min(window.innerWidth / w, window.innerHeight / h);', 'const chrome = getPreviewIdx() < 0 ? (document.querySelector(".deck-tools")?.getBoundingClientRect().height || 0) : 0;\n      const scale = Math.min(window.innerWidth / w, Math.max(1, window.innerHeight - chrome) / h);')
# Keep source paths and fingerprints as portable provenance data, not as runtime dependencies.
manifest = {'chapters':[{'file':str(Path(p).relative_to(Path(SOURCES['source_root']))).replace('\\','/'),'sha256':h} for p,h in SOURCES['source_hashes'].items() if p.endswith('.tex')], 'figures': {k:{'file':'pic/'+Path(v['source']).name,'sha256':SOURCES['source_hashes'][v['source']]} for k,v in SOURCES['figures'].items()}, 'style_reference':'项目展示/assets/engineering.css'}
document = '''<!DOCTYPE html>
<!-- Adapted from html-ppt tech-sharing, arch-diagram and image-text-split templates.
     Original thesis files are read only. Figures retain their complete content. -->
<html lang="zh-CN" data-themes="engineering"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>硕士论文核心算法成果展示 · 任佳乐</title><meta name="description" content="复杂动态环境下机器人导航系统设计与应用：第3章定位、第4章感知、第5章规划。10页离线展示。">
<style>''' + css + '''</style></head><body>
<div class="deck" data-w="1920" data-h="1080">
<div class="deck-header"><span class="deck-brand"><span class="monogram" aria-hidden="true">RJ</span>任佳乐 / 硕士论文</span><nav class="chapter-nav" aria-label="章节导航"><a href="#/1" data-chapter="overview">总览</a><a href="#/2" data-chapter="3">03 定位</a><a href="#/4" data-chapter="4">04 感知</a><a href="#/6" data-chapter="5">05 规划</a><a href="#/9" data-chapter="results">实验结果</a></nav></div>
''' + '\n'.join(slides) + '''
</div>
<nav class="deck-tools" aria-label="展示控制"><div class="tool-group"><button id="prev-slide" aria-label="上一页">←</button><select id="slide-select" aria-label="跳转页面"></select><button id="next-slide" aria-label="下一页">→</button><span id="slide-position" aria-live="polite"></span></div><div class="tool-group"><span class="keyhint">← → 翻页 · 点击原图放大</span><button id="show-source">本页来源</button><button data-key="o">页总览 O</button><button data-key="n" class="extra-tool">讲解提示 N</button><button data-key="f">全屏 F</button></div></nav>
<div id="zoom-modal" class="modal" role="dialog" aria-modal="true" aria-label="论文原图放大" data-no-swipe><button class="close-modal" aria-label="关闭原图">×</button><div class="zoom-box"><img alt=""></div><p class="caption"></p></div>
<div id="source-modal" class="modal" role="dialog" aria-modal="true" aria-label="内容来源" data-no-swipe><button class="close-modal" aria-label="关闭来源">×</button><div class="source-box"><div id="source-content"></div><h3 style="margin-top:24px">原图文件</h3><pre id="source-files"></pre><p class="micro">内容整理自论文第3–5章。数据与方法按原文摘录，插图保持完整；论文源文件未修改。</p></div></div>
<script type="application/json" id="source-manifest">''' + json.dumps(manifest,ensure_ascii=False) + '</script><script>' + custom_js + '</script><script>' + runtime + '</script></body></html>'
target=ROOT/'成果展示.html'
target.write_text(document,encoding='utf-8')
print(json.dumps({'output':str(target),'slides':len(slides),'bytes':target.stat().st_size},ensure_ascii=False))
