import numpy as np
import matplotlib.pyplot as plt
import json

def plot_dielectric_heatmap(data_file):
    # 读取JSON数据
    print("正在读取数据...")
    with open(data_file, 'r') as f:
        data = json.load(f)
    
    # 将数据转换为numpy数组并获取第一个平面（因为深度为1）
    dielectric_data = np.array(data['params'])[0]  # 取第一个平面
    
    # 获取数据维度
    height, width = dielectric_data.shape
    print(f"平面维度: {height} x {width}")
    print(f"数据范围: 最小值 = {dielectric_data.min():.4f}, 最大值 = {dielectric_data.max():.4f}")
    
    # 创建图表
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 创建带有特定大小比例的图表
    fig = plt.figure(figsize=(12, 8))
    
    # 创建主绘图区域，留出空间给颜色条
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    
    # 创建热力图
    im = ax.imshow(dielectric_data, cmap='viridis', interpolation='nearest', aspect='auto')
    
    # 添加颜色条，确保与主图对齐
    cax = fig.add_axes([0.92, 0.1, 0.02, 0.8])  # [left, bottom, width, height]
    cbar = fig.colorbar(im, cax=cax)
    cbar.set_label('Permittivity', fontsize=50)
    # 设置颜色条刻度字体大小
    cbar.ax.tick_params(labelsize=50)
    
    # 设置轴标签
    ax.set_xlabel('X', fontsize=50)
    ax.set_ylabel('Y', fontsize=50)
    
    # 设置刻度标签字体大小
    ax.tick_params(axis='both', which='major', labelsize=50)
    
    # 显示网格线
    ax.grid(True, which='major', color='white', linestyle='-', linewidth=0.5, alpha=0.3)
    
    # 设置主要刻度
    ax.set_xticks(np.arange(0, width, 40))  # 减少刻度数量，使标签更清晰
    ax.set_yticks(np.arange(0, height, 20))
    
    # 设置次要刻度（每个网格）
    ax.set_xticks(np.arange(-.5, width, 1), minor=True)
    ax.set_yticks(np.arange(-.5, height, 1), minor=True)
    
    # 添加网格
    ax.grid(which='minor', color='w', linestyle='-', linewidth=0.2, alpha=0.2)
    
    # 保存图片
    output_file = 'dielectric_heatmap.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"热力图已保存为: {output_file}")
    plt.close()

if __name__ == '__main__':
    # 使用solution.json作为数据源
    data_file = 'solution.json'
    print(f"正在处理文件: {data_file}")
    plot_dielectric_heatmap(data_file) 