import numpy as np
import matplotlib.pyplot as plt
import re
import os

# 获取当前工作目录
current_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(current_dir, 'scipt', 'splitter.txt')

def parse_log(filename):
    iterations = []
    t_params = []
    
    print(f"正在解析文件...")
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line in lines:
        # 匹配迭代次数
        if line.startswith('['):
            iter_match = re.search(r'\[(\d+)\]', line)
            if iter_match:
                iterations.append(int(iter_match.group(1)))
        
        # 匹配新格式的传输参数
        elif 'T o2@0,o1@0' in line:
            t_match = re.search(r'T o2@0,o1@0 λ=1.55 0.5: ([\d.]+)', line)
            if t_match:
                t_params.append(float(t_match.group(1)))
    
    print(f"共找到 {len(iterations)} 个迭代数据点")
    return iterations, t_params

def plot_results(iterations, t_params):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 创建图表并设置大小
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_axes([0.15, 0.15, 0.75, 0.75])
    
    # 绘制传输率变化
    ax.plot(iterations[:len(t_params)], t_params, 'b-o', label='Port 2', markersize=15)
    ax.set_title('Splitter T(o2,o1)', fontsize=50, pad=20)
    ax.set_xlabel('Iteration', fontsize=50, labelpad=20)
    ax.set_ylabel('Transmission', fontsize=50, labelpad=20)
    
    # 设置刻度间隔和大小
    # 获取当前的x轴范围
    x_min, x_max = min(iterations), max(iterations)
    y_min, y_max = 0, 1  # 传输率范围通常是0-1
    
    # 设置合适的刻度间隔
    x_interval = max(1, (x_max - x_min) // 5)  # 确保x轴最多显示5-6个刻度
    ax.set_xticks(np.arange(x_min, x_max + 1,2))
    ax.set_yticks(np.arange(0, 1.2, 0.5))  # y轴显示0, 0.2, 0.4, 0.6, 0.8, 1.0
    
    # 设置刻度标签字体大小
    ax.tick_params(axis='both', which='major', labelsize=40)
    
    # 设置网格
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # 添加目标线
    ax.axhline(y=0.5, color='r', linestyle='--', label='Target', linewidth=3)
    ax.legend(['actual', 'target'], fontsize=40, loc='best')
    
    # 调整布局并保存
    plt.savefig('splitter_transmission.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    print(f"正在读取日志文件: {log_file}")
    iterations, t_params = parse_log(log_file)
    print("正在生成图表...")
    plot_results(iterations, t_params)
    print("图表已保存为 splitter_transmission.png") 