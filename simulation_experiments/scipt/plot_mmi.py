import numpy as np
import matplotlib.pyplot as plt
import re
import os

# 获取当前工作目录
current_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(current_dir, 'scipt/mmi.txt')

def parse_log(filename):
    iterations = []
    t_params_o2 = []  # o2@0,o1@0
    t_params_o3 = []  # o3@0,o1@0
    
    print(f"正在解析文件...")
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    current_iter = None
    for i, line in enumerate(lines):
        # 匹配迭代次数
        if line.startswith('['):
            iter_match = re.search(r'\[(\d+)\]', line)
            if iter_match:
                current_iter = int(iter_match.group(1))
                iterations.append(current_iter)
        
        # 匹配T参数
        elif 'T o2@0,o1@0' in line:
            t_match = re.search(r'T o2@0,o1@0 λ=1.55 0.5: ([\d.]+)', line)
            if t_match:
                t_params_o2.append(float(t_match.group(1)))
        
        elif 'T o3@0,o1@0' in line:
            t_match = re.search(r'T o3@0,o1@0 λ=1.55 0.5: ([\d.]+)', line)
            if t_match:
                t_params_o3.append(float(t_match.group(1)))
    
    print(f"共找到 {len(iterations)} 个迭代数据点")
    return iterations, t_params_o2, t_params_o3

def plot_results(iterations, t_params_o2, t_params_o3):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    plt.figure(figsize=(10, 7))
    
    # 根据数据点数量决定是否采样
    sample_rate = 5 if len(iterations) > 20 else 1
    
    # 绘制T参数变化
    x_data = iterations[:len(t_params_o2)][::sample_rate]
    y_data1 = t_params_o2[::sample_rate]
    y_data2 = t_params_o3[::sample_rate]
    plt.plot(x_data, y_data1, 'g-o', label='Port 2', markersize=30)
    plt.plot(x_data, y_data2, 'r-o', label='Port 3', markersize=30)
    plt.title('Port Transmission', fontsize=40)
    plt.xlabel('Iteration', fontsize=40)
    plt.ylabel('Transmission', fontsize=40)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=40)
    plt.tick_params(axis='both', labelsize=40)
    
    plt.tight_layout()
    plt.savefig('mmi_transmission.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    print(f"正在读取日志文件: {log_file}")
    iterations, t_params_o2, t_params_o3 = parse_log(log_file)
    print("正在生成图表...")
    plot_results(iterations, t_params_o2, t_params_o3)
    print("图表已保存为 mmi_transmission.png") 