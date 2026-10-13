// Project descriptions and slide navigation.
window.PROJECTS = {
  "charge": {
    "folder": "自动回充",
    "title": "机器人自主充电",
    "desc": "导航到桩、视觉对接与电流确认，形成自主充电闭环。",
    "tags": "ROS2 · ArUco · 三轴控制 · FSM",
    "context": "千寻智能实习 / 算法开发与交付",
    "photo": "assets/media/charge-real.jpg",
    "id": "charge",
    "count": 4,
    "slides": [
      "项目概览",
      "整体框架",
      "核心思路",
      "运行演示"
    ],
    "url": "自动回充/index.html"
  },
  "terrain": {
    "folder": "DR02高度图",
    "title": "DR02 楼梯高度图",
    "desc": "融合点云、IMU 和里程计，输出面向落足规划的局部地形。",
    "tags": "C++ · PCL · DDS · 点云融合",
    "context": "云深处实习 / 地形感知框架",
    "photo": "assets/media/terrain.jpg",
    "id": "terrain",
    "count": 4,
    "slides": [
      "项目概览",
      "整体框架",
      "核心思路",
      "楼梯场景演示"
    ],
    "url": "DR02高度图/index.html"
  },
  "m20": {
    "folder": "M20巡检",
    "title": "M20 巡检规划",
    "desc": "全局路线与局部避障协同，处理行人风险并恢复巡检任务。",
    "tags": "ROS2 · 代价地图 · 局部规划 · FSM",
    "context": "云深处实习 / 巡检导航与动态检测",
    "photo": "assets/media/m20-avoid.jpg",
    "id": "m20",
    "count": 4,
    "slides": [
      "项目概览",
      "整体框架",
      "核心思路",
      "现场运行演示"
    ],
    "url": "M20巡检/index.html"
  },
  "go2": {
    "folder": "Go2强化学习导航",
    "title": "Go2 强化学习导航",
    "desc": "在 MuJoCo 障碍环境中构建 PPO-CBF 激光导航策略与训练流程。",
    "tags": "MuJoCo · PyTorch · PPO · CBF",
    "context": "自主研究 / 仿真导航与策略训练",
    "photo": "assets/media/go2.jpg",
    "id": "go2",
    "count": 4,
    "slides": [
      "项目概览",
      "整体框架",
      "训练思路",
      "仿真运行演示"
    ],
    "url": "Go2强化学习导航/index.html"
  }
};
