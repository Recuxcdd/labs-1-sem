from rules import *
from simulation import Simulation


if __name__ == '__main__':
    sim = Simulation(size_x=50, size_y=50, rules=ConwayRules(), delay=0.001, paused=True)
    sim.run()









# def event_handler(event):
#     print(event.key)


# fig, ax = plt.subplots()
# im = ax.imshow([
#     [1, 0],
#     [0, 1]
# ])
# fig.canvas.mpl_connect('key_press_event', event_handler)
# plt.show()
