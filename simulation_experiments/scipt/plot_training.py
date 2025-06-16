import numpy as np
import matplotlib.pyplot as plt
import re
import os

# 获取当前工作目录
current_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(current_dir, 'scipt', 'cross.txt')

# 读取数据文件
def parse_log(filename):
    t_o3_o1 = {1.5: [], 1.55: [], 1.6: []}
    t_o2_o1 = {1.5: [], 1.55: [], 1.6: []}
    t_o4_o1 = {1.5: [], 1.55: [], 1.6: []}
    
    print(f"正在解析文件...")
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    current_data = []
    for line in lines:
        if line.startswith('T'):
            try:
                # 使用正则表达式提取波长和值
                wavelength = float(re.search(r'λ=(\d+\.?\d*)', line).group(1))
                value = float(line.split(':')[-1].strip())
                
                if 'o3@0,o1@0' in line:
                    t_o3_o1[wavelength].append(value)
                elif 'o2@0,o1@0' in line:
                    t_o2_o1[wavelength].append(value)
                elif 'o4@0,o1@0' in line:
                    t_o4_o1[wavelength].append(value)
            except Exception as e:
                print(f"解析错误: {e} at line: {line}")
                continue

    iterations = list(range(1, len(t_o3_o1[1.5]) + 1))
    
    print(f"数据点数量:")
    print(f"o3@0,o1@0: {[len(t_o3_o1[w]) for w in [1.5, 1.55, 1.6]]}")
    print(f"o2@0,o1@0: {[len(t_o2_o1[w]) for w in [1.5, 1.55, 1.6]]}")
    print(f"o4@0,o1@0: {[len(t_o4_o1[w]) for w in [1.5, 1.55, 1.6]]}")
    
    return iterations, t_o3_o1, t_o2_o1, t_o4_o1

# 绘图函数
def plot_training_results(iterations, t_o3_o1, t_o2_o1, t_o4_o1):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(24, 7))
    
    wavelengths = [1.5, 1.55, 1.6]
    colors = ['b', 'g', 'r']
    markers = ['o', 's', '^']
    
    # 根据数据点数量决定是否采样
    sample_rate = 5 if len(iterations) > 20 else 1
    
    # 绘制 o3@0,o1@0 的传输系数
    for wavelength, color, marker in zip(wavelengths, colors, markers):
        if len(t_o3_o1[wavelength]) > 0:
            x_data = iterations[:len(t_o3_o1[wavelength])][::sample_rate]
            y_data = t_o3_o1[wavelength][::sample_rate]
            ax1.plot(x_data, y_data, 
                    color=color, marker=marker, linestyle='-', 
                    label=f'λ={wavelength}μm', markersize=25)
    ax1.set_title('T(o3,o1)', fontsize=50)
    ax1.set_xlabel('Iteration', fontsize=40)
    ax1.set_ylabel('Transmission', fontsize=40)
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.tick_params(axis='both', labelsize=40)
    
    # 绘制 o2@0,o1@0 的传输系数
    for wavelength, color, marker in zip(wavelengths, colors, markers):
        if len(t_o2_o1[wavelength]) > 0:
            x_data = iterations[:len(t_o2_o1[wavelength])][::sample_rate]
            y_data = t_o2_o1[wavelength][::sample_rate]
            ax2.plot(x_data, y_data,
                    color=color, marker=marker, linestyle='-',
                    label=f'λ={wavelength}μm', markersize=25)
    ax2.set_title('T(o2,o1)', fontsize=50)
    ax2.set_xlabel('Iteration', fontsize=40)
    ax2.set_ylabel('')
    ax2.grid(True, linestyle='--', alpha=0.7)
    ax2.tick_params(axis='both', labelsize=40)
    
   
    
    # 绘制 o4@0,o1@0 的传输系数
    for wavelength, color, marker in zip(wavelengths, colors, markers):
        if len(t_o4_o1[wavelength]) > 0:
            x_data = iterations[:len(t_o4_o1[wavelength])][::sample_rate]
            y_data = t_o4_o1[wavelength][::sample_rate]
            ax3.plot(x_data, y_data,
                    color=color, marker=marker, linestyle='-',
                        label=f'λ={wavelength}μm', markersize=25)
    ax3.set_title('T(o4,o1)', fontsize=50)
    ax3.set_xlabel('Iteration', fontsize=40)
    ax3.set_ylabel('')
    if any(len(t_o4_o1[w]) > 0 for w in wavelengths):
        ax3.legend(fontsize=40)
    ax3.grid(True, linestyle='--', alpha=0.7)
    ax3.tick_params(axis='both', labelsize=40)
    # 隐藏y轴刻度标签
    
    
    plt.tight_layout()
    plt.savefig('training_results.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    print(f"正在读取日志文件: {log_file}")
    iterations, t_o3_o1, t_o2_o1, t_o4_o1 = parse_log(log_file)
    print("正在生成图表...")
    plot_training_results(iterations, t_o3_o1, t_o2_o1, t_o4_o1)
    print("图表已保存为 training_results.png") 