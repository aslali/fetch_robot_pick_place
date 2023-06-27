import pickle
import matplotlib
import matplotlib.pyplot as plt
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

def plot_human_measures(data):
    fig, ax = plt.subplots()
    x_val1 = [x[0]/2 for x in data.p_f]
    y_val1 = [x[1] for x in data.p_f]
    x_val2 = [x[0]/2 for x in data.p_e]
    y_val2 = [x[1] for x in data.p_e]
    ax.plot(x_val1, y_val1, linewidth=3)
    ax.plot(x_val2, y_val2, linewidth=3)
    ax.set_xlabel('time (s)', fontsize=16)
    ax.set_ylabel(r'$p_e, p_f$',fontsize=20)
    lgd = ax.legend([r'$p_f$', r'$p_e$'], fontsize=15, loc='upper left', frameon=False,
                    bbox_to_anchor=(0.25, 1), ncol=2)
    ax.set_title(r'Bayes estimate of $p_e$ and $p_f$', fontsize=16)
    ax.set_ylim([0, 1.19])
    ax.set_xlim([0, round(x_val1[-1] + 10)])
    ax.set_xticks(range(0, int(round(x_val1[-1] + 10)), 100))
    ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.tick_params(axis='x', labelsize=16)
    ax.tick_params(axis='y', labelsize=16)
    plt.show()

def creat_table(data):
    wrong = [x[2] for x in data.action_times_human if (x[2] == 'Wrong_Return' or x[2] == 'Reject' or x[2] == 'Return')]
    wrong_corrected = [x[2] for x in data.action_times_human if (x[2] == 'Correct_Return' or x[2] == 'Cancel_Wrong_Assign')]
    data.nwrong = len(wrong)
    print('n wrong actions: ', data.nwrong)
    hassign = [x[2] for x in data.action_times_human if x[2] == 'Assigned_to_Robot' or x[2] == 'Reject']
    hcassign = [x[2] for x in data.action_times_human if x[2] == 'Cancel_Assign' or x[2] == 'Cancel_Wrong_Assign']

    data.n_tot_hum_assign = len(hassign)
    print('n assigned total by human: ', data.n_tot_hum_assign)

    total_human_tasks = [x[2] for x in data.action_times_human if (x[2] == 'Wrong_Return' or
                                                                   x[2] == 'Return' or
                                                                   x[2] == 'Correct_Return' or
                                                                   x[2] == 'Human' or
                                                                   x[2] == 'Wrong_Return' or
                                                                   x[2] == 'Assigned_to_Human')]

    n_total_human_tasks = len(total_human_tasks)
    print('n_total_human_tasks: ', n_total_human_tasks)


    rassign = [x[3] for x in data.action_times_robot if x[5] == 'Assigned_to_Human']
    data.n_tot_rob_assign = len(rassign)
    print('n assigned by robot: ', data.n_tot_rob_assign)

    total_robot_tasks = [x[3] for x in data.action_times_robot if (x[5] == 'Robot' or
                                                                   x[5] == 'Assigned_to_Robot' or
                                                                   x[5] == 'Return' or
                                                                   x[5] == 'Human_by_Robot')]

    n_total_robot_tasks = len(total_robot_tasks)
    print('n_total_robot_tasks: ', n_total_robot_tasks)

    data.dr = sum(data.robot_travel_distance)
    data.dh = sum(data.human_travel_distance)
    print('d total robot: ', data.dr)
    print('d total human: ', data.dh)

    print('time: ', data.experiment_end_time - data.experiment_start_time)

def plot_frames(data):
    x_val1 = [x[0]/2 for x in data.p_f]
    y_val1 = [x[1] for x in data.p_f]
    x_val2 = [x[0]/2 for x in data.p_e]
    y_val2 = [x[1] for x in data.p_e]
    for i in range(26):
        fig, ax = plt.subplots()
        l1 = ax.plot(x_val1[0:i+1], y_val1[0:i+1], linewidth=3)
        c1 = l1[0].get_color()
        l2 = ax.plot(x_val2[0:i+1], y_val2[0:i+1], linewidth=3)
        c2 = l2[0].get_color()
        ax.plot(x_val1[0], y_val1[0], marker="o", markersize=10, markeredgecolor=c1, markerfacecolor=c1)
        ax.plot(x_val1[0], y_val2[0], marker="o", markersize=10, markeredgecolor=c2, markerfacecolor=c2)
        ax.set_xlabel('time (s)', fontsize=16)
        ax.set_ylabel(r'$p_e, p_f$', fontsize=20)
        lgd = ax.legend([r'$p_f$', r'$p_e$'], fontsize=15, loc='upper left', frameon=False,
                        bbox_to_anchor=(0.25, 1), ncol=2)
        ax.set_title(r'Bayes estimate of $p_e$ and $p_f$', fontsize=16)
        ax.set_ylim([0, 1.19])
        ax.set_xlim([0, round(x_val1[-1] + 10)])
        ax.set_xticks(range(0, int(round(x_val1[-1] + 10)), 100))
        ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
        ax.tick_params(axis='x', labelsize=16)
        ax.tick_params(axis='y', labelsize=16)
        # plt.show()
        figname = 'video1/frame' + str(i) + '.png'
        fig.savefig(figname, format='png', bbox_extra_artists=(lgd,), bbox_inches='tight')
file = open('11671/task2.pickle', 'rb') #18178
data = pickle.load(file)
creat_table(data)
# plot_frames(data)
plot_human_measures(data)




    # fig.savefig('samplefigure.png', format='png', bbox_extra_artists=(lgd,), bbox_inches='tight')