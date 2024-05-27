import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation, FFMpegWriter

def SixDOFanimation(p, R, **kwargs):
    # Default values of optional arguments
    sample_plot_freq = kwargs.get('SamplePlotFreq', 1)
    trail = kwargs.get('Trail', 'Off')
    limit_ratio = kwargs.get('LimitRatio', 1)
    position = kwargs.get('Position', None)
    full_screen = kwargs.get('FullScreen', False)
    view = kwargs.get('View', [30, 20])
    axis_length = kwargs.get('AxisLength', 1)
    show_arrow_head = kwargs.get('ShowArrowHead', True)
    xlabel = kwargs.get('Xlabel', 'X')
    ylabel = kwargs.get('Ylabel', 'Y')
    zlabel = kwargs.get('Zlabel', 'Z')
    title = kwargs.get('Title', '6DOF Animation')
    show_legend = kwargs.get('ShowLegend', True)
    create_avi = kwargs.get('CreateAVI', False)
    avi_file_name = kwargs.get('AVIfileName', '6DOF_Animation')
    avi_fps = kwargs.get('AVIfps', 30)

    # Reduce data to samples to plot only
    p = p[::sample_plot_freq, :]
    R = R[:, :, ::sample_plot_freq] * axis_length
    num_plot_samples = p.shape[0]

    # Setup figure and plot
    fig = plt.figure('6DOF Animation')
    ax = fig.add_subplot(111, projection='3d')
    ax.grid(True)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)
    ax.view_init(view[0], view[1])

    if full_screen:
        fig_manager = plt.get_current_fig_manager()
        fig_manager.window.showMaximized()

    # Initialize plot data arrays
    x = np.zeros(num_plot_samples)
    y = np.zeros(num_plot_samples)
    z = np.zeros(num_plot_samples)

    org_handle, = ax.plot([], [], [], 'k.')
    quivX_handle = None
    quivY_handle = None
    quivZ_handle = None

    if show_legend:
        ax.legend(['Origin', 'X', 'Y', 'Z'])

    def init():
        nonlocal quivX_handle, quivY_handle, quivZ_handle
        org_handle.set_data([], [])
        org_handle.set_3d_properties([])
        quivX_handle = ax.quiver([], [], [], [], [], [], color='r', arrow_length_ratio=0.1 if show_arrow_head else 0)
        quivY_handle = ax.quiver([], [], [], [], [], [], color='g', arrow_length_ratio=0.1 if show_arrow_head else 0)
        quivZ_handle = ax.quiver([], [], [], [], [], [], color='b', arrow_length_ratio=0.1 if show_arrow_head else 0)
        return org_handle, quivX_handle, quivY_handle, quivZ_handle

    def update(num):
        nonlocal quivX_handle, quivY_handle, quivZ_handle
        if trail in ['DotsOnly', 'All']:
            x[:num+1] = p[:num+1, 0]
            y[:num+1] = p[:num+1, 1]
            z[:num+1] = p[:num+1, 2]
        else:
            x[num] = p[num, 0]
            y[num] = p[num, 1]
            z[num] = p[num, 2]

        org_handle.set_data(x, y)
        org_handle.set_3d_properties(z)

        # Remove previous quivers
        if quivX_handle:
            quivX_handle.remove()
        if quivY_handle:
            quivY_handle.remove()
        if quivZ_handle:
            quivZ_handle.remove()

        # Update quivers
        quivX_handle = ax.quiver(p[num, 0], p[num, 1], p[num, 2], R[0, 0, num], R[1, 0, num], R[2, 0, num], color='r', arrow_length_ratio=0.1 if show_arrow_head else 0)
        quivY_handle = ax.quiver(p[num, 0], p[num, 1], p[num, 2], R[0, 1, num], R[1, 1, num], R[2, 1, num], color='g', arrow_length_ratio=0.1 if show_arrow_head else 0)
        quivZ_handle = ax.quiver(p[num, 0], p[num, 1], p[num, 2], R[0, 2, num], R[1, 2, num], R[2, 2, num], color='b', arrow_length_ratio=0.1 if show_arrow_head else 0)

        ax.set_title(f'{title} (Sample {num*sample_plot_freq + 1} of {num_plot_samples * sample_plot_freq})')

        return org_handle, quivX_handle, quivY_handle, quivZ_handle

    ani = FuncAnimation(fig, update, frames=num_plot_samples, init_func=init, blit=False, repeat=False)

    if create_avi:
        writer = FFMpegWriter(fps=avi_fps)
        ani.save(f"{avi_file_name}.mp4", writer=writer)

    plt.show()

    return ani
